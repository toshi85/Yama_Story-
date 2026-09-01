import sys
import re
import os

# Configuration
LOG_FILE = "/Users/tosimasa/Desktop/Antigravity/Yama_Story/yama_safety_validation.log"

# Strict Prohibited Words (Demonetization Risk & Style)
BANNED_WORDS = {
    # Death (High Risk) - Must use euphemisms
    r"(?<!必)(?<!不)死(?!守|角|球|力|闘|去)": "NG: '死' (Direct Death/Corpse reference). Use '悲劇', '帰らぬ人', '命を落とす'. (Exception: '必死', '不死' included in regex)",
    r"死亡": "NG: '死亡'. Use '帰らぬ人', '命が失われた'.",
    r"死体": "NG: '死体'. Use '遺体', 'なきがら'.",
    r"全滅": "NG: '全滅'. Use '誰ひとり戻らない', '壊滅'.",
    r"即死": "NG: '即死'. Use 'その瞬間に意識を失う'.",
    
    # Violence/Crime
    r"殺す": "NG: '殺す'. Use '奪う', '手にかける'.",
    r"殺人": "NG: '殺人'. Use '事件', '犯行'.",
    r"殺害": "NG: '殺害'. Use '命を奪う'.",
    r"刺す": "NG: '刺す'.",
    r"殴る": "NG: '殴る'.",
    r"暴行": "NG: '暴行'.",
    
    # Mental
    r"発狂": "NG: '発狂'. Use '錯乱', 'パニック'.",
    r"狂う": "NG: '狂う'. Use '常軌を逸する'.",
    
    # Children
    r"子供の死": "NG: '子供の死'. Use '小さな命が失われる'.",

    # Pronouns (Strict Ban: No Generic Pronouns)
    r"彼(?!女)": "NG: '彼' (He). Use specific name (e.g. 'Liang', 'The Runner').",
    r"彼女": "NG: '彼女' (She). Use specific name.",
    r"彼ら": "NG: '彼ら' (They). Use '選手たち', '村人たち'.",
    r"あいつ": "NG: 'あいつ'. Use Name.",
    r"こいつ": "NG: 'こいつ'. Use Name.",
    r"やつ": "NG: 'やつ'. Use Name.",
}

# --- TITLE / THUMBNAIL ONLY (2026-09-01 新設) ---
# 本文では許容し、タイトル・サムネイルでのみ止める語。
# 根拠: 出荷済み12本が本文で '遺体' を使い、すべて公開・収益化されている
#       （十和利山30件・三毛別9件・福岡大7件・朱鞠内湖4件。朱鞠内湖は平均視聴率34.1%の実測トップ）。
#       旧実装は '遺体' を BANNED_WORDS に置いていたが、本文だけを止めていた。
#       '#' で始まる行はメタデータとして読み飛ばすため、肝心のタイトルは一度も検査されていなかった。
#       さらに辞書内で矛盾していた（'死体' の指示が「'遺体' を使え」）。
# → feedback_calibrate_audits_to_shipped_content.md（出荷済みの内容が通る値に較正する）
TITLE_THUMB_BANNED = {
    r"遺体": "NG(タイトル/サムネのみ): '遺体'. Use '発見', '姿'. 本文での使用は可.",
}

# --- SENSATIONALISM CHECK (Warning Level) ---
SENSATIONAL_WORDS = {
    r"衝撃": "WARN: '衝撃' in script body may trigger clickbait detection.",
    r"驚愕": "WARN: '驚愕' is sensational. Use factual description.",
    r"ヤバい": "WARN: 'ヤバい' is too casual for educational documentary.",
    r"地獄絵図": "WARN: '地獄絵図' is sensational. Use '悲惨な状況'.",
    r"グロ": "WARN: 'グロ' risks age-restriction. Use clinical description.",
    r"閲覧注意": "WARN: '閲覧注意' in script may trigger content warning flags.",
}

