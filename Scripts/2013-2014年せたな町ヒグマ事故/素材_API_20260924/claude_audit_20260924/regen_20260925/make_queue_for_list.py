#!/usr/bin/env python3
"""生成リスト.tsv の画像を、資料（Asset_Prompts_Fix*.md）ごとの image_queue に組む（2026-09-25）。

  python3 make_queue_for_list.py                 … 取りこぼしの確認だけ（何も書かない）
  python3 make_queue_for_list.py Fix4 --write   … その資料の分だけ image_queue.json に書く
  python3 make_queue_for_list.py Fix4 --write --ids CHAR-05,ASSET-043_char,ASSET-043_bg,ASSET-032_still

プロンプトは extract_prompts.py（ChatGPT経路の正規の抽出）を使い、抽出器が拾えないもの
（### CHAR-05｜ 形式の基準キャラ、ラベル無しの静止画）は .md のコードブロックをそのまま使う。
id は抽出器の id（ASSET-031_bg など）。納品時のファイル名は deliver_as（生成リストのとおり）。
"""
import csv, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
YAMA = HERE.parents[4]
sys.path.insert(0, str(YAMA / "System_Tools" / "imagegen"))
import extract_prompts as ep  # noqa: E402

KIND_SLOT = {"キャラ": "char", "キャラ（追加の1人）": "char", "背景": "bg",
             "静止画": "still", "静止画（動画の元）": "still"}


def raw_blocks(md_text):
    """{ASSET番号: [(直前ラベル文, フェンス本文), ...]}"""
    out = {}
    for block in re.split(r"(?=【制作メモ】ASSET-)", md_text)[1:]:
        head = re.match(r"【制作メモ】ASSET-(\d+)", block)
        if not head:
            continue
        no = int(head.group(1))
        fences = []
        for fm in re.finditer(r"```[^\n]*\n(.*?)```", block, re.S):
            label = block[max(0, fm.start() - 80):fm.start()]
            fences.append((label, ep.re.sub(r"\s+", " ", fm.group(1)).strip()))
        out[no] = fences
    return out


def char_refs(md_text):
    out = {}
    for m in re.finditer(r"^### (CHAR-\d+)[｜:]", md_text, re.M):
        fence = re.search(r"```[^\n]*\n(.*?)```", md_text[m.end():], re.S)
        if fence:
            out[m.group(1)] = re.sub(r"\s+", " ", fence.group(1)).strip()
    return out


def build(fix=None):
    rows = list(csv.DictReader((HERE / "生成リスト.tsv").open(encoding="utf-8"), delimiter="\t"))
    queue, missing, videos = [], [], []
    by_md = {}
    for r in rows:
        md = r["プロンプトのある資料"]
        if fix and md != f"Asset_Prompts_{fix}.md":
            continue
        if r["種類"] == "動画":
            videos.append(r["ファイル名"])
            continue
        if md not in by_md:
            text = (HERE / md).read_text(encoding="utf-8")
            items = {it["id"]: it for it in ep.parse(HERE / md)}
            by_md[md] = (items, raw_blocks(text), char_refs(text))
        items, blocks, refs = by_md[md]
        stem = r["ファイル名"].rsplit(".", 1)[0]
        base, suffix = stem.split("_", 1)
        no = int(base.split("-")[1])
        slot = KIND_SLOT[r["種類"]]
        want = f"{base}_{slot}" + ("2" if suffix == "char2" else "")
        # 051_char2: 資料の 051 ブロックにあるキャラプロンプトは「聞く住民」1人分＝抽出器の ASSET-051_char がそれ
        it = items.get(f"{base}_char") if suffix == "char2" else items.get(want)
        if it is not None:
            queue.append({"id": it["id"], "slot": it["slot"], "aspect": it["aspect"],
                          "prompt": it["prompt"], "deliver_as": r["ファイル名"], "md": md})
            continue
        # 抽出器が拾えない静止画（ラベル無しフェンス）
        cand = [f for lab, f in blocks.get(no, []) if "Google Flow" not in lab and "キャラプロンプト" not in lab and "背景プロンプト" not in lab]
        if slot == "still" and cand:
            queue.append({"id": want, "slot": "still", "aspect": "16:9", "prompt": cand[0],
                          "deliver_as": r["ファイル名"], "md": md})
            continue
        missing.append((r["ファイル名"], r["種類"], md, sorted(k for k in items if k.startswith(base))))
    # 基準キャラ（Fix4 の ### CHAR-05｜…）
    for md, (items, blocks, refs) in by_md.items():
        for cid, prompt in refs.items():
            queue.append({"id": cid, "slot": "char_ref", "aspect": "1:1", "prompt": prompt,
                          "deliver_as": f"{cid}.png", "md": md})
    return queue, missing, videos


def main():
    args = sys.argv[1:]
    fix = args[0] if args and not args[0].startswith("--") else None
    queue, missing, videos = build(fix)
    ids = None
    if "--ids" in args:
        ids = set(args[args.index("--ids") + 1].split(","))
        queue = [q for q in queue if q["id"] in ids]
        unknown = ids - {q["id"] for q in queue}
        if unknown:
            sys.exit(f"--ids に無いID: {sorted(unknown)}")
    for q in queue:  # キャラが再利用する固定人物（run.py が基準画像を添付する）
        q["char_refs"] = [f"CHAR-{int(m):02d}" for m in dict.fromkeys(re.findall(r"CHAR-(\d+)", q["prompt"]))] if q["slot"] == "char" else []
    for q in queue:  # collect.py の進捗表示が kind を読む
        q.setdefault("kind", {"char_ref": "キャラ基準画像", "char": "キャラ", "bg": "背景", "still": "静止画"}[q["slot"]])
    print(f"画像 {len(queue)}件（動画 {len(videos)}件は別）／取りこぼし {len(missing)}件")
    for m in missing:
        print("  ✗", *m)
    if "--write" in args:
        if len({q['md'] for q in queue}) > 1:
            sys.exit("複数の資料が混ざっています。資料は1つずつ（関所は1回の生成を1資料に限る）")
        out = HERE / "image_queue.json"
        old = HERE / "image_queue_before_20260925.json"
        if out.exists() and not old.exists():
            old.write_bytes(out.read_bytes())
        out.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"書きました: {out.name} ← {[q['id'] for q in queue]}")


if __name__ == "__main__":
    main()
