#!/usr/bin/env python3
"""Check exact cartoon inventory and create contact sheets for human style review."""

import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "画像_v3"
NAMES = [f"CHAR-0{i}-front-v3.png" for i in (2, 3, 4)]
NAMES += [f"ASSET-{x['asset_no']:03d}_char.png" for x in json.loads((ROOT / "cartoon_character_plan.json").read_text())]


def main() -> None:
    failures = []
    for name in NAMES:
        path = OUT / name
        if not path.is_file():
            failures.append(f"missing: {name}")
            continue
        try:
            with Image.open(path) as im:
                if im.size != (1024, 1024) or im.mode != "RGBA" or im.getchannel("A").getextrema()[0] != 0:
                    failures.append(f"size/alpha: {name}")
        except Exception as exc:
            failures.append(f"broken: {name}: {exc}")
    if failures:
        print(f"FAIL {len(failures)} items")
        for item in failures[:20]:
            print(item)
        raise SystemExit(1)
    columns, rows, cell, label_h = 6, 5, 180, 25
    for start in range(0, len(NAMES), columns * rows):
        sheet = Image.new("RGB", (columns * cell, rows * (cell + label_h)), "#e6e6e6")
        draw = ImageDraw.Draw(sheet)
        for offset, name in enumerate(NAMES[start:start + columns * rows]):
            x, y = (offset % columns) * cell, (offset // columns) * (cell + label_h)
            with Image.open(OUT / name) as im:
                im.thumbnail((cell - 8, cell - 8), Image.Resampling.LANCZOS)
                sheet.paste(im, (x + (cell - im.width) // 2, y + (cell - im.height) // 2), im)
            draw.text((x + 4, y + cell + 3), name.removesuffix(".png"), fill="black")
        sheet.save(ROOT / f"cartoon_contact_{start // (columns * rows) + 1:02d}.jpg", quality=90)
    print(f"PASS {len(NAMES)} images; {((len(NAMES)-1)//(columns*rows))+1} contact sheets")


if __name__ == "__main__":
    main()