# --- VICTIM DIGNITY CHECK ---
DIGNITY_NEGATIVE_WORDS = [
    "愚かな", "馬鹿な", "無謀な", "身勝手な", "自業自得",
    "怠慢な", "無能な", "迂闊な", "軽率な",
]

# --- CONSISTENCY DICTIONARY (Standardized Readings) ---
# Format: { "KeyTerm": "CorrectReading/String" }
# The validator ensures that if 'KeyTerm' appears, it matches the strictly defined string.
TERM_DB = {
    "白銀": "白銀（パイイン）",
    "景泰": "景泰（ケイタイ）"
}

# Whitelist exceptions not covered by Regex lookbehinds
# 検査対象外にする行（読み上げられない＝YouTubeが見ない行）
# 2026-08-30 追加の根拠: Analytics/Why_Shumarinai_Hit.md §5-1
#   朱鞠内湖（実測で当たった1本）の「違反」12件は全て制作メモ・編集者指示・SE指定だった。
#   例: 「衝撃音（ドン）と同時にカットイン」＝効果音の名前／「遺体描写は厳禁」＝禁止する指示
WHITELIST_LINES = [
    "【制作メモ】",
    "【SE】",            # 効果音の指定（「衝撃音」等が入る）
    "<!-- SAFETY_OVERRIDE -->",  # 公文書の逐語引用など、言い換えると事実が変わる行に付ける
    "[BGM:",
    "[SEQ:"
]

def log_print(msg):
    print(msg)
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(msg + "\n")
    except Exception:
        pass

