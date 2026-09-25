#!/usr/bin/env python3
"""Audit generated Setana media against the locked API manifests."""

import json
from pathlib import Path
import subprocess
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parent
IMAGES = json.loads((ROOT / "images_plan.json").read_text())
VIDEOS = json.loads((ROOT / "video_plan.json").read_text())
MASTERS = ["CHAR-01.png", "CHAR-02-v2.png", "CHAR-03-v2.png", "CHAR-04-v2.png"]


def audit() -> dict:
    issues = []
    present_images = 0
    for name in MASTERS:
        if not (ROOT / "画像" / name).is_file():
            issues.append(f"固定キャラ画像欠落: {name}")
    for item in IMAGES:
        path = ROOT / "画像" / (item["id"] + ".png")
        if not path.is_file():
            issues.append(f"画像欠落: {item['id']}")
            continue
        present_images += 1
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                expected = item["image_size"]
                allowed = {(expected["width"], expected["height"])}
                if expected["width"] == 1920 and expected["height"] == 1080:
                    allowed.add((1920, 1072))  # GPT Image 2 rounds height to a model-supported size.
                if image.size not in allowed:
                    issues.append(f"画像サイズ不一致: {item['id']} {image.size}")
                if item["slot"] == "char":
                    if image.mode != "RGBA" or image.getchannel("A").getextrema()[0] > 0:
                        issues.append(f"キャラ画像に透明背景なし: {item['id']}")
        except Exception as exc:
            issues.append(f"画像を開けない: {item['id']} {exc}")
    present_videos = 0
    for item in VIDEOS:
        path = ROOT / "動画" / f"ASSET-{item['shot_id']:03d}_video.mp4"
        if not path.is_file():
            issues.append(f"動画欠落: {item['id']}")
            continue
        present_videos += 1
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
        if probe.returncode or not 4.5 <= float(probe.stdout.strip() or 0) <= 5.8:
            issues.append(f"動画の尺または読み込み異常: {item['id']}")
    text_cards = list((ROOT / "文字").glob("ASSET-*_text.png"))
    if text_cards:
        issues.append(f"編集者担当の文字カードを生成物に含めています: {len(text_cards)}")
    return {"expected_final_images": len(IMAGES) + len(MASTERS),
            "saved_final_images": present_images + sum((ROOT / "画像" / name).is_file() for name in MASTERS),
            "expected_videos": len(VIDEOS), "saved_videos": present_videos,
            "editor_text_cards_generated": len(text_cards), "issues": issues}


if __name__ == "__main__":
    result = audit()
    (ROOT / "audit_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "issues"}, ensure_ascii=False))
    print("issues", len(result["issues"]))
    sys.exit(bool(result["issues"]))
