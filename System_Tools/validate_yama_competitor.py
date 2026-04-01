import sys
import os
import re

"""
Gate 0: Competitor & Thumbnail Analysis Check
==============================================
台本に「競合との差別化要因レポート」と「サムネイル競合分析」が含まれていなければFAIL。
マスタープロンプトの「競合・完全包囲リサーチ（Competitor Crush）」を機械的に強制する。

Usage:
    python3 validate_yama_competitor.py <台本ファイルパス>

チェック項目:
    1. 競合分析セクションの存在
    2. 競合動画が最低1本記載されているか
    3. 差別化要因が3軸（映像・リサーチ・ナラティブ）記載されているか
    4. 情報の穴が3つ以上特定されているか
    5. サムネイル競合分析セクションの存在
    6. 競合サムネのテキスト・構図パターン分析が記載されているか
"""

# 必須セクションの検出パターン
COMPETITOR_SECTION_PATTERNS = [
    r'##\s*競合.*(?:差別化|分析|レポート|リサーチ|包囲)',
    r'##\s*Competitor',
    r'##\s*競合との差別化',
    r'##\s*競合分析',
    r'##\s*競合調査',
]

THUMBNAIL_SECTION_PATTERNS = [
    r'##\s*サムネ.*(?:競合|分析|比較)',
    r'##\s*サムネイル.*(?:競合|分析|比較)',
    r'##\s*Thumbnail.*(?:Competitor|Analysis)',
    r'##\s*競合サムネ',
]

# 差別化3軸のキーワード
DIFF_AXES = {
    "映像": [r'映像[面:]', r'ビジュアル[面:]', r'映像差別化'],
    "リサーチ": [r'リサーチ[面:]', r'情報[面:]', r'一次情報', r'リサーチ差別化'],
    "ナラティブ": [r'ナラティブ[面:]', r'構成[面:]', r'切り口', r'ナラティブ差別化'],
}

# サムネ分析の必須要素
THUMBNAIL_ELEMENTS = {
    "テキスト": [r'テキスト', r'コピー', r'キャッチ', r'文字'],
    "構図": [r'構図', r'レイアウト', r'配置', r'人物'],
    "色調": [r'色[調味]', r'配色', r'カラー', r'トーン'],
}


