#!/usr/bin/env python3
"""
Yama Phase2 納品物リント（人間チェック基準）

使い方:
    python3 validate_asset_deliverable.py <Asset_Prompts_Full.md>

`validate_yama_prompts.py` / `validate_phase2_assets.py` が「プロンプトの中身」を見るのに対し、
こちらは **「本人がそのまま編集に回せる納品物になっているか」** だけを見る。

較正の根拠（2026-08-25）:
    Scripts/2025年東成瀬村クマ襲撃事件/Asset_Prompts_Full_人間チェック済み.md
    ＝AI生成版を本人が全部読んで直した実物。**この実物が全ルールを通る値に較正してある**。
    AI生成版(Asset_Prompts_Full.md)は同じ検査で大量に落ちる。その差が「人間チェックの中身」。
    → feedback_calibrate_audits_to_shipped_content.md

ルール:
    H1 血液・負傷の打ち消し語の統一（"injuries visible" 禁止 → "No blood, no wounds, no gore."）
    H2 実在個人の[実写]にAIフォールバックを付けない（インタビュー/公式ポートレート/防犯カメラ）
    H3 [Lovart動画]の2ブロックにラベルを付ける（静止画プロンプト / Google Flow動画プロンプト）
    H4 納品物にAIの内部注記を残さない（設計の理由・確認事項・目視確認・出典メモ）
    H5 納品物にMarkdown装飾を使わない（Docsに貼ると ** や ``` がそのまま出る）
    H6 新規生成しなくていいカット（ベース／転換／再掲／説明だけの人物カット）の検出
    H7 Phase1の宿題をPhase2に持ち込まない（未確認・出典不明の申し送り）
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


ASSET_RE = re.compile(r'^【制作メモ】(ASSET-\d+)\s*(?:\[([^\]]*)\])?(.*)$', re.M)


def split_assets(text):
    """【制作メモ】単位でブロック化。(asset_id, type, body, 開始行番号) を返す"""
    marks = list(ASSET_RE.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.start():end]
        line_no = text.count('\n', 0, m.start()) + 1
        out.append((m.group(1), (m.group(2) or '').strip(), body, line_no))
    return out


def prompt_blocks(body):
    """英語プロンプト本文だけを取り出す（``` で囲まれていても、囲まれていなくても拾う）"""
    fenced = re.findall(r'```\n?(.*?)\n?```', body, re.S)
    if fenced:
        return fenced
    # 人間チェック済み版は ``` を外してある。英文の連なりを拾う
    return [ln for ln in body.split('\n')
            if len(ln) > 80 and re.match(r'^[A-Z"\'(]', ln.strip())
            and len(re.findall(r'[ぁ-んァ-ヶ一-龥]', ln)) < 5]


# ---------------------------------------------------------------- H1
def h1_gore_wording(assets):
    """血液・負傷の打ち消し語の統一"""
    hard, soft = [], []
    PERSON = re.compile(r'\b(man|woman|person|people|hunter|farmer|patient|officer|'
                        r'couple|villager|bear|body|bodies)\b', re.I)
    ATTACK = re.compile(r'\b(attack|attacked|mauled|charge|charging|pounce|claw|'
                        r'strike|slams?|victim|collapsed|lying|fallen)\b', re.I)
    for aid, atype, body, ln in assets:
        for b in prompt_blocks(body):
            if re.search(r'injuries visible', b, re.I):
                hard.append((aid, ln, '"injuries visible" → "No blood, no wounds, no gore." に統一'))
                break
        else:
            for b in prompt_blocks(body):
                if PERSON.search(b) and ATTACK.search(b) and not re.search(r'\bno blood\b', b, re.I):
                    soft.append((aid, ln, '襲撃/人物を描くのに "No blood, no gore." の打ち消しが無い'))
                    break
    return hard, soft


# ---------------------------------------------------------------- H2
REAL_PERSON_CUT = re.compile(r'インタビュー|証言|会見|顔写真|ポートレート|防犯カメラ|'
                             r'ライブ中継|実映像|出演')
FAKE_FOOTAGE = re.compile(r'being interviewed|interview framing|official portrait|'
                          r'portrait style|security camera style|news-helicopter|'
                          r'TV news style|speaking directly to an interviewer', re.I)


