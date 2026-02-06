import sys
import os
import re

# Add local directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)).replace("System_Tools", "Tools"))

try:
    import validate_yama_safety
except ImportError:
    # Fallback if in same directory or different structure
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        import validate_yama_safety
    except ImportError:
        print("⚠️ Warning: Could not import 'validate_yama_safety'. Safety check skipped (Not Ideal).")
        validate_yama_safety = None

MIN_VOLUME_CHARS = 6000

def validate_structure(file_path):
    print(f"[Structure Check]: Validating Yama Story Structure + Safety + Volume: {os.path.basename(file_path)}")
    
    # --- LAYER 1: NG WORD & PRONOUN BLOCKADE ---
    # Physically block entry if Safety Check fails.
    if validate_yama_safety:
        print("\n[Layer 1] Physical Blockade: NG Words & Pronouns...")
        if not validate_yama_safety.validate_file(file_path):
            print("[BLOCKADE]: NG Words or Pronouns detected.")
            sys.exit(1)
    else:
        print("⚠️ [Layer 1] Skipped (Module not found).")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    # 1. Check for Markers
    markers = ["<!-- PART: KI -->", "<!-- PART: SHO -->", "<!-- PART: TEN-KETSU -->"]
    if not all(marker in content for marker in markers):
        print("[CRITICAL]: Missing Structural Markers.")
        print("   Required: <!-- PART: KI -->, <!-- PART: SHO -->, <!-- PART: TEN-KETSU -->")
        print("   Please demarcate the script sections explicitly.")
        sys.exit(1)

    # 2. Extract Sections
    parts = re.split(r'<!-- PART: [A-Z-]+ -->', content)
    
    if len(parts) < 4:
         print("[ERROR]: Could not split content correctly. Ensure markers are synonymous with the start of sections.")
         sys.exit(1)
         
    ki_text = parts[1]
    sho_text = parts[2]
    ten_text = parts[3]
    
    # Cleaning for PACING check (removes metadata)
    def clean_text(text):
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.startswith('【'): continue # Production Notes
            if line.startswith('['): continue # Scene Headers / Visuals
            if line.startswith('<!--'): continue # HTML Comments
            if line.startswith('#'): continue # Markdown Headers
            cleaned_lines.append(line)
        return "".join(cleaned_lines)

    len_ki = len(clean_text(ki_text))
    len_sho = len(clean_text(sho_text))
    len_ten = len(clean_text(ten_text))
    total = len_ki + len_sho + len_ten
    
    # --- LAYER 2: VOLUME PHYSICAL BLOCKADE ---
    # Physically block if the script is too "thin" (Summarized/Compressed).
    print(f"\n[Layer 2] Physical Blockade: Volume Floor ({MIN_VOLUME_CHARS} chars)...")
    if total < MIN_VOLUME_CHARS:
         print(f"[BLOCKADE]: Script volume ({total}) is below safety floor ({MIN_VOLUME_CHARS}).")
         print("   Reason: Potential over-summarization detected.")
         sys.exit(1)
    else:
         print(f"[OK]: Volume OK: {total} chars")

    # --- LAYER 3: RATIO BLOCKADE (1:8:1) ---
    print(f"\n[Layer 3] Golden Ratio Check (1:8:1)...")
    
    ratio_ki = (len_ki / total) * 100
    ratio_sho = (len_sho / total) * 100
    ratio_ten = (len_ten / total) * 100
    
    print("-" * 40)
    print(f"[Analysis]: Structural Analysis (Total: {total} chars)")
    print(f"   起 (Ki):       {ratio_ki:.1f}%  (Target: 10% ±5%)")
    print(f"   承 (Sho):      {ratio_sho:.1f}%  (Target: 80% ±10%)")
    print(f"   転結 (Ten):    {ratio_ten:.1f}%  (Target: 10% ±5%)")
    print("-" * 40)
    
    errors = []
    
    # KI Logic (5-15%)
    if not (5 <= ratio_ki <= 15):
        errors.append(f"[Structure Violation]: 'Ki' is {ratio_ki:.1f}%. Must be between 5-15%.")
        
    # SHO Logic (70-90%) - Massive Body
    if not (70 <= ratio_sho <= 90):
        errors.append(f"[Structure Violation]: 'Sho' is {ratio_sho:.1f}%. Must be between 70-90%.")
        
    # TEN Logic (5-15%) - Short & Impactful
    if not (5 <= ratio_ten <= 15):
        errors.append(f"[Warning]: Structure Violation: 'Ten-Ketsu' is {ratio_ten:.1f}%. Must be between 5-15%.")
        
    if errors:
        for e in errors:
            print(e)
        print("\n[FAILED]: VALIDATION FAILED. Please resize sections to match the Golden Ratio.")
        sys.exit(1)
    else:
        print("[PASSED]: VALIDATION PASSED. Golden Ratio (1:8:1) Achieved.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_structure.py <file_path>")
        sys.exit(1)
    validate_structure(sys.argv[1])
