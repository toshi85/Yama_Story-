"""要求文と保存画像の対応記録で進捗を判定する。"""
import hashlib
import json
from pathlib import Path


def verified_ids(work, queue):
    work = Path(work)
    if not (work / '.imagegen' / 'require_receipts').exists():
        return {p.stem for p in (work / 'images').glob('*.png')}
    records = {}
    recovery = work / '.imagegen' / 'recovery.json'
    if recovery.exists():
        records.update(json.loads(recovery.read_text()).get('verified', {}))
    for path in (work / '.imagegen' / 'receipts').glob('*.json'):
        try:
            item = json.loads(path.read_text())
            records[item['id']] = item
        except (OSError, ValueError, KeyError):
            continue
    done = set()
    for item in queue:
        record = records.get(item['id'], {})
        if record.get('prompt_sha256') != hashlib.sha256(item['prompt'].encode()).hexdigest():
            continue
        path = work / 'images' / (item['id'] + '.png')
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == record.get('sha256'):
            done.add(item['id'])
    return done
