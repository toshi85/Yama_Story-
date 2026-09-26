#!/usr/bin/env python3
"""2026-09-26 夕方: 本人の修正指示で作る・作り直す動画16本を fal H3 の発注リスト（video_plan_fix6.json）にする。
プロンプト＝最後に上書きした資料（Fix5a < Fix5b < Fix6）のそのカットの「Google Flow動画プロンプト」を一字一句そのまま。
id は作り直しと区別するため H3_NNN_r（納品名は前と同じ ASSET-NNN_video.mp4＝本人「修正後の素材名は修正前と同じに」）。"""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
IMG = "claude_audit_20260924/regen_20260925/images/"
CUTS = {  # カット: 元の静止画（素材_API_20260924 から見た場所）
    77: IMG + "ASSET-077_still.png", 82: IMG + "ASSET-082_still.png", 87: IMG + "ASSET-087_still.png",
    90: IMG + "ASSET-090_still.png", 111: IMG + "ASSET-111_still.png", 118: IMG + "ASSET-118_still.png",
    124: IMG + "ASSET-124_bg.png", 126: "画像/ASSET-126_still.png", 144: IMG + "ASSET-144_still.png",
    145: IMG + "ASSET-145_still.png", 155: IMG + "ASSET-155_still.png", 156: "画像/ASSET-156_bg.png",
    166: IMG + "ASSET-166_still.png", 198: IMG + "ASSET-198_still.png", 208: IMG + "ASSET-208_still.png",
    214: IMG + "ASSET-214_still.png"}
ORDER = ["Asset_Prompts_Fix5a.md", "Asset_Prompts_Fix5b.md", "Asset_Prompts_Fix5c.md", "Asset_Prompts_Fix6.md"]
plan = []
for no, image in CUTS.items():
    found = None
    for md in ORDER:
        text = (HERE / md).read_text(encoding="utf-8")
        for b in re.split(r"(?=【制作メモ】ASSET-)", text):
            if b.startswith(f"【制作メモ】ASSET-{no:03d} "):
                m = re.search(r"Google Flow動画プロンプト[^\n]*\n```[^\n]*\n(.*?)```", b, re.S)
                if m:
                    found = (md, m.group(1).strip())
    if not found:
        raise SystemExit(f"ASSET-{no:03d}: 動画プロンプトが見つからない")
    plan.append({"id": f"H3_{no:03d}_r", "shot_id": no, "prompt": found[1], "image": image,
                 "deliver_as": f"ASSET-{no:03d}_video.mp4", "md": found[0]})
(HERE / "video_plan_fix6.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
root = HERE.parents[1]
for p in plan:
    print(p["id"], p["md"], p["image"].split("/")[-1], "元あり" if (root / p["image"]).exists() else "元まだ")
print(f"{len(plan)}本 → video_plan_fix6.json")
