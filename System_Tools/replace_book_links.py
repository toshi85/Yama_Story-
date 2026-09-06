#!/usr/bin/env python3
"""既存の書籍リンクだけを差し替える。既定は調査、--applyで更新・再取得検証。"""
import argparse
import copy
import datetime
import json
import time
from pathlib import Path

from add_book_promo_to_pinned_comments import service

REPLACEMENTS = {
    'https://www.amazon.co.jp/dp/B0HHKVMJTW': 'https://link.amazon/B05HZc0AN',
    'https://www.amazon.co.jp/kindle-dbs/hz/signup?tag=a120d-22':
        'https://www.amazon.co.jp/kindle-dbs/hz/signup?tag=a120a-22',
}


def replace(text):
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def pages(resource, **kwargs):
    token = None
    while True:
        result = resource.list(**kwargs, pageToken=token).execute()
        yield from result.get('items', [])
        token = result.get('nextPageToken')
        if not token:
            break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    yt = service()
    channel = yt.channels().list(part='snippet,contentDetails', mine=True).execute()['items'][0]
    print('Channel:', channel['snippet']['title'], channel['id'], flush=True)
    ids = [v['contentDetails']['videoId'] for v in pages(
        yt.playlistItems(), part='contentDetails', maxResults=50,
        playlistId=channel['contentDetails']['relatedPlaylists']['uploads'])]
    changes = []
    for offset in range(0, len(ids), 50):
        videos = yt.videos().list(part='snippet,localizations,status',
                                  id=','.join(ids[offset:offset+50])).execute()['items']
        for video in videos:
            new = copy.deepcopy(video)
            new['snippet']['description'] = replace(video['snippet']['description'])
            for loc in new.get('localizations', {}).values():
                if 'description' in loc:
                    loc['description'] = replace(loc['description'])
            if new != video:
                changes.append(('video', video, new))
    seen = set()

    def inspect(comment):
        if comment['id'] in seen:
            return
        seen.add(comment['id'])
        snippet = comment['snippet']
        if snippet.get('authorChannelId', {}).get('value') != channel['id']:
            return
        original = snippet['textOriginal']
        if replace(original) != original:
            new = copy.deepcopy(comment)
            new['snippet']['textOriginal'] = replace(original)
            changes.append(('comment', comment, new))

    for thread in pages(yt.commentThreads(), part='snippet,replies', maxResults=100,
                        allThreadsRelatedToChannelId=channel['id'], textFormat='plainText'):
        inspect(thread['snippet']['topLevelComment'])
        replies = thread.get('replies', {}).get('comments', [])
        for reply in replies:
            inspect(reply)
        if thread['snippet']['totalReplyCount'] > len(replies):
            for reply in pages(yt.comments(), part='snippet', maxResults=100,
                               parentId=thread['snippet']['topLevelComment']['id'], textFormat='plainText'):
                inspect(reply)
    counts = {kind: sum(c[0] == kind for c in changes) for kind in ('video', 'comment')}
    print(json.dumps({'videos_scanned': len(ids), 'comments_scanned': len(seen),
                      'changes': counts}, ensure_ascii=False), flush=True)
    backup = Path(__file__).resolve().parent / 'metadata_backups' / (
        'link_replace_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    backup.mkdir(parents=True)
    (backup / 'plan.json').write_text(json.dumps(changes, ensure_ascii=False, indent=2))
    print('Backup:', backup, flush=True)
    if not args.apply:
        return
    for kind, old, new in changes:
        if kind == 'video':
            fields = ('title', 'description', 'tags', 'categoryId', 'defaultLanguage', 'defaultAudioLanguage')
            body = {'id': new['id'], 'snippet': {k: v for k, v in new['snippet'].items() if k in fields}}
            part = 'snippet'
            if new.get('localizations'):
                body['localizations'] = new['localizations']
                part += ',localizations'
            yt.videos().update(part=part, body=body).execute()
            for attempt in range(6):
                actual = yt.videos().list(part=part, id=new['id']).execute()['items'][0]
                if (actual['snippet']['description'] == new['snippet']['description']
                        and actual.get('localizations', {}) == new.get('localizations', {})):
                    break
                time.sleep(2)
            assert actual['snippet']['description'] == new['snippet']['description']
            assert actual.get('localizations', {}) == new.get('localizations', {})
        else:
            body = {'id': new['id'], 'snippet': {'textOriginal': new['snippet']['textOriginal']}}
            yt.comments().update(part='snippet', body=body).execute()
            for attempt in range(6):
                actual = yt.comments().list(part='snippet', id=new['id'], textFormat='plainText').execute()['items'][0]
                if actual['snippet']['textOriginal'] == new['snippet']['textOriginal']:
                    break
                time.sleep(2)
            assert actual['snippet']['textOriginal'] == new['snippet']['textOriginal']
        print('VERIFIED', kind, new['id'], flush=True)
    (backup / 'verified.json').write_text(json.dumps(counts))


if __name__ == '__main__':
    main()
