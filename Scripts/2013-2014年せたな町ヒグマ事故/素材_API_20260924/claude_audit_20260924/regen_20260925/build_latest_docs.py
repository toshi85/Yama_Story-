"""せたな町: 作り直し分（Regen・Fix2〜Fix5）を元の Asset_Prompts_Full.md に差し込んで、最新版の
プロンプト表（Asset_Prompts_Latest.md）と編集者用（編集者用_Latest.md・プロンプトなし）を作る。

後から書いたファイルが優先: Full < Regen < Fix2 < Fix3 < Fix4 < Fix5a < Fix5b < Fix5c < Fix6。
「動画を外すだけのカット」は元のブロックから動画プロンプトを消し、編集者指示を「キャラと背景で表す」に変える。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editor_doc_additions import DIALOGUE

HERE = Path(__file__).resolve().parent
W = HERE.parents[2]
DRIVE = "https://drive.google.com/drive/u/0/folders/1e50euC7lBOkK8IYc1HdI9FaixuawvE3G"
OVERRIDES = ["Asset_Prompts_Regen.md", "Asset_Prompts_Fix2.md", "Asset_Prompts_Fix3.md", "Asset_Prompts_Fix4.md",
             "Asset_Prompts_Fix5a.md", "Asset_Prompts_Fix5b.md", "Asset_Prompts_Fix5c.md", "Asset_Prompts_Fix6.md"]
# 001〜050 で本人が「動画はいらない」と言ったカット（Fix側に新しいブロックが無いもの）＋ lint55 の対象
VIDEO_DROP_EXTRA = {15, 23, 25, 26, 31, 33, 36, 38, 39, 45, 47}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def split_blocks(text: str):
    """(ナレーション行を含む) ASSET ブロックごとに切る。返り値: {asset: block}, 見出し部分"""
    parts = re.split(r"\n---\n", text)
    blocks, head = {}, []
    for part in parts:
        m = re.search(r"^【制作メモ】ASSET-(\d+)", part, re.M)
        if m:
            blocks[int(m.group(1))] = part.strip("\n")
        else:
            head.append(part)
    return blocks, head


full = read(W / "Asset_Prompts_Full.md")
base, head = split_blocks(full)
source = {n: "元の資料" for n in base}
drop_only = set(VIDEO_DROP_EXTRA)
char_heads = []
for name in OVERRIDES:
    p = HERE / name
    if not p.exists():
        continue
    text = read(p)
    # 固定人物の見出し（### CHAR-NN）を集める
    for m in re.finditer(r"^### (CHAR-\d+[^\n]*)\n+```text\n(.*?)\n```", text, re.M | re.S):
        char_heads.append((m.group(1), m.group(2)))
    tail = re.search(r"^## 動画を外すだけのカット\s*$(.*)", text, re.M | re.S)
    if tail:
        drop_only |= {int(x) for x in re.findall(r"ASSET-(\d+)|(?<![\d])(\d{3})(?![\d])", tail.group(1)) for x in x if x}
        text = text[:tail.start()]
    blocks, _ = split_blocks(text)
    for n, b in blocks.items():
        # 作業ファイルの題（「# せたな町 作り直し28カット」など）は納品物に入れない
        base[n] = re.sub(r"\A(?:#[^\n]*\n+)+", "", b)
        source[n] = name.replace("Asset_Prompts_", "").replace(".md", "")


def drop_video(block: str) -> str:
    out, skip = [], False
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        s = lines[i]
        if "動画プロンプト" in s:
            # ラベル行と、その次のコードブロックを消す
            i += 1
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                i += 1
            continue
        if s.startswith("→ 編集者指示:"):
            s = re.sub(r"Flow動画をナレーションの尺に合わせて使用。?", "", s)
            s = s.replace("→ 編集者指示:", "→ 編集者指示: キャラと背景で表す（動画は使わない）。キャラは既存の _char.png、背景は既存の _still.png を使う。", 1)
        out.append(s)
        i += 1
    return "\n".join(out)


# 2026-09-26: 元の資料では、前のカット用の旧い汎用キャラ指示（「既存の写実素材は…」「キャラプロンプト（背景透過・1:1）: Cute 2D …
#   The person reacts to …」「→ 編集者指示: 既存の背景または動画に、画像/ASSET-NNN_char.pngを合成」）が、次のカットの
#   ナレーションと【制作メモ】の間に挟まって残っていた。旧い型（後ろ姿・年齢なし）の指示が最新版と編集者用に28カット分
#   出ていたので、ナレーションと【制作メモ】の間の行は捨てる（正しい並びは ナレーター → 【制作メモ】）。
LEFTOVER = re.compile(r"(^ナレーター:[^\n]*\n)(.*?)(?=^【制作メモ】)", re.M | re.S)
for n in list(base):
    base[n] = LEFTOVER.sub(lambda m: m.group(1) + "\n" if m.group(2).strip() else m.group(0), base[n], count=1)

for n in sorted(drop_only):
    if n in base and source[n] == "元の資料":
        base[n] = drop_video(base[n])
        source[n] = "動画を外す"

# --- プロンプト表（最新版）
head_text = "\n---\n".join(head).strip("\n")
# 2026-09-26: 後の資料で基準を作り直した固定人物（CHAR-02〜04 など）は、元の資料の古い定義（旧い汎用の型）を最新版から外す
_newer = {re.match(r"(CHAR-\d+)", h).group(1) for h, _ in char_heads if re.match(r"CHAR-\d+", h)}
head_text = re.sub(r"^### (CHAR-\d+)[^\n]*\n+```text\n.*?\n```\n*",
                   lambda m: ("（" + m.group(1) + " は下の「追加の固定人物」で作り直した）\n\n") if m.group(1) in _newer else m.group(0),
                   head_text, flags=re.M | re.S)
extra = ""
if char_heads:
    extra = "\n\n# 追加の固定人物（2026-09-25）\n\n" + "\n\n".join(
        f"### {h}\n\n```text\n{b}\n```" for h, b in dict(char_heads).items() if h)
roster = read(HERE / "CHAR_固定人物_20260925.md") if (HERE / "CHAR_固定人物_20260925.md").exists() else ""
latest = (head_text + extra + "\n\n" + roster + "\n\n---\n\n"
          + "\n\n---\n\n".join(base[n] for n in sorted(base)) + "\n")
(HERE / "Asset_Prompts_Latest.md").write_text(latest, encoding="utf-8")

# --- 編集者用（プロンプトなし）
ed = ["# 2013・2014年せたな町ヒグマ事故 編集者用指示書（プロンプトなし）",
      "",
      "- 2026-09-26 最新版（本人の修正指示 約60件と全カットの点検を反映。作り直した素材はドライブの今と同じファイル名）",
      f"- 素材の置き場所: Google ドライブ「画像」フォルダ（{DRIVE}）",
      "- ファイル名は ASSET-番号_種類。_still.png＝16:9の静止画（キャラの背景にも使う）、_bg.png＝キャラを重ねる背景、_char.png＝背景透過のキャラ、_video.mp4＝動画",
      "- 「動画は使わない」とあるカットは、キャラと背景で表す（同じ番号の動画ファイルは使わない）",
      "- 地図（Google Earth）のカットは、書いてある座標・高さ・角度・向きで編集者が作る",
      ""]
for n in sorted(base):
    b = base[n]
    kind = re.search(r"【制作メモ】ASSET-\d+\s*\[([^\]]*)\]", b)
    narr = re.search(r"^ナレーター: (.*)$", b, re.M)
    scene = re.search(r"^シーン: (.*)$", b, re.M)
    lines, in_code = [], False
    for line in b.split("\n"):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not s or "プロンプト" in s or s.startswith(("ナレーター:", "【制作メモ】", "シーン:", "キャラ参照:")):
            continue
        lines.append(s)
    if not any("セリフ" in s for s in lines) and n in DIALOGUE and source.get(n) in ("元の資料", "動画を外す"):
        lines.insert(0, DIALOGUE[n])
    ed.append(f"## ASSET-{n:03d}（{kind.group(1) if kind else ''}）")
    ed.append("")
    ed.append(f"- ナレーション: {narr.group(1).strip() if narr else ''}")
    if scene:
        ed.append(f"- 場面: {scene.group(1).strip()}")
    for s in lines:
        ed.append(f"- {s.lstrip('→ ').strip()}")
    ed.append("")
(HERE / "編集者用_Latest.md").write_text("\n".join(ed), encoding="utf-8")

changed = {k: v for k, v in source.items() if v != "元の資料"}
print(f"カット数 {len(base)}／差し替え {len(changed)}")
from collections import Counter
print(Counter(changed.values()))

# 2026-09-26: 編集者用の指示が指すファイルが、ドライブに実在するか・作る予定にあるかを毎回確かめる（074「キャラ画像がありません」）
import subprocess as _sp
_r = _sp.run([sys.executable, str(HERE / "check_editor_refs.py")], capture_output=True, text=True)
print(_r.stdout.strip().splitlines()[-1] if _r.stdout.strip() else "参照チェック: 出力なし")
if _r.returncode:
    print(_r.stdout)
