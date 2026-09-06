#!/usr/bin/env python3
"""画像回収の読み取り専用進捗画面。生成処理の起動・再起動はしない。"""
import argparse
import json
from pathlib import Path
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def classify(running, age, finished, count, total):
    if running:
        return ('waiting', '応答・更新待ち') if age > 120 else ('running', '実行中')
    if finished:
        return ('review', '回収終了・目視確認待ち') if count == total else ('stopped', '回収終了・未回収あり')
    return 'stopped', '停止中'


def snapshot(work, log):
    state_path = work / '.imagegen/recovery.json'
    state = json.loads(state_path.read_text())
    total = len(json.loads((work / 'image_queue.json').read_text()))
    records = state['verified']
    for path in (work / '.imagegen/receipts').glob('*.json'):
        receipt = json.loads(path.read_text())
        records[receipt['id']] = receipt
    # 記録だけ残って実ファイルが失われた枠はカウントしない。
    records = {k: v for k, v in records.items() if (work / 'images' / (k + '.png')).is_file()}
    commands = subprocess.run(['ps', '-axo', 'command='], capture_output=True, text=True, check=True).stdout.splitlines()
    running = any(any('/imagegen/' + n + ' ' in c for n in ('recover.py', 'run.py')) and str(work) in c for c in commands)
    now = time.time()
    updated = state_path.stat().st_mtime
    result_path = work / '.imagegen/recovery_job_result.json'
    finished = False
    if result_path.exists() and result_path.stat().st_mtime >= updated:
        finished = json.loads(result_path.read_text()).get('exit_code') == 0
    code, label = classify(running, now - updated, finished, len(records), total)
    service_path = work / '.imagegen/service.json'
    retry_at = None
    phase = 'recover'
    count = len(records)
    evidence = None
    if service_path.exists():
        service = json.loads(service_path.read_text())
        phase = service.get('phase', 'recover')
        generation_path = work / '.imagegen/generation_status.json'
        if phase == 'generate' and generation_path.exists():
            generation = json.loads(generation_path.read_text())
            count = generation.get('verified', count)
            updated = max((v.get('at', 0) for v in records.values()), default=updated)
            if running and now - generation.get('at', 0) < 90:
                code, label = 'running', '画像を生成・検査中'
                evidence = generation.get('evidence')
                if generation.get('status') == 'limit_wait' and evidence and evidence.get('kind') == 'image_limit':
                    code, label = 'waiting', '画像生成の上限表示を確認・再試行待ち'
                elif generation.get('status') == 'access_wait' and evidence:
                    code, label = 'waiting', 'アクセス頻度の制限表示を確認・再試行待ち'
                elif generation.get('status') in ('limit_wait', 'access_wait', 'scheduled_wait'):
                    code, label = 'waiting', '再試行待ち・現在の制限表示は未確認'
                elif generation.get('status') in ('error', 'retrying'):
                    code, label = 'waiting', '生成エラー・再試行中'
                elif generation.get('status') == 'checking':
                    label = '保存・結果確認中'
                retry_at = generation.get('retry_at')
            elif service.get('status') == 'finished' and count == total:
                code, label = 'review', '全画像の生成・自動検査終了'
        service_alive = any('/imagegen/recovery_service.py ' in c and str(work) in c for c in commands)
        if service_alive and service.get('status') == 'retry_wait' and now - service.get('at', 0) < 30:
            code, label = 'waiting', '自動復旧・再開待ち'
            if service.get('exit_code') == 76:
                label = 'ログイン確認待ち'
            elif service.get('exit_code') == 75 and (work / '.imagegen/access_limit.json').exists():
                label = 'アクセス制限通知後の再試行待ち'
            retry_at = service.get('retry_at')
    latest = sorted(records.items(), key=lambda x: x[1].get('at', 0), reverse=True)[:8]
    lines = log.read_text(errors='replace').splitlines() if log.exists() else []
    safe_lines = [line for line in lines if line.startswith(('回収 ', '会話確認', '既存会話', '通信エラー', '回収終了', '通信エラーが継続', '自動移行', '全311', 'ChatGPTのアクセス制限', '画像回収を自動復旧'))][-8:]
    return dict(project=work.name, status=code, label=label, running=running,
                verified=count, phase=phase, total=total, inspected=len(state['visited']),
                updated=updated, checked=now, age=int(now-updated), retry_at=retry_at, evidence=evidence,
                latest=[dict(id=k, at=v.get('at', 0)) for k, v in latest], logs=safe_lines)


