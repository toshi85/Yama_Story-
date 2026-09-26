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
import argparse
import base64
from collections import deque
import hashlib
import json
import math
import os
import pathlib
import socket
import struct
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urlparse

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


def js(expression, timeout=45, target=None):
    """自動化用タブでJavaScriptを実行し、返り値を受け取る。"""
    target = target or next((t for t in bridge.tabs() if 'chatgpt.com' in t.get('url', '')), None)
    if not target:
        raise RuntimeError('chatgpt.com のタブがありません')
    res = bridge.command(target['webSocketDebuggerUrl'], 'Runtime.evaluate', {
        'expression': expression, 'awaitPromise': True, 'returnByValue': True,
    }, timeout=timeout)
    if res.get('error'):
        raise RuntimeError(res['error'])
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


def dismiss_access_notice(target=None):
    """既知のアクセス制限通知だけを閉じる。送信・再試行はしない。"""
    return bool(js('''(()=>{
      const d=[...document.querySelectorAll('[role=dialog],[role=alertdialog]')]
        .find(x=>/リクエストが多すぎ|リクエストの頻度が高|Too many requests/i.test(x.innerText));
      const b=d&&[...d.querySelectorAll('button')].find(x=>/^(了解|OK|Okay)$/i.test(x.innerText.trim()));
      if(!b)return false;b.click();return true;
    })()''', timeout=10, target=target))


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
        print('ChatGPTのアクセス制限を検知。終了コード75で停止します。再開は3分以降に外部から実行してください', flush=True)
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




DEFAULT_PARALLEL = 2  # 2026-09-13: 2枚89.5秒（44.8秒/枚）、失敗0件。


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('work')
    parser.add_argument('--parallel', type=int, default=DEFAULT_PARALLEL)
    parser.add_argument('--min-interval', type=float, default=60)
    parser.add_argument('--exclude', default='', help='投入しないID（カンマ区切り）')
    parser.add_argument('--exclude-slots', default='', help='投入しないslot（例: bg,still）')
    args = parser.parse_args(argv)
    if args.parallel < 1:
        parser.error('--parallel は1以上を指定してください')
    if not math.isfinite(args.min_interval) or args.min_interval < 0:
        parser.error('--min-interval は0以上の有限の秒数を指定してください')
    return args


class ParallelQueue:
    """割当ての所有者はPythonだけ。ブラウザは1件を処理して返す。"""
    def __init__(self, todo):
        self.items = {item['id']: item for item in todo}
        if len(self.items) != len(todo):
            raise ValueError('キューのIDが重複しています')
        self.pending = deque(self.items)
        self.inflight = {}
        self.attempts = {}
        self.failures = 0
        self.item_failures = {}
        self.retries = 0
        self.stopped = False

    def assign(self, worker, skip=None):
        if self.stopped or worker in self.inflight or not self.pending:
            return None
        while self.pending:
            key = self.pending.popleft()
            if skip is None or not skip(self.items[key]):
                break
        else:
            return None
        self.inflight[worker] = key
        self.attempts[key] = self.attempts.get(key, 0) + 1
        self.retries += int(self.attempts[key] > 1)
        return self.items[key]

    def finish(self, worker, success):
        key = self.inflight.pop(worker)
        if not success:
            self.failures += 1
            self.item_failures[key] = self.item_failures.get(key, 0) + 1
            if self.item_failures[key] >= 2:
                self.stopped = True
            else:
                self.pending.appendleft(key)

    def stop(self):
        self.stopped = True


class DispatchFilter:
    """ディスクのキューを変えず、各割当て直前の保存状況で判定する。"""
    def __init__(self, work, queue, exclude='', exclude_slots=''):
        self.images = work / 'images'
        self.slots = {item['id']: item.get('slot') for item in queue}
        self.exclude = {value.strip() for value in exclude.split(',') if value.strip()}
        self.exclude_slots = {value.strip() for value in exclude_slots.split(',') if value.strip()}
        self.logged = set()

    def __call__(self, item):
        key = item['id']
        reason = ('保存済み' if (self.images / (key + '.png')).exists() else
                  '除外指定' if key in self.exclude or self.slots.get(key) in self.exclude_slots else None)
        if reason and key not in self.logged:
            print(f'飛ばした：{key}（{reason}）', flush=True)
            self.logged.add(key)
        return bool(reason)


