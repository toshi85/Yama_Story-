"""要求文と保存画像の対応記録で進捗を判定する。"""
import hashlib
import json
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=1024)
def image_valid(path, size, mtime, aspect, slot):
    from PIL import Image
    try:
        with Image.open(path) as im:
            im.load()
            expected = 1 if aspect == '1:1' else 16/9
            if im.format != 'PNG' or abs(im.width / im.height - expected) > .06:
                return False
            if slot in ('char', 'char_ref'):
                if 'A' not in im.getbands() or im.getchannel('A').getextrema()[0] == 255 or im.getchannel('A').getextrema()[1] == 0:
                    return False
            return True
    except (OSError, ValueError):
        return False


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
            if (work / '.imagegen/require_image_validation').exists():
                stat = path.stat()
                if not image_valid(str(path), stat.st_size, stat.st_mtime_ns, item['aspect'], item['slot']):
                    continue
            done.add(item['id'])
    return done
