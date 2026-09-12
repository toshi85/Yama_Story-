#!/usr/bin/env python3
"""Resumable, free metadata collection; no automatic retries or incident inference."""
import csv
import datetime
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import traceback

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
LOG = ROOT / '.codex/handoff/delegations/logs/2026-09-12-yama-next-topic'
NAMES = ['生きて山から帰るには【山岳遭難解説】', '山岳遭難ファイル', 'ゆっくり災難資料館【裏】']
YTDLP = shutil.which('yt-dlp')
state = {}
last_detail_finished = None


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def record(value):
    with (BASE / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(value, ensure_ascii=False) + '\n')


def run(label, target, flat=False, limit=None):
    global last_detail_finished
    path = BASE / (label + '.json')
    if path.exists():
        try:
            cached = json.loads(path.read_text())
            valid = isinstance(cached, dict) and (
                isinstance(cached.get('entries'), list) if flat else bool(cached.get('id')))
            if valid:
                record({'at': now(), 'label': label, 'status': 'cached', 'output': str(path)})
                print(now(), 'cached', label, flush=True)
                return cached
        except (ValueError, OSError):
            pass  # Incomplete outputs are not successful cache entries.
    args = [YTDLP, '--ignore-config', '--no-cache-dir', '--retries', '0', '--extractor-retries',
            '0', '--socket-timeout', '30', '--skip-download',
            '--ignore-no-formats-error', '--dump-single-json' if flat else '--dump-json']
    if not flat:
        args += ['--no-playlist']
    if flat:
        args += ['--flat-playlist']
    if limit is not None:
        args += ['--playlist-end', str(limit)]
    args += [target]
    if not flat and last_detail_finished is not None:
        time.sleep(max(0, 0.5 - (time.monotonic() - last_detail_finished)))
    state.update(stage=label, updated_at=now())
    save('collection_state.json', state)
    record({'started_at': now(), 'argv': args, 'output': str(path)})
    print(now(), label, flush=True)
    code = None
    try:
        with path.open('w') as out, (LOG / (label + '.stderr.log')).open('a') as err:
            p = subprocess.run(args, stdout=out, stderr=err, timeout=600)
        code = p.returncode
        if code:
            raise RuntimeError(label + ': yt-dlp exit ' + str(code))
        data = json.loads(path.read_text())
        if flat and not isinstance(data.get('entries'), list):
            raise RuntimeError(label + ': missing playlist entries')
        return data
    finally:
        if not flat:
            last_detail_finished = time.monotonic()
        record({'finished_at': now(), 'label': label, 'returncode': code})


def norm(value):
    return re.sub(r'\s+', '', value or '')


def export(label, entries):
    fields = ['id', 'title', 'view_count', 'upload_date', 'duration', 'channel',
              'channel_id', 'webpage_url']
    save(label + '.json', entries)
    with (BASE / (label + '.csv')).open('w') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(entries)


def select(entries):
    # Method 1 uses flat counts; method 2 uses individually acquired metadata.
    return [e for e in entries if isinstance(e.get('view_count'), (int, float))
            and e['view_count'] >= 100000]


def write_counts(counts):
    save('channel_counts.json', counts)
    report = BASE.parent / 'Next_Topic_Candidates_2026-09-12.md'
    marker = '\n## チャンネル取得件数\n'
    text = report.read_text().split(marker)[0]
    total = sum(c['listed'] for c in counts)
    available = sum(c['view_count_available'] for c in counts)
    lines = [f"取得方法: 手順{state['method']}（既定クライアント）。view_count取得率: {available}/{total}本。",
             '欠測は取得済みでも再生数が得られなかった動画。処理待ちは別欄。比較用の対象は既存の最大100本。', '',
             '| チャンネル | URL | 対象本数 | 再生数取得 | 取得後欠測 | 処理待ち | 10万回以上 |',
             '|---|---|---:|---:|---:|---:|---:|']
    for c in counts:
        lines.append(f"| {c['channel']} | {c['url']} | {c['listed']} | {c['view_count_available']} | {c['missing_view_count']} | {c['pending']} | {c['selected_100k']} |")
    report.write_text(text + marker + '\n'.join(lines) + '\n')


def refresh(i, channel, entries, processed, counts):
    selected = select(entries)
    available = sum(isinstance(e.get('view_count'), (int, float)) for e in entries)
    counts[i-1] = {'channel': channel['channel_name'], 'url': channel['url'],
                   'listed': len(entries), 'view_count_available': available,
                   'missing_view_count': sum(e['id'] in processed and e.get('view_count') is None for e in entries),
                   'pending': sum(e['id'] not in processed for e in entries),
                   'selected_100k': len(selected), 'scope': 'popular100' if i == 3 else 'all'}
    label = 'channel_'+str(i)
    export(label+('_popular100' if i == 3 else '_all'), entries)
    export(label+'_100k', selected)
    write_counts(counts)
    state.update(updated_at=now(), view_count_available=sum(c['view_count_available'] for c in counts),
                 total=sum(c['listed'] for c in counts), pending=sum(c['pending'] for c in counts))
    save('collection_state.json', state)


