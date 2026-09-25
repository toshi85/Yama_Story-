#!/usr/bin/env python3
"""Create readable sheets of every character cut's static background."""

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "scene_fitness_review"
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 15)


def main() -> None:
    rows = [r for r in json.loads((OUT / "manifest.json").read_text())
            if r["category"] == "キャラアニメーション"]
    if len(rows) != 132:
        raise SystemExit(f"FAIL: expected 132 character cuts, found {len(rows)}")
    for start in range(0, len(rows), 12):
        page = Image.new("RGB", (1600, 1440), "#eeeeee")
        draw = ImageDraw.Draw(page)
        for offset, row in enumerate(rows[start:start + 12]):
            x, y = (offset % 3) * 533, (offset // 3) * 360
            draw.text((x + 5, y + 4), f"{row['asset']} {row['scene'][:28]}", font=FONT, fill="black")
            if row["primary"]:
                with Image.open(row["primary"]) as image:
                    image = image.convert("RGB")
                    image.thumbnail((520, 305), Image.Resampling.LANCZOS)
                    page.paste(image, (x + 5, y + 32))
            draw.text((x + 5, y + 340),
                      "動画併存" if row["video"] else "静止のみ", font=FONT,
                      fill="red" if row["video"] else "black")
        page.save(OUT / f"character_background_{start // 12 + 1:02d}.jpg", quality=88)
    print("PASS 132 static backgrounds, 11 sheets")


if __name__ == "__main__":
    main()
