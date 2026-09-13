"""承認済み10件だけ。nohupで一度起動し、結果はsummary.jsonへ保存。"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback

BENCH = Path(__file__).resolve().parent
HERE = BENCH.parent
sys.path.insert(0, str(HERE))
import run
import collect as collector

# 実測中はDownloadsの既存素材を回収しない。既存collector自体は変更しない。
collector.DOWNLOADS = BENCH / 'empty_downloads'
collector.DOWNLOADS.mkdir(exist_ok=True)
run.collect = collector.collect
original_parallel = run.run_parallel
results = []
LOG = HERE.parents[2] / '.codex/handoff/delegations/logs/2026-09-13-imagegen-parallel'


def write_summary(status, **extra):
    report = dict(status=status, at=time.time(), pid=os.getpid(),
                  reference_n1_seconds=105, results=results, **extra)
    tmp = BENCH / 'summary.tmp'
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    tmp.replace(BENCH / 'summary.json')


def main():
    # 再起動で同じ10件を追加発注しない。再実行は人の明示判断が必要。
    marker = BENCH / 'launched.json'
    if marker.exists():
        prior = json.loads((BENCH / 'summary.json').read_text())
        fix = BENCH / 'preflight_fix.json'
        if not (fix.exists() and prior['status'] == 'stopped_error'
                and prior.get('results') and all(r['attempts'] == 0 and r['verified'] == 0
                and not r['limit_display'] and 'Cannot find default execution context' in (r['error'] or '')
                for r in prior['results'])):
            raise RuntimeError('既存の開始記録があるため追加発注しません')
    marker.write_text(json.dumps({'pid': os.getpid(), 'at': time.time(), 'cap': 10}))
    (BENCH / 'exit_code.txt').write_text('running\n')
    write_summary('starting')
    for n, count in [(2, 4), (3, 6)]:
        work = BENCH / f'n{n}'
        previous_path = work / '.imagegen/parallel_state.json'
        if previous_path.exists():
            previous = json.loads(previous_path.read_text())
            if previous.get('attempts') or previous.get('inflight'):
                raise RuntimeError('実測の既存投入記録があるため再投入しません')
        run.run_parallel = lambda w, c: original_parallel(w, c, max_attempts=count)
        sys.argv = [str(HERE / 'run.py'), str(work), '--parallel', str(n)]
        started = time.time()
        print(f'BENCH START N={n} count={count} at={started}', flush=True)
        write_summary('running', current=n)
        code, error = 0, None
        try:
            run.main()
        except SystemExit as exc:
            code = exc.code
        except Exception as exc:
            code, error = 1, str(exc)
            traceback.print_exc()
        elapsed = time.time()-started
        run.collect(work)
        queue, left = run.remaining(work)
        state_path = work / '.imagegen/parallel_state.json'
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        complete = len(queue)-len(left)
        evidence = state.get('evidence')
        limit = state.get('status') == 'limit_wait' or code == 75
        result = dict(parallel=n, requested=count, verified=complete, started=started,
                      elapsed_seconds=elapsed, seconds_per_image=elapsed/complete if complete else None,
                      all_saved=complete == count, failures=state.get('failures', 0),
                      retries=state.get('retries', 0), attempts=sum(state.get('attempts', {}).values()),
                      limit_display=limit, evidence=evidence, exit_code=code, error=error,
                      displayed_text={k:v.get('text','') for k,v in state.get('snapshots', {}).items()},
                      queue_sha256=hashlib.sha256((work/'image_queue.json').read_bytes()).hexdigest())
        results.append(result)
        print('BENCH RESULT ' + json.dumps(result, ensure_ascii=False), flush=True)
        if limit:
            write_summary('stopped_limit', remaining='実測中止。既定値・README・コミットは要判断')
            return 75
        if code:
            # 保存待ちの別ウィンドウが残る可能性があるため保存先を切り替えない。
            write_summary('stopped_error', remaining='ログ確認。N=3へ自動で切り替えない')
            return code
    valid = [r for r in results if r['all_saved'] and r['failures'] == 0]
    best = min(valid, key=lambda r:r['seconds_per_image'])['parallel'] if valid else 1
    write_summary('review_required', recommended_parallel=best,
                  remaining='実測値確認→既定値変更→README確定→再検査→明示パスでコミット')
    return 0


if __name__ == '__main__':
    code = 1
    try:
        code = main()
    except Exception as exc:
        traceback.print_exc()
        write_summary('stopped_error', error=str(exc))
    (BENCH / 'exit_code.txt').write_text(str(code)+'\n')
    raise SystemExit(code)
