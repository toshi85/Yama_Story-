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
from urllib.parse import urlparse

PORT = 9222
CHROME = '/Applications/Google Chrome.app'
FLAGS = [
    f'--remote-debugging-port={PORT}',
    # 隠れたタブのタイマーをChromeが凍結すると、「動いているのに進まない」状態になる。
    '--disable-backgrounding-occluded-windows',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding',
]


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
    """Chromeをデバッグ用の口つきで開き直す。既に開いていれば何もしない。"""
    if is_ready():
        print('Chromeは既に準備できています')
        return
    if subprocess.run(['pgrep', '-x', 'Google Chrome'],
                      capture_output=True).returncode == 0:
        # 起動オプションは起動時にしか効かないので、一度きちんと閉じる
        subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to quit'],
                       capture_output=True)
        for _ in range(30):
            if subprocess.run(['pgrep', '-x', 'Google Chrome'],
                              capture_output=True).returncode != 0:
                break
            time.sleep(1)
    subprocess.run(['open', '-a', CHROME, '--args'] + FLAGS, check=True)
    for _ in range(40):
        time.sleep(1)
        if is_ready():
            print('Chromeを準備しました')
            return
    sys.exit('Chromeが応答しません')


def tabs():
    return [t for t in _http('/json') if t.get('type') == 'page']


def evaluate(ws_url, expression):
    """CDPのRuntime.evaluateを1回だけ叩く。WebSocketは標準ライブラリで喋る。"""
    u = urlparse(ws_url)
    sock = socket.create_connection((u.hostname, u.port), timeout=10)
    sock.settimeout(180)
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
        'id': 1, 'method': 'Runtime.evaluate',
        'params': {'expression': expression, 'awaitPromise': True, 'returnByValue': True},
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
