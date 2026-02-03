import sys
import re
import os

LOG_FILE = "yama_safety_validation.log"

# Strict Prohibited Words (Demonetization Risk)
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
    
    # Mental
    r"発狂": "NG: '発狂'. Use '錯乱', 'パニック'.",
    r"狂う": "NG: '狂う'. Use '常軌を逸する'.",
    
    # Children
    r"子供の死": "NG: '子供の死'. Use '小さな命が失われる'.",

    # Pronouns (New Rule: No Generic Pronouns)
    r"彼(?!女)": "NG: '彼' (He). Use specific name (e.g. 'Liang', 'The Runner').",
    r"彼女": "NG: '彼女' (She). Use specific name.",
    r"彼ら": "NG: '彼ら' (They). Use '選手たち', '村人たち'.",
    r"あいつ": "NG: 'あいつ'. Use Name.",
    r"こいつ": "NG: 'こいつ'. Use Name.",
}

# Whitelist exceptions not covered by Regex lookbehinds
WHITELIST_LINES = [
    "【制作メモ】", # Ignore contents inside memo blocks? No, memos should also be safe? Actually visual descriptions might need words like 'corpse' for image gen prompts, but let's be strict for now.
    "<!-- SAFETY_OVERRIDE -->"
]

def log_print(msg):
    print(msg)
    # Simple logging without file lock issues
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(msg + "\n")
    except Exception:
        pass

def validate_file(file_path):
    log_print(f"\n--- Checking: {os.path.basename(file_path)} ---")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        log_print("❌ FILE ERROR: File not found.")
        return False

    errors = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # logical_check: Memo Placement
        # If line starts with 【制作メモ】, check if previous line was empty or narrative?
        # Actually, rule is "Memo BELOW Dialogue".
        # This is hard to validate strictly without parsing blocks, but we can check if a memo block interrupts a sentence?
        # Let's focus on keywords first.
        
        if any(w in line for w in WHITELIST_LINES):
            continue

        for pattern, reason in BANNED_WORDS.items():
            matches = re.finditer(pattern, line)
            for match in matches:
                # Highlight the error context
                errors.append(f"Line {line_num}: {reason} \n   -> Context: \"{line.strip()}\"")

    if errors:
        log_print(f"🚫 FAILED: Found {len(errors)} issues.")
        for e in errors:
            log_print(e)
        return False
    
    log_print("✅ SUCCESS: No Issues Found.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_print("Usage: python3 validate_yama_safety.py <file_path>")
        sys.exit(1)
    
    validate_file(sys.argv[1])
