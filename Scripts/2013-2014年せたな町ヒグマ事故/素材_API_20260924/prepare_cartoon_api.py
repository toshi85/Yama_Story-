#!/usr/bin/env python3
"""Prepare reference-image edits while preserving the approved pilot as CHAR-02."""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DELIVERY = Path.home() / "Desktop/せたな町_素材_20260924"
REFS = ROOT / "cartoon_references"
OUT = ROOT / "画像_v3"
SAMPLE = DELIVERY / "試作_CHAR-02_カートゥン.png"
APPROVED = "CHAR-02-front-v3.png"
EDIT_PREFIX = (
    "Edit image 1 as the target character, using image 2 only as the approved compact cartoon style reference. "
    "Preserve the target character's identity, clothing colors and scene-specific pose, but decisively redraw "
    "the anatomy to match image 2's large head, short compact torso, short stubby arms and legs, "
    "thick black outlines and flat colors. Do not copy image 2's male identity or navy jacket unless "
    "image 1 already has them. Remove any extraneous symbols or text. "
)


def link(name: str, source: Path) -> None:
    if not source.is_file():
        raise SystemExit(f"FAIL: missing reference {source}")
    dest = REFS / name
    if dest.is_symlink() or dest.exists():
        if dest.resolve() != source.resolve():
            raise SystemExit(f"FAIL: conflicting reference {dest}")
    else:
        dest.symlink_to(source)


def main() -> None:
    plan = json.loads((ROOT / "cartoon_character_plan.json").read_text())
    masters = json.loads((ROOT / "cartoon_masters.json").read_text())
    REFS.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    if not SAMPLE.is_file():
        raise SystemExit("FAIL: approved cartoon sample is missing")
    with Image.open(SAMPLE) as im:
        im.convert("RGBA").resize((1024, 1024), Image.Resampling.LANCZOS).save(OUT / APPROVED)
    link("approved_style.png", OUT / APPROVED)
    api_items = []
    for item in masters:
        if item["id"] == "CHAR-02-front-v3":
            continue
        target = item["id"].replace("-v3", "-v2") + ".png"
        link(target, DELIVERY / "画像" / target)
        api_items.append({**item, "prompt": EDIT_PREFIX + item["prompt"], "references": [target, "approved_style.png"]})
    for item in plan:
        target = item["id"] + ".png"
        link(target, DELIVERY / "画像" / target)
        api_items.append({**item, "prompt": EDIT_PREFIX + item["prompt"], "references": [target, "approved_style.png"]})
    if len(api_items) != 134 or len({i["id"] for i in api_items}) != 134:
        raise SystemExit("FAIL: API edit count mismatch")
    (ROOT / "cartoon_api_edit_plan.json").write_text(json.dumps(api_items, ensure_ascii=False, indent=2) + "\n")
    print(f"Prepared {len(api_items)} reference-image edits and approved master {APPROVED}; paid requests: 0")


if __name__ == "__main__":
    main()
