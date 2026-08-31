#!/usr/bin/env python3
"""タスクスケジューラから画面を出さずにrun.pyを監督するWindows用ランナー。"""
import ctypes
import hashlib
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent


def main():
    if len(sys.argv) != 2:
        return 2
    work = pathlib.Path(sys.argv[1]).resolve()
    mutex_name = 'Local\\YamaImagegen_' + hashlib.sha256(
        str(work).lower().encode('utf-8')).hexdigest()[:20]
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if not mutex or ctypes.windll.kernel32.GetLastError() == 183:
        return 0
    state = work / '.imagegen'
    state.mkdir(parents=True, exist_ok=True)
    log_path = state / 'imagegen.log'

    while True:
        with log_path.open('a', encoding='utf-8', buffering=1) as log:
            result = subprocess.run(
                [sys.executable, '-u', str(HERE / 'run.py'), str(work)],
                stdout=log, stderr=subprocess.STDOUT,
            )
            if result.returncode == 0:
                return 0
            log.write(f'\n異常終了（終了コード {result.returncode}）— 30秒後に再起動します\n')
        time.sleep(30)


if __name__ == '__main__':
    raise SystemExit(main())
