#!/usr/bin/env python3
"""追加課金なしのキャラ修正: 既存の合格キャラPNGを流用（複製・2人/3人の並置合成）して fixed/画像/ に置く。
生成が要るもの（警察＋消防、小学生）は char_queue に出す。
"""
import json, hashlib
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent
D = Path.home() / "Desktop/せたな町_素材_20260924/画像"
OUT = HERE / "fixed" / "画像"; OUT.mkdir(parents=True, exist_ok=True)
log = []

def load(no):
    return Image.open(D / f"ASSET-{no:03d}_char.png").convert("RGBA")

def bbox_crop(im):
    b = im.getbbox(); return im.crop(b) if b else im

def copy_as(src_no, dst_no, note):
    im = load(src_no); im.save(OUT / f"ASSET-{dst_no:03d}_char.png")
    log.append({"asset": f"ASSET-{dst_no:03d}", "method": "reuse", "source": f"ASSET-{src_no:03d}_char.png", "note": note})

def compose(dst_no, srcs, note, flip_last=False):
    """複数の透過キャラを1024x1024に横並びで置く（足元を揃える）。"""
    canvas = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    n = len(srcs); slot = 1024 / n
    figs = [bbox_crop(load(s)) for s in srcs]
    if flip_last: figs[-1] = figs[-1].transpose(Image.FLIP_LEFT_RIGHT)
    target_h = int(1024 * (0.92 if n == 2 else 0.80))
    for i, f in enumerate(figs):
        scale = target_h / f.height
        w = int(f.width * scale); h = target_h
        if w > slot * 1.15: scale = slot * 1.15 / f.width; w = int(f.width * scale); h = int(f.height * scale)
        f = f.resize((w, h), Image.Resampling.LANCZOS)
        x = int(slot * i + (slot - w) / 2); y = 1024 - h - 40
        canvas.alpha_composite(f, (x, y))
    canvas.save(OUT / f"ASSET-{dst_no:03d}_char.png")
    log.append({"asset": f"ASSET-{dst_no:03d}", "method": "compose", "source": [f"ASSET-{s:03d}_char.png" for s in srcs], "note": note})

# 差し替え（台本の人物へ）
copy_as(19, 17, "CHAR-02（夫）が食卓の前で心配そうに立つ＝019の夫を流用")
copy_as(19, 20, "CHAR-02（夫）がワゴン車を見つける＝019の夫を流用")
copy_as(85, 79, "CHAR-04（男性）が体長比較の横に立つ＝085の無傷の男性を流用")
copy_as(105, 157, "役場の職員が窓の外を見る＝105の職員を流用")
copy_as(206, 168, "86歳の元漁師＝206の高齢男性を流用")
copy_as(57, 51, "地区長が掲示を貼る＝057の拡声器の高齢男性を流用")
copy_as(105, 202, "資料を見る職員＝105を流用")
# 2人・3人の並置
compose(66, [85, 63], "CHAR-04（男性）とCHAR-03（女性）が並んで入山")
compose(71, [85, 63], "看板の先へ入る2人（CHAR-04・CHAR-03）")
compose(74, [85, 63], "男性を先頭に下山する2人（CHAR-04が前・CHAR-03が後ろ）")
compose(213, [85, 63], "2人で山道を歩く（CHAR-04・CHAR-03）")
compose(214, [63, 77], "複数歩行で周囲を警戒する2人")
compose(215, [85, 63], "入山前に装備を確かめる2人")
compose(25, [34, 23], "沢で発見した捜索者2人（034の捜索者＋023の隊員）")
compose(26, [34, 23], "立ち尽くす捜索者2人", flip_last=True)
compose(39, [40, 105, 138], "3人の職員（研究者＋職員2人）")
# 生成が要るもの
char_queue = [
 {"id": "ASSET-023_char", "asset_no": 23, "kind": "キャラアニメーション", "slot": "char", "aspect": "1:1", "label": "", "narration": "到着した警察と消防が、辺りを捜索することに。", "char_ref": None,
  "prompt": "Cute 2D children's animation cartoon. A large head taking about one quarter of total height; four to five heads tall, large head, short compact torso, short stubby arms and legs. Uniform thick black outlines around the silhouette and major shapes, flat colors with at most one flat shadow shade, large expressive eyes. No realistic adult proportions, no slender or elongated body, no detailed fabric texture, no gradients, no painterly rendering, no photo realism. Exactly TWO full-body Japanese men standing side by side, count them 1, 2: 1) on the left a police officer in a dark navy uniform and cap with a flashlight, 2) on the right a firefighter in an orange rescue jacket and white helmet with a radio. Both three-quarter front view, faces clearly visible with distinct eyes, nose and mouth, serious alert expressions, no smile. NO TWO OF THEM SHARE A FACE OR AN OUTFIT. No emblem, no badge lettering, no logo. Show only the two people; do not draw scenery, a bear, a vehicle, a building, a map, or printed material. Heads and feet fully inside the square frame, no duplicate poses, no panel grid. Clean transparent alpha background. No written words, numbers, blood, wounds, or gore. 1:1 square image."},
 {"id": "ASSET-054_char", "asset_no": 54, "kind": "キャラアニメーション", "slot": "char", "aspect": "1:1", "label": "", "narration": "また、小中学生を乗せたスクールバスは、家の玄関まで送り迎えするようにしました。", "char_ref": None,
  "prompt": "Cute 2D children's animation cartoon. A large head taking about one quarter of total height; four to five heads tall, large head, short compact torso, short stubby arms and legs. Uniform thick black outlines around the silhouette and major shapes, flat colors with at most one flat shadow shade, large expressive eyes. No realistic adult proportions, no slender or elongated body, no detailed fabric texture, no gradients, no painterly rendering, no photo realism. One full-body Japanese elementary school boy, about 8 years old, wearing a yellow cap and a red randoseru school backpack, a light jacket and shorts, three-quarter front view, face clearly visible, slightly nervous expression, no smile, one hand gripping his backpack strap. Show only the boy; do not draw scenery, a bus, a house, a bear, or printed material. Head and feet fully inside the square frame, one figure only, no panel grid. Clean transparent alpha background. No written words, numbers, logos, blood, wounds, or gore. 1:1 square image."},
]
work = HERE / "regen_char"; work.mkdir(exist_ok=True)
(work / "image_queue.json").write_text(json.dumps(char_queue, ensure_ascii=False, indent=2))
for e in log:
    e["sha256"] = hashlib.sha256((OUT / f"{e['asset']}_char.png").read_bytes()).hexdigest()
(HERE / "char_fix_log.json").write_text(json.dumps(log, ensure_ascii=False, indent=1))
print("reuse/compose:", len(log), "| char queue:", len(char_queue))
