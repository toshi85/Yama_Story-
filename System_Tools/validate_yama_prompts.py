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
  9. 静止画連続 — 3連続以上の検出
  10. 映像密度 — 全体平均35字/ASSET以下か
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

    # 8. 静止画連続
    max_cons, runs = check_static_consecutive(lines)
    if max_cons >= 3:
        all_pass = False
        print(f"\n❌ FAIL: 静止画{max_cons}連続 ({len(runs)}箇所)")
        for run in runs[:3]:
            print(f"   {run[0][1][:50]}... ({len(run)}連続)")
    else:
        print(f"✅ PASS: 静止画連続 (最大{max_cons})")

    # 9. 映像密度
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
