#!/usr/bin/env python3
"""生成リスト.tsv のファイル名どおりに、できた素材をデスクトップの渡し用フォルダへコピーする（2026-09-26）。
キャラ（_char）は背景透過か（四隅が透明か）を確かめ、足りないもの・透過していないものを一覧にする。
  python make_delivery.py            … 確認だけ
  python make_delivery.py --copy     … デスクトップへコピー
"""
import csv, json, shutil, sys
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent
OUT = Path.home() / "Desktop" / "せたな町_差し替え素材_20260926"
sys.argv += []
import importlib.util
spec = importlib.util.spec_from_file_location("mq", HERE / "make_queue_for_list.py"); mq = importlib.util.module_from_spec(spec)
_argv = sys.argv; sys.argv = ["x"]; spec.loader.exec_module(mq); sys.argv = _argv
queue, _, _ = mq.build()
src_by_deliver = {q["deliver_as"]: HERE / "images" / f"{q['id']}.png" for q in queue if q.get("deliver_as") and not q["id"].startswith("CHAR-")}
video_plan = json.loads((HERE / "video_plan_regen.json").read_text(encoding="utf-8"))
for v in video_plan:
    src_by_deliver[v["deliver_as"]] = HERE / "動画_H3" / f"{v['id']}.mp4"
rows = list(csv.DictReader((HERE / "生成リスト.tsv").open(encoding="utf-8"), delimiter="\t"))
missing, not_clear, ok = [], [], []
for r in rows:
    name = r["ファイル名"]; src = src_by_deliver.get(name)
    if not src or not src.exists():
        missing.append((name, r["種類"])); continue
    if "_char" in name:
        im = Image.open(src)
        if im.mode != "RGBA" or any(im.getpixel(p)[3] > 10 for p in [(0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)]):
            not_clear.append(name)
    ok.append((name, src))
print(f"そろった {len(ok)}/{len(rows)}件（足りない {len(missing)}件・透過していないキャラ {len(not_clear)}件）")
for m in missing: print("  足りない:", *m)
for n in not_clear: print("  透過していない:", n)
if "--copy" in sys.argv:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in ok:
        shutil.copy2(src, OUT / name)
    print("コピー先:", OUT)
