#!/usr/bin/env python3
"""バッチ検査の準備（フック上限300KB以内・長辺1536pxの検査用JPEG）:
 review/ASSET-xxx_still.jpg   … 静止背景の原寸相当（1536px）
 review/ASSET-xxx_char.jpg    … 透過キャラを市松の上に置いた確認画（1024→768px）
 review/ASSET-xxx_composite.jpg … 現物の背景＋キャラの合成見本
 review/ASSET-xxx_video.jpg   … 動画を1fpsで全尺コマ抜き＋最終コマ
使い方: python batch_prep.py 1 12
"""
import json, subprocess, sys, hashlib, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
D = Path.home() / "Desktop/せたな町_素材_20260924"
spec = {a["no"]: a for a in json.load(open(HERE / "spec.json"))}
inv = json.load(open(HERE / "inventory.json"))
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 20)
R = HERE / "review"; R.mkdir(exist_ok=True); TMP = HERE / "tmp"; TMP.mkdir(exist_ok=True)
LIMIT = 290_000
def save_small(im, out, long_edge=1536):
    im = im.convert("RGB"); im.thumbnail((long_edge, long_edge), Image.Resampling.LANCZOS)
    for q in (82, 74, 66, 58, 50, 42):
        b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
        if b.tell() <= LIMIT: break
    while b.tell() > LIMIT and long_edge > 700:
        long_edge = int(long_edge * 0.85); im.thumbnail((long_edge, long_edge), Image.Resampling.LANCZOS)
        b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    out.write_bytes(b.getvalue()); return b.tell(), q
def checker(size, cell=32):
    im = Image.new("RGB", size, "#cfcfcf"); d = ImageDraw.Draw(im)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2: d.rectangle((x, y, x + cell, y + cell), fill="#9a9a9a")
    return im
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for no in range(lo, hi + 1):
    a = spec[no]; stem = f"ASSET-{no:03d}"; files = inv.get(stem, {}); line = [f"{stem} [{a['category']}]"]
    bgkey = "still" if "still" in files else ("bg" if "bg" in files else None)
    if bgkey:
        n, q = save_small(Image.open(D / files[bgkey]["path"]), R / f"{stem}_still.jpg"); line.append(f"still q{q} {n//1024}KB")
    if "char" in files:
        ch = Image.open(D / files["char"]["path"]).convert("RGBA")
        base = checker(ch.size).convert("RGBA"); base.alpha_composite(ch)
        n, q = save_small(base, R / f"{stem}_char.jpg", 768); line.append(f"char {n//1024}KB")
        if bgkey:
            bg = Image.open(D / files[bgkey]["path"]).convert("RGBA"); c2 = ch.copy()
            c2.thumbnail((int(bg.width * .36), int(bg.height * .72)), Image.Resampling.LANCZOS)
            bg.alpha_composite(c2, (int(bg.width * .04), bg.height - c2.height))
            n, q = save_small(bg, R / f"{stem}_composite.jpg"); line.append(f"composite {n//1024}KB")
            # 静止背景（上）＋合成（下）を1枚に: キャラの裏に隠れる人物も見える
            top = Image.open(D / files[bgkey]["path"]).convert("RGB"); top.thumbnail((1280, 1280)); bot = bg.convert("RGB"); bot.thumbnail((1280, 1280))
            pair = Image.new("RGB", (1280, top.height + bot.height + 6), "#000"); pair.paste(top, (0, 0)); pair.paste(bot, (0, top.height + 6))
            n, q = save_small(pair, R / f"{stem}_pair.jpg", 1600); line.append(f"pair q{q} {n//1024}KB")
    if "video" in files:
        v = D / files["video"]["path"]; dur = files["video"]["duration"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vf", "fps=1,scale=512:-1", str(TMP / f"{stem}_f%02d.png")], check=True)
        frames = sorted(TMP.glob(f"{stem}_f*.png"))
        last = TMP / f"{stem}_last.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", str(v), "-frames:v", "1", "-vf", "scale=512:-1", str(last)], check=True)
        frames.append(last); cols = 3; rows = (len(frames) + cols - 1) // cols
        w, h = Image.open(frames[0]).size
        tile = Image.new("RGB", (cols * w, rows * (h + 24)), "#222"); dr = ImageDraw.Draw(tile)
        for i, f in enumerate(frames):
            x, y = (i % cols) * w, (i // cols) * (h + 24)
            tile.paste(Image.open(f).convert("RGB"), (x, y + 24))
            dr.text((x + 6, y + 2), f"{stem} t={i if f != last else dur}s", font=FONT, fill="white")
        n, q = save_small(tile, R / f"{stem}_video.jpg", 1536); line.append(f"video {dur}s {len(frames)}コマ {n//1024}KB")
        for f in frames: f.unlink()
    print(" | ".join(line))
