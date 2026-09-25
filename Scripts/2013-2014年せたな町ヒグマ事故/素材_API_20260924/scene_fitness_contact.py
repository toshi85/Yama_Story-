#!/usr/bin/env python3
"""Put every delivered visual beside its actual scene instruction for visual QA."""

import json
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "Asset_Prompts_Full.md"
DELIVERY = Path.home() / "Desktop/せたな町_素材_20260924"
OUT = ROOT / "scene_fitness_review"
MARK = re.compile(r"【制作メモ】ASSET-(\d+) \[([^\]]+)\]")
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 18)
SMALL = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 14)


def draw_thumb(canvas, image_path, box):
    d = ImageDraw.Draw(canvas)
    x, y, w, h = box
    d.rectangle((x, y, x+w-1, y+h-1), outline="#999")
    if not image_path.is_file():
        d.text((x+8, y+8), "素材なし", font=FONT, fill="red")
        return
    with Image.open(image_path) as im:
        im = im.convert("RGBA")
        im.thumbnail((w-8, h-8), Image.Resampling.LANCZOS)
        bg = Image.new("RGBA", im.size, "white")
        bg.alpha_composite(im)
        canvas.paste(bg.convert("RGB"), (x+(w-im.width)//2, y+(h-im.height)//2))


def main():
    src = SOURCE.read_text()
    markers = list(MARK.finditer(src))
    if len(markers) != 220:
        raise SystemExit("FAIL: 220 cuts required")
    OUT.mkdir(exist_ok=True)
    rows = []
    for i, m in enumerate(markers):
        no, kind = int(m.group(1)), m.group(2)
        block = src[m.start():markers[i+1].start() if i+1<len(markers) else len(src)]
        scene = re.search(r"^シーン: (.+)$", block, re.M)
        if not scene:
            raise SystemExit(f"FAIL: scene missing {no}")
        stem = f"ASSET-{no:03d}"
        images = DELIVERY / "画像"
        primary = next((images / f"{stem}_{suffix}.png" for suffix in ("still", "bg") if (images / f"{stem}_{suffix}.png").is_file()), None)
        character = images / f"{stem}_char.png"
        rows.append({"asset":stem,"category":kind,"scene":scene.group(1),"primary":str(primary) if primary else None,"character":str(character) if character.is_file() else None,"video":str(DELIVERY/'動画'/f'{stem}_video.mp4') if (DELIVERY/'動画'/f'{stem}_video.mp4').is_file() else None})
    (OUT/'manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    for start in range(0,len(rows),20):
        page=Image.new("RGB",(1200,2300),"#eee")
        d=ImageDraw.Draw(page)
        for j,row in enumerate(rows[start:start+20]):
            x=(j%2)*600;y=(j//2)*230
            d.rectangle((x+2,y+2,x+597,y+227),outline="#bbb",width=2)
            d.text((x+8,y+5),f"{row['asset']} [{row['category']}]",font=FONT,fill="black")
            scene=row['scene']
            for k in range(0,min(len(scene),72),35):
                d.text((x+8,y+30+(k//35)*21),scene[k:k+35],font=SMALL,fill="black")
            primary=Path(row['primary']) if row['primary'] else None
            character=Path(row['character']) if row['character'] else None
            if primary:draw_thumb(page,primary,(x+8,y+78,370 if character else 580,142))
            if character:draw_thumb(page,character,(x+385,y+78,205,142))
            if not primary and not character:
                d.text((x+10,y+90),"編集者担当 / ローカル素材なし",font=FONT,fill="#555")
            else:
                d.text((x+8,y+204),"背景/開始画像" if primary else "背景なし",font=SMALL,fill="#555")
                if character:d.text((x+385,y+204),"キャラ",font=SMALL,fill="#555")
        page.save(OUT/f"scene_contact_{start//20+1:02d}.jpg",quality=87)
    print(f"PASS {len(rows)} scene cards, 11 contact sheets")


if __name__ == '__main__':
    main()
