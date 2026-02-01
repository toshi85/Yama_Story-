import sys
import re
import os

LOG_FILE = "yama_safety_validation.log"

# Strict Prohibited Words (Demonetization Risk)
BANNED_WORDS = {
    # Death
    r"死": "NG: '死' (Exception: '必死' is OK, check manually). Use '悲劇', '帰らぬ人', '消失'.",
    r"死亡": "NG: '死亡'. Use '帰らぬ人', '命を落とす'.",
    r"死体": "NG: '死体'. Use '遺体', 'なきがら'.",
    r"遺体": "NG: '遺体' (Avoid in Title/Thumb). Use '発見', '姿'. Script OK if respectful.",
    r"全滅": "NG: '全滅'. Use '誰ひとり戻らない', '壊滅'.",
    r"即死": "NG: '即死'. Use 'その瞬間に意識を失う'.",
    
    # Violence/Crime
    r"殺す": "NG: '殺す'. Use '奪う', '手にかける'.",
    r"殺人": "NG: '殺人'. Use '事件', '犯行'.",
    r"殺害": "NG: '殺害'. Use '命を奪う'.",
    r"刺す": "NG: '刺す' (Context dependent). Avoid graphic description.",
    
    # Mental
    r"発狂": "NG: '発狂'. Use '錯乱', 'パニック', '精神の崩壊'.",
    r"狂う": "NG: '狂う'. Use '常軌を逸する', '異変'.",
    
    # Children
    r"子供の死": "NG: '子供の死'. Use '小さな命が失われる'.",
}

# Whitelist (Exceptions)
WHITELIST = [
    "必死", "死角", "起死回生", "死守", # Common compounds
]

def log_print(msg):
    print(msg)
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(msg + "\n")
    except Exception:
        pass

def validate_file(file_path):
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(f"\n--- Checking: {os.path.basename(file_path)} ---\n")

    log_print(f"🔍 Validating Safety: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        log_print("❌ FILE ERROR: File not found.")
        return False

    errors = []
    
    for pattern, reason in BANNED_WORDS.items():
        # Simple string search first
        if pattern in content:
            # Check whitelist
            is_whitelisted = False
            for white in WHITELIST:
                if white in content and pattern in white:
                    # This is weak logic (substring match), but sufficient for now.
                    # Ideally, regex context check.
                    # If "必死" is present, "死" will be flagged unless we ignore lines with whitelisted words.
                    pass 
            
            # Allow manual override tag? <!-- SAFETY_OVERRIDE -->
            if "<!-- SAFETY_OVERRIDE -->" in content:
                continue

            matches = re.findall(pattern, content)
            if matches:
                 # Context check: Filter out whitelisted occurrences
                real_matches = []
                for m in matches:
                    # regex to find context... keeping it simple for v1.
                    # Just flag it, user must verify.
                    real_matches.append(m)
                
                if real_matches:
                    errors.append(f"⚠️ FOUND NG WORD: '{pattern}' -> {reason}")

    if errors:
        log_print("🚫 SAFETY CHECK FAILED (Potential Risks Found):")
        for e in errors:
            log_print(e)
        log_print("👉 If this is a false positive (e.g. '必死'), manually verify.")
        return False
    
    log_print("✅ SUCCESS: No Demonetization Keywords Found.")
    return True

if __name__ == "__main__":
    # Create log file if not exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding='utf-8') as f:
            f.write("Yama Story Safety Log\n")

    if len(sys.argv) < 2:
        log_print("Usage: python3 validate_yama_safety.py <file_path>")
        sys.exit(1)
    
    validate_file(sys.argv[1])