def validate_file(file_path):
    log_print(f"\n--- [Safety Blockade]: Checking {os.path.basename(file_path)} ---")
    log_print(f"    Targeting: NG Words, Pronouns, Repetitive Endings, & Term Consistency")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        log_print("[ERROR]: File not found.")
        return False

    errors = []

    # --- Title / Thumbnail scoped check (2026-09-01) ---
    # H1（動画タイトル）と、見出しに「サムネ」を含む節だけを対象にする
    in_thumb = False
    for i, line in enumerate(lines):
        s_line = line.strip()
        if s_line.startswith('#'):
            in_thumb = ('サムネ' in s_line) or ('thumbnail' in s_line.lower())
        is_title = s_line.startswith('# ') and not s_line.startswith('##')
        if not (is_title or in_thumb):
            continue
        for pattern, reason in TITLE_THUMB_BANNED.items():
            if re.search(pattern, s_line):
                errors.append(f"Line {i+1}: {reason} \n   -> Context: \"{s_line}\"")

    # Repetition Check Variables
    last_ending = ""
    repetition_count = 0

    # Simple ending pattern: Capture 'でした', 'ました', 'だ', 'ある' at end of line (ignoring punctuation)
    ending_pattern = re.compile(r'(でした|ました|だ|ある|いる)[。、]?$')

    # Track production note context (制作メモ, SE, CapCut, 演出 sections)
    in_production_section = False

    for i, line in enumerate(lines):
        line_num = i + 1
        stripped_line = line.strip()

        if not stripped_line: continue

        # Detect production section headers → skip until next ASSET header or ナレーション
        if re.match(r'\*\*(制作メモ|SE|CapCut編集指示|演出|Lovart|AI動画プロンプト|Google Earth)', stripped_line):
            in_production_section = True
        elif re.match(r'### ASSET-|ナレーター:', stripped_line):
            in_production_section = False
        elif stripped_line.startswith('**ナレーション'):
            in_production_section = False

        # Skip Production Notes & Metadata for checks
        is_metadata = (
            any(w in line for w in WHITELIST_LINES) or
            stripped_line.startswith('[') or stripped_line.startswith('#') or
            stripped_line.startswith('<') or stripped_line.startswith('|') or
            stripped_line.startswith('```') or stripped_line.startswith('**') or
            stripped_line.startswith('- ') or  # Bullet points in production notes
            # --- 2026-08-30 追加: 制作メモ・編集者指示は「読み上げない文」なので検査対象外 ---
            # 根拠: 朱鞠内湖（実測で当たった1本）の違反12件が全てここだった。
            #   「衝撃音（ドン）と同時にカットイン」＝効果音の名前
            #   「遺体描写は厳禁」＝むしろ禁止している指示
            #   「2023年度 全国219人／死亡6人」＝環境省統計の出典つき引用
            # YouTubeが判定するのは完成した動画であって、編集者向けの指示文ではない。
            # → Analytics/Why_Shumarinai_Hit.md §5-1
            stripped_line.startswith('【') or      # 【SE】【制作メモ】等の指定行
            stripped_line.startswith('→') or       # → 編集者指示: / → シーン:
            stripped_line.startswith('>') or       # 引用ブロック（台本冒頭の方針メモ）
            stripped_line.startswith('シーン:') or
            '編集者指示' in stripped_line or
            in_production_section  # Inside production note sections
        )
        
        # Reset ending counter when hitting metadata (prevents cross-ASSET false positives)
        if is_metadata:
            last_ending = ""
            repetition_count = 0

        # 1. NG Word & Pronoun Check
        if not is_metadata:
            for pattern, reason in BANNED_WORDS.items():
                matches = re.finditer(pattern, line)
                for match in matches:
                    errors.append(f"Line {line_num}: {reason} \n   -> Context: \"{stripped_line}\"")

            # 2. Consecutive Ending Check
            match = ending_pattern.search(stripped_line)
            if match:
                current_ending = match.group(1)
                if current_ending == last_ending:
                    repetition_count += 1
                else:
                    last_ending = current_ending
                    repetition_count = 1
                
                if repetition_count >= 2: 
                    errors.append(f"Line {line_num}: Repetitive Ending '{current_ending}' (Count: {repetition_count}). Change to noun stop (体言止め) or other form.")
            else:
                last_ending = ""
                repetition_count = 0

            # 3. CONSISTENCY CHECK
            for term, correct_form in TERM_DB.items():
                if term in stripped_line:
                    # Regex to find "Term(Reading)" pattern
                    # Matches "白銀（...）" or "白銀(...)"
                    match_reading = re.search(re.escape(term) + r"[（\(](.+?)[）\)]", stripped_line)
                    if match_reading:
                        actual_reading = match_reading.group(1)
                        expected_reading = correct_form.split("（")[1].replace("）", "")

                        if actual_reading != expected_reading:
                            errors.append(f"Line {line_num}: Inconsistent Reading for '{term}'. Found '（{actual_reading}）', expected '（{expected_reading}）'.")

            # 4. SENSATIONALISM CHECK (Warning)
            for pattern, reason in SENSATIONAL_WORDS.items():
                if re.search(pattern, line):
                    errors.append(f"Line {line_num}: {reason}\n   -> \"{stripped_line}\"")

            # 5. VICTIM DIGNITY CHECK
            for neg_word in DIGNITY_NEGATIVE_WORDS:
                if neg_word in stripped_line:
                    # Check if a person's name (katakana or kanji name) is near the negative word
                    # Simple heuristic: same line contains both a negative descriptor and a proper noun pattern
                    has_name = bool(re.search(r'[ァ-ヶー]{2,}', stripped_line)) or bool(re.search(r'[A-Z][a-z]+', stripped_line))
                    if has_name:
                        errors.append(f"Line {line_num}: Victim dignity concern: '{neg_word}' used near a proper name. Rephrase to respect victims.\n   -> \"{stripped_line}\"")

    if errors:
        log_print(f"[FAILED]: Found {len(errors)} issues.")
        for e in errors:
            log_print(e)
        return False
    
    log_print("[SUCCESS]: No Safety or Style Issues Found.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_print("Usage: python3 validate_yama_safety.py <file_path>")
        sys.exit(1)
    
    result = validate_file(sys.argv[1])
    sys.exit(0 if result else 1)
