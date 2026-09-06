#!/usr/bin/env python3
"""回収プロセスを単独で管理し、無応答・異常終了から保存済み位置へ復帰する。"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from integrity import verified_ids


def write_state(work, **data):
    path = work / '.imagegen/service.json'
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(dict(at=time.time(), **data), ensure_ascii=False, indent=2))
    tmp.replace(path)


def notify(message):
    print(message, flush=True)
    try:
        subprocess.run(['osascript', '-e', 'on run argv\n display notification (item 1 of argv) with title "戸沢村・画像復旧"\nend run', message], timeout=10, check=False, capture_output=True)
    except (OSError, subprocess.TimeoutExpired):
        pass


def stop_child(child):
    if child.poll() is None:
        os.killpg(child.pid, signal.SIGTERM)
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid, signal.SIGKILL)
            child.wait()


def clear_orphan(work):
    """サービス強制終了後に残った、自分のワーカーだけを片付ける。"""
    path = work / '.imagegen/service.json'
    if not path.exists():
        return
    pid = json.loads(path.read_text()).get('pid')
    if not isinstance(pid, int):
        return
    cmd = subprocess.run(['ps', '-p', str(pid), '-o', 'command='], capture_output=True, text=True).stdout
    if str(Path(__file__).with_name('recover.py')) + ' ' in cmd and str(work) in cmd:
        try:
            if os.getpgid(pid) == pid:
                os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass


def run_worker(command, work, restarts=0, stall=240, poll=5):
    child = subprocess.Popen(command, start_new_session=True)
    started = time.time()
    record = work / '.imagegen/recovery.json'
    try:
        while child.poll() is None:
            last = max(started, record.stat().st_mtime if record.exists() else started)
            write_state(work, status='running', pid=child.pid, restarts=restarts, last_progress=last)
            if time.time() - last > stall:
                print('無応答を検知：回収処理を終了し、保存済み位置から再開します', flush=True)
                stop_child(child)
                return 124
            time.sleep(poll)
        return child.returncode
    finally:
        stop_child(child)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('work', type=Path)
    ap.add_argument('--history', type=Path, required=True)
    ap.add_argument('--retry-unmatched', action='store_true')
    args = ap.parse_args()
    work = args.work.resolve()
    (work / '.imagegen').mkdir(exist_ok=True)
    # サービス自身の二重起動を防止。ワーカーは生成処理と共通の別ロックを取る。
    lock = (work / '.imagegen/recovery_service.lock').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('回収サービスは既に実行中です', flush=True)
        return
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    clear_orphan(work)
    queue = json.loads((work / 'image_queue.json').read_text())
    command = [sys.executable, '-u', str(Path(__file__).with_name('recover.py')), str(work), '--history', str(args.history.resolve())]
    if args.retry_unmatched:
        command.append('--retry-unmatched')
    restarts = 0
    while True:
        result = run_worker(command, work, restarts)
        if result == 0:
            count = len(verified_ids(work, queue))
            data = dict(at=time.time(), exit_code=0, verified=count, total=len(queue), visual_review_complete=False)
            path = work / '.imagegen/recovery_job_result.json'
            tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2)); tmp.replace(path)
            write_state(work, status='finished', verified=count, total=len(queue), restarts=restarts)
            notify(f'画像回収終了：{count}/{len(queue)}枠。' + ('目視確認が必要です。' if count == len(queue) else '未回収素材の対応が必要です。'))
            return
        restarts += 1
        # 制限通知は15分待つ。通信障害も繰り返し連打しない。
        delay = 900 if result in (75, 76) else min(300, 30 * 2 ** min(restarts - 1, 4))
        if restarts == 1 or restarts % 6 == 0:
            notify('ChatGPTの専用ブラウザでログイン確認が必要です。画像は保存されています。' if result == 76 else f'画像回収を自動復旧中です。{delay}秒後に再開します（再起動{restarts}回）。')
        until = time.time() + delay
        while time.time() < until:
            write_state(work, status='retry_wait', restarts=restarts, retry_at=until, exit_code=result)
            time.sleep(min(5, max(0, until-time.time())))


if __name__ == '__main__':
    main()
