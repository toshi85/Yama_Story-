#!/usr/bin/env python3
"""画像を作り終わるまで面倒を見る。使う人がやるのは、最初の1回のログインだけ。

  python3 run.py <作品フォルダ>

やっていること:
  1. 自動化専用のChromeを開く（普段のChromeとは別。初回だけログインを頼む）
  2. 未生成のぶんだけキューを作る（途中から始めても勝手に続きになる）
  3. 生成ループをページに流し込んで走らせる
  4. 出来た画像を作品フォルダへ回収する
  5. 生成の上限で止まったら待ち、解除されたら勝手に再開する
  6. 全部そろうまで見張る。ループが死んでいたら入れ直す

Chromeの拡張機能も、AIエージェントの常駐も要らない。このコマンド1つで完結する。
"""
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request

if sys.platform == 'win32':
    import msvcrt
else:
    import fcntl

import chrome_bridge as bridge
from integrity import verified_ids

HERE = pathlib.Path(__file__).resolve().parent
DRIVER = HERE / 'driver.js'
STALL_LIMIT = 45 * 60      # これだけ画像が増えなければ、入れ直して様子を見る


def prepare_work(work):
    """キューが無ければAsset_Prompts.mdから自動作成する。"""
    queue = work / 'image_queue.json'
    if queue.exists():
        return
    prompts = work / 'Asset_Prompts.md'
    if not prompts.exists():
        sys.exit(f'{work} に image_queue.json または Asset_Prompts.md がありません')
    subprocess.run(
        [sys.executable, str(HERE / 'extract_prompts.py'), str(prompts), str(queue)],
        check=True,
    )


def acquire_lock(work):
    """同じ作品を二重起動しない。ファイルは進捗ではなくロックの器だけ。"""
    lock_path = work / '.imagegen.lock'
    handle = lock_path.open('a+')
    try:
        if sys.platform == 'win32':
            handle.seek(0)
            if not handle.read(1):
                handle.write(' ')
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (BlockingIOError, OSError):
        sys.exit('この作品の画像生成はすでに動いています。二重起動はしません。')
    handle.seek(0)
    handle.write(str(os.getpid()))
    handle.truncate()
    handle.flush()
    return handle


def js(expression, timeout=45):
    """自動化用タブでJavaScriptを実行し、返り値を受け取る。"""
    target = next((t for t in bridge.tabs() if 'chatgpt.com' in t.get('url', '')), None)
    if not target:
        raise RuntimeError('chatgpt.com のタブがありません')
    res = bridge.command(target['webSocketDebuggerUrl'], 'Runtime.evaluate', {
        'expression': expression, 'awaitPromise': True, 'returnByValue': True,
    }, timeout=timeout)
    inner = res.get('result', {})
    if 'exceptionDetails' in inner:
        raise RuntimeError(json.dumps(inner['exceptionDetails'], ensure_ascii=False)[:300])
    return inner.get('result', {}).get('value')


def open_chatgpt():
    if not any('chatgpt.com' in t.get('url', '') for t in bridge.tabs()):
        request = urllib.request.Request(
            f'http://127.0.0.1:{bridge.PORT}/json/new?https://chatgpt.com/',
            method='PUT',
        )
        try:
            urllib.request.urlopen(request, timeout=10).close()
        except OSError:
            pass
        time.sleep(6)


def wait_for_login():
    """ログインしていなければ、済むまで待つ。ここだけは人の手が要る。"""
    if js('!!document.querySelector("#prompt-textarea")'):
        return
    print('\n  開いたChromeでChatGPTにログインしてください（最初の1回だけです）')
    print('  ※ 普段のChromeとは別のウィンドウです\n')
    for _ in range(6):
        time.sleep(5)
        if js('!!document.querySelector("#prompt-textarea")'):
            break
    else:
        raise SystemExit(76)
    print('  ログインを確認しました\n')


def remaining(work):
    """全体から保存済みを引く。これが唯一の進捗の source of truth。"""
    queue = json.loads((work / 'image_queue.json').read_text(encoding='utf-8'))
    have = verified_ids(work, queue)
    return queue, [{'id': q['id'], 'prompt': q['prompt']}
                   for q in queue if q['id'] not in have]