class SendPacer:
    """全ウィンドウ共通で、実送信の確認後から次の許可までを計測する。"""
    def __init__(self, interval, previous=None):
        previous = previous or {}
        self.interval = interval
        self.last_sent_at = previous.get('last_sent_at', 0)
        self.pending = None
        self.sends = previous.get('sends', [])
        if previous.get('pending'):
            self.last_sent_at = max(self.last_sent_at, time.time())

    def ready(self, now):
        return self.pending is None and now >= self.last_sent_at + self.interval

    def reserve(self, worker, request, now):
        if not self.ready(now):
            return False
        self.pending = dict(worker=worker, **request)
        return True

    def observe(self, states, now):
        if not self.pending:
            return
        state = states.get(self.pending['worker'], {})
        if state.get('sentToken') == self.pending['token'] and state.get('sentAt') is not None:
            self.last_sent_at = max(now, state['sentAt'])
            self.sends.append(dict(**self.pending, sent_at=state['sentAt'], observed_at=now))
            self.pending = None

    def cancel(self, now):
        # 許可済み送信の成否が不明でも、次の許可は少なくともinterval秒後。
        if self.pending:
            self.last_sent_at = max(self.last_sent_at, now)
        self.pending = None

    def state(self):
        return dict(interval=self.interval, last_sent_at=self.last_sent_at,
                    pending=self.pending, sends=self.sends)


def grant_next_send(pacer, targets, snapshots, inflight, persist):
    pacer.observe(snapshots, time.time())
    if pacer.pending:
        pending = pacer.pending
        state = snapshots.get(pending['worker'], {})
        if state.get('installed') and state.get('running'):
            return
        target = next(t for t in targets if t['id'] == pending['worker'])
        js('(()=>{if(window.__yamaGen) __yamaGen.sendGrant=null;return true})()', target=target)
        pacer.cancel(time.time())
    for target in targets:
        worker = target['id']
        request = snapshots[worker].get('sendRequest')
        if not request or request['id'] != inflight.get(worker):
            continue
        if not pacer.reserve(worker, request, time.time()):
            return
        persist()  # 許可を渡す前に所有者と時刻を記録する。
        granted = js("""(()=>{
          const g=window.__yamaGen, p=window.__yamaParallel;
          if(!g || g.stop || localStorage.getItem(p.limitKey) || g.sendRequest?.token!==%s)return false;
          g.sendGrant=%s; return true;
        })()""" % (json.dumps(request['token']), json.dumps(request['token'])), target=target)
        if not granted:
            pacer.cancel(time.time())
        return


class AccessCooldown:
    """アクセス制限だけの待機。画像枚数上限のlimit_until.jsonは触らない。"""
    def __init__(self, work, have):
        self.path = work / '.imagegen/access_limit.json'
        previous = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.consecutive = previous.get('consecutive', 0)
        self.until = previous.get('until', 0)
        self.have = set(previous.get('verified', have))
        self.evidence = previous.get('evidence')
        if self.consecutive >= 4 and self.until <= time.time():
            self.consecutive = 0  # 20分後の明示的な外部起動は新しい試行として扱う。
        self.saved(have)

    def persist(self):
        self.path.write_text(json.dumps(dict(consecutive=self.consecutive, until=self.until,
                                            verified=sorted(self.have), evidence=self.evidence), ensure_ascii=False))

    def saved(self, have):
        have = set(have)
        if have - self.have:
            self.consecutive = 0
            self.have = have
            self.persist()

    def detect(self, evidence):
        self.consecutive += 1
        minutes = min(self.consecutive, 4) * 5
        self.until = time.time() + minutes*60
        self.evidence = evidence
        self.persist()
        return minutes

    def waiting(self):
        return time.time() < self.until

    def finish(self):
        self.until = 0
        self.persist()

    def log_wait(self):
        minutes = max(1, math.ceil((self.until-time.time())/60))
        at = time.strftime('%H:%M', time.localtime(self.until))
        print(f'アクセス制限: 待機中 {minutes}分（再開予定 {at}）', flush=True)


