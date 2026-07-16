#!/usr/bin/env python3
"""
Yama Phase2 アセット割り振り 自動検証（羅臼岳標準）
使い方: python3 validate_phase2_assets.py <Master.md> <台本.txt>

「ユーザーに見せる前」に必ず実行し、全項目GREENにしてから提示する。
2026-07-16の朱鞠内湖で4〜5回の作り直しが発生した反省から作成。
ルール根拠: memory/feedback_yama_one_asset_per_narration_line.md
"""
import re, sys

def main(master_path, daihon_path):
    m = open(master_path, encoding='utf-8').read()
    src = [l.strip() for l in open(daihon_path, encoding='utf-8') if l.strip()]
    lines = m.split('\n')
    errors, warns, info = [], [], []

    # 1) 本文完全一致（順序・重複・改変）
    nar = [re.sub(r'^ナレーター:\s*', '', l).rstrip() for l in lines if l.startswith('ナレーター:')]
    if src != nar:
        errors.append(f'本文不一致: 台本{len(src)}行 vs Master{len(nar)}行')
        for i, (a, b) in enumerate(zip(src, nar)):
            if a != b:
                errors.append(f'  最初の不一致 行{i}: 台本「{a[:30]}」≠ Master「{b[:30]}」'); break
    else:
        info.append(f'本文完全一致 {len(nar)}行')

    # 2) 1ナレ行=1制作メモ
    memo = sum(1 for l in lines if l.startswith('【制作メモ】'))
    if memo != len(nar):
        errors.append(f'1ナレ行=1メモ違反: メモ{memo} vs ナレ{len(nar)}')
    else:
        info.append(f'1ナレ行=1メモ {memo}')

    # 3) アセットタイプ（3種+黒カード+実写のみ。背景静止画/図解の単独禁止）
    tag_counts = {}
    for t in ['キャラアニメーション', 'Lovart動画', 'Google Earth', '画面エフェクト', '実写', '背景静止画', '図解', 'AI動画']:
        tag_counts[t] = len(re.findall(r'-\s*【' + t, m))
    if tag_counts['背景静止画'] > 0:
        errors.append(f'背景静止画の単独アセット {tag_counts["背景静止画"]}件（禁止→Lovart動画かキャラに）')
    if tag_counts['図解'] > 0:
        errors.append(f'図解の単独アセット {tag_counts["図解"]}件（禁止→実景に編集者指示で重ねる）')
    info.append('タイプ内訳: ' + ' / '.join(f'{k}{v}' for k, v in tag_counts.items() if v))

    # 4) コードフェンス整合
    if m.count('```') % 2 != 0:
        errors.append('コードフェンス奇数（```の対応崩れ）')

    # 5) 生成枚数（1枚＝Generate N separate images を書かない）
    g = len(re.findall(r'Generate \d+ separate', m))
    if g > 0:
        errors.append(f'「Generate N separate images」が{g}件残存（1枚生成なら削除）')

    # 5b) 日本語文字ぼかしの逃げ（掲示/看板/書類は実文字を描き【chatGPT推奨】を付ける。免許証等の個人情報のみ例外）
    tb = re.findall(r'(文字はぼかす|Japanese text softly blurred|text columns softly blurred|blurred Japanese text|with blurred text)', m)
    if tb:
        warns.append(f'日本語文字ぼかし {len(tb)}件（掲示/書類は実文字を描く＋ラベルに【chatGPT推奨】。免許証等の個人情報のみ例外）')

    # 6) Google Earth 座標必須
    ge = re.findall(r'- 【Google Earth】.*?(?=\n\nナレーター|\n## |\Z)', m, re.S)
    no_coord = [b for b in ge if '座標' not in b]
    if no_coord:
        errors.append(f'Google Earth座標欠落 {len(no_coord)}件')
    else:
        info.append(f'Google Earth {len(ge)}件 全座標あり')

    # 7) キャラプロンプトに環境語（白背景・環境なし）
    cp = re.findall(r'キャラプロンプト（1:1）:\s*\n```\n(.*?)\n```', m, re.S)
    scene = ['window', 'lakeshore', ' shore', 'riverbank', ' boat ', 'boat,', 'forest', 'bushes', ' trail', 'tundra', ' river ', 'wading']
    badcp = [b[:60] for b in cp if any(w in b.lower() for w in scene)]
    if badcp:
        errors.append(f'キャラプロンプトに環境語混入 {len(badcp)}件（白背景・環境なしに）')

    # 8) 背景使い回し（BGプリセット参照＝新規固有背景の原則違反の疑い）
    reuse = len(re.findall(r'背景プロンプト（16:9）:\s*BG-[A-Z]', m))
    if reuse > 0:
        warns.append(f'BGプリセット参照 {reuse}件（羅臼岳標準は毎回固有。使い回し過多に注意）')

    # 9) 動画比率（羅臼岳=約26%。少なすぎ注意）
    flow = m.count('Google Flow動画プロンプト')
    ratio = flow / len(nar) * 100 if nar else 0
    info.append(f'動画(Google Flow) {flow}本 = 全体の{ratio:.0f}%')
    if ratio < 20:
        warns.append(f'動画比率{ratio:.0f}%が低い（羅臼岳は約26%。動きで見せる動画を増やす）')

    # 10) 冒頭=実写 / 末尾=AI動画
    body_after = m[m.find('<!-- PART: KI -->'):] if '<!-- PART: KI -->' in m else m
    first_memo = body_after.split('【制作メモ】', 1)[-1][:200] if '【制作メモ】' in body_after else ''
    if '【実写】' not in first_memo:
        warns.append('冒頭アセットが実写でない可能性（フックは実写）')
    tail = m[m.rfind('## §'):] if '## §' in m else m
    last2 = tail.rsplit('ナレーター:', 2)
    if len(last2) >= 2 and '【Lovart動画】' not in last2[-1] and '【AI動画】' not in last2[-1]:
        warns.append('末尾（視聴御礼）がAI動画でない可能性（末尾は必ず動画）')

    # 11/12) 文字が写る「静止画/背景」画像プロンプトのみを対象に、実文字指定/no text 強制＋【chatGPT推奨】必須
    #   （Google Flow動画プロンプト=映像は静止画を動かすだけなので対象外。実写アセットも対象外）
    TEXTOBJ = re.compile(r"warning sign|bear-warning|beware of|notice board|\bnotice\b|rules board|information board|newspaper|statement document|\bdocument\b|driver's licen[sc]e|licen[sc]e|signboard|placard|\bposter\b|headline|nameplate|plaque|certificate", re.I)
    LITERAL = re.compile(r"'[^']*[一-龠ぁ-んァ-ヴー々〇]+[^']*'|「[^」]+」")  # 単一引用符内に日本語を含む(reading/headed問わず)＝実文字指定とみなす
    NOTEXT  = re.compile(r"no text|no legible text|\bblank\b|not legible|blurred|unreadable", re.I)  # blurred/unreadable=個人情報の意図的非可読(遺族配慮)を許容。文字ぼかしの逃げは別途5bが捕捉
    ENGSIGN = re.compile(r'"[A-Za-z][A-Za-z ]+"\s*(?:warning\s+)?sign', re.I)
    unspoken, engs, missing_gpt = [], [], 0
    for mo in re.finditer(r'(- [^\n]*プロンプト[^\n]*:)\n```\n(.*?)\n?```', m, re.S):
        label, b = mo.group(1), mo.group(2)
        if 'no written words' in b or 'Cute cartoon character design' in b:  # キャラ立ち絵は文字/環境を持たない規則→除外（"notice"=動詞の誤検出も回避）
            continue
        if ENGSIGN.search(b):
            engs.append(b[:48])
        if TEXTOBJ.search(b) and not NOTEXT.search(b) and not LITERAL.search(b):
            unspoken.append(b[:48])
        if LITERAL.search(b) and '【chatGPT推奨】' not in label:
            missing_gpt += 1
    if engs:
        errors.append(f'看板が英語概念のまま {len(engs)}件（"beware of bears"等→画面の実文字「クマ出没注意」等を指定）')
    if unspoken:
        warns.append(f'文字要素だが実文字/no text未指定 {len(unspoken)}件（掲示/書類/新聞は描かせる文字を明記・出さないなら no text・実在物は実写）: 例「{unspoken[0]}...」')
    if missing_gpt:
        warns.append(f'実文字プロンプトなのに【chatGPT推奨】なし {missing_gpt}件（静止画/背景ラベル冒頭に付与）')

    # 13) Master.mdの各制作メモにASSET番号併記（Asset_Prompts.mdと突き合わせ用）
    memo_all = [l for l in lines if l.startswith('【制作メモ】')]
    numbered = [l for l in memo_all if l.startswith('【制作メモ】ASSET-')]
    if memo_all and len(numbered) != len(memo_all):
        warns.append(f'制作メモのASSET番号併記が不足 {len(memo_all)-len(numbered)}件（全メモに ASSET-NNN を付ける）')

    # ---- 出力 ----
    print('=' * 60)
    for s in info: print('  INFO :', s)
    for s in warns: print('  WARN ⚠:', s)
    for s in errors: print('  FAIL ❌:', s)
    print('=' * 60)
    if errors:
        print(f'❌ NG: {len(errors)}件のエラー / {len(warns)}件の警告 → 修正してから提示すること')
        return 1
    print(f'✅ 全チェックPASS（警告{len(warns)}件）。提示可能。')
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python3 validate_phase2_assets.py <Master.md> <台本.txt>'); sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