def h2_no_fake_real_person(assets):
    bad = []
    for aid, atype, body, ln in assets:
        if '実写' not in atype:
            continue
        scene = re.search(r'^シーン: (.*)$', body, re.M)
        scene_txt = scene.group(1) if scene else ''
        if not REAL_PERSON_CUT.search(scene_txt):
            continue
        for b in prompt_blocks(body):
            if FAKE_FOOTAGE.search(b):
                bad.append((aid, ln, f'実在個人の「{scene_txt[:22]}」にAI再現プロンプトが付いている'))
                break
    return bad


# ---------------------------------------------------------------- H3
def h3_video_block_labels(assets):
    bad = []
    for aid, atype, body, ln in assets:
        if 'Lovart動画' not in atype:
            continue
        miss = []
        if '静止画プロンプト' not in body:
            miss.append('「静止画プロンプト（16:9・フォトリアル）:」ラベル')
        if 'Google Flow動画プロンプト' not in body:
            miss.append('「Google Flow動画プロンプト:」')
        if miss:
            bad.append((aid, ln, '／'.join(miss) + ' が無い'))
    return bad


# ---------------------------------------------------------------- H4
INTERNAL_NOTE = [
    (r'設計の理由', '設計の理由'),
    (r'⚠?\s*確認事項', '確認事項'),
    (r'生成後に(必ず)?目視', '生成後の目視確認メモ'),
    (r'数値の出典', '数値の出典メモ'),
    (r'新規生成しない', '「新規生成しない」の説明'),
    (r'素材の入手性', '素材の入手性メモ'),
    (r'ズーム位置・トリミング・色調補正で画変わり', '背景再使用の長文説明'),
]


def h4_internal_notes(assets):
    bad = []
    for aid, atype, body, ln in assets:
        for pat, label in INTERNAL_NOTE:
            if re.search(pat, body):
                bad.append((aid, ln, f'{label} が納品物に残っている'))
    return bad


# ---------------------------------------------------------------- H5
def h5_markdown_decoration(assets):
    bad = []
    for aid, atype, body, ln in assets:
        hits = []
        if body.count('**') >= 2:
            hits.append('**強調**')
        if re.search(r'^###', body, re.M):
            hits.append('### 見出し')
        if re.search(r'`[^`\n]{1,40}`', body):
            hits.append('`インラインコード`')
        if hits:
            bad.append((aid, ln, '／'.join(hits) + ' が本文にある（Docsに貼ると記号のまま出る）'))
    return bad


# ---------------------------------------------------------------- H6
FILLER_SCENE = re.compile(r'ベース|転換カット|再掲|見出し|回想|'
                          r'考え込む|切り出す|うなずく|指を立て|色調が急変|'
                          r'語り手|キャスター|説明する|示す（?転換')
NEW_GEN = re.compile(r'Cute cartoon character design|Photorealistic, shot on RED')


def h6_avoidable_generation(assets):
    bad = []
    for aid, atype, body, ln in assets:
        scene = re.search(r'^シーン: (.*)$', body, re.M)
        if not scene:
            continue
        if not FILLER_SCENE.search(scene.group(1)):
            continue
        if any(NEW_GEN.search(b) for b in prompt_blocks(body)):
            bad.append((aid, ln, f'「{scene.group(1)[:26]}」→ 既存アセット再利用か黒背景テキストで足りないか'))
    return bad


# ---------------------------------------------------------------- H7
PHASE1_LEFTOVER = re.compile(r'出典が確認できない|未検証|台本に無い|'
                             r'ナレーションの数字を実測値に直す|根拠が確認できな')


def h7_phase1_leftover(assets):
    bad = []
    for aid, atype, body, ln in assets:
        m = PHASE1_LEFTOVER.search(body)
        if m:
            bad.append((aid, ln, f'Phase1で解決すべき申し送り「{m.group(0)}」が残っている'))
    return bad