def install_and_run(todo):
    """キューとループをページへ入れ、走らせる。"""
    if js('!!window.__yamaGen?.running'):
        print('生成ループは稼働中です。再注入・二重起動はしません', flush=True)
        return
    # 再読込した会話に未保存の結果があれば、その要求を先頭にして引き継ぐ。
    from recover import normalize
    users = json.loads(js('JSON.stringify([...document.querySelectorAll("[data-message-author-role=user]")].map(x=>x.innerText))'))
    if len(users) == 1:
        todo = sorted(todo, key=lambda item: normalize(item['prompt']) != normalize(users[0]))
    js(f'window.__yamaQueue = {json.dumps(todo, ensure_ascii=False)}; '
       'window.__yamaQueue.length')
    js(DRIVER.read_text(encoding='utf-8'))
    js('''(() => {
      const g = window.__yamaGen;
      g.forget(); g.failed = []; g.stop = false;
      clearInterval(window.__yamaSuper);
      window.__yamaSuper = setInterval(() => {
        const s = window.__yamaGen;
        if (!s) return;
        const left = (window.__yamaQueue || []).filter(x => !s.done.includes(x.id)).length;
        if (!s.running && !s.stop && left > 0) window.__yamaRun();
      }, 60000);
      __yamaRun();
      return "started";
    })()
    ''')


def collect(work):
    subprocess.run([sys.executable, str(HERE / 'collect.py'), str(work)],
                   capture_output=True, timeout=30, check=True)


def heartbeat(work, **state):
    path = work / '.imagegen/generation_status.json'
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(dict(at=time.time(), **state), ensure_ascii=False))
    tmp.replace(path)


def observed_generation_state(state):
    evidence = state.get('liveLimit')
    waiting = state.get('waitState') or {}
    if evidence and evidence.get('kind') in ('image_limit', 'access_limit') and evidence.get('text'):
        return dict(status='limit_wait' if evidence['kind'] == 'image_limit' else 'access_wait',
                    evidence=evidence, retry_at=waiting.get('retryAt'), until=state.get('until'))
    if waiting:
        return dict(status='scheduled_wait', evidence=waiting.get('evidence'), retry_at=waiting.get('retryAt'))
    if state.get('retryVisible'):
        return dict(status='retrying' if state.get('busy') else 'error', evidence=None)
    return dict(status='generating' if state.get('busy') else 'checking', evidence=None)


def dismiss_access_notice():
    """既知のアクセス制限通知だけを閉じる。送信・再試行はしない。"""
    return bool(js('''(()=>{
      const d=[...document.querySelectorAll('[role=dialog],[role=alertdialog]')]
        .find(x=>/リクエストが多すぎ|リクエストの頻度が高|Too many requests/i.test(x.innerText));
      const b=d&&[...d.querySelectorAll('button')].find(x=>/^(了解|OK|Okay)$/i.test(x.innerText.trim()));
      if(!b)return false;b.click();return true;
    })()''', timeout=10))


def handle_access_limit(work):
    path = work / '.imagegen/access_limit.json'
    previous = json.loads(path.read_text()) if path.exists() else None
    # 通知を閉じる操作は待機期限の判定より先に行う。
    dismissed = dismiss_access_notice()
    if dismissed:
        print('アクセス制限通知の「了解」を押しました', flush=True)
    if previous and previous['until'] > time.time():
        raise SystemExit(75)
    if dismissed:
        js('(()=>{if(window.__yamaGen)window.__yamaGen.stop=true;clearInterval(window.__yamaSuper)})()')
        path.write_text(json.dumps({'until': time.time() + 180}))
        print('ChatGPTのアクセス制限を検知。3分待って自動再開します', flush=True)
        raise SystemExit(75)
    if previous:
        path.unlink()


def quarantine_pending(work, todo):
    quarantine = work / '.imagegen/unverified_existing'
    quarantine.mkdir(exist_ok=True)
    for item in todo:
        old = work / 'images' / (item['id'] + '.png')
        if old.exists():
            old.replace(quarantine / (str(time.time_ns()) + '_' + old.name))


