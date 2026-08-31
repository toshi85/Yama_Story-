#!/usr/bin/env python3
"""受講生向けの一括設定。作品フォルダを1つ指定するだけで常駐実行まで行う。"""
import json
import os
import pathlib
import plistlib
import subprocess
import sys

import chrome_bridge as bridge

HERE = pathlib.Path(__file__).resolve().parent
LABEL = 'com.yama.imagegen'
WINDOWS_TASK = 'Yama Imagegen'


def run_launchctl(*args, check=True):
    return subprocess.run(
        ['launchctl', *args], check=check, capture_output=True, text=True,
    )


def ensure_queue(work):
    queue = work / 'image_queue.json'
    if queue.exists():
        items = json.loads(queue.read_text(encoding='utf-8'))
        if not isinstance(items, list) or not all('id' in x and 'prompt' in x for x in items):
            sys.exit(f'image_queue.json の形式が正しくありません: {queue}')
        return len(items)
    prompts = work / 'Asset_Prompts.md'
    if not prompts.exists():
        sys.exit('作品フォルダに Asset_Prompts.md または image_queue.json がありません。')
    subprocess.run(
        [sys.executable, str(HERE / 'extract_prompts.py'), str(prompts), str(queue)],
        check=True,
    )
    return len(json.loads(queue.read_text(encoding='utf-8')))


def install_macos_agent(work):
    state_dir = work / '.imagegen'
    state_dir.mkdir(parents=True, exist_ok=True)
    launch_agents = pathlib.Path.home() / 'Library' / 'LaunchAgents'
    launch_agents.mkdir(parents=True, exist_ok=True)
    plist_path = launch_agents / f'{LABEL}.plist'
    log_path = state_dir / 'imagegen.log'

    payload = {
        'Label': LABEL,
        'ProgramArguments': [
            sys.executable, '-u', str(HERE / 'run.py'), str(work),
        ],
        'WorkingDirectory': str(HERE),
        'RunAtLoad': True,
        # 異常終了だけ再起動。全画像完成（exit 0）後の再起動ループを防ぐ。
        'KeepAlive': {'SuccessfulExit': False},
        'ThrottleInterval': 30,
        'StandardOutPath': str(log_path),
        'StandardErrorPath': str(log_path),
        'EnvironmentVariables': {
            'PATH': os.environ.get('PATH', '/usr/local/bin:/usr/bin:/bin'),
            'PYTHONUNBUFFERED': '1',
        },
    }
    with plist_path.open('wb') as f:
        plistlib.dump(payload, f, sort_keys=False)

    domain = f'gui/{os.getuid()}'
    run_launchctl('bootout', f'{domain}/{LABEL}', check=False)
    result = run_launchctl('bootstrap', domain, str(plist_path), check=False)
    if result.returncode:
        sys.exit(f'自動起動の登録に失敗しました: {result.stderr.strip()}')
    run_launchctl('kickstart', '-k', f'{domain}/{LABEL}')
    return plist_path, log_path


def run_schtasks(*args, check=True):
    return subprocess.run(
        ['schtasks.exe', *args], check=check, capture_output=True, text=True,
    )


def install_windows_task(work):
    state_dir = work / '.imagegen'
    state_dir.mkdir(parents=True, exist_ok=True)
    log_path = state_dir / 'imagegen.log'
    pythonw = pathlib.Path(sys.executable).with_name('pythonw.exe')
    executable = pythonw if pythonw.exists() else pathlib.Path(sys.executable)
    action = subprocess.list2cmdline([
        str(executable), str(HERE / 'windows_runner.py'), str(work),
    ])

    # 現在のユーザーだけのログオンタスク。管理者権限やパスワード入力は不要。
    result = run_schtasks(
        '/Create', '/SC', 'ONLOGON', '/TN', WINDOWS_TASK,
        '/TR', action, '/RL', 'LIMITED', '/F', check=False,
    )
    if result.returncode:
        sys.exit(f'自動起動の登録に失敗しました: {(result.stderr or result.stdout).strip()}')
    run_schtasks('/End', '/TN', WINDOWS_TASK, check=False)
    result = run_schtasks('/Run', '/TN', WINDOWS_TASK, check=False)
    if result.returncode:
        sys.exit(f'画像生成の開始に失敗しました: {(result.stderr or result.stdout).strip()}')
    return WINDOWS_TASK, log_path


def main():
    if sys.platform not in {'darwin', 'win32'}:
        sys.exit('この配布版はmacOSまたはWindows用です。')
    if len(sys.argv) != 2:
        sys.exit('使い方: python3 install_for_student.py <作品フォルダ>')
    work = pathlib.Path(sys.argv[1]).expanduser().resolve()
    if not work.is_dir():
        sys.exit(f'作品フォルダが見つかりません: {work}')

    count = ensure_queue(work)
    # Chromeが起動する前に専用プロファイルへ「複数ダウンロードを常に許可」を入れる。
    # 稼働中の場合も run.py がCDPで同じ許可を設定する。
    if not bridge.is_ready():
        bridge.prepare_profile()
    if sys.platform == 'darwin':
        startup, log_path = install_macos_agent(work)
    else:
        startup, log_path = install_windows_task(work)

    print('画像生成の準備ができました。')
    print(f'  作品: {work}')
    print(f'  予定枚数: {count}')
    print(f'  自動起動設定: {startup}')
    print(f'  ログ: {log_path}')
    print('初回だけ、開いた専用ChromeでChatGPTにログインしてください。')


if __name__ == '__main__':
    main()
