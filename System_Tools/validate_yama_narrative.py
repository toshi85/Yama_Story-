import sys
import re

def validate_narrative_tone(file_path):
    """
    Validates Yama_Story narrator lines for:
    1. Show Don't Tell (banned preachy phrases)
    2. Dash (──) prohibition
    3. Written-language expressions (以下の通り, etc.)
    4. Literary/jargon expressions
    """

    # Gate 1: Banned preachy phrases (Show Don't Tell)
    BANNED_PHRASES = [
        "学ぶべき",
        "教訓",
        "社会の闇",
        "警鐘",
        "私たち",
        "現代社会",
        "考えるべき",
        "知るべき",
    ]

    # Gate 2: Dash prohibition
    DASH_PATTERN = re.compile(r'──|—―|━━')

    # Gate 3: Written-language expressions (not suitable for audio narration)
    WRITTEN_LANG_PHRASES = [
        "以下の通り",
        "上記の",
        "前述の",
        "後述の",
        "下記の",
        "以下に示す",
    ]

    # Gate 4: Literary/jargon expressions to flag as warnings
    LITERARY_PHRASES = [
        ("机上の空論", "→ 「通用しない」等に言い換え"),
        ("火を噴いた", "→ 「発砲」等に言い換え"),
        ("紛糾", "→ 「白熱」等に言い換え"),
        ("登攀", "→ 「登る」「作業」等に言い換え"),
        ("取り付いた", "→ 一般的な表現に言い換え"),
        ("取り付く", "→ 一般的な表現に言い換え"),
        ("取りついた", "→ 一般的な表現に言い換え"),
    ]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp932') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error opening file: {e}")
            sys.exit(1)

    errors = []
    warnings = []
    dash_count = 0

    print("=" * 60)
    print(f"[Yama Narrative Validator] {file_path}")
    print("=" * 60)

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Skip headers and empty lines
        if line_stripped.startswith("#") or line_stripped.startswith("<!--") or not line_stripped:
            continue

        # Only check Narrator lines
        if not line_stripped.startswith("ナレーター:"):
            continue

        content = line_stripped.replace("ナレーター:", "").strip()

        # Gate 1: Show Don't Tell
        for phrase in BANNED_PHRASES:
            if phrase in content:
                errors.append(
                    f"[Show Don't Tell] Line {i+1}: '{phrase}'\n"
                    f"   > \"{content[:60]}...\""
                )

        # Gate 2: Dash prohibition
        if DASH_PATTERN.search(content):
            dash_count += 1
            errors.append(
                f"[Dash Prohibited] Line {i+1}: ダッシュ（──）を検出\n"
                f"   > \"{content[:60]}...\"\n"
                f"   → 句読点と文構造で間を表現してください"
            )

        # Gate 3: Written-language
        for phrase in WRITTEN_LANG_PHRASES:
            if phrase in content:
                errors.append(
                    f"[Written Language] Line {i+1}: '{phrase}' は書き言葉\n"
                    f"   > \"{content[:60]}...\"\n"
                    f"   → 音声ナレーションでは不適切。削除または言い換え"
                )

        # Gate 4: Literary/jargon (warnings)
        for phrase, suggestion in LITERARY_PHRASES:
            if phrase in content:
                warnings.append(
                    f"[Literary/Jargon] Line {i+1}: '{phrase}' {suggestion}\n"
                    f"   > \"{content[:60]}...\""
                )

    # Output results
    print()

    if errors:
        print(f"[FAIL] {len(errors)} error(s) found.")
        print("-" * 40)
        for err in errors:
            print(f"  ❌ {err}")
            print()

    if warnings:
        print(f"[WARN] {len(warnings)} warning(s) found.")
        print("-" * 40)
        for warn in warnings:
            print(f"  ⚠️  {warn}")
            print()

    if not errors and not warnings:
        print("[PASS] All narrative checks passed.")
        print("  ✅ Show Don't Tell: OK")
        print("  ✅ Dash prohibition: OK")
        print("  ✅ Written language: OK")
        print("  ✅ Literary/jargon: OK")
    elif not errors:
        print("[PASS with warnings] No errors, but warnings should be reviewed.")

    print()
    print("=" * 60)

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_yama_narrative.py <script_file>")
        sys.exit(1)

    validate_narrative_tone(sys.argv[1])
