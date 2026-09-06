#!/usr/bin/env python3
"""開いているChromeのタブへ、外からJavaScriptを流し込む。

  python3 chrome_bridge.py start                     … Chromeを開き直す（初期設定はこれだけ）
  python3 chrome_bridge.py eval <URLの一部> <JSファイル>  … そのタブでJSを実行する
  python3 chrome_bridge.py tabs                      … 開いているタブを一覧する

拡張機能も、追加インストールも、メニューのチェックも要らない。
Chromeが最初から持っているデバッグ用の口を使うだけ。標準ライブラリのみで動く。

なぜこの形か:
  ・chatgpt.com はCSPが厳しく、ページの中から localhost へ通信できない。
    ページ内の eval も封じられている。外から入れるしかない。
  ・この口を通した実行はページのCSPに縛られないので、生成ループを入れられる。
  ・「Apple EventsからのJavaScriptを許可」のチェックが要る osascript 方式と違い、
    こちらは人が画面を触る場面がゼロになる。
"""
import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

PORT = 9222


def default_profile():
    if sys.platform == 'win32':
        base = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData' / 'Local'))
        return base / 'YamaImagegen' / 'Chrome'
    return Path.home() / '.yama_imagegen_chrome'


PROFILE = default_profile()


def chrome_candidates():
    if sys.platform == 'win32':
        roots = [os.environ.get('PROGRAMFILES'), os.environ.get('PROGRAMFILES(X86)'),
                 os.environ.get('LOCALAPPDATA')]
        return [Path(root) / 'Google' / 'Chrome' / 'Application' / 'chrome.exe'
                for root in roots if root]
    return [
        Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'),
        Path.home() / 'Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ]


def flags():
    return [
        f'--user-data-dir={PROFILE}',
        f'--remote-debugging-port={PORT}',
        # 隠れたタブのタイマーをChromeが凍結すると、「動いているのに進まない」状態になる。
        '--disable-backgrounding-occluded-windows',
        '--disable-background-timer-throttling',
        '--disable-renderer-backgrounding',
        '--no-first-run',
        '--no-default-browser-check',
    ]


def chrome_binary():
    found = next((p for p in chrome_candidates() if p.exists()), None)
    if not found:
        sys.exit('Google Chrome が見つかりません。Chromeをインストールしてから、もう一度実行してください。')
    return found


def prepare_profile(profile=PROFILE):
    """専用プロファイルに、画像保存で人の確認を求めない設定を入れる。"""
    default = Path(profile) / 'Default'
    default.mkdir(parents=True, exist_ok=True)
    prefs_path = default / 'Preferences'
    try:
        prefs = json.loads(prefs_path.read_text(encoding='utf-8')) if prefs_path.exists() else {}
    except (json.JSONDecodeError, OSError):
        prefs = {}

    profile_prefs = prefs.setdefault('profile', {})
    defaults = profile_prefs.setdefault('default_content_setting_values', {})
    defaults['automatic_downloads'] = 1       # 「複数ファイルを常に許可」
    exceptions = profile_prefs.setdefault('content_settings', {}).setdefault(
        'exceptions', {}).setdefault('automatic_downloads', {})
    exceptions['https://chatgpt.com,*'] = {'last_modified': '0', 'setting': 1}
    download = prefs.setdefault('download', {})
    download['prompt_for_download'] = False
    download['directory_upgrade'] = True

    tmp = prefs_path.with_suffix('.tmp')
    tmp.write_text(json.dumps(prefs, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    tmp.replace(prefs_path)


def _http(path):
    with urllib.request.urlopen(f'http://127.0.0.1:{PORT}{path}', timeout=5) as r:
        return json.load(r)


def is_ready():
    try:
        _http('/json/version')
        return True
    except (urllib.error.URLError, OSError):
        return False


def start():
    """通常のChromeに触れず、自動化専用Chromeを起動する。"""
    if is_ready():
        print('Chromeは既に準備できています')
        return
    prepare_profile()
    options = {
        'stdout': subprocess.DEVNULL,
        'stderr': subprocess.DEVNULL,
    }
    if sys.platform == 'win32':
        options['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        options['start_new_session'] = True
    subprocess.Popen([str(chrome_binary()), *flags()], **options)
    for _ in range(40):
        time.sleep(1)
        if is_ready():
            print('Chromeを準備しました')
            return
    sys.exit('Chromeが応答しません')


def tabs():
    return [t for t in _http('/json') if t.get('type') == 'page']


def command(ws_url, method, params=None, timeout=180):
    """CDPコマンドを1回だけ叩く。WebSocketは標準ライブラリで喋る。"""
    u = urlparse(ws_url)
    sock = socket.create_connection((u.hostname, u.port), timeout=10)
    try:
        sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        sock.sendall((
            f'GET {u.path} HTTP/1.1\r\n'
            f'Host: {u.hostname}:{u.port}\r\n'
            'Upgrade: websocket\r\nConnection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
        ).encode())
        head = b''
        while b'\r\n\r\n' not in head:
            head += sock.recv(4096)

        body = json.dumps({
            'id': 1, 'method': method, 'params': params or {},
        }).encode()
        mask = os.urandom(4)
        n = len(body)
        if n < 126:
            header = bytes([0x81, 0x80 | n])
        elif n < 65536:
            header = bytes([0x81, 0xFE]) + struct.pack('>H', n)
        else:
            header = bytes([0x81, 0xFF]) + struct.pack('>Q', n)
        sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(body)))

        def read(count):
            buf = b''
            while len(buf) < count:
                chunk = sock.recv(count - len(buf))
                if not chunk:
                    raise ConnectionError('接続が切れました')
                buf += chunk
            return buf

        while True:
            first, second = read(2)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack('>H', read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', read(8))[0]
            message = json.loads(read(length))
            if message.get('id') == 1:
                sock.close()
                return message
    finally:
        sock.close()


def evaluate(ws_url, expression):
    return command(ws_url, 'Runtime.evaluate', {
        'expression': expression, 'awaitPromise': True, 'returnByValue': True,
    })


def allow_downloads(download_path):
    """CDP側でも自動ダウンロードを許可し、作品の images/ へ直接保存する。"""
    target = next((t for t in tabs() if 'chatgpt.com' in t.get('url', '')), None)
    if not target:
        raise RuntimeError('chatgpt.com のタブがありません')
    path = Path(download_path).resolve()
    path.mkdir(parents=True, exist_ok=True)
    result = command(target['webSocketDebuggerUrl'], 'Browser.setDownloadBehavior', {
        'behavior': 'allow', 'downloadPath': str(path), 'eventsEnabled': True,
    })
    if result.get('error'):
        raise RuntimeError(result['error'].get('message', 'ダウンロード許可の設定に失敗しました'))
    return path


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    command = sys.argv[1]

    if command == 'start':
        start()
    elif command == 'tabs':
        for t in tabs():
            print(f"{t['title'][:50]:52} {t['url'][:70]}")
    elif command == 'eval':
        needle, jsfile = sys.argv[2], sys.argv[3]
        target = next((t for t in tabs() if needle in t.get('url', '')), None)
        if not target:
            sys.exit(f'{needle} を含むタブがありません')
        result = evaluate(target['webSocketDebuggerUrl'],
                          open(jsfile, encoding='utf-8').read())
        if 'exceptionDetails' in result.get('result', {}):
            print('エラー:', json.dumps(result['result']['exceptionDetails'],
                                     ensure_ascii=False)[:500])
            sys.exit(1)
        value = result.get('result', {}).get('result', {}).get('value')
        print(value if value is not None else json.dumps(result, ensure_ascii=False)[:400])
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
