import re
import difflib
import sys

def normalize_text(text):
    """
    Normalizes text for comparison:
    - Removes whitespace
    - Removes newlines
    - Removes specific artifacts found in prompts (like ']')
    """
    text = text.replace(' ', '').replace('　', '').replace('\n', '').replace('\r', '')
    text = text.replace(']', '').replace('[', '') # Remove brackets that might be left over
    return text

def extract_narration_from_full_script(file_path):
    """
    Extracts narration lines from the full script.
    - Ignores lines starting with #, [, 【, <!, (, etc.
    - Strips 'ナレーター:' prefix.
    """
    narration_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='cp932') as f:
            lines = f.readlines()
            
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Meta-data patterns to IGNORE
        if line.startswith('#'): continue
        if line.startswith('['): continue
        if line.startswith('【'): continue
        if line.startswith('<!--'): continue
        if line.startswith('（'): continue # (全編完...)
        
        # Specific Narration handling
        content = line
        if line.startswith('ナレーター:'):
            content = line.replace('ナレーター:', '').strip()
        elif line.startswith('ナレーター：'): # Full width colon check
            content = line.replace('ナレーター：', '').strip()
            
        # If it's just a line of text now, assume it's narration
        narration_lines.append(content)
        
    return "\n".join(narration_lines)

def extract_narration_from_text_file(file_path):
    """
    Reads the raw narration text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='cp932') as f:
            content = f.read()
            
    # Remove lines that look like they might be accidentally pasted meta-data
    # e.g. "「生還率 0%」]" might be cleaned differently
    # For now, return as is, relying on normalizer for strict char comparison
    return content

def compare_files(full_script_path, narr_only_path):
    full_narr_raw = extract_narration_from_full_script(full_script_path)
    only_narr_raw = extract_narration_from_text_file(narr_only_path)
    
    # Normalize but keep some structure for readability in diff? No, strict match requested.
    # But for diffing, let's normalize strictly first.
    norm_full = normalize_text(full_narr_raw)
    norm_only = normalize_text(only_narr_raw)
    
    if norm_full == norm_only:
        print("[MATCH] EXACT MATCH: The narration is identical character-for-character.")
    else:
        print("[DIFF] DIFFERENCES DETECTED:")
        print("--------------------------------------------------")
        
        matcher = difflib.SequenceMatcher(None, norm_full, norm_only)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                continue
            elif tag == 'replace':
                print(f"[REPLACE] Full Script: '{norm_full[i1:i2]}' -> Narr Only: '{norm_only[j1:j2]}'")
            elif tag == 'delete':
                print(f"[DELETE]  Full Script has '{norm_full[i1:i2]}' which is MISSING in Narr Only")
            elif tag == 'insert':
                print(f"[INSERT]  Narr Only has '{norm_only[j1:j2]}' which is MISSING in Full Script")
                
        print("--------------------------------------------------")

if __name__ == "__main__":
    compare_files(sys.argv[1], sys.argv[2])
