import sys
import re
import os

# Configuration
LOG_FILE = "/Users/tosimasa/Desktop/Antigravity/Yama_Story/yama_safety_validation.log"

# Strict Prohibited Words (Demonetization Risk & Style)
BANNED_WORDS = {
    # Death (High Risk) - Must use euphemisms
    r"(?<!必)死(?!守|角|球|力|闘|去)": "NG: '死' (Direct Death/Corpse reference). Use '悲劇', '帰らぬ人', '命を落とす'. (Exception: '必死' included in regex)",
    r"死亡": "NG: '死亡'. Use '帰らぬ人', '命が失われた'.",
    r"死体": "NG: '死体'. Use '遺体', 'なきがら'.",
    r"遺体": "NG: '遺体' (Avoid in Title/Thumb). Use '発見', '姿'. Script OK if respectful.",
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

# --- CONSISTENCY DICTIONARY (Standardized Readings) ---
# Format: { "KeyTerm": "CorrectReading/String" }
# The validator ensures that if 'KeyTerm' appears, it matches the strictly defined string.
TERM_DB = {
    "白銀": "白銀（はくぎん）",
    "景泰": "景泰（ケイタイ）" 
}

# Whitelist exceptions not covered by Regex lookbehinds
WHITELIST_LINES = [
    "【制作メモ】", 
    "<!-- SAFETY_OVERRIDE -->",
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
    
    # Repetition Check Variables
    last_ending = ""
    repetition_count = 0
    
    # Simple ending pattern: Capture 'でした', 'ました', 'だ', 'ある' at end of line (ignoring punctuation)
    ending_pattern = re.compile(r'(でした|ました|だ|ある|いる)[。、]?$')

    for i, line in enumerate(lines):
        line_num = i + 1
        stripped_line = line.strip()
        
        if not stripped_line: continue
        
        # Skip Production Notes & Metadata for checks
        is_metadata = any(w in line for w in WHITELIST_LINES) or stripped_line.startswith('[') or stripped_line.startswith('#') or stripped_line.startswith('<')
        
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
    
    validate_file(sys.argv[1])