def note_limit(work, until_ms):
    """解除予定の時刻を残す。常駐（kick.py）がこれを見て、その時刻まで触らない。"""
    path = work / '.imagegen' / 'limit_until.json'
    path.parent.mkdir(exist_ok=True)
    if until_ms:
        path.write_text(json.dumps({'until': until_ms / 1000}), encoding='utf-8')
    elif path.exists():
        path.unlink()



def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    work = pathlib.Path(sys.argv[1]).resolve()
    if not work.is_dir():
        sys.exit(f'作品フォルダが見つかりません: {work}')
    prepare_work(work)
    _lock_handle = acquire_lock(work)

    bridge.start()
    open_chatgpt()
    try:
        js('1')
    except (TimeoutError, ConnectionError):
        from recover import fresh_recovery_tab
        ws = fresh_recovery_tab()
        bridge.command(ws, 'Page.navigate', {'url': 'https://chatgpt.com/'}, timeout=30)
    handle_access_limit(work)
    wait_for_login()
    bridge.allow_downloads(work / 'images')
    # 停止直前に保存された画像・照合記録を取り込み、再起動時の重複生成を防ぐ。
    collect(work)

    queue, todo = remaining(work)
    if not todo:
        print(f'すべて完成しています（{len(queue)}枚）')
        return
    print(f'全{len(queue)}枚のうち、残り{len(todo)}枚を作ります')
    if (work / '.imagegen' / 'require_receipts').exists():
        if not js('!!window.__yamaGen?.running'):
            quarantine_pending(work, todo)
    install_and_run(todo)

    last_count, last_change = len(queue) - len(todo), time.time()
    last_note = None
    heartbeat(work, verified=last_count, total=len(queue), status='generating')
    while True:
        time.sleep(15)
        handle_access_limit(work)
        collect(work)
        _, todo = remaining(work)
        done = len(queue) - len(todo)
        heartbeat(work, verified=done, total=len(queue), status='generating')

        if not todo:
            heartbeat(work, verified=done, total=len(queue), status='finished')
            print(f'完成しました（{len(queue)}枚）')
            return

        if done != last_count:
            note_limit(work, None)        # 動き出したので上限待ちの印は消す
            last_count, last_change = done, time.time()
            print(f'  {done}/{len(queue)} 枚', flush=True)
            continue

        # 増えていないとき。上限待ちなら正常なので、そのまま待つ。
        try:
            state = json.loads(js(
                'JSON.stringify({running: __yamaGen.running, '
                'busy: !!document.querySelector("[data-testid=stop-button]"), current: __yamaGen.current, '
                'until: __yamaGen.limitUntil || 0, '
                'liveLimit: window.__yamaLimitEvidence?.() || null, waitState: __yamaGen.waitState || null, '
                'retryVisible: [...document.querySelectorAll("main button")].some(b=>/^(再試行|Retry)$/.test(b.innerText.trim())), '
                'last: __yamaGen.log.slice(-1)[0] || ""})'))
        except Exception as e:
            print(f'  ページを見失いました（{e}）— 入れ直します', flush=True)
            open_chatgpt(); wait_for_login(); install_and_run(todo)
            last_change = time.time()
            continue

        observation = observed_generation_state(state)
        heartbeat(work, verified=done, total=len(queue), current=state.get('current'), **observation)

        if observation['status'] in ('limit_wait', 'access_wait', 'scheduled_wait'):
            # 待てば空く。driver.js が自分で再開する。
            # 解除予定の時刻を書き出しておくと、常駐がその時刻に合わせて起こしてくれる。
            note_limit(work, state.get('until'))
            if state.get('until'):
                at = time.strftime('%m/%d %H:%M', time.localtime(state['until'] / 1000))
                if at != last_note:
                    print(f'  上限待ち。解除は {at} ごろ', flush=True)
                    last_note = at
            continue
        if not state['running'] or time.time() - last_change > STALL_LIMIT:
            print('  止まっているので入れ直します', flush=True)
            if state['running'] and not state.get('busy'):
                target = next(t for t in bridge.tabs() if 'chatgpt.com' in t.get('url', ''))
                bridge.command(target['webSocketDebuggerUrl'], 'Page.reload', {}, timeout=30)
                time.sleep(5)
            if not js('!!window.__yamaGen?.running'):
                quarantine_pending(work, todo)
            install_and_run(todo)
            last_change = time.time()


if __name__ == '__main__':
    main()
