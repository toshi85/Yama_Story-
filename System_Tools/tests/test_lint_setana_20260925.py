"""2026-09-25 せたな町で本人が指摘した間違いを、わざとプロンプトに入れて lint が止めるかを確かめる。
正しい版（Fix4 の元の書き方）は通り、間違い版だけが止まること。"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
FIX4 = HERE.parent / "Scripts/2013-2014年せたな町ヒグマ事故/素材_API_20260924/claude_audit_20260924/regen_20260925/Asset_Prompts_Fix4.md"


def lint(text: str) -> str:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "Asset_Prompts_test.md"
        p.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(HERE / "validate_phase2_assets.py"), "--prompts", str(p)],
                              capture_output=True, text=True, encoding="utf-8").stdout


BASE = FIX4.read_text(encoding="utf-8")
CASES = [
    # (名前, 間違いの入れ方, 止まるべき文言)
    ("045 ハンターに CHAR 番号が無い（043 と別人になる）",
     lambda t: t.replace("(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese local hunter in his 60s with short grey hair and a grey stubble, an orange cap, a dark green field jacket under a blaze-orange safety vest, khaki trousers and brown boots, standing square to the viewer with his shoulder line parallel to the picture plane, his face clearly visible. He rests",
                         "Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese hunter in his 30s, standing square to the viewer with his shoulder line parallel to the picture plane, his face clearly visible. He rests"),
     "何度も出る役にCHAR番号が無い"),
    ("043 4月の背景に No snow が無い（雪が描かれる）",
     lambda t: t.replace("No snow anywhere, no snow patches, no frost, no ice, no winter. Dim", "Dim"),
     "No snow が無い"),
    ("064 地名の文が静止画（地図にしていない）",
     lambda t: t + "\n---\n\nナレーター: 現場は、大成区の太田地区。\n\n【制作メモ】ASSET-064 [Lovart静止画 + 編集者] 台本L110\nシーン: 太田地区の山道。\n```\nA gravel mountain road near Setana, southwestern Hokkaido, in mid-April early spring, No snow anywhere, no frost, no ice, no winter. No people, no figures, no humans visible. Photorealistic, shot on RED camera. 16:9 aspect ratio. Generate 1 image.\n```\n→ 編集者指示: 中央に「太田地区」を白字で表示し、「太田」だけ赤字。\n",
     "地図になっていない"),
    ("060 48字の文が静止画だけ",
     lambda t: t + "\n---\n\nナレーター: こうした取り組みを必死ですすめていましたが、人を襲ったクマは結局、誰も捕まえることはできませんでした。\n\n【制作メモ】ASSET-060 [Lovart静止画 + 編集者] 台本L104\nシーン: 森に置かれた空の箱わな。\n```\nAn empty steel box trap in a forest near Setana, southwestern Hokkaido, in mid-April early spring, No snow anywhere, no frost, no ice, no winter. No people, no figures, no humans visible. Photorealistic, shot on RED camera. 16:9 aspect ratio. Generate 1 image.\n```\n→ 編集者指示: 中央に「捕獲できず」を白字で表示し、「できず」だけ赤字。\n",
     "静止画だけ"),
    ("031 キャラのカットに動画も重ねる",
     lambda t: t.replace("→女性セリフ「娘さんに／会いに行くはずだったのに、、」",
                         "→ **Google Flow動画プロンプト:**\n```\nOne single continuous take. A hand closes a diary. 8 seconds. Photorealistic.\n```\n→女性セリフ「娘さんに／会いに行くはずだったのに、、」"),
     "動画プロンプトもある"),
    # 2026-09-26: ChatGPT が絵を返さない言葉（026 の元の書き方）。打ち消し（No blood）は止めない
    ("026 亡くなった人を clearly dead / dark red stains で書く（ChatGPT が描かない）",
     lambda t: t.replace("baffled and troubled, NOT calm, NOT smiling.",
                         "baffled and troubled, NOT calm, NOT smiling, clearly dead, lifeless, with dark red stains soaking his jacket."),
     "ChatGPT が描かない言葉"),
    # 2026-09-26 本人指摘（159・162「実写のクマとキャラ」／164「若い人」／168「なんで泣いてる」）
    ("159 キャラのカットの背景に実写のクマ",
     lambda t: t.replace("dry brown grass along the track, a faint blue pre-dawn light", "an adult Hokkaido brown bear about 2 metres long stands on all fours among the trees, dry brown grass along the track, a faint blue pre-dawn light"),
     "背景に実写のクマ"),
    ("164 旧い汎用キャラの型",
     lambda t: t.replace("(CHAR-05 再利用) Cute cartoon character design,", "(CHAR-05 再利用) The person reacts to or performs the action in this Japanese scene description. Cute cartoon character design,", 1),
     "旧い汎用キャラの型"),
    ("168 台本に無い泣き顔",
     lambda t: t.replace("(CHAR-05 再利用) Cute cartoon character design,", "(CHAR-05 再利用) Tears streaming down his cheeks, crying. Cute cartoon character design,", 1),
     "泣いている"),
    ("082 動画のクマの頭数が無い",
     lambda t: t.replace("→女性セリフ「娘さんに／会いに行くはずだったのに、、」", "→ Google Flow動画プロンプト:\n```\nOne single continuous shot: a brown bear runs away up the trail. 5 seconds.\n```\n→女性セリフ「娘さんに／会いに行くはずだったのに、、」"),
     "クマの頭数"),
    ("198 動画に8秒分の動き",
     lambda t: t.replace("→女性セリフ「娘さんに／会いに行くはずだったのに、、」", "→ Google Flow動画プロンプト:\n```\nOne single continuous shot: two hunters walk to a van, load it and drive away. 8 seconds.\n```\n→女性セリフ「娘さんに／会いに行くはずだったのに、、」"),
     "6秒以上"),
    ("164 キャラの人物に年齢が無い",
     lambda t: t.replace("A full-body Japanese local hunter in his 60s with short grey hair", "A full-body Japanese local hunter with short grey hair", 1),
     "年齢が無い"),
]


def main() -> int:
    ng = 0
    base_out = lint(BASE)
    for key in ("何度も出る役にCHAR番号が無い", "No snow が無い", "静止画だけ", "動画プロンプトもある", "ChatGPT が描かない言葉"):
        if key in base_out:
            print(f"NG  正しい版なのに止まった: {key}")
            ng += 1
    for name, inject, expect in CASES:
        out = lint(inject(BASE))
        ok = expect in out
        print(("ok  " if ok else "NG  ") + name)
        ng += 0 if ok else 1
    print(f"NG={ng}")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
