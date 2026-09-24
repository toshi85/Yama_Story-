#!/usr/bin/env python3
"""Generate each ready H3 clip once, waiting for its API-generated source frame."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
PLAN = json.loads((ROOT / "video_plan.json").read_text())
OUT = ROOT / "動画"
OUT.mkdir(exist_ok=True)
PYTHON = ROOT / ".venv/bin/python"
QUEUE = Path(__file__).resolve().parents[4] / "System_Tools/edit/fal_video_queue.py"
APPROVAL = json.loads((ROOT / "video_approval_full.json").read_text())
ALL_IDS = {item["id"] for item in PLAN}


def live_image_process() -> bool:
    pid = int((ROOT / "image_generation.pid").read_text().strip())
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


def main() -> int:
    policy = json.loads((ROOT.parents[3] / ".codex/quality/yama_setana_asset_generation_policy.json").read_text())
    if policy.get("video_generation_allowed") is not True:
        raise SystemExit("FAIL: せたな町の動画生成は本人指示で一時停止中。既存動画の読み取り検査のみ")
    while True:
        completed = {path.stem for path in OUT.glob("H3_*.mp4")}
        if completed >= ALL_IDS:
            print(f"動画完成 {len(completed)}/{len(ALL_IDS)}", flush=True)
            return 0
        ready = [item for item in PLAN if item["id"] not in completed and (ROOT / item["image"]).is_file()]
        if ready:
            if shutil.disk_usage(ROOT).free < 512 * 1024 * 1024:
                raise RuntimeError("空き容量が512MiB未満")
            # Run every currently ready item, preserving its existing request record.
            batch = ready[:12]
            record = dict(APPROVAL)
            record["scene_ids"] = [f'S{item["shot_id"]:03d}' for item in batch]
            record["approval_update"] = dict(APPROVAL["approval_update"])
            record["approval_update"]["max_total_usd"] = f"{len(batch) * 0.2:.2f}"
            approval_path = ROOT / "video_approval_current_batch.json"
            approval_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
            command = [str(PYTHON), str(QUEUE), str(ROOT / "video_plan.json"),
                       "--root", str(ROOT), "--out", str(OUT), "--jobs", "4",
                       "--only", *[item["id"] for item in batch],
                       "--approval-record", str(approval_path)]
            print("発注/結果取得", ",".join(item["id"] for item in batch), flush=True)
            result = subprocess.run(command, check=False)
            if result.returncode:
                print(f"動画バッチ停止: exit={result.returncode}", flush=True)
                return result.returncode
            continue
        missing = [item["id"] for item in PLAN if item["id"] not in completed]
        if not live_image_process():
            raise RuntimeError("画像生成が停止し、未生成の動画開始画像が残っています: " + ",".join(missing))
        print(f"開始画像待ち 動画{len(completed)}/{len(ALL_IDS)}", flush=True)
        time.sleep(10)


if __name__ == "__main__":
    raise SystemExit(main())
