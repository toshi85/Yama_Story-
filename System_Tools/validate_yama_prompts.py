#!/usr/bin/env python3
"""
Yama_Story プロンプト品質バリデーター
台本内のLovartプロンプト・制作メモの品質を自動チェックする。

使い方:
  python3 Yama_Story/System_Tools/validate_yama_prompts.py <台本ファイルパス>

チェック項目:
  1. ナレーター:プレフィックス — 全ナレーション行に「ナレーター:」があるか
  2. 禁止ワード（プロンプト内） — diagram/chart/text等の図解・テキスト系ワード
  3. Generate表現 — 「Generate 5 images.」(separateなし)の検出
  4. Character design reference sheet — 複数アングル事故の原因
  5. 地名チェック — 背景プロンプトに日本/北海道の地名があるか
  6. 安全ワード — blood/death/corpse等のNGワード
  7. カメラ専門用語 — パン/チルト/ドリー等の禁止用語
  8. CHAR参照タグ — 初出/再利用の区別があるか
  9. 複数キャラCHAR矛盾 — 複数キャラ/Generic groupなのに "only this one character" を使用していないか
  10. キャラプロンプト環境混入 — 1:1キャラプロンプトに環境・構図要素が含まれていないか
  11. キャラプロンプト全身 — Full body必須、bust shot等の部分構図禁止
  12. 1ナレ複数アセット — 1ナレーションに2+アセット紐づき検出
  13. 孤立アセット — ナレーション紐づきなしのアセット検出
  14. 静止画連続 — 3連続以上の検出
  15. 映像密度 — 全体平均35字/ASSET以下か
"""

import sys
import re
from pathlib import Path


def load_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()


def check_narrator_prefix(lines):
    """全ナレーション行に ナレーター: があるか"""
    issues = []
    in_code = False
    in_asset_section = False

    non_narr_prefixes = [
        '#', '```', '---', '>', '|', '【', '→', 'シーン:', 'キャラプロンプト',
        '背景プロンプト', 'Lovart', 'Google Flow', '[CHAR-', '[Generic',
        '[New', 'ASSET-', '座標:', 'カメラ:', '<!-- ', 'ナレーター:'
    ]

    for i, line in enumerate(lines):
        s = line.strip()
        if '<!-- PART:' in s:
            in_asset_section = True
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code or not in_asset_section or not s:
            continue
        if any(s.startswith(p) for p in non_narr_prefixes):
            continue

        if re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', s):
            issues.append((i + 1, s[:60]))

    return issues


def check_forbidden_words_in_prompts(lines):
    """Lovartプロンプト内の禁止ワード"""
    forbidden = [
        ('diagram', '図解表現'),
        ('infographic', '図解表現'),
        ('chart', '図解表現'),
        ('schematic', '図解表現'),
        ('blueprint', '図解表現'),
        ('timeline design', '図解表現'),
        ('trajectory lines', '図解表現'),
        ('Character design reference sheet', '複数アングル'),
    ]

    # text but not "no text" or "texture"
    text_pattern = re.compile(r'\btext\b', re.I)

    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for word, category in forbidden:
            if word.lower() in s.lower():
                issues.append((i + 1, category, word, s[:80]))

        if text_pattern.search(s) and 'no text' not in s.lower() and 'texture' not in s.lower():
            issues.append((i + 1, 'テキスト混入', 'text', s[:80]))

    return issues


def check_generate_wording(lines):
    """Generate 5 images. (separateなし) の検出"""
    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        if 'Generate 5 images.' in s and 'separate' not in s:
            issues.append((i + 1, s[:80]))

    return issues


