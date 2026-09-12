"""Measure top-level pinned comment IDs with yt-dlp, never infer from length."""
import json
import shutil
import subprocess
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOG = BASE.parents[1] / '.codex/handoff/delegations/logs/2026-09-12-pinned-affiliate'


def main():
    videos = json.loads((BASE / 'affiliate_video_map.json').read_text())
    results = {v: {'pinned_comment_id': None} for v in videos}
    output = BASE / 'pinned_comment_ids.json'
    executable = shutil.which('yt-dlp')
    if not executable:
        raise RuntimeError('yt-dlp executable not found')
    LOG.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    evidence = {}
    halted_by_block = False
    for index, video in enumerate(videos):
        if halted_by_block:
            evidence[video] = [{'not_attempted': True, 'reason': 'Earlier block persisted after one delayed retry'}]
            (LOG / 'detection-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
            print(f'UNKNOWN {video} None reason=earlier-block-persists', flush=True)
            continue
        if index:
            time.sleep(5)
        attempts = []
        for attempt in range(1, 3):
            directory = LOG / 'yt-dlp' / video / str(attempt)
            directory.mkdir(parents=True, exist_ok=True)
            command = [executable, '--ignore-config', '--no-cache-dir', '--skip-download',
                       '--write-info-json', '--write-comments', '--no-warnings',
                       '--ignore-no-formats-error', '--socket-timeout', '30',
                       '--retries', '0', '--extractor-retries', '0',
                       '--extractor-args', 'youtube:comment_sort=top;max_comments=100,100,0,0',
                       '-o', str(directory / '%(id)s'),
                       'https://www.youtube.com/watch?v=' + video]
            timed_out = False
            with (directory / 'extract.log').open('w') as stream:
                try:
                    process = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT,
                                             timeout=180, check=False)
                    exit_code = process.returncode
                except subprocess.TimeoutExpired:
                    timed_out = True
                    exit_code = 124
            raw_log = (directory / 'extract.log').read_text(errors='replace')
            lower = raw_log.lower()
            blocked = any(word in lower for word in ['429', 'too many requests', 'confirm you’re not a bot',
                        "confirm you're not a bot", 'ip has been blocked', 'http error 403'])
            info_file = directory / (video + '.info.json')
            comments = []
            parse_error = None
            if info_file.exists():
                try:
                    comments = json.loads(info_file.read_text()).get('comments') or []
                except (ValueError, OSError) as exc:
                    parse_error = type(exc).__name__
            pinned = {c['id']: c for c in comments if c.get('is_pinned') is True
                      and c.get('parent') == 'root' and c.get('id')}
            attempts.append({'argv': command, 'exit_code': exit_code, 'timeout': timed_out,
                             'blocked': blocked, 'comments': len(comments), 'pinned': len(pinned),
                             'parse_error': parse_error, 'log': str(directory / 'extract.log')})
            if len(pinned) == 1:
                cid, comment = next(iter(pinned.items()))
                results[video] = {'pinned_comment_id': cid, 'head': comment.get('text', '')[:60]}
                break
            if blocked and attempt == 1:
                print(f'RETRY {video} delay=60 reason=rate-limit-or-block', flush=True)
                time.sleep(60)
                continue
            break
        if not results[video]['pinned_comment_id'] and len(attempts) == 2 and attempts[-1]['blocked']:
            halted_by_block = True
        evidence[video] = attempts
        output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
        (LOG / 'detection-evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
        value = results[video]
        print(('FOUND' if value['pinned_comment_id'] else 'UNKNOWN') + ' ' + video + ' '
              + str(value['pinned_comment_id']) + ' ' + json.dumps(value.get('head', ''), ensure_ascii=False), flush=True)
    found = sum(bool(v['pinned_comment_id']) for v in results.values())
    print('SUMMARY ' + json.dumps({'videos': len(results), 'identified': found, 'UNKNOWN': len(results)-found}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
