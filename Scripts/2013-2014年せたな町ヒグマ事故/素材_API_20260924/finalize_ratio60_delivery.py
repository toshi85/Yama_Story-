#!/usr/bin/env python3
"""Build and atomically replace the desktop delivery after exact inventory audit."""

import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]
sys.path.insert(0, str(WORKSPACE / ".codex/skills/yama-asset-checker/scripts"))
from audit_ratio_delivery import audit
from check_character_generation import check as check_character_plan
from check_scene_fitness import check as check_scene_fitness

DEST = Path.home() / "Desktop/せたな町_素材_20260924"
STAGE = ROOT / "delivery_staging_ratio60"
BACKUP = ROOT / "previous_desktop_delivery_ratio60"
OLD = ROOT / "画像"
NEW = ROOT / "画像_v2"
VIDEOS = ROOT / "動画"


def main():
    mapping = json.loads((ROOT / "ratio60_cut_mapping.json").read_text())
    source = (ROOT.parent / "Asset_Prompts_Full_ratio60.md").read_text()
    plan = json.loads((ROOT / "ratio60_character_plan.json").read_text())
    masters = json.loads((ROOT / "ratio60_masters.json").read_text())
    plan_errors = check_character_plan(source, plan, masters, hook_end=12)
    if plan_errors:
        raise SystemExit("FAIL: " + "; ".join(plan_errors[:5]))
    if STAGE.exists() or BACKUP.exists():
        raise SystemExit("FAIL: staging or backup already exists; inspect before running")
    (STAGE / "画像").mkdir(parents=True)
    (STAGE / "動画").mkdir()
    for row in mapping:
        number, kind = row["asset_no"], row["previous_kind"]
        stem = f"ASSET-{number:03d}"
        if kind == "キャラアニメーション":
            shutil.copy2(OLD / f"{stem}_bg.png", STAGE / "画像")
        elif kind == "Lovart動画":
            shutil.copy2(OLD / f"{stem}_still.png", STAGE / "画像")
            shutil.copy2(VIDEOS / f"{stem}_video.mp4", STAGE / "動画")
        elif kind.startswith("Lovart静止画"):
            shutil.copy2(OLD / f"{stem}_still.png", STAGE / "画像")
        if row["revised_kind"] == "キャラアニメーション":
            shutil.copy2(NEW / f"{stem}_char.png", STAGE / "画像")
    for name in ("CHAR-01.png",):
        shutil.copy2(OLD / name, STAGE / "画像")
    for name in ("CHAR-02-front-v2.png", "CHAR-03-front-v2.png", "CHAR-04-front-v2.png"):
        shutil.copy2(NEW / name, STAGE / "画像")
    shutil.copy2(ROOT / "編集者用指示書_比率修正版.md", STAGE / "編集者用指示書.md")
    errors, counts = audit(mapping, STAGE)
    scene_source = (ROOT.parent / "Asset_Prompts_Full.md").read_text()
    scene_review = json.loads((ROOT / "scene_fitness_review/scene_fitness_review.json").read_text())
    baseline = json.loads((ROOT / "scene_fitness_review/replacement_baseline_names.json").read_text())
    errors.extend(check_scene_fitness(
        scene_source, scene_review, "delivery", STAGE, baseline=baseline,
        composite_root=ROOT / "scene_fitness_review/composites"
    ))
    (STAGE / "検査結果.json").write_text(json.dumps({"status": "PASS" if not errors else "FAIL", "errors": errors, **counts}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit("FAIL: " + "; ".join(errors[:5]))
    if DEST.exists():
        DEST.replace(BACKUP)
    try:
        STAGE.replace(DEST)
    except Exception:
        if BACKUP.exists() and not DEST.exists():
            BACKUP.replace(DEST)
        raise
    print(f"PASS Desktop delivery: {counts['images']} images, {counts['videos']} videos, {counts['character_cuts']}/{counts['cuts']} character cuts")
    print(f"Backup kept at {BACKUP}")


if __name__ == "__main__":
    main()