def check_location_in_prompts(lines):
    """背景プロンプトに日本/北海道の地名があるか"""
    japan_kw = ['japan', 'japanese', 'hokkaido', 'fuppushi', 'chitose',
                'tomakomai', 'hachinohe', 'aomori', 'shikotsu', 'tarumae']

    issues = []
    in_code = False
    current_asset = None

    for i, line in enumerate(lines):
        s = line.strip()
        if '【制作メモ】' in s and 'ASSET-' in s:
            m = re.search(r'ASSET-\d+', s)
            current_asset = m.group() if m else '?'

        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code or len(s) < 30:
            continue
        if 'white background' in s.lower():
            continue
        # Skip cartoon character prompts without backgrounds
        if 'Cute cartoon character design' in s and '16:9' not in s:
            continue

        has_loc = any(kw in s.lower() for kw in japan_kw)
        if not has_loc:
            generic = ['forest', 'mountain', 'trail', 'road', 'hospital',
                       'office', 'river', 'snow', 'camp', 'bear', 'bamboo',
                       'village', 'town', 'field', 'newspaper', 'document']
            if any(g in s.lower() for g in generic):
                issues.append((i + 1, current_asset, s[:80]))

    return issues


def check_safety_words(lines):
    """安全ワード違反"""
    ng_words = ['blood', 'death', 'dead body', 'corpse', 'gore', 'dismember',
                'decapitat', 'mutilat', 'entrails', 'severed']

    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for word in ng_words:
            if word.lower() in s.lower():
                issues.append((i + 1, word, s[:80]))

    return issues


def check_camera_terms(lines):
    """カメラ専門用語（編集者指示内）"""
    forbidden_terms = {
        'パン': '左から右にゆっくり動かす',
        'チルト': '上から下にゆっくり動かす',
        'ドリー': 'カメラが前にゆっくり進む',
        'Ken Burns': 'ゆっくり近づきながら横に動かす',
        'チルトダウン': '上から下にゆっくり動かす',
        'ドリーイン': 'カメラが前にゆっくり進む',
    }

    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith('→'):
            continue
        for term, replacement in forbidden_terms.items():
            if term in s:
                issues.append((i + 1, term, replacement))

    return issues


def check_char_tags(lines):
    """CHAR参照タグの初出/再利用チェック"""
    pattern = re.compile(r'\[CHAR-\d+ reference\]')  # タグなし
    issues = []
    in_code = False
    in_asset_section = False

    for i, line in enumerate(lines):
        s = line.strip()
        if '## 1.' in s or 'ASSET-001' in s:
            in_asset_section = True
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code or not in_asset_section:
            continue

        matches = pattern.findall(s)
        if matches:
            issues.append((i + 1, matches, s[:80]))

    return issues


def check_char_multi_conflict(lines):
    """複数キャラCHARプロンプトに 'only this one character' が含まれていないか"""
    multi_char_indicators = re.compile(
        r'\bTwo\b|\bThree\b|\bFour\b|\bFive\b|'
        r'\bMultiple\b|\bseveral\b|\bgroup\b|'
        r'side by side|standing together|scattered|'
        r'\[Generic group\]|'
        r'\[CHAR-\d+.*\[CHAR-\d+',
        re.I
    )
    one_char_pattern = re.compile(r'only this one character', re.I)

    issues = []
    in_code = False
    code_block_start = 0
    code_lines = []

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            if not in_code:
                in_code = True
                code_block_start = i
                code_lines = []
            else:
                in_code = False
                block_text = ' '.join(code_lines)
                if multi_char_indicators.search(block_text) and one_char_pattern.search(block_text):
                    issues.append((
                        code_block_start + 1,
                        '複数キャラなのに "only this one character" を使用',
                        block_text[:100]
                    ))
                code_lines = []
            continue
        if in_code:
            code_lines.append(s)

    return issues


def check_char_single_use(lines):
    """CHAR-XX番号が1回しか使われていない（初出のみで再利用なし）ケースを警告"""
    char_pattern = re.compile(r'\[CHAR-(\d+)\s+reference')
    char_counts = {}  # {番号: [行番号リスト]}
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for m in char_pattern.finditer(s):
            num = m.group(1)
            if num not in char_counts:
                char_counts[num] = []
            char_counts[num].append(i + 1)

    issues = []
    for num, line_list in sorted(char_counts.items(), key=lambda x: int(x[0])):
        if len(line_list) == 1:
            issues.append((num, line_list[0]))

    return issues


