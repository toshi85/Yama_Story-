#!/usr/bin/env python3
"""Build visual QA previews from the actual static background and cartoon PNGs."""

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
DELIVERY = Path.home() / "Desktop/せたな町_素材_20260924"
OUT = ROOT / "scene_fitness_review/composites"
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 16)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows = [x for x in json.loads((ROOT / "scene_fitness_review/manifest.json").read_text())
            if x["category"] == "キャラアニメーション"]
    if len(rows) != 132:
        raise SystemExit(f"FAIL: expected 132 character cuts, got {len(rows)}")
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for row in rows:
        no = int(row["asset"].split("-")[1])
        bg_path = Path(row["primary"])
        char_path = Path(row["character"])
        if not bg_path.is_file() or not char_path.is_file():
            raise SystemExit(f"FAIL: missing image pair for {row['asset']}")
        with Image.open(bg_path) as bg_src, Image.open(char_path) as char_src:
            bg = bg_src.convert("RGBA")
            char = char_src.convert("RGBA")
            char.thumbnail((int(bg.width * .36), int(bg.height * .72)), Image.Resampling.LANCZOS)
            bg.alpha_composite(char, (int(bg.width * .04), bg.height - char.height))
            target = OUT / f"ASSET-{no:03d}_composite.jpg"
            bg.convert("RGB").save(target, quality=88)
        names = sorted((f"画像/{bg_path.name}", f"画像/{char_path.name}"))
        source_sig = hashlib.sha256(json.dumps(
            [(name, digest(DELIVERY / name)) for name in names],
            ensure_ascii=False, separators=(",", ":")
        ).encode()).hexdigest()
        records.append({"asset_no": no, "scene": row["scene"], "preview": target.name,
                        "preview_sha256": digest(target), "source_sha256": source_sig,
                        "background": f"画像/{bg_path.name}", "character": f"画像/{char_path.name}"})
    (OUT / "manifest.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    for start in range(0, len(records), 12):
        sheet = Image.new("RGB", (1600, 1360), "#eeeeee")
        draw = ImageDraw.Draw(sheet)
        for offset, item in enumerate(records[start:start + 12]):
            x, y = (offset % 3) * 533, (offset // 3) * 340
            draw.text((x + 5, y + 3), f"ASSET-{item['asset_no']:03d} {item['scene'][:27]}",
                      font=FONT, fill="black")
            with Image.open(OUT / item["preview"]) as im:
                im.thumbnail((520, 305), Image.Resampling.LANCZOS)
                sheet.paste(im, (x + 5, y + 28))
        sheet.save(OUT / f"composite_contact_{start // 12 + 1:02d}.jpg", quality=86)
    print("PASS: 132 composite previews and 11 contact sheets created; no semantic PASS assigned")


if __name__ == "__main__":
    main()