def resume_access_targets(targets, scheduler, key, pacer):
    # 待機中に完成した画像は同じ会話で回収する。稼働中の同じidを別窓に移さない。
    for target in targets:
        state = parallel_state(target, key)
        item_id = scheduler.inflight.get(target['id'])
        if not item_id:
            continue
        # 会話そのものの拒否文は新しい要求でしか消えない。生成中・完成画像は残す。
        own_limit = state.get('liveLimit') or {}
        if own_limit.get('source') == 'current_conversation' and not state.get('busy'):
            bridge.command(target['webSocketDebuggerUrl'], 'Page.navigate',
                           {'url': 'https://chatgpt.com/'}, timeout=30)
            wait_parallel_login(target)
        js('''(()=>{
          const g=window.__yamaGen;
          if(g){g.limitEvidence=null;g.limitUntil=null;g.waitState=null;g.sendGrant=null;g.stop=false;}
          return true;
        })()''', target=target)
    js(f'localStorage.removeItem({json.dumps(key)})', target=targets[0])
    pacer.cancel(time.time())
    for target in targets:
        item_id = scheduler.inflight.get(target['id'])
        if item_id and not js('!!window.__yamaGen?.running', target=target):
            install_parallel(target, scheduler.items[item_id], key)
    scheduler.stopped = False


def parallel_state(target, limit_key):
    return json.loads(js("""JSON.stringify({
      installed:!!window.__yamaGen, running:!!window.__yamaGen?.running, stopped:!!window.__yamaGen?.stop,
      busy:!!document.querySelector('[data-testid=stop-button]'),
      current:window.__yamaGen?.current,
      sendRequest:window.__yamaGen?.sendRequest || null,
      sentToken:window.__yamaGen?.sentToken || null, sentAt:window.__yamaGen?.sentAt || null,
      done:window.__yamaGen?.done || [], failed:window.__yamaGen?.failed || [],
      liveLimit:window.__yamaLimitEvidence?.() || window.__yamaGen?.limitEvidence || null,
      until:window.__yamaGen?.limitUntil || 0,
      shared:JSON.parse(localStorage.getItem(%s) || 'null'),
      text:[...document.querySelectorAll('[data-message-author-role=assistant],[role=dialog],[role=alertdialog]')].map(x=>x.innerText).join('\\n'),
      log:window.__yamaGen?.log || []
    })""" % json.dumps(limit_key), target=target))


def install_parallel(target, item, limit_key, *, resume=False):
    """supervisorや全件キューを入れず、中央で割り当てた1件だけ実行。"""
    config = json.dumps({'limitKey': limit_key, 'resume': resume, 'paced': True})
    js(f'window.__yamaParallel = {config};', target=target)
    js(DRIVER.read_text(encoding='utf-8'), target=target)
    js("""(() => {
      if (__yamaGen.running) throw new Error('割当先は稼働中');
      clearInterval(window.__yamaSuper);
      __yamaGen.forget(); __yamaGen.failed = []; __yamaGen.stop = false;
      window.__yamaQueue = [%s];
      __yamaRun(); return 'started';
    })()""" % json.dumps(item, ensure_ascii=False), target=target)


def stop_parallel(targets, limit_key):
    errors = []
    for target in targets:
        try:
            js("""(() => {
              localStorage.setItem(%s, localStorage.getItem(%s) || '{}');
              if(window.__yamaGen){window.__yamaGen.stop = true;window.__yamaGen.sendGrant=null;}
              clearInterval(window.__yamaSuper);
              return true;
            })()""" % (json.dumps(limit_key), json.dumps(limit_key)), target=target)
        except Exception as exc:
            errors.append(str(exc))
    return errors


