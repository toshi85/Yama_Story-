"""追加生成はこの2件のみ。nohupで実行し、画像と画面証拠を同じ作業先へ保存。"""
from pathlib import Path
import base64
import hashlib
import json
import os
import sys
import threading
import time
import traceback

BENCH = Path(__file__).resolve().parent
WORK = BENCH / 'diagnosis_n2'
sys.path.insert(0, str(BENCH.parent))
import run
import collect as collector

LOCK = threading.RLock()
TIMERS = []
STARTS = {}
TARGETS = {}
CAPTURES = []
ORIGINAL_STATE = run.parallel_state
ORIGINAL_INSTALL = run.install_parallel
ORIGINAL_PARALLEL = run.run_parallel
ORIGINAL_COLLECT = collector.collect
collector.DOWNLOADS = BENCH / 'empty_downloads'

DETAIL = r'''JSON.stringify({at:Date.now()/1000,url:location.href,visibility:document.visibilityState,focus:document.hasFocus(),busy:!!document.querySelector('[data-testid=stop-button]'),users:[...document.querySelectorAll('[data-message-author-role=user]')].map(x=>x.innerText),images:[...document.querySelectorAll('main img')].filter(x=>/backend-api\/estuary\/content|oaiusercontent/.test(x.src)).map(x=>({src:x.src,complete:x.complete,width:x.naturalWidth})),mainText:document.querySelector('main')?.innerText || '',dialogs:[...document.querySelectorAll('[role=dialog],[role=alertdialog]')].map(x=>x.innerText),driver:window.__yamaGen?{running:__yamaGen.running,stop:__yamaGen.stop,current:__yamaGen.current,done:__yamaGen.done,failed:__yamaGen.failed,log:__yamaGen.log}:null,events:window.__parallelDiagnosisEvents || []})'''
PROBE = r'''(()=>{
if(window.__parallelDiagnosisEvents)return true;
window.__parallelDiagnosisEvents=[];
const note=(x)=>{window.__parallelDiagnosisEvents.push({at:Date.now()/1000,...x})};
let previous='';
window.__parallelDiagnosisTimer=setInterval(()=>{
 const s={busy:!!document.querySelector('[data-testid=stop-button]'),users:document.querySelectorAll('[data-message-author-role=user]').length,images:[...document.querySelectorAll('main img')].filter(x=>/backend-api\/estuary\/content|oaiusercontent/.test(x.src)).length};
 const key=JSON.stringify(s);if(key!==previous){note({kind:'state',...s});previous=key}
},250);
const click=HTMLAnchorElement.prototype.click;
HTMLAnchorElement.prototype.click=function(...args){if(this.download)note({kind:'download',name:this.download});return click.apply(this,args)};
return true;
})()'''


def write_json(path, data):
    with LOCK:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def capture(target, label, origin):
    record = {'target': target['id'], 'label': label, 'at': time.time(), 'origin': origin}
    try:
        state = json.loads(run.js(DETAIL, target=target))
        result = run.bridge.command(target['webSocketDebuggerUrl'], 'Page.captureScreenshot',
                                    {'format': 'png', 'captureBeyondViewport': False}, timeout=20)
        if result.get('error'):
            raise RuntimeError(result['error'])
        stem = target['id'] + '_' + label
        path = WORK / 'screenshots' / (stem + '.png')
        path.write_bytes(base64.b64decode(result['result']['data']))
        write_json(path.with_suffix('.json'), state)
        record.update(path=str(path), bytes=path.stat().st_size, elapsed=time.time()-origin)
    except Exception as exc:
        record['error'] = str(exc)
    with LOCK:
        CAPTURES.append(record)
        write_json(WORK/'captures.json', CAPTURES)


def install(target, item, key, **kwargs):
    # 1IDにつき再送を許さない。リロード引継ぎ時はresume=Trueのみ。
    if target['id'] not in TARGETS:
        if len(TARGETS) >= 2:
            raise RuntimeError('追加生成上限2件')
        TARGETS[target['id']] = {'target': target, 'id': item['id'], 'at': time.time()}
    run.js(PROBE, target=target)
    return ORIGINAL_INSTALL(target, item, key, **kwargs)


