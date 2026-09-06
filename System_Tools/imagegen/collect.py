#!/usr/bin/env python3
"""~/Downloads に落ちた生成画像を、作品フォルダの images/ へ回収する。

使い方:
  python3 collect.py <作品フォルダ>          … 回収して進捗を表示
  python3 collect.py <作品フォルダ> --watch  … 30秒おきに回収し続ける

ChatGPT のページ側ドライバが「アセット番号.png」の名前で落とすので、
キューに載っている id と一致するファイルだけを移動する。
"""
import json
import re
import shutil
import sys
import time
from collections import Counter
from pathlib import Path
from integrity import verified_ids

DOWNLOADS = Path.home() / "Downloads"


def collect(work: Path) -> int:
    queue = json.loads((work / "image_queue.json").read_text(encoding="utf-8"))
    ids = {q["id"] for q in queue}
    images = work / "images"
    images.mkdir(parents=True, exist_ok=True)

    strict = (work / '.imagegen' / 'require_receipts').exists()
    receipts = work / '.imagegen' / 'receipts'
    receipts.mkdir(parents=True, exist_ok=True)
    for folder in (DOWNLOADS, images):
        for receipt in folder.glob('*.receipt*.json'):
            try:
                data = json.loads(receipt.read_text())
                if data.get('id') not in ids:
                    continue
            except (OSError, ValueError):
                continue
            shutil.move(str(receipt), str(receipts / (data['id'] + '.json')))

    moved = 0
    for f in DOWNLOADS.glob("*.png"):
        # Chrome の重複回避サフィックス "ASSET-004_char (1).png" も拾う
        stem = re.sub(r"\s*\(\d+\)$", "", f.stem)
        if stem not in ids:
            continue
        if strict:
            receipt = receipts / (stem + '.json')
            import hashlib
            valid = receipt.exists() and hashlib.sha256(f.read_bytes()).hexdigest() == json.loads(receipt.read_text()).get('sha256')
            if not valid:
                quarantine = work / '.imagegen' / 'unverified_downloads'
                quarantine.mkdir(exist_ok=True)
                target = quarantine / (str(time.time_ns()) + '_' + f.name)
                shutil.move(str(f), str(target))
                continue
        # ダウンロードは生成した時にしか起きないので、新しい方を常に採用する
        dest = images / f"{stem}.png"
        shutil.move(str(f), str(dest))
        moved += 1
    return moved


def report(work: Path):
    queue = json.loads((work / "image_queue.json").read_text(encoding="utf-8"))
    images = work / "images"
    have = verified_ids(work, queue)
    todo = [q for q in queue if q["id"] not in have]
    print(f"完了 {len(queue) - len(todo)} / 全 {len(queue)}  残り {len(todo)}")
    if todo:
        print("残り内訳:", dict(Counter(f'{t["kind"]}/{t["slot"]}' for t in todo)))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    work = Path(sys.argv[1])
    watch = "--watch" in sys.argv

    while True:
        n = collect(work)
        if n:
            print(f"{n}枚 回収", flush=True)
        report(work)
        if not watch:
            return
        time.sleep(30)


if __name__ == "__main__":
    main()
