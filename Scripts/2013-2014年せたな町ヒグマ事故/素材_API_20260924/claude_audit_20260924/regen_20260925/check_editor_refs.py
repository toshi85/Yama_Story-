#!/usr/bin/env python3
"""2026-09-26: 編集者用の指示が「使う」と言っているファイルが、ドライブに実在するか・作る予定にあるかを全カットで確かめる。
本人「キャラ画像がありません」（074）と同じ型が 023・033・038・041・047・056・108・125・151・194 に残っていた。
「既存の _char.png」のようにファイル名の無い指示も止める。使い方: python3 check_editor_refs.py（問題があれば終了コード1）"""
import csv, json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
known = {p.name for p in (HERE.parents[1] / "画像").glob("ASSET-*")}
known |= {r["ファイル名"] for r in csv.DictReader((HERE / "生成リスト.tsv").open(encoding="utf-8"), delimiter="\t")}
fix = Path.home() / "Desktop" / "せたな町_修正分_20260926"
if fix.exists():
    known |= {p.name for p in fix.glob("ASSET-*")}
for extra in ("drive_names.json",):   # ドライブで検索して確かめた実物の名前（2026-09-26）
    if (HERE / extra).exists():
        known |= set(json.loads((HERE / extra).read_text(encoding="utf-8")))
delivered = HERE / "delivered_names.json"          # 納品済み（ドライブ）の一覧。make_delivery.py の結果を保存したもの
if delivered.exists():
    known |= set(json.loads(delivered.read_text(encoding="utf-8")))
text = (HERE / "編集者用_Latest.md").read_text(encoding="utf-8")
bad = []
for block in re.split(r"(?=^## ASSET-)", text, flags=re.M)[1:]:
    no = block[3:12]
    for line in block.splitlines():
        if not line.startswith("- 編集者指示") and not line.startswith("- 背景は") and not line.startswith("- キャラは"):
            continue
        if re.search(r"既存の _(?:char|still|bg)\.png", line):
            bad.append(f"{no}: ファイル名の無い「既存の _char.png」型の指示 … {line[:80]}")
        for clause in re.split(r"[。、（）()]", line):
            if "使わない" in clause or "旧" in clause or "前の" in clause:
                continue
            for name in re.findall(r"ASSET-\d{3}_(?:char\d?|bg|still|bear|video)\.(?:png|mp4)", clause):
                if name not in known:
                    bad.append(f"{no}: {name} がドライブにも作る予定にも無い")
for b in dict.fromkeys(bad):
    print("✗", b)
print(f"{'問題なし' if not bad else str(len(set(bad))) + '件'}")
sys.exit(1 if bad else 0)