HTML = '''<!doctype html><html lang="ja"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>戸沢村｜作業状況</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f3f4ef;color:#20342c;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans",sans-serif}
main{max-width:860px;margin:48px auto;padding:0 24px}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:26px}
.eyebrow{font-size:12px;letter-spacing:.15em;color:#65746b}h1{font-size:25px;margin:10px 0}h2{font-size:16px;margin:0 0 18px}
.card{background:white;border:1px solid #dde3db;border-radius:18px;padding:28px;margin-bottom:18px}.badge{display:inline-block;padding:9px 15px;border-radius:40px;background:#edf0ec;font-size:14px;font-weight:600}
.running{background:#dff1e6;color:#17683f}.waiting,.review{background:#fff0d0;color:#895d0a}.stopped,.offline{background:#ffe4df;color:#9b3324}
.count{font-size:62px;font-weight:650;letter-spacing:-.06em;margin:24px 0 12px}.count span{font-size:23px;font-weight:400;letter-spacing:0;color:#79847e}
progress{width:100%;height:12px;accent-color:#337858}p{line-height:1.8;margin:12px 0;color:#58685e;font-size:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.stat{font-size:23px;margin:6px 0}
ul{padding:0;list-style:none;margin:0}li{display:flex;justify-content:space-between;border-top:1px solid #edf0ea;padding:10px 0;font-size:13px}time{color:#718078}pre{white-space:pre-wrap;font-size:12px;line-height:1.9;color:#526157;margin:0}
footer{font-size:12px;color:#758279;line-height:1.8}@media(max-width:600px){main{margin:25px auto;padding:0 16px}.grid{grid-template-columns:1fr}.card{padding:22px}h1{font-size:21px}.count{font-size:52px}header{display:block}.badge{margin-top:10px}}
</style><main><header><div><div class="eyebrow">山のチャンネル / 作業状況</div><h1>1988年 戸沢村ツキノワグマ食害事件</h1></div></header>
<section class="card"><div id="status" class="badge">状況を確認中</div><p id="phase">現在の工程を確認中</p>
<div class="count" id="count">— <span>/ 311 枠</span></div><progress id="bar" max="311" value="0"></progress>
<p id="detail">読み込み中…</p><p id="evidence"></p><p>「照合済み」はプロンプト・保存ファイルの対応を確認した枠数です。全編編集の完了を表す数字ではありません。</p></section>
<div class="grid"><section class="card"><h2>処理が進んでいるか</h2><p>回収記録の最終更新</p><div class="stat" id="updated">—</div><p id="age">—</p><p id="process">—</p><p>2分以上記録が更新されなければ「応答・更新待ち」、処理が終了していれば「停止」または「回収終了」と表示します。</p></section>
<section class="card"><h2>最近回収できた画像</h2><ul id="latest"></ul></section></div>
<section class="card"><h2>最近の作業ログ</h2><pre id="logs">—</pre></section>
<footer>5秒ごとに自動確認します。画面を閉じても回収処理は続きます。<br><span id="checked">画面接続確認中</span><br>回収終了後も、画像の目視確認・未回収素材の対応が必要です。</footer></main>
<script>
const el=id=>document.getElementById(id), stamp=t=>new Date(t*1000).toLocaleTimeString('ja-JP');
let busy=false;
async function refresh(){if(busy)return;busy=true;try{
const r=await fetch('/status',{cache:'no-store',signal:AbortSignal.timeout(4000)});if(!r.ok)throw Error('HTTP');const d=await r.json();
el('phase').textContent=d.phase==='generate'?'現在の工程：不足画像の生成・自動検査':'現在の工程：既存の生成履歴から、正しい画像を回収・照合';
el('evidence').textContent=d.evidence?'判定時の表示（'+stamp(d.evidence.observedAt)+'）：'+d.evidence.text:'制限を示す明確な表示は現在確認できていません。';
el('status').textContent=d.label;el('status').className='badge '+d.status;
el('count').replaceChildren(document.createTextNode(d.verified+' '));const n=document.createElement('span');n.textContent='/ '+d.total+' 枠';el('count').append(n);
el('bar').max=d.total;el('bar').value=d.verified;el('detail').textContent='照合済み '+Math.round(d.verified/d.total*100)+'% ・ 残り '+(d.total-d.verified)+' 枠 ・ 履歴確認 '+d.inspected+' 件';
el('updated').textContent=stamp(d.updated);el('age').textContent=d.age+'秒前に回収記録を更新';el('process').textContent=d.retry_at?'自動再開予定：'+stamp(d.retry_at):'回収プロセス：'+(d.running?'起動中':'終了・停止');
el('latest').replaceChildren(...d.latest.map(x=>{const li=document.createElement('li'),t=document.createElement('time');li.textContent=x.id;t.textContent=stamp(x.at);li.append(t);return li}));
el('logs').textContent=d.logs.join('\\n')||'作業ログはまだありません';el('checked').textContent='画面の接続確認：'+stamp(d.checked);
}catch(e){el('status').className='badge offline';el('status').textContent='状況を取得できません';el('process').textContent='表示は最後に取得した情報です。現在の稼働状況は不明です。'}finally{busy=false}}
refresh();setInterval(refresh,5000);
</script></html>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('work', type=Path)
    ap.add_argument('--log', type=Path, default=Path('/tmp/yama-image-recovery.log'))
    ap.add_argument('--port', type=int, default=8794)
    args = ap.parse_args()
    work = args.work.resolve()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            try:
                if self.path == '/':
                    data, content_type = HTML.encode(), 'text/html; charset=utf-8'
                elif self.path == '/status':
                    data, content_type = json.dumps(snapshot(work, args.log), ensure_ascii=False).encode(), 'application/json; charset=utf-8'
                else:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception:
                self.send_error(503, 'Status unavailable')

        def log_message(self, *args):
            pass

    print(f'進捗画面 http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()


if __name__ == '__main__':
    main()