# ---------------------------------------------------------------- main
# 人間チェック済み版（Scripts/2025年東成瀬村クマ襲撃事件/Asset_Prompts_Full_人間チェック済み.md
# ・273アセット）を同じ検査にかけて実測した残存件数。「アセット100件あたり何件まで許すか」。
# 本人が直した実物ですらゼロではない＝ここが現実の合格ラインで、目標は各行のゼロ。
# 較正の根拠: feedback_calibrate_audits_to_shipped_content.md
BASELINE_PER_100 = {
    'H1':  0.4,   # 人間版 1件/273
    'H1b': 9.9,   # 人間版 27件/273
    'H2':  0.4,   # 人間版 1件/273
    'H3':  7.0,   # 人間版 19件/273
    'H4': 16.1,   # 人間版 44件/273
    'H5': 23.8,   # 人間版 65件/273
    'H6':  4.0,   # 人間版 11件/273
    'H7':  0.0,   # 人間版 0件/273
}


def main(path):
    text = open(path, encoding='utf-8').read()
    assets = split_assets(text)
    if not assets:
        print(f'\u274c \u3010\u5236\u4f5c\u30e1\u30e2\u3011ASSET-XXX \u304c1\u4ef6\u3082\u898b\u3064\u304b\u308a\u307e\u305b\u3093: {path}')
        sys.exit(1)

    n = len(assets)
    print('=' * 66)
    print(f'Phase2 納品物リント（人間チェック基準） — {path}')
    print(f'アセット数: {n}／判定は「人間チェック済み版の実測残存率」との比較')
    print('=' * 66)

    over = 0
    clean = 0

    def report(key, title, items, hint=''):
        nonlocal over, clean
        limit = int(BASELINE_PER_100[key] * n / 100 + 0.999)
        cnt = len(items)
        if cnt == 0:
            print(f'✅ {key} {title}: 0件（人間チェック済み版と同等以上）')
            clean += 1
            return
        if cnt <= limit:
            print(f'🟡 {key} {title}: {cnt}件（許容 {limit}件以内。人間版も {BASELINE_PER_100[key]}件/100 残っている）')
        else:
            over += 1
            print(f'\n❌ {key} {title}: {cnt}件 — 人間チェック済み版の水準（{limit}件以内）を超過')
            if hint:
                print(f'   {hint}')
            for aid, ln, msg in items[:12]:
                print(f'   L{ln} {aid}: {msg}')
            if cnt > 12:
                print(f'   ...他{cnt - 12}件')
            print()

    hard, soft = h1_gore_wording(assets)
    report('H1', '血液・負傷の打ち消し語', hard,
           '本人は "no injuries visible" を "No blood, no wounds, no gore." に統一した')
    report('H1b', '襲撃カットの打ち消し漏れ', soft,
           '人物・クマ・襲撃を描くプロンプトには "No blood, no gore." を必ず入れる')
    report('H2', '実在個人のAI再現', h2_no_fake_real_person(assets),
           'インタビュー・公式ポートレート・防犯カメラのAI再現は本人が全部削除した')
    report('H3', 'Lovart動画の2ブロックラベル', h3_video_block_labels(assets),
           '1ブロック目＝静止画プロンプト、2ブロック目＝Google Flow動画プロンプト')
    report('H4', 'AIの内部注記', h4_internal_notes(assets),
           '根拠・警告・確認事項は納品物から外し `_制作ノート.md` に分ける')
    report('H5', 'Markdown装飾', h5_markdown_decoration(assets),
           '納品物はGoogleドキュメントに貼る前提＝プレーンテキストで書く')
    report('H6', '生成しなくていいカット', h6_avoidable_generation(assets),
           'ベース／転換／再掲／説明だけの人物カットは再利用か黒背景テキストで済む')
    report('H7', 'Phase1の宿題の持ち込み', h7_phase1_leftover(assets),
           '未確認の数字はPhase1で決着させる。Phase2の納品物に残さない')

    print('=' * 66)
    if over:
        print(f'結果: ❌ FAIL — {over}項目が人間チェック済み版より悪い。ここを直せば手直しが減る')
        sys.exit(1)
    print(f'結果: ✅ PASS — 全{len(BASELINE_PER_100)}項目が人間チェック済み版と同等以上（うち{clean}項目はゼロ）')
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
