import sys
import re

def validate_narrative_tone(file_path):
    """
    Validates that the narrator does not use "preachy" or "moralizing" language.
    Enforces a "Show, Don't Tell" policy by flagging banned keywords in Narrator lines.
    """
    
    # Banned keywords that indicate moralizing/preaching
    # These are high-precision signals of "Teaching Mode" vs "Storytelling Mode"
    BANNED_PHRASES = [
        "学ぶべき",      # e.g. "私たちが学ぶべきことは..."
        "教訓",          # e.g. "この事件の教訓は..."
        "社会の闇",      # e.g. "現代社会の闇が..."
        "警鐘",          # e.g. "私たちに警鐘を鳴らして..."
        "私たち",        # e.g. "最後に私たちを救うのは..." (Generic "We" is usually preachy)
        "現代社会",      # e.g. "現代社会には..."
        "考えるべき",    # e.g. "一度立ち止まって考えるべきです"
        "知るべき",      # e.g. "知るべき事実があります"
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
    
    current_section = "Unknown"
    
    print("--------------------------------------------------")
    print(f"[Analysis] Analyzing Narrative Tone: {file_path}")
    print("--------------------------------------------------")

    for i, line in enumerate(lines):
        line = line.strip()
        
        # Track sections if needed across headers
        if line.startswith("#"):
            current_section = line
            continue

        # Only check Narrator lines
        if line.startswith("ナレーター:"):
            content = line.replace("ナレーター:", "").strip()
            
            for phrase in BANNED_PHRASES:
                if phrase in content:
                    errors.append(f"Line {i+1}: Found Banned Phrase '{phrase}' in Narrator line.\n   > \"{content[:40]}...\"")

    if errors:
        print(f"[FAIL] Found {len(errors)} instances of 'Preachy/Moralizing' language.")
        print("   The Narrator must deal in FACTS and EMOTIONS (Show), not OPINIONS (Tell).")
        print("   Please remove these phrases and let the story speak for itself.\n")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)
    else:
        print("[PASS] No moralizing language detected in Narrator lines.")
        print("   (Good Intent: 'Show, Don't Tell' compliance checked)")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_yama_narrative.py <script_file>")
        sys.exit(1)
    
    validate_narrative_tone(sys.argv[1])