class ParallelDownloads:
    """Browser.setDownloadBehaviorのCDP接続を全件回収まで維持する。"""
    def __init__(self, path):
        path = pathlib.Path(path).resolve()
        path.mkdir(parents=True, exist_ok=True)
        endpoint = urlparse(bridge._http('/json/version')['webSocketDebuggerUrl'])
        self.socket = socket.create_connection((endpoint.hostname, endpoint.port), timeout=10)
        try:
            key = base64.b64encode(os.urandom(16)).decode()
            self.socket.sendall((
                f'GET {endpoint.path} HTTP/1.1\r\nHost: {endpoint.hostname}:{endpoint.port}\r\n'
                'Upgrade: websocket\r\nConnection: Upgrade\r\n'
                f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
            ).encode())
            header = b''
            while not header.endswith(b'\r\n\r\n'):
                header += self.read(1)
                if len(header) > 16384:
                    raise RuntimeError('CDP応答ヘッダーが不正です')
            if not header.startswith(b'HTTP/1.1 101 '):
                raise RuntimeError('CDPダウンロード接続に失敗しました')
            self.send(json.dumps({'id': 1, 'method': 'Browser.setDownloadBehavior',
                                  'params': {'behavior': 'allow', 'downloadPath': str(path)}}).encode())
            while True:
                first, second = self.read(2)
                length = second & 127
                if length == 126:
                    length = struct.unpack('>H', self.read(2))[0]
                elif length == 127:
                    length = struct.unpack('>Q', self.read(8))[0]
                payload = self.read(length)
                opcode = first & 15
                if opcode == 8:
                    raise ConnectionError('CDPダウンロード接続が閉じられました')
                if opcode == 9:
                    self.send(payload, opcode=10)
                    continue
                response = json.loads(payload)
                if response.get('id') == 1:
                    if response.get('error'):
                        raise RuntimeError(response['error'])
                    break
        except BaseException:
            self.close()
            raise

    def read(self, size):
        data = b''
        while len(data) < size:
            chunk = self.socket.recv(size-len(data))
            if not chunk:
                raise ConnectionError('CDPダウンロード接続が切れました')
            data += chunk
        return data

    def send(self, payload, opcode=1):
        mask = os.urandom(4)
        length = len(payload)
        if length < 126:
            header = bytes([128 | opcode, 128 | length])
        elif length < 65536:
            header = bytes([128 | opcode, 254]) + struct.pack('>H', length)
        else:
            header = bytes([128 | opcode, 255]) + struct.pack('>Q', length)
        self.socket.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))

    def close(self):
        self.socket.close()


def wait_parallel_login(target):
    # Target.createTarget直後はページのJS実行領域がまだ作られていない。
    for _ in range(30):
        try:
            if js('!!document.querySelector("#prompt-textarea")', target=target):
                return
        except RuntimeError as exc:
            if 'Cannot find default execution context' not in str(exc):
                raise
        time.sleep(1)
    raise RuntimeError('専用ChromeでChatGPTへのログインを確認できません')