def check_char_environment(lines):
    """キャラプロンプト(1:1)に環境・構図要素が混入していないか"""
    env_words = re.compile(
        r'\baerial view\b|\bbird.s eye\b|\boverhead\b|'
        r'\blandscape\b|\bmountain slope\b|\bforest floor\b|'
        r'\bstepping off train\b|\bstanding at.*summit\b|\bsitting in tent\b|'
        r'\bscattered far apart\b|\bscattered across\b|'
        r'\bin their own.*space\b|\bisolated in\b|'
        r'\bplatform\b|\bstation\b|\btrailhead\b|'
        r'\binterior\b|\broom\b|\bcorridor\b',
        re.I
    )

    issues = []
    in_code = False
    is_char_prompt = False

    for i, line in enumerate(lines):
        s = line.strip()

        # Detect character prompt section (1:1)
        if 'キャラプロンプト' in s and '1:1' in s:
            is_char_prompt = True
            continue
        if '背景プロンプト' in s or ('【制作メモ】' in s and 'ASSET-' in s):
            is_char_prompt = False

        if s.startswith('```'):
            in_code = not in_code
            if not in_code:
                is_char_prompt = False
            continue

        if not in_code or not is_char_prompt:
            continue

        # Skip CHAR reference section (section 0)
        if 'white background' in s.lower() and 'Single character' in s:
            continue

        matches = env_words.findall(s)
        if matches:
            issues.append((i + 1, matches, s[:100]))

    return issues


def check_char_fullbody(lines):
    """キャラプロンプト(1:1)が全身(Full body)であるかチェック"""
    prohibited = re.compile(
        r'\bbust shot\b|\bupper body shot\b|\bclose-up\b|\bhalf body\b|'
        r'\bwaist up\b|\bchest up\b|\bhands only\b|\bface close\b|'
        r'\bhead shot\b|\bpaw close\b|\bside profile bust\b',
        re.I
    )
    fullbody_pattern = re.compile(r'\bFull body\b', re.I)

    issues = []
    in_code = False
    is_char_prompt = False
    current_asset = None

    for i, line in enumerate(lines):
        s = line.strip()

        if '【制作メモ】' in s and 'ASSET-' in s:
            m = re.search(r'ASSET-\d+', s)
            current_asset = m.group() if m else '?'

        if 'キャラプロンプト' in s and '1:1' in s:
            is_char_prompt = True
            continue
        if '背景プロンプト' in s or ('【制作メモ】' in s and 'ASSET-' in s):
            is_char_prompt = False

        if s.startswith('```'):
            if in_code and is_char_prompt:
                # End of char prompt code block — no further action
                pass
            in_code = not in_code
            if not in_code:
                is_char_prompt = False
            continue

        if not in_code or not is_char_prompt:
            continue

        # Check for prohibited partial composition terms
        found = prohibited.findall(s)
        if found:
            issues.append((i + 1, current_asset, 'prohibited', found, s[:100]))

        # Check for missing "Full body"
        if '[CHAR-' in s or '[Generic' in s or '[New' in s:
            if not fullbody_pattern.search(s):
                issues.append((i + 1, current_asset, 'missing_fullbody', [], s[:100]))

    return issues


def check_static_consecutive(lines):
    """静止画3連続以上の検出"""
    static_cats = ['Lovart静止画]', 'Lovart静止画 + 編集者]']
    consecutive = 0
    max_cons = 0
    runs = []
    current_run = []

    for i, line in enumerate(lines):
        s = line.strip()
        if '【制作メモ】' in s and 'ASSET-' in s:
            is_static = any(c in s for c in static_cats)
            if is_static:
                consecutive += 1
                current_run.append((i + 1, s[:60]))
            else:
                if consecutive >= 3:
                    runs.append(current_run[:])
                consecutive = 0
                current_run = []
            max_cons = max(max_cons, consecutive)

    if consecutive >= 3:
        runs.append(current_run[:])

    return max_cons, runs


