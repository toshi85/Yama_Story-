#!/usr/bin/env python3
"""動画の残り（video_plan_regen.json）を、元の静止画ができたものから fal_video_queue.py（H3）で作る（2026-09-26）。
料金は本人了解済み（2026-09-26「料金の了解（約210円）承認します」）。1本$0.10上限・1カット1回だけ発注。
全部そろうか、10時間たったら終わる。"""
import json, subprocess, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # 素材_API_20260924
OUT = HERE / "動画_H3"
PY = str(ROOT / ".venv/bin/python")
QUEUE = "/Users/tosimasa/Desktop/Antigravity/System_Tools/edit/fal_video_queue.py"
AUTH = ("2026-09-26 本人チャット「料金の了解（約210円）承認します」「もういいって。自律的にやっておいて」。"
        "fal モデルページ: H3 Max Turbo 768P $0.02/秒（9/30まで半額）＝5秒$0.10")
plan = json.loads((HERE / "video_plan_regen.json").read_text(encoding="utf-8"))
end = time.time() + 10 * 3600
while time.time() < end:
    todo = [p for p in plan if not (OUT / f"{p['id']}.mp4").exists()]
    if not todo:
        print("動画ぜんぶ完了", flush=True); break
    ready = [p for p in todo if (ROOT / p["image"]).exists() and not (OUT / f"{p['id']}.request.json").exists()]
    by_md = {}
    for p in ready:
        by_md.setdefault(p["md"], []).append(p)
    for md, items in by_md.items():
        ids = [p["id"] for p in items]
        rec = OUT / "承認記録" / f"budget_{'_'.join(i[3:] for i in ids)}.json"
        rec.parent.mkdir(parents=True, exist_ok=True)
        rec.write_text(json.dumps({"schema": "fal_video_budget_gate_v1",
            "scene_ids": [f"S{p['shot_id']:03d}" for p in items],
            "approval_update": {"authorization_source": AUTH, "auto_recharge": False, "max_post_attempts_per_scene": 1,
                                "fallback_models_allowed": False, "max_usd_per_clip": "0.10",
                                "max_total_usd": f"{0.10 * len(items):.2f}"}}, ensure_ascii=False, indent=2), encoding="utf-8")
        print(time.strftime("%H:%M"), md, ids, flush=True)
        r = subprocess.run([PY, "-u", QUEUE, str(HERE / "video_plan_regen.json"), "--root", str(ROOT), "--out", str(OUT),
                            "--only", *ids, "--jobs", "4", "--approval-record", str(rec)],
                           cwd=Path(QUEUE).parent, capture_output=True, text=True)
        print((r.stdout + r.stderr).strip()[-800:], flush=True)
    done = sum(1 for p in plan if (OUT / f"{p['id']}.mp4").exists())
    print(time.strftime("%H:%M"), f"動画 {done}/{len(plan)}本", flush=True)
    time.sleep(300)
