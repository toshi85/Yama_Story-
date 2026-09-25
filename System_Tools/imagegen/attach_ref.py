#!/usr/bin/env python3
"""ChatGPT の入力欄に、固定人物の基準画像（CHAR-NN.png）を参照画像として添える（2026-09-25）。

chrome_bridge.command は1コマンドごとに接続を開き直すので DOM のノード番号が持ち越せない。
ここでは1つの WebSocket 接続の中で DOM.getDocument → querySelectorAll → setFileInputFiles を続ける。

  python3 attach_ref.py <タブURLの一部> <画像パス>   … 手で試すとき
"""
import base64
import json
import os
import socket
import struct
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import chrome_bridge as bridge  # noqa: E402


class Session:
    """1本の CDP 接続で複数コマンドを順に叩く。"""
    def __init__(self, ws_url, timeout=60):
        u = urlparse(ws_url)
        self.sock = socket.create_connection((u.hostname, u.port), timeout=10)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        self.sock.sendall((f'GET {u.path} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\n'
                           'Upgrade: websocket\r\nConnection: Upgrade\r\n'
                           f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        head = b''
        while b'\r\n\r\n' not in head:
            head += self.sock.recv(4096)
        self.n = 0

    def _read(self, count):
        buf = b''
        while len(buf) < count:
            chunk = self.sock.recv(count - len(buf))
            if not chunk:
                raise ConnectionError('接続が切れました')
            buf += chunk
        return buf

    def call(self, method, params=None):
        self.n += 1
        body = json.dumps({'id': self.n, 'method': method, 'params': params or {}}).encode()
        mask = os.urandom(4)
        n = len(body)
        if n < 126:
            header = bytes([0x81, 0x80 | n])
        elif n < 65536:
            header = bytes([0x81, 0xFE]) + struct.pack('>H', n)
        else:
            header = bytes([0x81, 0xFF]) + struct.pack('>Q', n)
        self.sock.sendall(header + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(body)))
        while True:
            first, second = self._read(2)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack('>H', self._read(2))[0]
            elif length == 127:
                length = struct.unpack('>Q', self._read(8))[0]
            msg = json.loads(self._read(length))
            if msg.get('id') == self.n:
                if msg.get('error'):
                    raise RuntimeError(f"{method}: {msg['error'].get('message')}")
                return msg.get('result', {})

    def close(self):
        self.sock.close()


def attach(ws_url, image_paths):
    """入力欄の画像用 <input type=file> に画像（1枚または複数）を渡す。返り値＝使った input の accept。"""
    if isinstance(image_paths, (str, Path)):
        image_paths = [image_paths]
    files = [str(Path(x).resolve()) for x in image_paths]
    for f in files:
        if not Path(f).is_file():
            raise FileNotFoundError(f)
    s = Session(ws_url)
    try:
        root = s.call('DOM.getDocument', {'depth': 0})['root']['nodeId']
        nodes = s.call('DOM.querySelectorAll', {'nodeId': root, 'selector': 'input[type=file]'})['nodeIds']
        if not nodes:
            raise RuntimeError('ファイル入力欄が見つかりません')
        chosen, accept = None, ''
        for nid in nodes:
            a = s.call('DOM.getAttributes', {'nodeId': nid})['attributes']
            attrs = dict(zip(a[::2], a[1::2]))
            if 'image' in attrs.get('accept', ''):
                chosen, accept = nid, attrs.get('accept', '')
                break
        if chosen is None:
            chosen = nodes[0]
        s.call('DOM.setFileInputFiles', {'nodeId': chosen, 'files': files})
        return accept
    finally:
        s.close()


ATTACHED_JS = """(() => {
  const form = document.querySelector('form');
  if (!form) return JSON.stringify({ok:false, why:'no form'});
  const imgs = [...form.querySelectorAll('img')].filter(i => i.src);
  const send = document.querySelector('[data-testid="send-button"]') || [...document.querySelectorAll('button')].find(b => /^(送信|Send)/.test(b.getAttribute('aria-label')||''));
  const uploading = !!form.querySelector('[role="progressbar"], svg.animate-spin, .animate-spin');
  return JSON.stringify({ok: imgs.length >= EXPECT && !uploading && !!send && !send.disabled, imgs: imgs.length, uploading, send: !!send && !send.disabled});
})()"""


def wait_attached(ws_url, timeout=90, expect=1):
    """添付のプレビューが枚数ぶん出て、アップロードの回転が消え、送信ボタンが押せるまで待つ。"""
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        res = bridge.evaluate(ws_url, ATTACHED_JS.replace('EXPECT', str(int(expect))))
        last = res.get('result', {}).get('result', {}).get('value')
        try:
            st = json.loads(last)
        except Exception:
            st = {}
        if st.get('ok'):
            return st
        time.sleep(1)
    raise RuntimeError(f'添付の確認ができません: {last}')


if __name__ == '__main__':
    part, img = sys.argv[1], sys.argv[2]
    t = next(t for t in bridge.tabs() if part in t.get('url', ''))
    print('accept =', attach(t['webSocketDebuggerUrl'], img))
    print(wait_attached(t['webSocketDebuggerUrl']))
