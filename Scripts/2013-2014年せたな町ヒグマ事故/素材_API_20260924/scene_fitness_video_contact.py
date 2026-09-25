#!/usr/bin/env python3
"""Extract three moments per existing video for scene and motion inspection."""

import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent / "scene_fitness_review"
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 16)
SMALL = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 13)


def sample(video: Path, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for index, second in enumerate((0.4, 2.4, 4.4), 1):
        target = out / f"{index}.jpg"
        if target.is_file():
            continue
        subprocess.run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(second),
            "-i", str(video), "-frames:v", "1", "-q:v", "3", str(target)
        ], check=True)
        if not target.is_file():
            raise RuntimeError(f"Missing sampled frame: {video} at {second}s")


def main() -> None:
    rows = [row for row in json.loads((ROOT / "manifest.json").read_text()) if row["video"]]
    if len(rows) != 60:
        raise SystemExit(f"FAIL: expected 60 videos, got {len(rows)}")
    frames = ROOT / "video_frames"
    for index, row in enumerate(rows):
        video = Path(row["video"])
        sample(video, frames / row["asset"])
        if index % 10 == 9:
            subset = rows[index - 9:index + 1]
            page = Image.new("RGB", (1200, 1720), "#eeeeee")
            draw = ImageDraw.Draw(page)
            for j, item in enumerate(subset):
                y = j * 172
                draw.text((10, y + 3), f"{item['asset']} {item['scene'][:46]}", font=FONT, fill="black")
                for k in range(1, 4):
                    image_path = frames / item["asset"] / f"{k}.jpg"
                    with Image.open(image_path) as im:
                        im.thumbnail((380, 125), Image.Resampling.LANCZOS)
                        page.paste(im, (10 + (k - 1) * 395, y + 30))
                    draw.text((10 + (k - 1) * 395, y + 155), f"{(0.4, 2.4, 4.4)[k-1]}s", font=SMALL, fill="black")
            page.save(ROOT / f"video_contact_{index // 10 + 1:02d}.jpg", quality=85)
    print(f"PASS: {len(rows)} videos sampled at three times; 6 contact sheets")


if __name__ == "__main__":
    main()
