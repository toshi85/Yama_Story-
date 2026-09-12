"""Serial metadata collection; aggregation is intentionally a later turn."""
import csv
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

BASE = Path(__file__).resolve().parent

def write_json(name, value):
    target = BASE / name
    temp = target.with_suffix(target.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temp.replace(target)

def targets():
    ids = []
    for name in ('channel_1_all.csv', 'channel_2_all.csv'):
        with (BASE / name).open(newline='') as stream:
            ids.extend(row['id'].strip() for row in csv.DictReader(stream))
    return list(dict.fromkeys(ids))

def present(vid):
    file = BASE / f'video_full_default_{vid}.json'
    return file.exists() and file.stat().st_size > 0

def main():
    lock = (BASE / 'collection2.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    (BASE / 'collection2.pid').write_text(str(os.getpid()) + '\n')
    ids = targets()
    failed_path = BASE / 'failed_ids.txt'
    previous_failed = set(failed_path.read_text().splitlines()) if failed_path.exists() else set()
    failed_path.touch(exist_ok=True)
    client = json.loads((BASE / 'collection2_client.json').read_text())['player_client']
    assert client in ('android', 'tv', 'ios')
    pending = [vid for vid in ids if not present(vid)]
    unresolved = {vid for vid in previous_failed if not present(vid)}
    failed_path.write_text(''.join(vid + '\n' for vid in ids if vid in unresolved))
    state = {'done': sum(present(vid) for vid in ids), 'remaining': len(pending),
             'failed': 0,
             'status': 'running'}
    write_json('collection_state2.json', state)
    print(json.dumps({'event': 'started', 'pid': os.getpid(), 'player_client': client, **state}), flush=True)
    try:
        for vid in pending:
            file = BASE / f'video_full_default_{vid}.json'
            ok = False
            for attempt in (1, 2):
                if attempt == 2:
                    time.sleep(30)
                # Disable yt-dlp's own retries and cache writes; retry budget lives here.
                argv = ['yt-dlp', '--quiet', '--no-warnings', '--skip-download',
                        '--dump-single-json', '--ignore-config', '--no-cache-dir',
                        '--retries', '0', '--extractor-retries', '0',
                        '--extractor-args', f'youtube:player_client={client}',
                        f'https://www.youtube.com/watch?v={vid}']
                started = time.time()
                print(json.dumps({'event': 'attempt', 'id': vid, 'attempt': attempt,
                                  'started': started}), flush=True)
                with file.open('w') as output:
                    result = subprocess.run(argv, stdout=output, cwd=BASE)
                try:
                    value = json.loads(file.read_text())
                    ok = result.returncode == 0 and isinstance(value, dict) and bool(value.get('title'))
                except (ValueError, OSError):
                    ok = False
                entry = {'id': vid, 'attempt': attempt, 'argv': argv, 'started': started,
                         'ended': time.time(), 'exit_code': result.returncode, 'valid': ok,
                         'output': str(file),
                         'sha256': hashlib.sha256(file.read_bytes()).hexdigest() if ok else None}
                with (BASE / 'collection2_commands.jsonl').open('a') as log:
                    log.write(json.dumps(entry, ensure_ascii=False) + '\n')
                if ok:
                    break
                file.unlink(missing_ok=True)
            if ok:
                state['done'] += 1
                unresolved.discard(vid)
            else:
                unresolved.add(vid)
                state['failed'] += 1
            failed_path.write_text(''.join(item + '\n' for item in ids if item in unresolved))
            state['remaining'] -= 1
            write_json('collection_state2.json', state)
            print(json.dumps({'event': 'processed', 'id': vid, **state}), flush=True)
            time.sleep(3)
        state['status'] = 'complete'
        write_json('collection_state2.json', state)
        print(json.dumps({'event': 'finished', 'exit_code': 0, **state}), flush=True)
    except BaseException:
        state['status'] = 'error'
        write_json('collection_state2.json', state)
        raise

if __name__ == '__main__':
    main()
