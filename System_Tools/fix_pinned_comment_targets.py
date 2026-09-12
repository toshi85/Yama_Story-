"""Correct only measured pinned targets and the comments modified in the previous run."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from update_pinned_comments_products import BASE, CHANNEL_ID, PRODUCTS, connect, strip_book, product_block

PREVIOUS = BASE / 'metadata_backups/pinned_products_20260912_173131'


def read_comment(youtube, cid, video):
    response = youtube.comments().list(part='snippet', id=cid, textFormat='plainText').execute(num_retries=0)
    entries = response.get('items', [])
    if len(entries) != 1:
        raise ValueError('Comment missing or ambiguous')
    snippet = entries[0]['snippet']
    if (snippet.get('authorChannelId', {}).get('value') != CHANNEL_ID
            or snippet.get('videoId') != video or snippet.get('parentId')):
        raise ValueError('Comment is not a channel-owned top-level comment on this video')
    return snippet['textOriginal']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    mapping = json.loads((BASE / 'affiliate_video_map.json').read_text())
    products = json.loads((BASE / 'affiliate_products.json').read_text())['items']
    pinned = json.loads((BASE / 'pinned_comment_ids.json').read_text())
    if set(pinned) != set(mapping):
        raise ValueError('Pinned results must cover exactly the 28 mapped videos')
    backups = {v: json.loads((PREVIOUS / (v + '.json')).read_text()) for v in mapping}
    backup_dir = BASE / 'metadata_backups' / ('pinned_fix_' + datetime.now().strftime('%Y%m%d_%H%M%S'))
    counts = dict.fromkeys(['ok', 'fixed-pinned', 'reverted', 'unknown', 'FAIL'], 0)
    youtube = connect()
    print('MODE ' + ('apply' if args.apply else 'dry-run'), flush=True)

    def report(status, video, cid, text, detail=''):
        counts[status] += 1
        print(f'{status} {video} {cid or "-"} {len(text)}' + (' ' + detail if detail else ''), flush=True)

    def update(video, cid, old, new):
        if not new.strip() or len(new) > 9000:
            raise ValueError('Replacement is empty or exceeds 9000 characters')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', cid):
            raise ValueError('Unexpected comment ID format')
        if not args.apply:
            return
        backup_dir.mkdir(parents=True, exist_ok=True)
        with (backup_dir / (cid + '.json')).open('x', encoding='utf-8') as stream:
            json.dump({'video_id': video, 'comment_id': cid, 'text': old}, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        youtube.comments().update(part='snippet', body={'id': cid, 'snippet': {'textOriginal': new}}).execute(num_retries=0)

    for video, keys in mapping.items():
        cid = pinned[video]['pinned_comment_id']
        text = ''
        if not cid:
            report('unknown', video, None, '')
            continue
        try:
            previous = backups[video]
            if previous['video_id'] != video:
                raise ValueError('Backup video mismatch')
            text = read_comment(youtube, cid, video)
            if cid == previous['comment_id']:
                report('ok', video, cid, text)
                continue
            wrong_id = previous['comment_id']
            wrong_text = read_comment(youtube, wrong_id, video)
            restored = strip_book(previous['text'])
            expected_previous_update = product_block(keys, products) + restored
            if wrong_text not in (expected_previous_update, restored):
                raise ValueError('Nonpinned comment changed since previous update; manual review needed')
            if text.count(PRODUCTS) > 1:
                raise ValueError('Pinned comment already has duplicate product headings')
            new_pinned = text if PRODUCTS in text else product_block(keys, products) + strip_book(text)
            # Validate both replacements before any mutation for this video.
            if any(not candidate.strip() or len(candidate) > 9000 for candidate in (new_pinned, restored)):
                raise ValueError('Replacement is empty or exceeds 9000 characters')
            if new_pinned != text:
                update(video, cid, text, new_pinned)
                report('fixed-pinned', video, cid, new_pinned)
            else:
                report('ok', video, cid, text)
            if wrong_text != restored:
                update(video, wrong_id, wrong_text, restored)
                report('reverted', video, wrong_id, restored)
            else:
                report('ok', video, wrong_id, wrong_text)
        except Exception as exc:
            http_status = getattr(getattr(exc, 'resp', None), 'status', None)
            detail = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
            report('FAIL', video, cid, text, f'error={detail} http_status={http_status}')
    print('SUMMARY ' + json.dumps(counts), flush=True)
    if backup_dir.exists():
        print('BACKUP ' + str(backup_dir), flush=True)
    return int(counts['FAIL'] > 0)


if __name__ == '__main__':
    raise SystemExit(main())
