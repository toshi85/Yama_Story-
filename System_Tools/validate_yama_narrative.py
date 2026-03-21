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
    narrator_lines = []  # (line_number, content) for math check

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
        narrator_lines.append((i + 1, content))

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

    # Gate 5: Math consistency check (YCP-025 related)
    # Detect lines with numbers and frequency expressions, check if math adds up
    NUM_PATTERN = re.compile(r'(\d+(?:,\d+)*(?:\.\d+)?)')
    FREQ_PATTERNS = [
        (re.compile(r'(\d+)日に(\d+)回'), 'day_freq'),
        (re.compile(r'(\d+)週間?に(\d+)回'), 'week_freq'),
        (re.compile(r'(\d+)ヶ月?に(\d+)回'), 'month_freq'),
    ]
    CALC_KEYWORDS = re.compile(r'計算|ペース|つまり|換算|割る|÷')

    # Scan for number pairs within a 5-line window
    for idx, (line_num, content) in enumerate(narrator_lines):
        # Look for frequency claims with "計算" or "ペース" nearby
        if not CALC_KEYWORDS.search(content):
            continue

        # Gather numbers from this line and nearby lines (window of 5)
        window_start = max(0, idx - 4)
        window_end = min(len(narrator_lines), idx + 1)
        window_numbers = []
        for w_idx in range(window_start, window_end):
            w_line_num, w_content = narrator_lines[w_idx]
            nums = NUM_PATTERN.findall(w_content)
            for n in nums:
                try:
                    val = float(n.replace(',', ''))
                    if val > 0:
                        window_numbers.append((w_line_num, val, w_content))
                except ValueError:
                    pass

        # Check frequency claims: "X日に1回のペース" with total count N and period D
        for freq_pat, freq_type in FREQ_PATTERNS:
            match = freq_pat.search(content)
            if match:
                claimed_interval = float(match.group(1))
                # Look for a total count in the window
                for w_line_num, val, w_content in window_numbers:
                    if val >= 10 and w_line_num != line_num:
                        # val is likely total count, estimate period
                        # For "X日に1回" with count N: expected interval = period / N
                        # Flag if claimed interval differs significantly from any reasonable period/count
                        # Common periods: 30 days (1 month), 90 days (3 months), 120 days (4 months), 240 days (8 months), 365 days (1 year)
                        for period_days, period_name in [(30, "1ヶ月"), (90, "3ヶ月"), (120, "4ヶ月"), (150, "5ヶ月"), (240, "8ヶ月"), (365, "1年")]:
                            actual_interval = period_days / val
                            if abs(actual_interval - claimed_interval) < 1.0:
                                break  # Math checks out for this period
                        else:
                            # No reasonable period makes the math work
                            warnings.append(
                                f"[Math Check] Line {line_num}: 「{claimed_interval:.0f}日に1回」の計算を確認してください\n"
                                f"   近くの数値: {val:.0f}（Line {w_line_num}）\n"
                                f"   → 期間が不明確、または換算が合わない可能性があります\n"
                                f"   > \"{content[:70]}...\""
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
        print("  ✅ Math consistency: OK")
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
