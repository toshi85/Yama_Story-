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

    # Gate 6: メタ語り禁止（YCP-020 ③「メタ語り全削除」）2026-09-01 追加
    # ナレーターが「これから何をするか」を段取りとして説明する文は全削除し、直接内容に入る。
    # 実例（戸沢村・2026-09-01 に12件検出）:
    #   「ここで一度、山形県が残している資料を開きます。」「見つかった場所を、地図で見てみます。」
    #   「ここで、まったく別の形の事故を一つ挟みます。」「ここからは、持ち帰ってほしい数字です。」
    META_NARRATION = [
        (r'^(ここで|ここから|ここからは)[、。]', "「ここで」「ここから」で始まる段取り説明"),
        (r'(見てみます|見ていきます|見ておきます|開きます|並べます|挟みます|整理します)。$', "これから何をするかの予告"),
        (r'(紹介します|説明します|お伝えします|触れておきます|押さえておきます)。$', "これから何を語るかの予告"),
        (r'^(最後に|次に|まず最初に)[、].*(します|しましょう)。$', "セクションの段取り説明"),
        (r'(詳しく見て|順に見て|後ほど|のちほど|次のセクション|この章では|本編では)', "ナレーター視点のメタ発言"),
        (r'^これは、?あとで', "あとで意味を持つ、という予告"),
    ]

    # Gate 7: 孤立した固有名詞の警告（2026-09-01 追加）
    # 台本に1回しか出てこない地名・組織名は「出しただけで使っていない」候補。
    # 実例: 戸沢村§2の「最上川」は以降一度も出てこず、村紹介で終わっていた。
    # ※ 比較事例・列挙（笹神村・岩泉町など）は正当なので WARNING 止まりにする。
    PROPER_NOUN = re.compile(r'[一-龥ヶヵ]{2,6}(?:川|山|岳|湖|沼|峠|市|町|村|区|大学|学院|病院|署|センター|新聞|研究所|林業|役場)')

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

        # Gate 6: メタ語り禁止（YCP-020）
        # ⚠️ 証言の導入（「〜さんは、こう振り返ります。」等）は除外する。
        #    2026-09-01 の較正で、大千軒岳の4件が全て証言導入だったため。
        is_quote_intro = re.search(r'(こう|このように|次のように)(語|話|振り返|説明|証言|記し|書い)', content) \
                         or re.search(r'(さん|氏|教授|さんたち)(は|も)、?こう', content)
        for pat, why in (META_NARRATION if not is_quote_intro else []):
            if re.search(pat, content):
                errors.append(
                    f"[メタ語り禁止 YCP-020] Line {i+1}: {why}\n"
                    f"   > \"{content[:60]}\"\n"
                    f"   → 削除して直接内容に入る。出典を示したいなら文の後ろへ回す"
                )
                break

        # Gate 4: Literary/jargon (warnings)
        for phrase, suggestion in LITERARY_PHRASES:
            if phrase in content:
                warnings.append(
                    f"[Literary/Jargon] Line {i+1}: '{phrase}' {suggestion}\n"
                    f"   > \"{content[:60]}...\""
                )

    # Gate 8: 引用の作法（2026-09-01 追加）
    # 出荷済みの型（羅臼岳・大千軒岳）: 導入文で「誰が・どこで」を示し、次の行に「引用」を置く。
    #   例) 「西山修次さんは、HTB北海道ニュースの取材にこう語っています。」→「とんでもないクマだと〜」
    #       「知床財団の調査速報に」→「人を避けない〜」→「と記録されています。」
    # 2026-09-01 の事故: 佐藤さんの証言を「」なしで9行にばらし、ナレーターが「俺」と言う形になっていた。
    INTRO_PAT = re.compile(r'(こう(語|話|振り返|述べ|記|書|発表|コメント|説明|証言)|によると|によれば|"?と(記録|記載)されて|の(取材|調査|報告)に|こう(記して|書いて))')
    COLLOQUIAL = re.compile(r'(^|[^」])(俺|僕|わたし)[、。はがもの]|(よな|だよ|ですよ|ないね|かな|だろうな)。\s*$')
    prev_two = []
    for idx, (ln, content) in enumerate(narrator_lines):
        # 8a. 引用行に、直前2行以内の導入があるか
        if content.startswith("「") and content.rstrip().endswith("」"):
            ctx = [c for _, c in narrator_lines[max(0, idx - 2):idx]]
            prev_quote = bool(ctx) and ctx[-1].startswith("「")
            if not prev_quote and not any(INTRO_PAT.search(c) for c in ctx):
                warnings.append(
                    f"[引用に導入がない] Line {ln}: 誰の・どこでの発言か直前に示されていません\n"
                    f"   > \"{content[:44]}\"\n"
                    f"   → 「◯◯さんは、△△の取材にこう話しています。」を直前に置く（羅臼岳・大千軒岳の型）"
                )
        # 8c. 帰属だけの単独行を後ろに置かない（2026-09-01）
        #  出荷済み3本（羅臼岳・朱鞠内湖・大千軒岳）に「そう書いています。」単独行は0件。
        #  唯一の後置は羅臼岳の「と記録されています。」で、直前が必ず「」引用だった。
        # 「こう〜います。」は前置（これから引用を導く）＝正しい。「そう〜います。」だけが後置。
        # 後置と、「と語っています。」型の閉じは、直前が「」引用でなければ誤り。
        is_trailing = bool(re.fullmatch(
            r'([^、。]{0,14}(さん|氏|教授|さんたち))?(は|も)?[、]?そう(書いて|記して|話して|語って|述べて|振り返って|コメントして)います。', content)
        ) or bool(re.fullmatch(r'と[、]?(記録|記載)されています。|と[、]?(語って|話して|述べて)います。', content))
        if is_trailing:
            prev = narrator_lines[idx - 1][1] if idx else ""
            if not prev.startswith("「"):
                errors.append(
                    f"[帰属だけの単独行] Line {ln}: 引用でない地の文に、後置の帰属行を足しています\n"
                    f"   > \"{content}\"\n"
                    f"   → 導入を前に置く（「米田さんは、こう書いています。」→ 本文）か、1行にまとめる。"
                    f"後置の単独行は出荷済み3本で0件"
                )
        # 8b. 話し言葉が「」の外に出ていないか（引用行そのものは対象外）
        is_quoted = content.startswith("「") and content.rstrip().endswith("」")
        if not is_quoted and COLLOQUIAL.search(content):
            errors.append(
                f"[話し言葉が括弧の外] Line {ln}: 証言は「」で囲む\n"
                f"   > \"{content[:44]}\"\n"
                f"   → ナレーターが一人称で話す形になっています。引用なら「」で囲み、導入文を付ける"
            )

    # Gate 7: 1回しか出てこない固有名詞を列挙（WARNING）
    all_body = "\n".join(c for _, c in narrator_lines)
    seen = {}
    for _, c in narrator_lines:
        for m in PROPER_NOUN.findall(c) or []:
            pass
    for ln, c in narrator_lines:
        for m in set(PROPER_NOUN.findall(c)):
            seen.setdefault(m, []).append(ln)
    for word, hits in sorted(seen.items()):
        if all_body.count(word) == 1:
            line_no = hits[0]
            warnings.append(
                f"[孤立した固有名詞] Line {line_no}: '{word}' は台本に1回しか出てきません\n"
                f"   → 後半で使わないなら削る。比較事例・列挙なら問題なし（判断は人間）"
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
        print("  ✅ Show Don't Tell: OK\n  ✅ メタ語り禁止(YCP-020): OK\n  ✅ 引用の作法(Gate8): OK\n  ✅ 孤立した固有名詞: 警告のみ（下記参照）")
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