def check_density(lines):
    """映像密度チェック"""
    in_code = False
    current_section = None
    total_chars = 0
    total_assets = 0

    memo_prefixes = ['【制作メモ】', 'シーン:', 'キャラプロンプト', '背景プロンプト',
                     'Lovart静止画プロンプト', 'Google Flow動画プロンプト', '→',
                     '座標:', 'カメラ:', '[CHAR-', '[Generic', 'ASSET-']

    for line in lines:
        s = line.strip()
        if '<!-- PART: KI -->' in s: current_section = 'KI'
        elif '<!-- PART: SHO -->' in s: current_section = 'SHO'
        elif '<!-- PART: TEN-KETSU -->' in s: current_section = 'TEN-KETSU'

        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code or not current_section:
            continue

        if '【制作メモ】' in s and 'ASSET-' in s:
            total_assets += 1
            continue

        if not s or s.startswith('#') or s.startswith('---') or s.startswith('>') or s.startswith('|'):
            continue
        if any(s.startswith(p) for p in memo_prefixes):
            continue

        if re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', s):
            total_chars += len(s)

    avg = total_chars / total_assets if total_assets > 0 else 0
    return total_chars, total_assets, avg


def check_narrator_consecutive(lines):
    """ナレーター行が2行以上連続している箇所を検出"""
    issues = []
    in_code = False
    prev_is_narrator = False
    prev_line_num = 0
    prev_text = ''

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            prev_is_narrator = False
            continue
        if in_code or not s:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        if is_narrator and prev_is_narrator:
            issues.append((prev_line_num, prev_text[:60], i + 1, s[:60]))
        prev_is_narrator = is_narrator
        if is_narrator:
            prev_line_num = i + 1
            prev_text = s

    return issues


def check_multi_asset_per_narration(lines):
    """1つのナレーションに複数アセットが紐づいている箇所を検出"""
    issues = []
    in_code = False
    last_narrator_line = 0
    last_narrator_text = ''
    asset_count_since_narrator = 0
    assets_since_narrator = []

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        is_asset = '【制作メモ】' in s and 'ASSET-' in s

        if is_narrator:
            # 前のナレーターに複数アセットが紐づいていたら報告
            if last_narrator_line > 0 and asset_count_since_narrator >= 2:
                issues.append((
                    last_narrator_line,
                    last_narrator_text[:60],
                    asset_count_since_narrator,
                    [a for a in assets_since_narrator]
                ))
            last_narrator_line = i + 1
            last_narrator_text = s
            asset_count_since_narrator = 0
            assets_since_narrator = []

        if is_asset:
            asset_count_since_narrator += 1
            m = re.search(r'ASSET-\d+', s)
            assets_since_narrator.append(m.group() if m else '?')

    # 最後のナレーターもチェック
    if last_narrator_line > 0 and asset_count_since_narrator >= 2:
        issues.append((
            last_narrator_line,
            last_narrator_text[:60],
            asset_count_since_narrator,
            [a for a in assets_since_narrator]
        ))

    return issues


def check_orphan_assets(lines):
    """ナレーションが紐づかない孤立アセットを検出（直前にナレーター行がないアセット）"""
    issues = []
    in_code = False
    found_narrator_before_asset = False
    in_asset_section = False

    for i, line in enumerate(lines):
        s = line.strip()
        if '<!-- PART:' in s:
            in_asset_section = True
        if not in_asset_section:
            continue

        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        is_asset = '【制作メモ】' in s and 'ASSET-' in s

        if is_narrator:
            found_narrator_before_asset = True

        if is_asset:
            if not found_narrator_before_asset:
                m = re.search(r'ASSET-\d+', s)
                asset_id = m.group() if m else '?'
                issues.append((i + 1, asset_id, s[:80]))
            found_narrator_before_asset = False

    return issues