def main():
    # Persistent flock file is intentionally retained; kernel releases lock on exit.
    with (BASE / 'collection.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('Another collector holds collection.lock; not starting.', flush=True)
            return 3
        state.update(pid=os.getpid(), started_at=now(), status='running', stage='initializing')
        save('collection_state.json', state)
        print(now(), 'started', 'pid='+str(os.getpid()), 'cwd='+os.getcwd(),
              'yt-dlp='+str(YTDLP), flush=True)
        try:
            if not YTDLP:
                raise RuntimeError('yt-dlp missing from PATH')
            version = subprocess.check_output([YTDLP, '--ignore-config', '--version'], text=True).strip()
            save('environment.json', {'yt_dlp_version': version, 'started_at': now(),
                                     'player_client': 'default', 'executable': YTDLP})
            channels = json.loads((BASE / 'channels.json').read_text())
            if len(channels) != 3 or [c['requested_name'] for c in channels] != NAMES:
                raise RuntimeError('Previously identified channels do not match requested set')
            probe = run('channel_1_default_all_flat', channels[0]['url']+'/videos', flat=True)
            probe_rows = [e for e in probe.get('entries', []) if e]
            if not probe_rows:
                raise RuntimeError('Default-client probe returned no videos')
            has_views = any(isinstance(e.get('view_count'), (int, float)) for e in probe_rows)
            method = 1 if has_views else 2
            state['method'] = method
            save('collection_method.json', {'method': method, 'client': 'default',
                 'probe_available': sum(isinstance(e.get('view_count'), (int, float)) for e in probe_rows),
                 'probe_total': len(probe_rows), 'selected_at': now()})
            all_entries = []
            counts = []
            for i, channel in enumerate(channels, 1):
                comparison = i == 3
                suffix = '_popular100_flat' if comparison else '_all_flat'
                if method == 1:
                    target = channel['url'] + ('/videos?view=0&sort=p' if comparison else '/videos')
                    data = run('channel_'+str(i)+'_default'+suffix, target, flat=True,
                               limit=100 if comparison else None)
                else:
                    # Reuse the completed ID inventories: no new all-channel scan.
                    data = json.loads((BASE / ('channel_'+str(i)+suffix+'.json')).read_text())
                entries = [dict(e) for e in data.get('entries', []) if e]
                if comparison and len(entries) > 100:
                    raise RuntimeError('Comparison list exceeds 100 videos')
                for entry in entries:
                    if not isinstance(entry.get('view_count'), (int, float)):
                        entry['view_count'] = None
                    entry['metadata_status'] = 'pending' if method == 2 else 'flat_acquired'
                all_entries.append(entries)
                counts.append({'channel':channel['channel_name'], 'url':channel['url'],
                               'listed':len(entries), 'view_count_available':0, 'missing_view_count':0,
                               'pending':len(entries), 'selected_100k':0,
                               'scope':'popular100' if comparison else 'all'})
            write_counts(counts)
            for i, (channel, entries) in enumerate(zip(channels, all_entries), 1):
                processed = set()
                refresh(i, channel, entries, processed, counts)
                for entry in entries:
                    needs_detail = method == 2 or (entry.get('view_count') is not None
                        and entry['view_count'] >= 100000
                        and (not entry.get('upload_date') or entry.get('duration') is None))
                    if needs_detail:
                        detail = run('video_full_default_'+entry['id'],
                                     'https://www.youtube.com/watch?v='+entry['id'])
                        if detail.get('id') != entry['id']:
                            raise RuntimeError('Individual metadata video ID mismatch')
                        for key in ('upload_date', 'duration', 'title', 'webpage_url'):
                            if detail.get(key) is not None:
                                entry[key] = detail[key]
                        if method == 2:
                            views = detail.get('view_count')
                            entry['view_count'] = views if isinstance(views, (int, float)) else None
                        entry['metadata_status'] = 'acquired'
                    processed.add(entry['id'])
                    refresh(i, channel, entries, processed, counts)
            if not state['view_count_available']:
                raise RuntimeError('view_count unavailable for all videos after full metadata acquisition')
            state.update(status='channel_collection_complete', finished_at=now(),
                         next_action='題材同定、PDF事例抽出、既出28本照合、事件ごとのytsearch20、統合表、受け入れ検査。')
            return 0
        except Exception as exc:
            state.update(status='failed', finished_at=now(), error=str(exc))
            traceback.print_exc()
            return 1
        finally:
            save('collection_state.json', state)
            print(json.dumps(state, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    raise SystemExit(main())