def run_parallel(work, count, *, min_interval=60, max_attempts=None, exclude='', exclude_slots=''):
    """独立ウィンドウへ配分。max_attemptsは実測の発注上限用（CLI非公開）。"""
    (work / '.imagegen').mkdir(exist_ok=True)
    limit_path = work / '.imagegen/limit_until.json'
    if limit_path.exists() and json.loads(limit_path.read_text())['until'] > time.time():
        raise SystemExit(75)
    collect(work)
    queue, todo = remaining(work)
    skip = DispatchFilter(work, queue, exclude, exclude_slots)
    for item in queue:
        skip(item)
    todo = [item for item in todo if not skip(item)]
    if not todo:
        print(f'投入対象は残り0件（全キュー{len(queue)}件）', flush=True)
        return
    scheduler = ParallelQueue(todo)
    key = 'yamaParallelLimit:' + hashlib.sha256(str(work).encode()).hexdigest()
    state_path = work / '.imagegen/parallel_state.json'
    targets = []
    started = time.time()
    previous = json.loads(state_path.read_text()) if state_path.exists() else {}
    pacer = SendPacer(min_interval, previous.get('pacing'))
    initial_have = verified_ids(work, queue)
    access = AccessCooldown(work, initial_have)
    cooling = access.waiting()
    last_wait_log = 0
    snapshots = {}
    dispatched_at = {}
    idle_since = {}
    status = 'starting'
    downloads = None
    evidence = None

    def record():
        data = dict(status=status, started=started, at=time.time(), parallel=count,
                    elapsed=time.time()-started, failures=scheduler.failures,
                    retries=scheduler.retries, attempts=scheduler.attempts,
                    inflight=scheduler.inflight, targets=targets, evidence=evidence,
                    snapshots=snapshots, pacing=pacer.state(),
                    pending=list(scheduler.pending), remaining_ids=sorted(set(scheduler.pending) | set(scheduler.inflight.values())),
                    access_consecutive=access.consecutive, access_retry_at=access.until)
        tmp = state_path.with_suffix('.tmp')
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        tmp.replace(state_path)
        return data

    try:
        # 中断時の対象タブを引き継ぐ。同じidを別ウィンドウへ送らない。
        existing = {t['id']: t for t in bridge.tabs()}
        for old in previous.get('targets', []):
            if old['id'] not in existing:
                if old['id'] in previous.get('inflight', {}):
                    raise RuntimeError('処理中のウィンドウがありません。再送前に結果の確認が必要です')
                continue
            targets.append(existing[old['id']])
        while len(targets) < min(count, len(todo)):
            targets.append(bridge.new_window())
            record()
        for target in targets:
            old_state = previous.get('snapshots', {}).get(target['id'], {})
            if previous.get('status') == 'limit_wait' and old_state.get('liveLimit'):
                bridge.command(target['webSocketDebuggerUrl'], 'Page.navigate',
                               {'url': 'https://chatgpt.com/'}, timeout=30)
            wait_parallel_login(target)
        downloads = ParallelDownloads(work / 'images')
        js(f'localStorage.removeItem({json.dumps(key)})', target=targets[0])
        for target in targets:
            worker = target['id']
            item_id = previous.get('inflight', {}).get(worker)
            if item_id in scheduler.items:
                scheduler.pending.remove(item_id)
                scheduler.inflight[worker] = item_id
                scheduler.attempts[item_id] = previous.get('attempts', {}).get(item_id, 1)
                dispatched_at[worker] = time.time()
        status = 'access_wait' if cooling else 'generating'
        if cooling:
            stop_parallel(targets, key)
        print(f'並列 N={count}: 残り{len(todo)}/{len(queue)}件、別ウィンドウ{len(targets)}本、送信間隔{min_interval:g}秒', flush=True)
        while True:
            # 全ウィンドウの上限を先に確認し、途中で完了があっても投入を先行させない。
            snapshots = {t['id']: parallel_state(t, key) for t in targets}
            pacer.observe(snapshots, time.time())
            collect(work)
            _, left = remaining(work)
            have = ({i['id'] for i in queue} - {i['id'] for i in left}) | {
                i['id'] for i in queue if (work / 'images' / (i['id'] + '.png')).exists()}
            left = [item for item in left if not skip(item)]
            access.saved(have)
            if not left:
                scheduler.pending.clear()
                scheduler.inflight.clear()
                status = 'finished'
                result = record()
                heartbeat(work, verified=len(have), total=len(queue), status=status)
                print(f'投入対象の処理終了（保存済み{len(have)}/{len(queue)}枚） / {result["elapsed"]:.1f}秒 / 失敗{scheduler.failures} / 再投入{scheduler.retries}', flush=True)
                return result
            if cooling:
                if access.consecutive >= 4:
                    status = 'access_stopped'
                    record()
                    at = time.strftime('%H:%M', time.localtime(access.until))
                    print(f'アクセス制限が4回連続。終了コード75で停止します。外部からの再開は{at}以降です', flush=True)
                    raise SystemExit(75)
                if access.waiting():
                    if time.time()-last_wait_log >= 60:
                        access.log_wait()
                        last_wait_log = time.time()
                    record()
                    heartbeat(work, verified=len(have), total=len(queue), status='access_wait',
                              retry_at=access.until, access_consecutive=access.consecutive)
                    time.sleep(2)
                    continue
                for target in targets:
                    worker = target['id']
                    if scheduler.inflight.get(worker) in have and not snapshots[worker]['running']:
                        scheduler.finish(worker, True)
                resume_access_targets(targets, scheduler, key, pacer)
                access.finish()
                cooling, status, evidence = False, 'generating', None
                idle_since.clear()
                dispatched_at.update({worker: time.time() for worker in scheduler.inflight})
                print(f'待機終了。未完了{len(left)}件から再開します', flush=True)
                record()
                continue
            candidates = [s for s in snapshots.values() if s['liveLimit'] or s['shared']]
            limited = next((s for s in candidates if (s.get('liveLimit') or (s.get('shared') or {}).get('evidence') or {}).get('kind') == 'image_limit'),
                           candidates[0] if candidates else None)
            if limited:
                scheduler.stop()
                shared = limited.get('shared') or {}
                evidence = limited.get('liveLimit') or shared.get('evidence')
                if evidence and evidence.get('kind') == 'access_limit':
                    errors = stop_parallel(targets, key)
                    if errors:
                        raise RuntimeError('投入停止を確認できません: ' + '; '.join(errors))
                    pacer.cancel(time.time())
                    for target in targets:
                        if dismiss_access_notice(target):
                            print(f'{target["id"]}: アクセス制限通知の「了解」を押しました', flush=True)
                    access.detect(evidence)
                    cooling, status = True, 'access_wait'
                    record()
                    if access.consecutive >= 4:
                        status = 'access_stopped'
                        record()
                        at = time.strftime('%H:%M', time.localtime(access.until))
                        heartbeat(work, verified=len(have), total=len(queue), status=status, retry_at=access.until)
                        print(f'アクセス制限が4回連続。終了コード75で停止します。外部からの再開は{at}以降です', flush=True)
                        raise SystemExit(75)
                    access.log_wait()
                    last_wait_log = time.time()
                    continue
                until = limited.get('until') or shared.get('until') or (time.time()+1200)*1000
                note_limit(work, until)
                status = 'limit_wait'
                record()
                heartbeat(work, total=len(queue), status=status, evidence=evidence, until=until)
                print('全ウィンドウの投入停止: ' + json.dumps(evidence, ensure_ascii=False), flush=True)
                raise SystemExit(75)
            for target in targets:
                worker = target['id']
                state = snapshots[worker]
                item_id = scheduler.inflight.get(worker)
                if item_id is None:
                    if state['running']:
                        raise RuntimeError('割当て記録のない生成ループを検出しました')
                    continue
                if state['running']:
                    idle_since.pop(worker, None)
                    if time.time()-dispatched_at[worker] > STALL_LIMIT:
                        raise RuntimeError('生成処理の応答がありません。重複再送を停止しました')
                    continue
                if item_id in have:
                    scheduler.finish(worker, True)
                elif not state['installed'] or state.get('stopped'):
                    # リロード後も同じ会話で引き継ぎ、完成済みなら再送せず保存。
                    install_parallel(target, scheduler.items[item_id], key, resume=True)
                elif state['failed'] or time.time()-idle_since.setdefault(worker, time.time()) > 30:
                    scheduler.finish(worker, False)
            if scheduler.stopped:
                raise RuntimeError('同じ項目が2回失敗したため停止しました')
            for target in targets[:count]:
                worker = target['id']
                if worker in scheduler.inflight:
                    continue
                if max_attempts is not None and sum(scheduler.attempts.values()) >= max_attempts:
                    if not scheduler.inflight:
                        raise RuntimeError('実測の投入数上限に達したため停止しました')
                    break
                item = scheduler.assign(worker, skip)
                if item:
                    dispatched_at[worker] = time.time()
                    idle_since.pop(worker, None)
                    record()  # 送信前に所有権を保存。通信断で別ウィンドウへ再送しない。
                    install_parallel(target, item, key)
            grant_next_send(pacer, targets, snapshots, scheduler.inflight, record)
            record()
            heartbeat(work, verified=len(have), total=len(queue), status=status)
            time.sleep(2)
    except SystemExit:
        raise
    except Exception as exc:
        status = 'error'
        evidence = {'error': str(exc)}
        record()
        raise
    finally:
        errors = stop_parallel(targets, key)
        if downloads is not None:
            downloads.close()
        if errors:
            print('停止指示の未確認: ' + json.dumps(errors, ensure_ascii=False), flush=True)


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass
    args = parse_args()
    work = pathlib.Path(args.work).resolve()
    if not work.is_dir():
        sys.exit(f'作品フォルダが見つかりません: {work}')
    prepare_work(work)
    _lock_handle = acquire_lock(work)

    bridge.start()
    return run_parallel(work, args.parallel, min_interval=args.min_interval,
                        exclude=args.exclude, exclude_slots=args.exclude_slots)


if __name__ == '__main__':
    main()
