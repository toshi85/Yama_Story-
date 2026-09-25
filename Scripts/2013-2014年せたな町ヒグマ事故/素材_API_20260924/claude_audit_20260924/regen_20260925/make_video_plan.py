#!/usr/bin/env python3
"""生成リスト.tsv の動画18本を、いつもの fal_video_queue.py（H3）の発注リストにする（2026-09-25）。
プロンプト＝そのカットの「Google Flow動画プロンプト」（一字一句そのまま）。元の静止画＝同じ番号の _still.png。
例外（資料のブロックに書いてあるとおり）: 198→ASSET-174_bg.png、207→ASSET-182_bg.png、160・178→ドライブの _still.png。
"""
import csv, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
SOURCE_OVERRIDE = {198: "images/ASSET-174_bg.png", 207: "images/ASSET-182_bg.png",
                   160: "drive/ASSET-160_still.png", 178: "drive/ASSET-178_still.png"}
rows = [r for r in csv.DictReader((HERE / "生成リスト.tsv").open(encoding="utf-8"), delimiter="\t") if r["種類"] == "動画"]
plan = []
for r in rows:
    no = int(re.search(r"ASSET-(\d+)", r["ファイル名"]).group(1))
    text = (HERE / r["プロンプトのある資料"]).read_text(encoding="utf-8")
    block = re.split(r"(?=【制作メモ】ASSET-)", text)
    block = next(b for b in block if b.startswith(f"【制作メモ】ASSET-{no:03d}"))
    m = re.search(r"Google Flow動画プロンプト[^\n]*\n```[^\n]*\n(.*?)```", block, re.S)
    if not m:
        raise SystemExit(f"ASSET-{no:03d}: 動画プロンプトが見つからない")
    plan.append({"id": f"H3_{no:03d}", "shot_id": no, "prompt": m.group(1).strip(),
                 "image": SOURCE_OVERRIDE.get(no, f"images/ASSET-{no:03d}_still.png"),
                 "deliver_as": r["ファイル名"], "md": r["プロンプトのある資料"]})
(HERE / "video_plan_regen.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for p in plan:
    print(p["id"], p["md"], p["image"], "元あり" if (HERE / p["image"]).exists() else "元まだ")
print(f"{len(plan)}本 → video_plan_regen.json")