def observed_state(target, key):
    state = ORIGINAL_STATE(target, key)
    details = json.loads(run.js(DETAIL, target=target))
    with (WORK/'observations.jsonl').open('a') as out:
        out.write(json.dumps({'target': target['id'], **details}, ensure_ascii=False)+'\n')
    if target['id'] in TARGETS and target['id'] not in STARTS:
        elapsed = time.time()-TARGETS[target['id']]['at']
        if details['busy'] or details['users'] or elapsed >= 30:
            origin = time.time()
            STARTS[target['id']] = origin
            label = 'start' if details['busy'] or details['users'] else 'no_start_30s'
            capture(target, label, origin)
            for delay in (60, 120):
                timer = threading.Timer(max(0, origin+delay-time.time()), capture,
                                        args=(target, f'{delay}s', origin))
                TIMERS.append(timer)
                timer.start()
    return state


def collect(work):
    result = ORIGINAL_COLLECT(work)
    with (WORK/'collection.jsonl').open('a') as out:
        files = [dict(path=str(p.relative_to(WORK)), size=p.stat().st_size)
                 for folder in [WORK/'images', WORK/'.imagegen/receipts']
                 for p in folder.glob('*') if p.is_file()]
        out.write(json.dumps({'at':time.time(),'moved':result,'files':files})+'\n')
    return result


def main():
    WORK.mkdir(exist_ok=True)
    with (WORK/'launched.json').open('x') as marker:
        json.dump({'pid':os.getpid(),'at':time.time(),'additional_generation_cap':2}, marker)
    (WORK/'screenshots').mkdir(exist_ok=True)
    (WORK/'.imagegen').mkdir(exist_ok=True)
    (WORK/'.imagegen/require_receipts').touch()
    queue = json.loads((BENCH/'image_queue.json').read_text())[:2]
    write_json(WORK/'image_queue.json', queue)
    started = time.time()
    write_json(WORK/'summary.json', {'status':'running','pid':os.getpid(),'started':started,'cap':2})
    print(f'DIAGNOSIS START N=2 cap=2 PID={os.getpid()}', flush=True)
    run.install_parallel = install
    run.parallel_state = observed_state
    run.collect = collect
    run.run_parallel = lambda w,n: ORIGINAL_PARALLEL(w,n,max_attempts=2)
    sys.argv = [str(BENCH.parent/'run.py'),str(WORK),'--parallel','2']
    code, error = 0, None
    try:
        run.main()
    except SystemExit as exc:
        code = exc.code
    except Exception as exc:
        code,error=1,str(exc)
        traceback.print_exc()
    ended=time.time()
    collect(WORK)
    _, left=run.remaining(WORK)
    state_path=WORK/'.imagegen/parallel_state.json'
    state=json.loads(state_path.read_text()) if state_path.exists() else {}
    verified=2-len(left)
    result=dict(status='capturing',pid=os.getpid(),started=started,ended=ended,
                elapsed_seconds=ended-started,parallel=2,verified=verified,
                seconds_per_image=(ended-started)/2 if verified==2 else None,
                failures=state.get('failures',0),retries=state.get('retries',0),
                assignments=sum(state.get('attempts',{}).values()),
                limit_display=state.get('status')=='limit_wait',evidence=state.get('evidence'),
                error=error,exit_code=code)
    write_json(WORK/'summary.json',result)
    for timer in TIMERS:
        timer.join()
    for worker in TARGETS.values():
        try:
            run.js('clearInterval(window.__parallelDiagnosisTimer);true',target=worker['target'])
        except Exception:
            pass
    result.update(status='stopped_limit' if result['limit_display'] else 'review_required',
                  captures=len(CAPTURES),capture_errors=sum('error' in c for c in CAPTURES),
                  candidate_default=2 if code==0 and verified==2 and result['failures']==0 and result['seconds_per_image']<105 else 1,
                  next_action='追加生成禁止。画面と状態遷移を確認し、判定・既定値・README確定後にテストとコミット。')
    write_json(WORK/'summary.json',result)
    (WORK/'exit_code.txt').write_text(str(code)+'\n')
    print('DIAGNOSIS RESULT '+json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
