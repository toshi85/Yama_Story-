#!/usr/bin/env python3
"""キャラ画像が、添えた基準画像（CHAR-NN.png）の丸写しになっていないかを調べる（2026-09-26）。
117・120・122・128 で、ChatGPT が場面を描かずに基準画像そのままの笑顔の立ち姿を返した。
  python find_ref_copies.py           … 一覧だけ
  python find_ref_copies.py --reject  … 丸写しを rejected/ へ移し、.imagegen/no_ref_ids.txt に足す（次は基準なしで作る）
"""
import json, shutil, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageStat
HERE = Path(__file__).resolve().parent
IMG = HERE / "images"
def small(p):
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.convert("L").resize((64, 64))
refs = {p.stem: small(p) for p in IMG.glob("CHAR-*.png")}
hits = []
for p in sorted(IMG.glob("ASSET-*_char*.png")):
    s = small(p)
    for name, r in refs.items():
        diff = ImageStat.Stat(ImageChops.difference(s, r)).mean[0]
        if diff < 12:
            hits.append((p.stem, name, round(diff, 1)))
for h in hits: print("丸写し:", *h)
print(f"{len(hits)}件")
if "--reject" in sys.argv and hits:
    (HERE / "rejected").mkdir(exist_ok=True)
    nr = HERE / ".imagegen" / "no_ref_ids.txt"
    ids = set(nr.read_text().split()) if nr.exists() else set()
    for stem, _, _ in hits:
        shutil.move(str(IMG / f"{stem}.png"), str(HERE / "rejected" / f"{stem}_基準の丸写し.png"))
        rc = HERE / ".imagegen" / "receipts" / f"{stem}.json"
        if rc.exists(): rc.unlink()
        ids.add(stem)
    nr.write_text("\n".join(sorted(ids)) + "\n")
    print("rejected/ へ移し、基準なしで作り直す一覧に追加:", sorted(ids))
