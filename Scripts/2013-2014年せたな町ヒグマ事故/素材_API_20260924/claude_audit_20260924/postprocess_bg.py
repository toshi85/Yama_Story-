#!/usr/bin/env python3
"""ChatGPTで生成した背景（regen_bg/images/<id>.png）を納品寸法（1920x1072・RGB）に整え、fixed/画像/ へ元名で置く。
ついでに検査用の合成見本（新背景＋キャラ）を review_fixed/ に作る。
使い方: python postprocess_bg.py [id ...]（省略で全件）
"""
import sys, json, hashlib, io
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent
D = Path.home() / "Desktop/せたな町_素材_20260924/画像"
SRC = HERE / "regen_bg" / "images"; OUT = HERE / "fixed" / "画像"; OUT.mkdir(parents=True, exist_ok=True)
REV = HERE / "review_fixed"; REV.mkdir(exist_ok=True)
inv = json.load(open(HERE / "inventory.json"))
W, H = 1920, 1072
ids = sys.argv[1:] or sorted(p.stem for p in SRC.glob("*.png"))
log = json.load(open(HERE / "bg_fix_log.json")) if (HERE / "bg_fix_log.json").exists() else {}
for i in ids:
    src = SRC / f"{i}.png"
    if not src.exists(): print("missing", i); continue
    im = Image.open(src).convert("RGB")
    # 16:9 に中央クロップ → 1920x1072
    r = W / H; w, h = im.size
    if w / h > r: nw = int(h * r); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / r); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((W, H), Image.Resampling.LANCZOS)
    dst = OUT / f"{i}.png"; im.save(dst, optimize=True)
    asset = i.rsplit("_", 1)[0]
    log[i] = {"asset": asset, "source": str(src.relative_to(HERE)), "source_size": list(Image.open(src).size), "sha256": hashlib.sha256(dst.read_bytes()).hexdigest()}
    # 合成見本
    charp = OUT / f"{asset}_char.png"
    if not charp.exists(): charp = D / f"{asset}_char.png"
    canvas = im.convert("RGBA")
    if charp.exists():
        ch = Image.open(charp).convert("RGBA"); ch.thumbnail((int(W * .36), int(H * .72)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(ch, (int(W * .04), H - ch.height))
    prev = canvas.convert("RGB"); prev.thumbnail((1400, 1400))
    b = io.BytesIO(); prev.save(b, "JPEG", quality=76, optimize=True)
    while b.tell() > 290000: prev.thumbnail((int(prev.width * .85), int(prev.height * .85))); b = io.BytesIO(); prev.save(b, "JPEG", quality=72, optimize=True)
    (REV / f"{asset}_fixed.jpg").write_bytes(b.getvalue())
    print("ok", i, Image.open(src).size, "→", dst.name)
json.dump(log, open(HERE / "bg_fix_log.json", "w"), ensure_ascii=False, indent=1)
