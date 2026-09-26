"""せたな町: 別のPCで作るファイルの一覧（生成リスト.tsv）と、ドライブから消すファイルの一覧（削除リスト.tsv）を作る。

生成リスト: 作り直しの md（Fix2〜Fix5）にプロンプトがあり、「既存を使う」と書かれていないもの。
  ファイル名はドライブの今の名前に合わせる（背景は今 _bg.png があれば _bg、_still.png があれば _still、無ければ _bg）。
削除リスト: 生成リストで置き換わるファイル＋動画を外すカットの _video.mp4＋地図にしたカットの画像・動画
  ＋キャラを使わなくなったカットの _char.png。
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE.parent
FIX = ["Asset_Prompts_Fix2.md", "Asset_Prompts_Fix3.md", "Asset_Prompts_Fix4.md",
       "Asset_Prompts_Fix5a.md", "Asset_Prompts_Fix5b.md", "Asset_Prompts_Fix5c.md", "Asset_Prompts_Fix6.md"]
review = json.loads((A / "scene_fitness_review_claude.json").read_text(encoding="utf-8"))
now = {c["asset_no"]: sorted(Path(f).name for f in c["files"]) for c in review["cuts"]}
drive_dir = HERE.parents[1] / "drive_images_20260925"
if drive_dir.exists():  # ドライブの実物（画像）で上書き
    for p in drive_dir.glob("ASSET-*.png"):
        n = int(p.name[6:9])
        now.setdefault(n, [])
        if p.name not in now[n]:
            now[n].append(p.name)

# 本人判断で既に済んだもの（生成しない）
DONE = {"ASSET-008_video.mp4", "ASSET-008_still.png"}  # 008 は本人が「このままでよい」と承認済み

gen, delete = [], []
ALL_FIX = "\n".join((HERE / m).read_text(encoding="utf-8") for m in ["Asset_Prompts_Regen.md"] + FIX if (HERE / m).exists())


def add_del(name, why):
    if not any(d[0] == name for d in delete):
        delete.append((name, why))


def _nums(md):
    q = HERE / md
    return {int(x) for x in re.findall(r"^【制作メモ】ASSET-(\d+)", q.read_text(encoding="utf-8"), re.M)} if q.exists() else set()


for i_md, mdname in enumerate(FIX):
    p = HERE / mdname
    if not p.exists():
        continue
    # 2026-09-26: 後のファイルで上書きしたカットは数えない（Fix5b の132と Fix6 の132が両方リストに載り、古い指示で作りかけた）
    later = set().union(*[_nums(m) for m in FIX[i_md + 1:]]) if i_md + 1 < len(FIX) else set()
    text = p.read_text(encoding="utf-8").replace("\r\n", "\n")
    tail = re.search(r"^## 動画を外すだけのカット\s*$(.*)", text, re.M | re.S)
    if tail:
        for n in sorted({int(x) for x in re.findall(r"(?<![\d])(\d{3})(?![\d])", tail.group(1))}):
            add_del(f"ASSET-{n:03d}_video.mp4", "動画を外す（キャラと背景で表す）")
        text = text[:tail.start()]
    for part in re.split(r"\n---\n", text):
        m = re.search(r"^【制作メモ】ASSET-(\d+)\s*\[([^\]]*)\]", part, re.M)
        if not m:
            continue
        n, kind = int(m.group(1)), m.group(2)
        if n in later:
            continue
        have = now.get(n, [])
        if "Google Earth" in kind or "再利用" in kind:
            for f in have:
                add_del(f, "地図（編集者が作る）に変更" if "Google Earth" in kind else "別カットの再利用に変更")
            continue
        labels = re.findall(r"^(.*?)\n```", part, re.M)
        reuse_bg = re.search(r"背景は既存の (ASSET-\d+_\w+\.png)", part)
        # 別カットで作る背景を借りるカット（059＝055の背景、080＝079の静止画）は、自分の背景を作らない
        # 2026-09-26: 借りる対象は背景・静止画のファイルだけ。015「背景は新規、キャラは ASSET-029_char.png を再利用」を
        #   背景の借用と取り違え、015 の新しい背景が生成リストから落ちていた（本人「アセット15がないです」）
        borrow = next((m for m in re.finditer(r"背景は[^\n。、]*?ASSET-(\d+)_(?:bg|still)\w*\.png[^\n。]*?(?:再使用|再利用)", part)
                       if int(m.group(1)) != n), None)
        if borrow and not reuse_bg:
            reuse_bg = borrow
            if "キャラ" in kind:
                for f in have:
                    if f.endswith(("_still.png", "_bg.png")):
                        add_del(f, f"背景は ASSET-{int(borrow.group(1)):03d} のものを使うので不要")
        reuse_char = re.search(r"キャラは既存の (ASSET-\d+_char\.png)|キャラは (ASSET-\d+_char\.png) を再利用", part)
        has = lambda key: any(key in l for l in labels)
        files = []
        if has("キャラプロンプト") and not reuse_char:
            files.append((f"ASSET-{n:03d}_char.png", "キャラ"))
        # 既存キャラに1人足すカット（051＝既存の地区長＋新しく作る住民）は _char2.png で作る
        for extra in re.findall(r"新規の (ASSET-\d+_char\d+\.png)", part):
            files.append((extra, "キャラ（追加の1人）"))
        if has("背景プロンプト") and not reuse_bg:
            bgname = next((f for f in have if f.endswith("_bg.png")), None) or \
                     next((f for f in have if f.endswith("_still.png")), None) or f"ASSET-{n:03d}_bg.png"
            # 資料が _bg.png の名前で指している背景（「ASSET-181_bg.png として保存」「055の ASSET-055_bg.png を再使用」）はその名前で作り、
            # ドライブの古い _still.png は消す
            want = f"ASSET-{n:03d}_bg.png"
            if want in ALL_FIX and bgname != want:
                if bgname in have:
                    add_del(bgname, f"背景を {want} の名前で作り直す")
                bgname = want
            files.append((bgname, "背景"))
        # 動画の元の静止画を既存・別カットの画像で済ませるカット（160＝既存の _still、198＝174の _bg）
        still_src = re.search(r"静止画は[^\n。]*?(ASSET-(\d+)_\w+\.png)[^\n。]*?(?:そのまま使い|を使い)", part)
        if "動画" in kind or has("動画プロンプト"):
            if (any(not l.strip() or "静止画" in l for l in labels) or re.search(r"^```\n", part, re.M)) and not still_src:
                files.append((f"ASSET-{n:03d}_still.png", "静止画（動画の元）"))
            if still_src and int(still_src.group(2)) != n and f"ASSET-{n:03d}_still.png" in have:
                add_del(f"ASSET-{n:03d}_still.png", f"動画の元は {still_src.group(1)} を使うので不要")
            files.append((f"ASSET-{n:03d}_video.mp4", "動画"))
        elif ("静止画" in kind or "Lovart" in kind) and not has("キャラ") and not has("背景"):
            files.append((f"ASSET-{n:03d}_still.png", "静止画"))
        # キャラをやめて実写にしたカットは、古いキャラと背景を消す
        if "キャラ" not in kind and not has("キャラプロンプト"):
            for f in have:
                if f.endswith(("_char.png", "_bg.png")):
                    add_del(f, "キャラをやめて実写にしたので不要")
        for name, what in files:
            if name in DONE:
                continue
            gen.append((name, what, mdname))
            if name in have or name.endswith(".mp4"):
                add_del(name, "作り直す（別のPCで同じ名前で作る）")
        # 動画を作らなくなったキャラのカットは、動画を消す
        if "キャラ" in kind and f"ASSET-{n:03d}_video.mp4" in have and not has("動画プロンプト"):
            add_del(f"ASSET-{n:03d}_video.mp4", "動画を外す（キャラと背景で表す）")
        # 別カットのキャラを使うことにしたカットは、自分の _char.png を消す（015＝029のキャラを使う）
        if reuse_char and (reuse_char.group(1) or reuse_char.group(2)) != f"ASSET-{n:03d}_char.png" and f"ASSET-{n:03d}_char.png" in have:
            add_del(f"ASSET-{n:03d}_char.png", "別カットのキャラを使うので不要")

# 検収で「キャラは使わない」と決めたカットの _char.png（他のカットが再利用していないものだけ）
UNUSED_CHAR = {47, 56, 83, 96, 103, 108, 125, 148, 149, 194}
latest = (HERE / "Asset_Prompts_Latest.md").read_text(encoding="utf-8") if (HERE / "Asset_Prompts_Latest.md").exists() else ""
overridden = {int(m) for mdname in FIX if (HERE / mdname).exists()
              for m in re.findall(r"^【制作メモ】ASSET-(\d+)", (HERE / mdname).read_text(encoding="utf-8"), re.M)}
for n in sorted(UNUSED_CHAR):
    name = f"ASSET-{n:03d}_char.png"
    if n not in overridden and name in now.get(n, []) and f"{name} を再利用" not in latest and f"既存の {name}" not in latest:
        add_del(name, "キャラは使わない（検収で決定）")

gen = list(dict.fromkeys(gen))
(HERE / "生成リスト.tsv").write_text("ファイル名\t種類\tプロンプトのある資料\n" + "\n".join("\t".join(g) for g in gen) + "\n", encoding="utf-8")
(HERE / "削除リスト.tsv").write_text("ファイル名\t理由\n" + "\n".join("\t".join(d) for d in sorted(delete)) + "\n", encoding="utf-8")
print(f"生成 {len(gen)} 件（画像 {sum(1 for g in gen if g[0].endswith('.png'))}・動画 {sum(1 for g in gen if g[0].endswith('.mp4'))}）／削除 {len(delete)} 件")
