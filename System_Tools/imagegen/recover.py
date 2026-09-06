#!/usr/bin/env python3
"""既存の生成会話から、プロンプトが一致する完成画像だけを回収する。新規生成しない。"""
import argparse
import base64
import hashlib
import json
import pathlib
import re
import sqlite3
import time
import fcntl

import chrome_bridge as bridge


def normalize(text):
    text = re.sub(r'\n(?:表示を増やす|表示を減らす|Show more|Show less)\s*$', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def evaluate(ws, expression):
    result = bridge.command(ws, 'Runtime.evaluate', {
        'expression': expression, 'awaitPromise': True, 'returnByValue': True,
    }, timeout=45).get('result', {})
    if result.get('exceptionDetails'):
        raise RuntimeError('ブラウザの読み取りに失敗')
    return result.get('result', {}).get('value')


def fresh_recovery_tab():
    """回収専用タブを作り直し、応答しない実行環境を引き継がない。"""
    old = next(t for t in bridge.tabs() if 'chatgpt.com' in t.get('url', ''))
    browser_ws = bridge._http('/json/version')['webSocketDebuggerUrl']
    result = bridge.command(browser_ws, 'Target.createTarget', {'url': 'https://chatgpt.com/'}, timeout=20)
    new_id = result['result']['targetId']
    bridge.command(browser_ws, 'Target.closeTarget', {'targetId': old['id']}, timeout=20)
    return next(t for t in bridge.tabs() if t['id'] == new_id)['webSocketDebuggerUrl']


def write_json(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    temp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('work', type=pathlib.Path)
    ap.add_argument('--history', type=pathlib.Path, required=True)
    ap.add_argument('--since', type=float, default=13432953600000000)
    ap.add_argument('--limit', type=int, default=1500)
    args = ap.parse_args()
    work = args.work.resolve()
    lock = (work / '.imagegen.lock').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('生成・回収処理が既に起動しています。二重起動せず待機します', flush=True)
        raise SystemExit(75)
    queue = json.loads((work / 'image_queue.json').read_text())
    lookup = {}
    for item in queue:
        lookup.setdefault(normalize(item['prompt']), []).append(item)
    state_path = work / '.imagegen' / 'recovery.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else {'verified': {}, 'visited': {}}
    state_path.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(f'file:{args.history.resolve()}?mode=ro', uri=True)
    rows = conn.execute("SELECT url, title FROM urls WHERE url LIKE 'https://chatgpt.com/c/%' AND last_visit_time >= ? ORDER BY last_visit_time DESC", (args.since,)).fetchall()
    rows = [(u, t) for u, t in rows if re.fullmatch(r'https://chatgpt.com/c/[a-f0-9-]{36}', u)]
    ws = fresh_recovery_tab()
    print(f'既存会話{len(rows)}件 / 回収済み{len(state["verified"])}/{len(queue)}', flush=True)
    inspected = 0
    for url, title in rows:
        if len(state['verified']) == len(queue) or inspected >= args.limit:
            break
        if url in state['visited']:
            continue
        if re.search(r'上限|limit', title, re.I):
            state['visited'][url] = 'limit-notice'
            continue
        inspected += 1
        if inspected > 1 and inspected % 15 == 0:
            ws = fresh_recovery_tab()
        bridge.command(ws, 'Page.navigate', {'url': url}, timeout=30)
        data = None
        for attempt in range(24):
            time.sleep(1.5)
            raw = evaluate(ws, "JSON.stringify({loginRequired:!!document.querySelector('[data-testid=login-button]'), url:location.href, ready:document.readyState, busy:!!document.querySelector('[data-testid=stop-button]'), users:[...document.querySelectorAll('[data-message-author-role=user]')].map(x=>({text:x.innerText,id:x.getAttribute('data-message-id')})), images:[...document.querySelectorAll('main img')].filter(x=>/backend-api\\/estuary\\/content|oaiusercontent/.test(x.src)).map(x=>x.src), text:document.querySelector('main')?.innerText || ''})")
            data = json.loads(raw or '{}')
            if data.get('loginRequired'):
                print('ログイン確認待ち。保存済み画像を保持します', flush=True)
                raise SystemExit(76)
            if data.get('url') != url or data.get('ready') != 'complete':
                continue
            if data.get('users') and data.get('images') and not data.get('busy'):
                break
            if attempt >= 5 and re.search(r'Unable to load|Too many requests|会話を読み込めません|上限に達|hit.*limit', data.get('text', ''), re.I):
                break
        users = (data or {}).get('users', [])
        images = list(dict.fromkeys((data or {}).get('images', [])))
        status = 'not-matched'
        if len(users) == 1 and len(images) == 1 and not data.get('busy'):
            matches = lookup.get(normalize(users[0]['text']), [])
            missing = [item for item in matches if item['id'] not in state['verified']]
            if missing:
                # 画像URLの署名はログへ出さない。ページ内で取得し、バイト列だけ受け取る。
                raw = evaluate(ws, "(async()=>{const r=await fetch(" + json.dumps(images[0]) + ",{credentials:'include'});if(!r.ok)throw Error('download '+r.status);const b=await r.blob();return await new Promise((resolve,reject)=>{const f=new FileReader();f.onload=()=>resolve(f.result);f.onerror=reject;f.readAsDataURL(b)});})()")
                blob = base64.b64decode(raw.split(',', 1)[1])
                from PIL import Image
                import io
                with Image.open(io.BytesIO(blob)) as im:
                    im.load()
                    width, height = im.size
                    alpha = im.getchannel('A').getextrema()[0] if 'A' in im.getbands() else 255
                digest = hashlib.sha256(blob).hexdigest()
                for item in missing:
                    expected = 1 if item['aspect'] == '1:1' else 16/9
                    if abs(width/height - expected) > .06:
                        status = 'wrong-aspect'
                        continue
                    if item['slot'] in ('char', 'char_ref') and alpha == 255:
                        status = 'opaque-character'
                        continue
                    dst = work / 'images' / (item['id'] + '.png')
                    temp = dst.with_suffix('.recovery.tmp')
                    temp.write_bytes(blob)
                    temp.replace(dst)
                    state['verified'][item['id']] = {'sha256': digest, 'prompt_sha256': hashlib.sha256(item['prompt'].encode()).hexdigest(), 'conversation': url, 'message_id': users[0]['id'], 'width': width, 'height': height, 'method': 'exact prompt match + generated image from same single-turn conversation', 'at': time.time()}
                    print(f'回収 {item["id"]} ({len(state["verified"])}/{len(queue)})', flush=True)
                status = 'matched'
            elif matches:
                status = 'already-recovered'
        elif data and re.search(r'Too many requests', data.get('text', ''), re.I):
            write_json(state_path, state)
            print('履歴取得の一時制限。新規生成せず回収記録を保存して待機', flush=True)
            raise SystemExit(75)
        state['visited'][url] = status
        write_json(state_path, state)
        if inspected % 10 == 0:
            print(f'会話確認{inspected}件 / 回収{len(state["verified"])}/{len(queue)}', flush=True)
        time.sleep(1)
    print(f'回収終了 {len(state["verified"])}/{len(queue)}。未回収は再生成前に確認する', flush=True)


def run_with_retries(operation=main, sleep=time.sleep, attempts=4, progress=None):
    """通信切断時は保存済みの回収記録から再開する。制限エラーは再試行しない。"""
    failures = 0
    while True:
        before = progress() if progress else None
        try:
            operation()
            return
        except (TimeoutError, ConnectionError) as exc:
            if progress and progress() != before:
                failures = 0
            failures += 1
            if failures == attempts:
                print('通信エラーが継続したため停止。回収済み記録は保持しています。', flush=True)
                raise
            delay = 5 * failures
            print(f'通信エラー {type(exc).__name__}: {delay}秒後にタブを作り直して再開 (連続失敗{failures}/{attempts - 1})', flush=True)
            sleep(delay)


if __name__ == '__main__':
    import sys
    def progress():
        path = pathlib.Path(sys.argv[1]) / '.imagegen/recovery.json'
        return path.stat().st_mtime_ns if path.exists() else None
    run_with_retries(progress=progress)