def validate_competitor(file_path):
    print(f"\n{'='*60}")
    print(f"[Gate 0] Competitor & Thumbnail Analysis Check")
    print(f"  File: {os.path.basename(file_path)}")
    print(f"{'='*60}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    errors = []
    warnings = []

    # ===== CHECK 1: 競合分析セクションの存在 =====
    print("\n[Check 1] 競合分析セクションの存在...")
    has_competitor_section = False
    for pattern in COMPETITOR_SECTION_PATTERNS:
        if re.search(pattern, content):
            has_competitor_section = True
            break

    if not has_competitor_section:
        errors.append(
            "[BLOCKADE] 競合分析セクションが見つかりません。\n"
            "   台本に以下のいずれかのセクションを追加してください:\n"
            "   ## 競合との差別化要因レポート\n"
            "   ## 競合分析\n"
            "   マスタープロンプト §2-A「競合・完全包囲リサーチ」参照"
        )
        print("   ❌ MISSING")
    else:
        print("   ✅ Found")

    # ===== CHECK 2: 競合動画の記載（Top 3） =====
    print("\n[Check 2] 競合動画の記載...")
    # 再生数パターン（例: 84万再生、100万回、1.2M views）
    view_patterns = [
        r'\d+[万億]?\s*(?:再生|回|views)',
        r'\d+\.?\d*[MmKk]\s*(?:views|再生)',
    ]
    view_count = 0
    for vp in view_patterns:
        view_count += len(re.findall(vp, content))

    if view_count == 0:
        errors.append(
            "[BLOCKADE] 競合動画の再生数が記載されていません。\n"
            "   同テーマの既存人気動画Top 3の再生数を記載してください。\n"
            "   例: 「生きて山から帰るには」84万再生"
        )
        print("   ❌ NO competitor videos found")
    elif view_count < 3:
        warnings.append(
            f"[WARNING] 競合動画が{view_count}本のみ。Top 3の分析を推奨。"
        )
        print(f"   ⚠️ Only {view_count} competitor(s) found (recommend 3+)")
    else:
        print(f"   ✅ {view_count} competitor references found")

    # ===== CHECK 3: 差別化3軸 =====
    print("\n[Check 3] 差別化3軸（映像・リサーチ・ナラティブ）...")
    missing_axes = []
    for axis_name, patterns in DIFF_AXES.items():
        found = False
        for p in patterns:
            if re.search(p, content):
                found = True
                break
        if not found:
            missing_axes.append(axis_name)

    if missing_axes:
        errors.append(
            f"[BLOCKADE] 差別化軸が不足: {', '.join(missing_axes)}\n"
            "   映像面・リサーチ面・ナラティブ面の3軸で差別化要因を記載してください。"
        )
        print(f"   ❌ Missing axes: {', '.join(missing_axes)}")
    else:
        print("   ✅ All 3 axes covered")

    # ===== CHECK 4: 情報の穴（3つ以上） =====
    print("\n[Check 4] 情報の穴の特定...")
    hole_patterns = [
        r'穴\s*[\d①②③④⑤]',
        r'[\d①②③④⑤][.．:：]\s*.+(?:していない|ていない|ない|未|欠落|不足|触れて)',
        r'(?:判決文|地形図|手記|日記|報告書|証言|一次情報).*(?:読んでいない|出していない|引用していない|使っていない|触れていない|未)',
    ]
    hole_count = 0
    for hp in hole_patterns:
        hole_count += len(re.findall(hp, content))

    if hole_count < 3:
        warnings.append(
            f"[WARNING] 情報の穴が{hole_count}個のみ検出。3つ以上の特定を推奨。\n"
            "   例: 「判決文を読んでいない」「地形図を出していない」「手記を引用していない」"
        )
        print(f"   ⚠️ Only {hole_count} hole(s) detected (recommend 3+)")
    else:
        print(f"   ✅ {hole_count} holes identified")

    # ===== CHECK 5: サムネイル競合分析セクション =====
    print("\n[Check 5] サムネイル競合分析セクションの存在...")
    has_thumbnail_section = False
    for pattern in THUMBNAIL_SECTION_PATTERNS:
        if re.search(pattern, content):
            has_thumbnail_section = True
            break

    if not has_thumbnail_section:
        errors.append(
            "[BLOCKADE] サムネイル競合分析セクションが見つかりません。\n"
            "   台本に以下のセクションを追加してください:\n"
            "   ## サムネイル競合分析\n"
            "   競合Top 3のサムネのテキスト・構図・色調パターンを分析し、\n"
            "   差別化ポイントを明記してください。"
        )
        print("   ❌ MISSING")
    else:
        print("   ✅ Found")

    # ===== CHECK 6: サムネ分析の必須要素 =====
    print("\n[Check 6] サムネ分析の要素（テキスト・構図・色調）...")
    missing_thumb_elements = []
    for elem_name, patterns in THUMBNAIL_ELEMENTS.items():
        found = False
        for p in patterns:
            if re.search(p, content):
                found = True
                break
        if not found:
            missing_thumb_elements.append(elem_name)

    if has_thumbnail_section and missing_thumb_elements:
        warnings.append(
            f"[WARNING] サムネ分析に不足要素: {', '.join(missing_thumb_elements)}\n"
            "   テキスト・構図・色調の3要素で競合サムネを分析してください。"
        )
        print(f"   ⚠️ Missing elements: {', '.join(missing_thumb_elements)}")
    elif has_thumbnail_section:
        print("   ✅ All elements covered")
    else:
        print("   ⏭️ Skipped (no thumbnail section)")

    # ===== RESULT =====
    print(f"\n{'='*60}")
    if errors:
        print(f"[FAILED] Gate 0: {len(errors)} BLOCKADE(s), {len(warnings)} warning(s)")
        print(f"{'='*60}")
        for e in errors:
            print(f"\n{e}")
        for w in warnings:
            print(f"\n{w}")
        print("\n台本に競合分析・サムネ分析を追加してから再実行してください。")
        sys.exit(1)
    else:
        if warnings:
            print(f"[PASSED with warnings] Gate 0: {len(warnings)} warning(s)")
            for w in warnings:
                print(f"\n{w}")
        else:
            print("[PASSED] Gate 0: Competitor & Thumbnail Analysis Check OK")
        print(f"{'='*60}")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_competitor.py <file_path>")
        sys.exit(1)
    validate_competitor(sys.argv[1])
