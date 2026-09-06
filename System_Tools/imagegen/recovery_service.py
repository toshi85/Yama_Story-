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
    if any(str(Path(__file__).with_name(name)) + ' ' in cmd for name in ('recover.py', 'run.py')) and str(work) in cmd:
        try:
            if os.getpgid(pid) == pid:
                os.killpg(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass


def run_worker(command, work, restarts=0, stall=240, poll=5, phase='recover'):
    child = subprocess.Popen(command, start_new_session=True)
    started = time.time()
    record = work / '.imagegen' / ('generation_status.json' if phase == 'generate' else 'recovery.json')
    try:
        while child.poll() is None:
            last = max(started, record.stat().st_mtime if record.exists() else started)
            write_state(work, status='running', phase=phase, pid=child.pid, restarts=restarts, last_progress=last)
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
    ap.add_argument('--generate-missing', action='store_true')
    args = ap.parse_args()
    work = args.work.resolve()
    (work / '.imagegen').mkdir(exist_ok=True)
    if args.generate_missing:
        (work / '.imagegen/require_receipts').touch(exist_ok=True)
        (work / '.imagegen/require_image_validation').touch(exist_ok=True)
    # サービス自身の二重起動を防止。ワーカーは生成処理と共通の別ロックを取る。
    lock = (work / '.imagegen/recovery_service.lock').open('a+')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('回収サービスは既に実行中です', flush=True)
        lock.close()
        return
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    clear_orphan(work)
    queue = json.loads((work / 'image_queue.json').read_text())
    command = [sys.executable, '-u', str(Path(__file__).with_name('recover.py')), str(work), '--history', str(args.history.resolve())]
    if args.retry_unmatched:
        command.append('--retry-unmatched')
    restarts = 0
    phase_path = work / '.imagegen/pipeline_phase.json'
    phase = json.loads(phase_path.read_text()).get('phase', 'recover') if phase_path.exists() else 'recover'
    if not args.generate_missing:
        phase = 'recover'
    while True:
        worker_command = [sys.executable, '-u', str(Path(__file__).with_name('run.py')), str(work)] if phase == 'generate' else command
        result = run_worker(worker_command, work, restarts, phase=phase)
        if result == 0:
            count = len(verified_ids(work, queue))
            if count < len(queue) and args.generate_missing:
                phase = 'generate'
                phase_path.write_text(json.dumps({'phase': phase}))
                print(f'自動移行：未完了の{len(queue)-count}枠を生成・検査します', flush=True)
                continue
            data = dict(at=time.time(), exit_code=0, verified=count, total=len(queue), visual_review_complete=False)
            path = work / '.imagegen/recovery_job_result.json'
            tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2)); tmp.replace(path)
            write_state(work, status='finished', phase=phase, verified=count, total=len(queue), restarts=restarts)
            notify((f'全画像の生成・自動検査終了：{count}/{len(queue)}枠。内容の最終目視確認が必要です。' if phase == 'generate' and count == len(queue) else f'画像回収終了：{count}/{len(queue)}枠。' + ('目視確認が必要です。' if count == len(queue) else '未回収素材の対応が必要です。')))
            lock.close()
            return
        restarts += 1
        # 制限通知は15分待つ。通信障害も繰り返し連打しない。
        delay = 900 if result in (75, 76) else min(300, 30 * 2 ** min(restarts - 1, 4))
        access_limit = work / '.imagegen/access_limit.json'
        if result == 75 and phase == 'generate' and access_limit.exists():
            delay = max(1, int(json.loads(access_limit.read_text())['until'] - time.time()) + 1)
        if restarts == 1 or restarts % 6 == 0:
            notify('ChatGPTの専用ブラウザでログイン確認が必要です。画像は保存されています。' if result == 76 else f'画像回収を自動復旧中です。{delay}秒後に再開します（再起動{restarts}回）。')
        until = time.time() + delay
        next_notice_check = 0
        while time.time() < until:
            write_state(work, status='retry_wait', phase=phase, restarts=restarts, retry_at=until, exit_code=result)
            if phase == 'generate' and time.time() >= next_notice_check:
                try:
                    from run import dismiss_access_notice
                    if dismiss_access_notice():
                        print('待機中のアクセス制限通知の「了解」を押しました', flush=True)
                except Exception as exc:
                    print(f'通知の確認待ち：{type(exc).__name__}', flush=True)
                next_notice_check = time.time() + 15
            time.sleep(min(5, max(0, until-time.time())))


if __name__ == '__main__':
    main()
