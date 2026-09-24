#!/usr/bin/env python3
"""Replace only the audited cartoon PNGs after all outputs pass inspection."""

import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]
sys.path.insert(0, str(WORKSPACE / ".codex/skills/yama-asset-checker/scripts"))
from audit_ratio_delivery import audit
from check_character_generation import check
from check_scene_fitness import check as check_scene_fitness

DEST = Path.home() / "Desktop/せたな町_素材_20260924"
STAGE = ROOT / "delivery_staging_cartoon"
BACKUP = ROOT / "previous_desktop_delivery_cartoon"
SOURCE = ROOT.parent / "Asset_Prompts_Full_cartoon.md"
NEW = ROOT / "画像_v3"
NAMES = [f"ASSET-{x['asset_no']:03d}_char.png" for x in json.loads((ROOT / "cartoon_character_plan.json").read_text())]
NAMES += [f"CHAR-0{i}-front-v3.png" for i in (2, 3, 4)]


def main() -> None:
    if len(NAMES) != 135 or len(set(NAMES)) != 135:
        raise SystemExit("FAIL: expected exactly 135 unique cartoon PNGs")
    if STAGE.exists() or BACKUP.exists():
        raise SystemExit("FAIL: staging or backup exists; inspect before running")
    plan = json.loads((ROOT / "cartoon_character_plan.json").read_text())
    masters = json.loads((ROOT / "cartoon_masters.json").read_text())
    errors = check(SOURCE.read_text(), plan, masters, hook_end=12)
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors[:5]))
    missing = [name for name in NAMES if not (NEW / name).is_file()]
    if missing:
        raise SystemExit(f"FAIL: {len(missing)} cartoon images missing: {missing[:5]}")
    from PIL import Image
    for name in NAMES:
        with Image.open(NEW / name) as im:
            if im.size != (1024, 1024) or im.mode != "RGBA" or im.getchannel("A").getextrema()[0] != 0:
                raise SystemExit(f"FAIL: image dimensions or transparency {name}")
    shutil.copytree(DEST, STAGE)
    for old in ("CHAR-02-front-v2.png", "CHAR-03-front-v2.png", "CHAR-04-front-v2.png"):
        (STAGE / "画像" / old).unlink()
    for name in NAMES:
        shutil.copy2(NEW / name, STAGE / "画像" / name)
    mapping = json.loads((ROOT / "ratio60_cut_mapping.json").read_text())
    errors, counts = audit(mapping, STAGE, master_version="v3")
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors[:10]))
    scene_source = (ROOT.parent / "Asset_Prompts_Full.md").read_text()
    scene_review = json.loads((ROOT / "scene_fitness_review/scene_fitness_review.json").read_text())
    baseline = json.loads((ROOT / "scene_fitness_review/replacement_baseline_names.json").read_text())
    scene_errors = check_scene_fitness(
        scene_source, scene_review, "delivery", STAGE, baseline=baseline,
        composite_root=ROOT / "scene_fitness_review/composites"
    )
    if scene_errors:
        raise SystemExit(f"FAIL: scene fitness {len(scene_errors)} issues; " + "; ".join(scene_errors[:5]))
    checksums = {name: hashlib.sha256((STAGE / "画像" / name).read_bytes()).hexdigest() for name in NAMES}
    (STAGE / "検査結果.json").write_text(json.dumps({"status":"PASS", "cartoon_style":"approved CHAR-02 pilot; all 135 images visually reviewed", "character_cuts":132, "cuts":220, "images":counts["images"], "videos":counts["videos"], "sha256":counts["sha256"], "cartoon_sha256":checksums},ensure_ascii=False,indent=2)+"\n")
    DEST.replace(BACKUP)
    try:
        STAGE.replace(DEST)
    except Exception:
        BACKUP.replace(DEST)
        raise
    print(f"PASS: replaced {len(NAMES)} cartoon images in Desktop delivery; backup kept at {BACKUP}")


if __name__ == "__main__":
    main()
