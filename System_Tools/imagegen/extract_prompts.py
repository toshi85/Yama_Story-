#!/usr/bin/env python3
"""Asset_Prompts.md から画像生成キュー(JSON)を作る。

使い方:
  python3 extract_prompts.py <Asset_Prompts.md> <出力queue.json>

1エントリ = 生成する画像1枚。id は保存ファイル名と一致する。
  CHAR-01              … キャラ基準画像
  ASSET-004_char       … キャラアニメーションのキャラ側(1:1)
  ASSET-004_bg         … 同じアセットの背景側(16:9)
  ASSET-002_still      … Lovart動画などの静止画(16:9)
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# --- キャラ画像のスタイル（2026-08-28 本人の実物サンプルに合わせて確定）---
# 素材ファイルの "Cute cartoon character design ... children's animation style." は
# ChatGPTだと頭身が高く描き込みの濃い絵になるため、これに丸ごと差し替える。
# 実物サンプルの特徴: 3頭身・均一に太い黒輪郭・完全フラット塗り・左右対称の直立・背景透過。
CHAR_STYLE = (
    "Simple flat cartoon sticker illustration for children, in the style of plain clean vector "
    "clip art. Bold uniform black outline of even thickness around the figure and around each "
    "interior shape. Absolutely flat solid fill colours - one flat tone per area, plus at most one "
    "slightly darker tone as a simple shadow. No gradients, no airbrushing, no blush, no cheek "
    "shading, no skin shading, no soft light, no ambient occlusion, no texture, no fabric pattern, "
    "no glossy highlights except one small white dot in each eye. Very large head, about one third "
    "of the total height, three heads tall overall, short stubby limbs, small simple mitten-like "
    "hands. Simple oval eyes with plain dark irises, tiny simple nose, small simple mouth, plain "
    "flat face with no wrinkles and no detailed features. Keep the clothing extremely simple: only "
    "a few large plain shapes, no small pockets, no straps, no cords, no buckles, no badges, no "
    "gadgets, no accessories other than the ones listed. If the description below mentions many "
    "pockets, straps or accessories, simplify them into a few plain shapes. "
    "Full body head to feet, whole figure inside the frame, centred."
)

# 姿勢の一文は素材の中身で切り替える（2026-08-28 の定型は「直立・左右対称」固定だった）。
#   四足の動物に「Standing upright」を付けると二足歩行の絵になる（Phase2の禁止事項）。
#   動きのあるカットに「arms relaxed at the sides」を付けると、指定した姿勢が消える。
POSE_UPRIGHT = "Standing upright, front-facing, symmetrical, arms relaxed at the sides. "
POSE_ALLFOURS = "Standing on all four legs in a side-front view, never upright and never on two legs. "
POSE_ASDESCRIBED = "Posed exactly as described below, front-facing where possible. "
POSE_VERBS = re.compile(
    r"\b(kneel|crouch|sprint|running|runs|walking|walks|leaning|lean|bent|bending|"
    r"seated|sitting|lying|lies|raised|raising|pointing|points|holding|holds|"
    r"reaching|clutch|gripping|grips|swinging|swings|turning|turns|shrug)", re.I)


def pose_of(body: str) -> str:
    if re.search(r"ON ALL FOURS|all four", body, re.I):
        return POSE_ALLFOURS
    if POSE_VERBS.search(body):
        return POSE_ASDESCRIBED
    return POSE_UPRIGHT

CHAR_TAIL = (
    "No written words or lettering anywhere. "
    "Fully transparent background, PNG with alpha, no backdrop and no ground shadow. "
    "1:1 square aspect ratio."
)

# 素材ファイル側の旧スタイル文（この1文を丸ごと CHAR_STYLE に差し替える）
OLD_STYLE_RE = re.compile(r"Cute cartoon character design.*?children's animation style\.\s*", re.S)
# 「文字を入れるな」系の定型文は CHAR_TAIL に集約するので本文からは落とす
BOILERPLATE_RE = re.compile(
    r"A single standalone character illustration with no written words.*?image\.\s*", re.S)

# フェンス直前のラベルからスロットを判定する
SLOT_RULES = [
    ("Google Flow動画プロンプト", None),          # 動画プロンプト＝生成対象外
    ("キャラプロンプト", ("char", "1:1")),
    ("背景プロンプト", ("bg", "16:9")),
    ("静止画プロンプト", ("still", "16:9")),
    ("静止画", ("still", "16:9")),                # 「静止画＋Google Flow」等の略記
]


def classify(preceding: str):
    """フェンス直前テキストから (slot, aspect) を返す。対象外は None。"""
    best, best_pos = None, -1
    for label, slot in SLOT_RULES:
        pos = preceding.rfind(label)
        if pos > best_pos:
            best_pos, best = pos, slot
    return best if best_pos >= 0 else None


def char_body(prompt: str) -> str:
    """素材のキャラ記述から、この1枚に固有の部分だけを取り出す。"""
    out = OLD_STYLE_RE.sub("", prompt, count=1)
    out = re.sub(r"(?i)(full body,\s*)?white background\.\s*", "", out)
    out = re.sub(r"(?i)\b1:1 aspect ratio\.\s*", "", out)
    out = BOILERPLATE_RE.sub("", out)
    return re.sub(r"\s+", " ", out).strip()


def char_ref_of(prompt: str):
    """このキャラ画像が参照する基準キャラ（CHAR-01 等）。無ければ None。"""
    m = re.search(r"\bCHAR-(\d+)\b", prompt)
    return f"CHAR-{int(m.group(1)):02d}" if m else None


def parse(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    items = []

    # --- キャラ基準画像 (### CHAR-01: ...) ---
    char_section = text.split("## 1. 全素材リスト", 1)[0]
    for m in re.finditer(r"^### (CHAR-\d+):\s*(.+?)$", char_section, re.M):
        cid, label = m.group(1), m.group(2).strip()
        fence = re.search(r"```(.*?)```", char_section[m.end():], re.S)
        if not fence:
            continue
        body = char_body(fence.group(1).strip())
        items.append({
            "id": cid, "asset_no": None, "kind": "キャラ基準画像", "slot": "char_ref",
            "aspect": "1:1", "label": label, "narration": "", "char_ref": None,
            "body": body, "prompt": f"{CHAR_STYLE} {pose_of(body)}{body} {CHAR_TAIL}",
        })

    # --- 本文アセット ---
    blocks = re.split(r"(?=【制作メモ】ASSET-)", text)
    for i, block in enumerate(blocks[1:], start=1):
        head = re.match(r"【制作メモ】ASSET-(\d+)\s*\[([^\]]+)\]", block)
        if not head:
            continue
        no, kind = int(head.group(1)), head.group(2)

        nar = re.findall(r"^ナレーター[:：]\s*(.+?)$", blocks[i - 1], re.M)
        narration = nar[-1].strip() if nar else ""

        seen = {}
        for fm in re.finditer(r"```(.*?)```", block, re.S):
            slot = classify(block[: fm.start()])
            if slot is None:
                continue
            name, aspect = slot
            seen[name] = seen.get(name, 0) + 1
            suffix = "" if seen[name] == 1 else f"-{seen[name]}"
            raw = fm.group(1).strip()

            if name == "char":
                body = char_body(raw)
                prompt = f"{CHAR_STYLE} {pose_of(body)}{body} {CHAR_TAIL}"
                ref = char_ref_of(raw)
            else:
                body = prompt = re.sub(r"\s+", " ", raw).strip()
                ref = None

            items.append({
                "id": f"ASSET-{no:03d}_{name}{suffix}", "asset_no": no, "kind": kind,
                "slot": name, "aspect": aspect, "label": "", "narration": narration,
                "char_ref": ref, "body": body, "prompt": prompt,
            })
    return items


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    items = parse(src)

    ids = [x["id"] for x in items]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"ID重複: {sorted(dup)}")

    dst.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(items)}枚 -> {dst}")
    for k, v in sorted(Counter(f'{x["kind"]}/{x["slot"]}' for x in items).items()):
        print(f"  {k}: {v}")
    noref = [x["id"] for x in items if x["slot"] == "char" and not x["char_ref"]]
    print(f"参照キャラ未特定のキャラ画像: {len(noref)}件", noref[:8])


if __name__ == "__main__":
    main()
