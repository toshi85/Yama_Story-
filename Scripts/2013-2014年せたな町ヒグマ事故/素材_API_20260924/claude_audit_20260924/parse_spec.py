#!/usr/bin/env python3
"""Asset_Prompts_Full.md → spec.json（ASSETごとの台本行・シーン・プロンプト・キャラ参照・編集者指示）"""
import json, re, sys
from pathlib import Path
SRC = Path(__file__).resolve().parents[2] / "Asset_Prompts_Full.md"
txt = SRC.read_text()
# ナレーション行の直後に制作メモが続く
MARK = re.compile(r"【制作メモ】ASSET-(\d+) \[([^\]]+)\](?: 台本L(\d+))?")
marks = list(MARK.finditer(txt))
out = []
for i, m in enumerate(marks):
    start = m.start(); end = marks[i+1].start() if i+1 < len(marks) else len(txt)
    block = txt[start:end]
    # 直前のナレーター行
    before = txt[:start]
    nar = re.findall(r"^ナレーター: (.+)$", before, re.M)
    scene = re.search(r"^シーン: (.+)$", block, re.M)
    charref = re.search(r"^キャラ参照: (.+)$", block, re.M)
    serif = re.search(r"^→セリフ「(.*)」", block, re.M)
    editor = re.search(r"^→ 編集者指示: (.+)$", block, re.M)
    fences = re.findall(r"^(.*?):?\n```(?:text)?\n(.*?)\n```", block, re.S | re.M)
    prompts = []
    for label, body in fences:
        label = label.strip().splitlines()[-1] if label.strip() else ""
        prompts.append({"label": label[:60], "text": body.strip()})
    out.append({
        "asset": f"ASSET-{int(m.group(1)):03d}", "no": int(m.group(1)), "category": m.group(2),
        "script_line": int(m.group(3)) if m.group(3) else None,
        "narration": nar[-1] if nar else None,
        "scene": scene.group(1) if scene else None,
        "char_ref": charref.group(1) if charref else None,
        "serif": serif.group(1) if serif else None,
        "editor": editor.group(1) if editor else None,
        "prompts": prompts,
        "block_lines": block.count("\n"),
    })
Path("spec.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
import collections
print("assets:", len(out), "categories:", collections.Counter(a["category"] for a in out))
print("no narration:", [a["asset"] for a in out if not a["narration"]][:10])
print("no scene:", [a["asset"] for a in out if not a["scene"]][:10])
print("with char_ref:", sum(1 for a in out if a["char_ref"]), " with serif:", sum(1 for a in out if a["serif"]))
