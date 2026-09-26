#!/usr/bin/env python3
"""目視点検用の一覧画像（ラベル付き・透過は市松で）を作る。 python make_sheet.py 出力.jpg ID...（images/ID.png）"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
out, ids = sys.argv[1], sys.argv[2:]
W, H, cols = 420, 260, 3
rows = (len(ids) + cols - 1) // cols
sheet = Image.new("RGB", (W * cols, (H + 22) * rows), "white")
try:
    font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 16)
except Exception:
    font = ImageFont.load_default()
for i, name in enumerate(ids):
    im = Image.open(Path("images") / f"{name}.png").convert("RGBA")
    im.thumbnail((W - 6, H - 6))
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    d = ImageDraw.Draw(bg)
    for y in range(0, im.size[1], 12):
        for x in range(0, im.size[0], 12):
            if (x // 12 + y // 12) % 2: d.rectangle([x, y, x + 11, y + 11], fill=(215, 215, 215, 255))
    bg.alpha_composite(im)
    x, y = (i % cols) * W, (i // cols) * (H + 22)
    sheet.paste(bg.convert("RGB"), (x + (W - im.size[0]) // 2, y + 22 + (H - im.size[1]) // 2))
    ImageDraw.Draw(sheet).text((x + 6, y + 3), name, fill="black", font=font)
sheet.save(out, quality=70)
print(out, Path(out).stat().st_size // 1024, "KB")
