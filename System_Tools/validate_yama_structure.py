import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _infermarks
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

MIN_VOLUME_CHARS = 8800  # 最適尺26分（340字/分）に基づく最低文字数
CLOSING = "違反した箇所は、語を置き換えるのではなく、その文を丸ごと書き直してください（前後の文とのつながりも読み直す）。"

# 出典: SCRIPT_CHECKLIST.md STEP 1、Structure_Rules.md §0.1・§0.2・§1・§2、
# Correction_Patterns.md YCP-031・YCP-032。
GOOD = {
    "competitor": "競合上位3本の分析と情報の穴3つを先にまとめ、その差別化を台本の構成へ反映する。",
    "safety": "禁止語や代名詞を含む文を、上に示された項目別の直し方に沿って文全体から組み直す。",
    "markers": "起、承、転結の各パートが役割どおりに分かれる構成へ戻し、それぞれの先頭に指定のPARTマーカーを置く。",
    "volume": "検査を通すための文を足さず、素材シートの未使用素材を棚卸しし、その事件自体を深掘りする構成から組み直す。",
    "ki_chars": "起をフック、最初の被害者の日常、その日常が崩れる予感の一文で組み、270〜950字に収める。",
    "ki_ratio": "起をフック、最初の被害者の日常、その日常が崩れる予感の一文までに絞り、全体の1割未満に組み直す。",
    "sho_ratio": "承に主人公の行動、障害、葛藤を集め、事件の具体が全体の70〜90%になるよう章を組み直す。",
    "ten_ratio": "転に最大の障害とテーマ、結に短い余韻を置き、転結全体を5〜15%に組み直す。",
}


def fail(message, good_key, *details):
    print(message)
    print(f"    → 直し方: {GOOD[good_key]}")
    for detail in details:
        print(detail)
    print(CLOSING)
    sys.exit(1)

def validate_structure(file_path):
    print(f"[Structure Check]: Validating Yama Story Structure + Safety + Volume: {os.path.basename(file_path)}")
    
    # --- LAYER 0: COMPETITOR & THUMBNAIL ANALYSIS BLOCKADE ---
    try:
        import validate_yama_competitor
        print("\n[Layer 0] Physical Blockade: Competitor & Thumbnail Analysis...")
        # validate_yama_competitor calls sys.exit(1) on failure, so reaching next line = PASS
        validate_yama_competitor.validate_competitor(file_path)
        print("[Layer 0] PASSED.")
    except SystemExit as e:
        if e.code != 0:
            fail("[BLOCKADE]: Competitor & Thumbnail Analysis missing. Cannot proceed.", "competitor")
    except ImportError:
        print("⚠️ [Layer 0] Skipped (validate_yama_competitor module not found).")

    # --- LAYER 1: NG WORD & PRONOUN BLOCKADE ---
    # Physically block entry if Safety Check fails.
    if validate_yama_safety:
        print("\n[Layer 1] Physical Blockade: NG Words & Pronouns...")
        if not validate_yama_safety.validate_file(file_path, show_closing=False):
            fail("[BLOCKADE]: NG Words or Pronouns detected.", "safety")
    else:
        print("⚠️ [Layer 1] Skipped (Module not found).")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = _infermarks.strip_infer(f.read())
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}")
        sys.exit(1)

    # 1. Check for Markers
    markers = ["<!-- PART: KI -->", "<!-- PART: SHO -->", "<!-- PART: TEN-KETSU -->"]
    if not all(marker in content for marker in markers):
        fail(
            "[CRITICAL]: Missing Structural Markers.",
            "markers",
            "   Required: <!-- PART: KI -->, <!-- PART: SHO -->, <!-- PART: TEN-KETSU -->",
            "   Please demarcate the script sections explicitly.",
        )

    # 2. Extract Sections
    parts = re.split(r'<!-- PART: [A-Z-]+ -->', content)
    
    if len(parts) < 4:
         fail("[ERROR]: Could not split content correctly. Ensure markers are synonymous with the start of sections.", "markers")
         
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
         fail(
             f"[BLOCKADE]: Script volume ({total}) is below safety floor ({MIN_VOLUME_CHARS}).",
             "volume",
             "   Reason: Potential over-summarization detected.",
         )
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

    # KI Logic — 2026-09-02: 起は「機能」で切るので、比率の下限では判定しない。
    #   起 = フック章 ＋ 最初の被害者の日常 ＋「その日常が崩れる予感」の一行。承はそこから事件の具体。
    #   下限は字数（フック120-380 ＋ セットアップ150-500 の合成／出荷済み実測 328-929字）、
    #   上限だけ比率で見る。切り方そのものは validate_yama_intro.py が検査する。
    KI_CHARS = (270, 950)
    if not (KI_CHARS[0] <= len_ki <= KI_CHARS[1]):
        errors.append((f"[Structure Violation]: 'Ki' is {len_ki} chars. "
                       f"Must be between {KI_CHARS[0]}-{KI_CHARS[1]} chars "
                       f"(hook 120-380 + setup 150-500).", "ki_chars"))
    # 2026-09-02 ユーザー指示:「起は短ければ短いほどいい。1割未満に抑える」
    if ratio_ki >= 10:
        errors.append((f"[Structure Violation]: 'Ki' is {ratio_ki:.1f}%. Must be under 10%.", "ki_ratio"))

    # SHO Logic (70-90%)
    if not (70 <= ratio_sho <= 90):
        errors.append((f"[Structure Violation]: 'Sho' is {ratio_sho:.1f}%. Must be between 70-90%.", "sho_ratio"))

    # TEN Logic (5-15%)
    if not (5 <= ratio_ten <= 15):
        errors.append((f"[Structure Violation]: 'Ten-Ketsu' is {ratio_ten:.1f}%. Must be between 5-15%.", "ten_ratio"))

    if errors:
        for message, good_key in errors:
            print(message)
            print(f"    → 直し方: {GOOD[good_key]}")
        print("\n[FAILED]: VALIDATION FAILED. Please resize sections to match the Golden Ratio.")
        print(CLOSING)
        sys.exit(1)
    else:
        print("[PASSED]: VALIDATION PASSED. Golden Ratio (1:8:1) Achieved.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_structure.py <file_path>")
        sys.exit(1)
    validate_structure(sys.argv[1])
