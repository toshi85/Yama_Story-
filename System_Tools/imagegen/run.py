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


def js(expression):
    """自動化用タブでJavaScriptを実行し、返り値を受け取る。"""
    target = next((t for t in bridge.tabs() if 'chatgpt.com' in t.get('url', '')), None)
    if not target:
        raise RuntimeError('chatgpt.com のタブがありません')
    res = bridge.evaluate(target['webSocketDebuggerUrl'], expression)
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
    while not js('!!document.querySelector("#prompt-textarea")'):
        time.sleep(5)
    print('  ログインを確認しました\n')


def remaining(work):
    """全体から保存済みを引く。これが唯一の進捗の source of truth。"""
    queue = json.loads((work / 'image_queue.json').read_text(encoding='utf-8'))
    have = {p.stem for p in (work / 'images').glob('*.png')}
    return queue, [{'id': q['id'], 'prompt': q['prompt']}
                   for q in queue if q['id'] not in have]


def install_and_run(todo):
    """キューとループをページへ入れ、走らせる。"""
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
                   capture_output=True)


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
    wait_for_login()
    bridge.allow_downloads(work / 'images')

    queue, todo = remaining(work)
    if not todo:
        print(f'すべて完成しています（{len(queue)}枚）')
        return
    print(f'全{len(queue)}枚のうち、残り{len(todo)}枚を作ります')
    install_and_run(todo)

    last_count, last_change = len(queue) - len(todo), time.time()
    while True:
        time.sleep(60)
        collect(work)
        _, todo = remaining(work)
        done = len(queue) - len(todo)

        if not todo:
            print(f'完成しました（{len(queue)}枚）')
            return

        if done != last_count:
            last_count, last_change = done, time.time()
            print(f'  {done}/{len(queue)} 枚', flush=True)
            continue

        # 増えていないとき。上限待ちなら正常なので、そのまま待つ。
        try:
            state = json.loads(js(
                'JSON.stringify({running: __yamaGen.running, '
                'last: __yamaGen.log.slice(-1)[0] || ""})'))
        except Exception as e:
            print(f'  ページを見失いました（{e}）— 入れ直します', flush=True)
            open_chatgpt(); wait_for_login(); install_and_run(todo)
            last_change = time.time()
            continue

        if '生成上限' in state['last']:
            continue                      # 待てば空く。driver.js が自分で再開する
        if not state['running'] or time.time() - last_change > STALL_LIMIT:
            print('  止まっているので入れ直します', flush=True)
            install_and_run(todo)
            last_change = time.time()


if __name__ == '__main__':
    main()