def check_static_narration_length(lines):
    """静止画アセットに紐づくナレーション文字数が25文字を超えている箇所を検出"""
    static_cats = ['Lovart静止画]', 'Lovart静止画 + 編集者]']
    issues = []
    in_code = False

    # ナレーション行を蓄積し、制作メモが来たら紐付ける
    narration_buffer = []  # [(line_num, text, char_count)]

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        # ナレーター行を検出
        if s.startswith('ナレーター:') or s.startswith('ナレーター：'):
            narr_text = s.split(':', 1)[1].strip() if ':' in s else s.split('：', 1)[1].strip()
            narration_buffer.append((i + 1, narr_text, len(narr_text)))
            continue

        # 制作メモ行を検出
        if '【制作メモ】' in s and 'ASSET-' in s:
            is_static = any(c in s for c in static_cats)
            if is_static and narration_buffer:
                # 直前のナレーションを紐付け
                last_narr = narration_buffer[-1]
                if last_narr[2] > 25:
                    asset_match = re.search(r'ASSET-\d+', s)
                    asset_id = asset_match.group() if asset_match else '?'
                    issues.append((
                        last_narr[0],
                        last_narr[2],
                        asset_id,
                        i + 1,
                        last_narr[1][:50]
                    ))
            narration_buffer = []
            continue

        # 制作メモ関連行はスキップ（バッファはクリアしない）
        if s.startswith('シーン:') or s.startswith('キャラプロンプト') or s.startswith('背景プロンプト'):
            continue
        if s.startswith('→') or s.startswith('座標:') or s.startswith('カメラ:'):
            continue
        if s.startswith('【') or s.startswith('#'):
            continue

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_prompts.py <台本ファイルパス>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    lines = load_file(filepath)

    all_pass = True
    warnings = 0

    print("=" * 60)
    print(f"Yama プロンプト品質バリデーション: {Path(filepath).name}")
    print("=" * 60)

    # 1. ナレーター:プレフィックス
    issues = check_narrator_prefix(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: ナレーター:プレフィックス欠落 ({len(issues)}件)")
        for ln, text in issues[:5]:
            print(f"   L{ln}: {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("\n✅ PASS: ナレーター:プレフィックス")

    # 2. 禁止ワード
    issues = check_forbidden_words_in_prompts(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: プロンプト内禁止ワード ({len(issues)}件)")
        for ln, cat, word, text in issues[:5]:
            print(f"   L{ln}: [{cat}] '{word}' — {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: プロンプト内禁止ワード")

    # 3. Generate表現
    issues = check_generate_wording(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 'Generate 5 images.' separateなし ({len(issues)}件)")
        for ln, text in issues[:3]:
            print(f"   L{ln}: {text}")
    else:
        print("✅ PASS: Generate表現")

    # 4. 地名チェック
    issues = check_location_in_prompts(lines)
    if issues:
        warnings += len(issues)
        print(f"\n⚠️  WARNING: 地名なし背景プロンプト ({len(issues)}件)")
        for ln, asset, text in issues[:5]:
            print(f"   L{ln} ({asset}): {text}")
    else:
        print("✅ PASS: 地名チェック")

    # 5. 安全ワード
    issues = check_safety_words(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 安全ワード違反 ({len(issues)}件)")
        for ln, word, text in issues:
            print(f"   L{ln}: '{word}' — {text}")
    else:
        print("✅ PASS: 安全ワード")

    # 6. カメラ専門用語
    issues = check_camera_terms(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: カメラ専門用語 ({len(issues)}件)")
        for ln, term, repl in issues:
            print(f"   L{ln}: '{term}' → '{repl}'")
    else:
        print("✅ PASS: カメラ専門用語")

    # 7. CHAR参照タグ
    issues = check_char_tags(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: CHAR参照タグ 初出/再利用なし ({len(issues)}件)")
        for ln, matches, text in issues[:5]:
            print(f"   L{ln}: {matches}")
    else:
        print("✅ PASS: CHAR参照タグ")

    # 8. 複数キャラCHAR矛盾チェック
    issues = check_char_multi_conflict(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 複数キャラCHARに 'only this one character' ({len(issues)}件)")
        for ln, msg, text in issues:
            print(f"   L{ln}: {msg}")
            print(f"         {text}")
    else:
        print("✅ PASS: 複数キャラCHAR整合性")

    # 9. CHAR番号1回使用（名前なし人物の可能性）
    issues = check_char_single_use(lines)
    if issues:
        warnings += len(issues)
        print(f"\n⚠️  WARNING: CHAR番号が1回しか使われていない ({len(issues)}件)")
        print(f"   名前のない人物にCHAR番号を振っていませんか？名前なし人物は [Generic group] を使用してください")
        for num, ln in issues[:5]:
            print(f"   CHAR-{num}: L{ln}のみ（再利用なし）")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: CHAR番号再利用")

    # 10. キャラプロンプト環境混入
    issues = check_char_environment(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: キャラプロンプト(1:1)に環境・構図要素 ({len(issues)}件)")
        for ln, matches, text in issues[:5]:
            print(f"   L{ln}: {matches}")
            print(f"         {text}")
    else:
        print("✅ PASS: キャラプロンプト環境要素")

    # 11. キャラプロンプト全身チェック
    issues = check_char_fullbody(lines)
    if issues:
        all_pass = False
        prohibited_count = sum(1 for x in issues if x[2] == 'prohibited')
        missing_count = sum(1 for x in issues if x[2] == 'missing_fullbody')
        print(f"\n❌ FAIL: キャラプロンプト全身ルール違反 ({len(issues)}件: 禁止語{prohibited_count}, Full body欠落{missing_count})")
        for ln, asset, kind, found, text in issues[:5]:
            if kind == 'prohibited':
                print(f"   L{ln} ({asset}): 禁止語 {found}")
            else:
                print(f"   L{ln} ({asset}): 'Full body' が含まれていません")
            print(f"         {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: キャラプロンプト全身ルール")

    # 12. 1ナレーション複数アセット
    issues = check_multi_asset_per_narration(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 1ナレーションに複数アセット紐づき ({len(issues)}件)")
        for ln, text, count, assets in issues[:5]:
            print(f"   L{ln}: {text}")
            print(f"   → {count}アセット紐づき: {', '.join(assets)}")
            print(f"   → ナレーションを分割して各アセットに1文ずつ対応させる")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 1ナレーション=1アセット")

    # 13. 孤立アセット（ナレーションなし）
    issues = check_orphan_assets(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 孤立アセット（ナレーション紐づきなし） ({len(issues)}件)")
        for ln, asset_id, text in issues[:5]:
            print(f"   L{ln}: {asset_id} — 直前にナレーター行がありません")
            print(f"   → ナレーションを追加して紐づけるか、アセットを削除する")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 孤立アセットなし")

    # 14. ナレーター行連続チェック
    issues = check_narrator_consecutive(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: ナレーター行2行以上連続 ({len(issues)}件)")
        for ln1, text1, ln2, text2 in issues[:5]:
            print(f"   L{ln1}: {text1}")
            print(f"   L{ln2}: {text2}")
            print(f"   → 各行の間に制作メモ+プロンプトを挿入して交互配置にする")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: ナレーター行交互配置")

    # 12. 静止画ナレーション文字数チェック
    issues = check_static_narration_length(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 静止画アセットのナレーション25文字超過 ({len(issues)}件)")
        for narr_ln, char_count, asset_id, asset_ln, text in issues[:5]:
            print(f"   L{narr_ln}: {char_count}字 → {asset_id} (L{asset_ln}) [静止画]")
            print(f"   ナレーション: {text}")
            print(f"   → キャラアニメーション or 動画に変更し制作メモも書き直す")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 静止画ナレーション文字数")

    # 13. 静止画連続
    max_cons, runs = check_static_consecutive(lines)
    if max_cons >= 3:
        all_pass = False
        print(f"\n❌ FAIL: 静止画{max_cons}連続 ({len(runs)}箇所)")
        for run in runs[:3]:
            print(f"   {run[0][1][:50]}... ({len(run)}連続)")
    else:
        print(f"✅ PASS: 静止画連続 (最大{max_cons})")

    # 14. 映像密度
    total_chars, total_assets, avg = check_density(lines)
    if avg > 50:
        all_pass = False
        print(f"\n❌ FAIL: 映像密度 {avg:.1f}字/ASSET (上限50)")
    elif avg > 35:
        warnings += 1
        print(f"\n⚠️  WARNING: 映像密度 {avg:.1f}字/ASSET (推奨35以下)")
    else:
        print(f"✅ PASS: 映像密度 {avg:.1f}字/ASSET ({total_chars}字/{total_assets}ASSET)")

    # Summary
    print("\n" + "=" * 60)
    if all_pass and warnings == 0:
        print("結果: ✅ ALL PASS")
        sys.exit(0)
    elif all_pass:
        print(f"結果: ⚠️  PASS (WARNING {warnings}件)")
        sys.exit(0)
    else:
        print("結果: ❌ FAIL — 修正が必要です")
        sys.exit(1)


if __name__ == '__main__':
    main()
