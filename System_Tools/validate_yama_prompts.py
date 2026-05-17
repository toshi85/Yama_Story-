#!/usr/bin/env python3
"""
Yama_Story プロンプト品質バリデーター
台本内のLovartプロンプト・制作メモの品質を自動チェックする。

使い方:
  python3 Yama_Story/System_Tools/validate_yama_prompts.py <台本ファイルパス>

チェック項目:
  1. ナレーター:プレフィックス — 全ナレーション行に「ナレーター:」があるか
  2. 禁止ワード（プロンプト内） — diagram/chart/text等の図解・テキスト系ワード
  3. Generate表現 — 「Generate 5 images.」(separateなし)の検出
  4. Character design reference sheet — 複数アングル事故の原因
  5. 地名チェック — 背景プロンプトに日本/北海道の地名があるか
  6. 安全ワード — blood/death/corpse等のNGワード
  7. カメラ専門用語 — パン/チルト/ドリー等の禁止用語
  8. CHAR参照タグ — 初出/再利用の区別があるか
  9. 複数キャラCHAR矛盾 — 複数キャラ/Generic groupなのに "only this one character" を使用していないか
  10. キャラプロンプト環境混入 — 1:1キャラプロンプトに環境・構図要素が含まれていないか
  11. キャラプロンプト全身 — Full body必須、bust shot等の部分構図禁止
  12. 1ナレ複数アセット — 1ナレーションに2+アセット紐づき検出
  13. 孤立アセット — ナレーション紐づきなしのアセット検出
  14. 静止画連続 — 3連続以上の検出
  15. 映像密度 — 全体平均35字/ASSET以下か
  16. ASSET構造順序 — ナレーター→制作メモ→プロンプトの正しい順序か (FAIL)
  17. 末尾ゴミ行 — 最後のASSET以降に孤立ナレーション行や大量空行がないか (FAIL)
  18. シーン行必須 — 全ASSETに「シーン:」行があるか (FAIL)
  19. Google Earthプロンプト禁止 — [Google Earth]カテゴリにブロックがないか (FAIL)
  20. 背景プロンプト人物矛盾 — 「No people visible」と人物描写が同居していないか (FAIL)
  21. 【AI動画】2ブロック構成 — Google Flow動画プロンプト欠落の検出 (FAIL)
  22. キャラ系プロンプト比率 — 60%以上の達成度（リファレンス羅臼岳72.8%）(FAIL/WARNING)
  23. CHAR-XX 再利用マーカー — 2回目以降のASSET冒頭に (CHAR-XX 再利用): があるか (WARNING)
  24. 複数キャラ個別生成パターン — 複数人シーンでキャラプロンプト①②形式か (WARNING)
"""

import sys
import re
from pathlib import Path


def load_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.readlines()


def check_narrator_prefix(lines):
    """全ナレーション行に ナレーター: があるか"""
    issues = []
    in_code = False
    in_asset_section = False

    non_narr_prefixes = [
        '#', '```', '---', '>', '|', '【', '→', 'シーン:', 'キャラプロンプト',
        '背景プロンプト', 'Lovart', 'Google Flow', '[CHAR-', '[Generic',
        '[New', 'ASSET-', '座標:', 'カメラ:', '<!-- ', 'ナレーター:'
    ]

    for i, line in enumerate(lines):
        s = line.strip()
        if '<!-- PART:' in s:
            in_asset_section = True
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code or not in_asset_section or not s:
            continue
        if any(s.startswith(p) for p in non_narr_prefixes):
            continue

        if re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', s):
            issues.append((i + 1, s[:60]))

    return issues


def check_forbidden_words_in_prompts(lines):
    """Lovartプロンプト内の禁止ワード"""
    forbidden = [
        ('diagram', '図解表現'),
        ('infographic', '図解表現'),
        ('chart', '図解表現'),
        ('schematic', '図解表現'),
        ('blueprint', '図解表現'),
        ('timeline design', '図解表現'),
        ('trajectory lines', '図解表現'),
        ('Character design reference sheet', '複数アングル'),
    ]

    # text but not "no text" or "texture"
    text_pattern = re.compile(r'\btext\b', re.I)

    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for word, category in forbidden:
            if word.lower() in s.lower():
                issues.append((i + 1, category, word, s[:80]))

        if text_pattern.search(s) and 'no text' not in s.lower() and 'texture' not in s.lower():
            issues.append((i + 1, 'テキスト混入', 'text', s[:80]))

    return issues


def check_generate_wording(lines):
    """Generate 5 images. (separateなし) の検出"""
    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        if 'Generate 5 images.' in s and 'separate' not in s:
            issues.append((i + 1, s[:80]))

    return issues


def check_location_in_prompts(lines):
    """背景プロンプトに日本/北海道の地名があるか"""
    japan_kw = ['japan', 'japanese', 'hokkaido', 'fuppushi', 'chitose',
                'tomakomai', 'hachinohe', 'aomori', 'shikotsu', 'tarumae']

    issues = []
    in_code = False
    current_asset = None

    for i, line in enumerate(lines):
        s = line.strip()
        if '【制作メモ】' in s and 'ASSET-' in s:
            m = re.search(r'ASSET-\d+', s)
            current_asset = m.group() if m else '?'

        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code or len(s) < 30:
            continue
        if 'white background' in s.lower():
            continue
        # Skip cartoon character prompts without backgrounds
        if 'Cute cartoon character design' in s and '16:9' not in s:
            continue

        has_loc = any(kw in s.lower() for kw in japan_kw)
        if not has_loc:
            generic = ['forest', 'mountain', 'trail', 'road', 'hospital',
                       'office', 'river', 'snow', 'camp', 'bear', 'bamboo',
                       'village', 'town', 'field', 'newspaper', 'document']
            if any(g in s.lower() for g in generic):
                issues.append((i + 1, current_asset, s[:80]))

    return issues


def check_safety_words(lines):
    """安全ワード違反"""
    ng_words = ['blood', 'death', 'dead body', 'corpse', 'gore', 'dismember',
                'decapitat', 'mutilat', 'entrails', 'severed']

    issues = []
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for word in ng_words:
            if word.lower() in s.lower():
                issues.append((i + 1, word, s[:80]))

    return issues


def check_camera_terms(lines):
    """カメラ専門用語（編集者指示内）"""
    forbidden_terms = {
        'パン': '左から右にゆっくり動かす',
        'チルト': '上から下にゆっくり動かす',
        'ドリー': 'カメラが前にゆっくり進む',
        'Ken Burns': 'ゆっくり近づきながら横に動かす',
        'チルトダウン': '上から下にゆっくり動かす',
        'ドリーイン': 'カメラが前にゆっくり進む',
    }

    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith('→'):
            continue
        for term, replacement in forbidden_terms.items():
            if term in s:
                issues.append((i + 1, term, replacement))

    return issues


def check_char_tags(lines):
    """CHAR参照タグの初出/再利用チェック"""
    pattern = re.compile(r'\[CHAR-\d+ reference\]')  # タグなし
    issues = []
    in_code = False
    in_asset_section = False

    for i, line in enumerate(lines):
        s = line.strip()
        if '## 1.' in s or 'ASSET-001' in s:
            in_asset_section = True
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code or not in_asset_section:
            continue

        matches = pattern.findall(s)
        if matches:
            issues.append((i + 1, matches, s[:80]))

    return issues


def check_char_multi_conflict(lines):
    """複数キャラCHARプロンプトに 'only this one character' が含まれていないか"""
    multi_char_indicators = re.compile(
        r'\bTwo\b|\bThree\b|\bFour\b|\bFive\b|'
        r'\bMultiple\b|\bseveral\b|\bgroup\b|'
        r'side by side|standing together|scattered|'
        r'\[Generic group\]|'
        r'\[CHAR-\d+.*\[CHAR-\d+',
        re.I
    )
    one_char_pattern = re.compile(r'only this one character', re.I)

    issues = []
    in_code = False
    code_block_start = 0
    code_lines = []

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            if not in_code:
                in_code = True
                code_block_start = i
                code_lines = []
            else:
                in_code = False
                block_text = ' '.join(code_lines)
                if multi_char_indicators.search(block_text) and one_char_pattern.search(block_text):
                    issues.append((
                        code_block_start + 1,
                        '複数キャラなのに "only this one character" を使用',
                        block_text[:100]
                    ))
                code_lines = []
            continue
        if in_code:
            code_lines.append(s)

    return issues


def check_char_single_use(lines):
    """CHAR-XX番号が1回しか使われていない（初出のみで再利用なし）ケースを警告"""
    char_pattern = re.compile(r'\[CHAR-(\d+)\s+reference')
    char_counts = {}  # {番号: [行番号リスト]}
    in_code = False

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            continue

        for m in char_pattern.finditer(s):
            num = m.group(1)
            if num not in char_counts:
                char_counts[num] = []
            char_counts[num].append(i + 1)

    issues = []
    for num, line_list in sorted(char_counts.items(), key=lambda x: int(x[0])):
        if len(line_list) == 1:
            issues.append((num, line_list[0]))

    return issues


def check_char_environment(lines):
    """キャラプロンプト(1:1)に環境・構図要素が混入していないか"""
    env_words = re.compile(
        r'\baerial view\b|\bbird.s eye\b|\boverhead\b|'
        r'\blandscape\b|\bmountain slope\b|\bforest floor\b|'
        r'\bstepping off train\b|\bstanding at.*summit\b|\bsitting in tent\b|'
        r'\bscattered far apart\b|\bscattered across\b|'
        r'\bin their own.*space\b|\bisolated in\b|'
        r'\bplatform\b|\bstation\b|\btrailhead\b|'
        r'\binterior\b|\broom\b|\bcorridor\b',
        re.I
    )

    issues = []
    in_code = False
    is_char_prompt = False

    for i, line in enumerate(lines):
        s = line.strip()

        # Detect character prompt section (1:1)
        if 'キャラプロンプト' in s and '1:1' in s:
            is_char_prompt = True
            continue
        if '背景プロンプト' in s or ('【制作メモ】' in s and 'ASSET-' in s):
            is_char_prompt = False

        if s.startswith('```'):
            in_code = not in_code
            if not in_code:
                is_char_prompt = False
            continue

        if not in_code or not is_char_prompt:
            continue

        # Skip CHAR reference section (section 0)
        if 'white background' in s.lower() and 'Single character' in s:
            continue

        matches = env_words.findall(s)
        if matches:
            issues.append((i + 1, matches, s[:100]))

    return issues


def check_char_fullbody(lines):
    """キャラプロンプト(1:1)が全身(Full body)であるかチェック"""
    prohibited = re.compile(
        r'\bbust shot\b|\bupper body shot\b|\bclose-up\b|\bhalf body\b|'
        r'\bwaist up\b|\bchest up\b|\bhands only\b|\bface close\b|'
        r'\bhead shot\b|\bpaw close\b|\bside profile bust\b',
        re.I
    )
    fullbody_pattern = re.compile(r'\bFull body\b', re.I)

    issues = []
    in_code = False
    is_char_prompt = False
    current_asset = None

    for i, line in enumerate(lines):
        s = line.strip()

        if '【制作メモ】' in s and 'ASSET-' in s:
            m = re.search(r'ASSET-\d+', s)
            current_asset = m.group() if m else '?'

        if 'キャラプロンプト' in s and '1:1' in s:
            is_char_prompt = True
            continue
        if '背景プロンプト' in s or ('【制作メモ】' in s and 'ASSET-' in s):
            is_char_prompt = False

        if s.startswith('```'):
            if in_code and is_char_prompt:
                # End of char prompt code block — no further action
                pass
            in_code = not in_code
            if not in_code:
                is_char_prompt = False
            continue

        if not in_code or not is_char_prompt:
            continue

        # Check for prohibited partial composition terms
        found = prohibited.findall(s)
        if found:
            issues.append((i + 1, current_asset, 'prohibited', found, s[:100]))

        # Check for missing "Full body"
        if '[CHAR-' in s or '[Generic' in s or '[New' in s:
            if not fullbody_pattern.search(s):
                issues.append((i + 1, current_asset, 'missing_fullbody', [], s[:100]))

    return issues


def check_static_consecutive(lines):
    """静止画3連続以上の検出"""
    static_cats = ['Lovart静止画]', 'Lovart静止画 + 編集者]']
    consecutive = 0
    max_cons = 0
    runs = []
    current_run = []

    for i, line in enumerate(lines):
        s = line.strip()
        if '【制作メモ】' in s and 'ASSET-' in s:
            is_static = any(c in s for c in static_cats)
            if is_static:
                consecutive += 1
                current_run.append((i + 1, s[:60]))
            else:
                if consecutive >= 3:
                    runs.append(current_run[:])
                consecutive = 0
                current_run = []
            max_cons = max(max_cons, consecutive)

    if consecutive >= 3:
        runs.append(current_run[:])

    return max_cons, runs


def check_density(lines):
    """映像密度チェック"""
    in_code = False
    current_section = None
    total_chars = 0
    total_assets = 0

    memo_prefixes = ['【制作メモ】', 'シーン:', 'キャラプロンプト', '背景プロンプト',
                     'Lovart静止画プロンプト', 'Google Flow動画プロンプト', '→',
                     '座標:', 'カメラ:', '[CHAR-', '[Generic', 'ASSET-']

    for line in lines:
        s = line.strip()
        if '<!-- PART: KI -->' in s: current_section = 'KI'
        elif '<!-- PART: SHO -->' in s: current_section = 'SHO'
        elif '<!-- PART: TEN-KETSU -->' in s: current_section = 'TEN-KETSU'

        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code or not current_section:
            continue

        if '【制作メモ】' in s and 'ASSET-' in s:
            total_assets += 1
            continue

        if not s or s.startswith('#') or s.startswith('---') or s.startswith('>') or s.startswith('|'):
            continue
        if any(s.startswith(p) for p in memo_prefixes):
            continue

        if re.search(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]', s):
            total_chars += len(s)

    avg = total_chars / total_assets if total_assets > 0 else 0
    return total_chars, total_assets, avg


def check_narrator_consecutive(lines):
    """ナレーター行が2行以上連続している箇所を検出"""
    issues = []
    in_code = False
    prev_is_narrator = False
    prev_line_num = 0
    prev_text = ''

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            prev_is_narrator = False
            continue
        if in_code or not s:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        if is_narrator and prev_is_narrator:
            issues.append((prev_line_num, prev_text[:60], i + 1, s[:60]))
        prev_is_narrator = is_narrator
        if is_narrator:
            prev_line_num = i + 1
            prev_text = s

    return issues


def check_multi_asset_per_narration(lines):
    """1つのナレーションに複数アセットが紐づいている箇所を検出"""
    issues = []
    in_code = False
    last_narrator_line = 0
    last_narrator_text = ''
    asset_count_since_narrator = 0
    assets_since_narrator = []

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        is_asset = '【制作メモ】' in s and 'ASSET-' in s

        if is_narrator:
            # 前のナレーターに複数アセットが紐づいていたら報告
            if last_narrator_line > 0 and asset_count_since_narrator >= 2:
                issues.append((
                    last_narrator_line,
                    last_narrator_text[:60],
                    asset_count_since_narrator,
                    [a for a in assets_since_narrator]
                ))
            last_narrator_line = i + 1
            last_narrator_text = s
            asset_count_since_narrator = 0
            assets_since_narrator = []

        if is_asset:
            asset_count_since_narrator += 1
            m = re.search(r'ASSET-\d+', s)
            assets_since_narrator.append(m.group() if m else '?')

    # 最後のナレーターもチェック
    if last_narrator_line > 0 and asset_count_since_narrator >= 2:
        issues.append((
            last_narrator_line,
            last_narrator_text[:60],
            asset_count_since_narrator,
            [a for a in assets_since_narrator]
        ))

    return issues


def check_orphan_assets(lines):
    """ナレーションが紐づかない孤立アセットを検出（直前にナレーター行がないアセット）"""
    issues = []
    in_code = False
    found_narrator_before_asset = False
    in_asset_section = False

    for i, line in enumerate(lines):
        s = line.strip()
        if '<!-- PART:' in s:
            in_asset_section = True
        if not in_asset_section:
            continue

        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        is_narrator = s.startswith('ナレーター:') or s.startswith('ナレーター：')
        is_asset = '【制作メモ】' in s and 'ASSET-' in s

        if is_narrator:
            found_narrator_before_asset = True

        if is_asset:
            if not found_narrator_before_asset:
                m = re.search(r'ASSET-\d+', s)
                asset_id = m.group() if m else '?'
                issues.append((i + 1, asset_id, s[:80]))
            found_narrator_before_asset = False

    return issues


def check_static_narration_length(lines):
    """静止画アセットに紐づくナレーション文字数が25文字を超えている箇所を検出"""
    static_cats = ['Lovart静止画]', 'Lovart静止画 + 編集者]']
    issues = []
    in_code = False

    # ナレーション行を蓄積し、制作メモが来たら紐付ける
    narration_buffer = []  # [(line_num, text, char_count)]

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        # ナレーター行を検出
        if s.startswith('ナレーター:') or s.startswith('ナレーター：'):
            narr_text = s.split(':', 1)[1].strip() if ':' in s else s.split('：', 1)[1].strip()
            narration_buffer.append((i + 1, narr_text, len(narr_text)))
            continue

        # 制作メモ行を検出
        if '【制作メモ】' in s and 'ASSET-' in s:
            is_static = any(c in s for c in static_cats)
            if is_static and narration_buffer:
                # 直前のナレーションを紐付け
                last_narr = narration_buffer[-1]
                if last_narr[2] > 25:
                    asset_match = re.search(r'ASSET-\d+', s)
                    asset_id = asset_match.group() if asset_match else '?'
                    issues.append((
                        last_narr[0],
                        last_narr[2],
                        asset_id,
                        i + 1,
                        last_narr[1][:50]
                    ))
            narration_buffer = []
            continue

        # 制作メモ関連行はスキップ（バッファはクリアしない）
        if s.startswith('シーン:') or s.startswith('キャラプロンプト') or s.startswith('背景プロンプト'):
            continue
        if s.startswith('→') or s.startswith('座標:') or s.startswith('カメラ:'):
            continue
        if s.startswith('【') or s.startswith('#'):
            continue

    return issues


def check_narration_coverage(asset_lines, master_path):
    """台本突合チェック: Asset_Prompts内のナレーション行が台本の全行をカバーしているか"""
    issues = []

    # 台本から全ナレーション行を抽出
    try:
        with open(master_path, 'r', encoding='utf-8') as f:
            master_lines = f.readlines()
    except Exception as e:
        return [(-1, f"台本ファイル読み込みエラー: {e}", "")]

    master_narrations = {}
    for i, line in enumerate(master_lines):
        stripped = line.strip()
        if stripped.startswith("ナレーター:") or stripped.startswith("ナレーター："):
            master_narrations[i + 1] = stripped

    # Asset_Promptsの全テキストを結合
    asset_content = ''.join(asset_lines)

    missing = []
    for line_num, text in sorted(master_narrations.items()):
        if text not in asset_content:
            missing.append((line_num, text))

    return missing, len(master_narrations)


def check_asset_structure_order(lines):
    """ASSETの構造順序チェック: ナレーター→【制作メモ】→プロンプトの正しい順序か。
    【制作メモ】の直前（---まで遡って）にナレーター行がないASSETを検出する。"""
    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'【制作メモ】(ASSET-\d+)', s)
        if m:
            asset_id = m.group(1)
            has_narr_before = False
            for j in range(i - 1, max(0, i - 15), -1):
                sj = lines[j].strip()
                if sj.startswith('ナレーター:'):
                    has_narr_before = True
                    break
                elif sj == '---' or sj.startswith('【制作メモ】'):
                    break
            if not has_narr_before:
                issues.append((i + 1, asset_id))
    return issues


def check_google_earth_no_prompt(lines):
    """[Google Earth]カテゴリのASSETに```プロンプトブロックがないかチェック。
    Google Earthは編集者がGoogle Earth Studioで画面録画する素材であり、
    Lovart用プロンプトを書いてはいけない。"""
    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'【制作メモ】(ASSET-\d+)\s*\[Google Earth\]', s)
        if m:
            asset_id = m.group(1)
            # 次の【制作メモ】または---まで探索し、```ブロックがあれば違反
            for j in range(i + 1, min(len(lines), i + 30)):
                sj = lines[j].strip()
                if sj.startswith('【制作メモ】'):
                    break
                if sj == '```':
                    issues.append((i + 1, asset_id))
                    break
    return issues


def check_scene_line_required(lines):
    """全ASSETに「シーン:」行があるかチェック。
    【制作メモ】ASSET-XXXの直後15行以内に「シーン:」行がなければ欠落と判定。"""
    issues = []
    for i, line in enumerate(lines):
        s = line.strip()
        m = re.match(r'【制作メモ】(ASSET-\d+)', s)
        if m:
            asset_id = m.group(1)
            has_scene = False
            for j in range(i + 1, min(len(lines), i + 15)):
                sj = lines[j].strip()
                if sj.startswith('シーン:') or sj.startswith('シーン：'):
                    has_scene = True
                    break
                elif sj.startswith('【制作メモ】') or sj == '---':
                    break
            if not has_scene:
                issues.append((i + 1, asset_id))
    return issues


def check_trailing_garbage(lines):
    """末尾ゴミ行チェック: 最後のASSETのプロンプト・編集者指示の後に
    孤立したナレーション行や大量の空行がないか検出する。"""
    issues = []

    # 最後のASSETの制作メモ位置を見つける
    last_asset_idx = None
    last_asset_id = None
    for i, line in enumerate(lines):
        m = re.match(r'【制作メモ】(ASSET-\d+)', line.strip())
        if m:
            last_asset_idx = i
            last_asset_id = m.group(1)

    if last_asset_idx is None:
        return issues

    # 最後のASSETの編集者指示/プロンプト末尾を見つける
    last_content_idx = last_asset_idx
    for i in range(last_asset_idx + 1, len(lines)):
        s = lines[i].strip()
        if s and not s == '---':
            last_content_idx = i

    # last_content_idx以降にナレーション行がないかチェック
    trailing_narr = []
    trailing_empty = 0
    for i in range(last_content_idx + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith('ナレーター:'):
            trailing_narr.append((i + 1, s[:60]))
        elif s == '':
            trailing_empty += 1

    if trailing_narr:
        for ln, text in trailing_narr:
            issues.append((ln, f"末尾の孤立ナレーション行: {text}..."))

    if trailing_empty > 5:
        issues.append((len(lines), f"末尾に連続空行{trailing_empty}行"))

    return issues


def check_background_people_contradiction(lines):
    """背景プロンプトに No people visible と人物描写が同居していないか"""
    people_keywords = re.compile(
        r'\b(person|people|human|man |woman |men |women |boy |girl |'
        r'climber|hiker|rescuer|official|soldier|police|doctor|nurse|'
        r'family|crowd|group of people|figure|silhouette|standing|walking|'
        r'running|sitting|carrying|holding|wearing|dressed)\b',
        re.IGNORECASE
    )
    # Exceptions: words that appear in non-human context
    exceptions = re.compile(
        r'(no people|no figures|no humans|no person|figurehead|figure-eight|'
        r'standing water|standing stone|standing dead|running water|'
        r'holding pattern|wearing away|dressed stone|'
        # Animal/nature context
        r'bear\s+walking|bear\s+standing|bear\s+running|bear\s+sitting|'
        r'walking\s+(calmly|slowly|away)|running\s+(motion|blur)|'
        r'frantic\s+running|signs?\s+of|'
        # Silhouette of non-human subjects
        r'silhouette\s+of\s+(a\s+)?(mount|mountain|tree|bear|rock|peak|ridge|'
        r'the\s+mountain|the\s+peak|the\s+ridge)|'
        r'silhouette\s+of\s+a\s+large\s+bear|'
        # Official as adjective for non-human
        r'official\s+(press|report|document|record|statement|announcement|'
        r'conference|investigation|setting|notice))',
        re.IGNORECASE
    )

    issues = []
    in_code = False
    current_asset = None

    for i, line in enumerate(lines):
        s = line.strip()
        if '【制作メモ】' in s and 'ASSET-' in s:
            m = re.search(r'ASSET-\d+', s)
            current_asset = m.group() if m else '?'

        if s.startswith('```'):
            in_code = not in_code
            continue
        if not in_code or len(s) < 30:
            continue
        # Only check 16:9 background prompts (not 1:1 character prompts)
        if 'white background' in s.lower():
            continue
        if '1:1' in s and '16:9' not in s:
            continue

        # Check if this line has "no people" type phrase
        has_no_people = bool(re.search(r'no (people|figures|humans|person)', s, re.I))
        if not has_no_people:
            continue

        # Remove exception phrases before checking for people keywords
        cleaned = exceptions.sub('', s)
        matches = people_keywords.findall(cleaned)
        if matches:
            unique = list(set(m.strip() for m in matches))
            issues.append((i + 1, current_asset, unique, s[:100]))

    return issues


def split_into_asset_blocks(lines):
    """ASSETブロック単位に分割する。各ブロックは (asset_id, start_line, end_line, block_lines) のタプル"""
    asset_header = re.compile(r'【制作メモ】(ASSET-\d+)')
    blocks = []
    current_id = None
    current_start = None
    current_lines = []
    for i, line in enumerate(lines):
        m = asset_header.search(line)
        if m:
            if current_id is not None:
                blocks.append((current_id, current_start, i - 1, current_lines))
            current_id = m.group(1)
            current_start = i
            current_lines = [line]
        elif current_id is not None:
            current_lines.append(line)
    if current_id is not None:
        blocks.append((current_id, current_start, len(lines) - 1, current_lines))
    return blocks


def check_video_prompt_two_blocks(lines):
    """【AI動画】タグ数 == Google Flow動画プロンプト数 を検証"""
    blocks = split_into_asset_blocks(lines)
    issues = []
    for asset_id, start, end, block_lines in blocks:
        header = block_lines[0]
        is_ai_video = bool(re.search(r'【AI動画】|\[AI動画', header))
        if not is_ai_video:
            continue
        block_text = ''.join(block_lines)
        has_flow_prompt = bool(re.search(r'Google Flow動画プロンプト', block_text))
        if not has_flow_prompt:
            issues.append((start + 1, asset_id, '【AI動画】指定だが Google Flow動画プロンプト欠落'))
    return issues


def check_character_prompt_ratio(lines):
    """キャラ系プロンプト比率（60%以上）を検証"""
    blocks = split_into_asset_blocks(lines)
    total = len(blocks)
    if total == 0:
        return None, 0, 0
    char_count = 0
    for asset_id, start, end, block_lines in blocks:
        block_text = ''.join(block_lines)
        if re.search(r'キャラプロンプト|キャラアニメ|キャラ流用|キャラ静止画', block_text):
            char_count += 1
    ratio = (char_count * 100.0) / total
    if ratio >= 60:
        verdict = 'PASS'
    elif ratio >= 50:
        verdict = 'WARNING'
    elif ratio >= 30:
        verdict = 'WARNING_STRONG'
    else:
        verdict = 'FAIL'
    return verdict, char_count, total, ratio


def check_character_style_header(lines):
    """キャラ系プロンプトに固定スタイルヘッダー6要素が含まれているか検証"""
    required_keywords = [
        'Cute cartoon character design',
        'thick black outlines',
        'flat cel-shaded colors',
        'large expressive eyes',
        'slightly chibi proportions',
        "children's animation style",
    ]
    char_prompt_label = re.compile(r'^\s*(キャラプロンプト|キャラアニメーション|キャラ流用|キャラ静止画)[①②③④⑤1-5]?[（(]?')
    blocks = split_into_asset_blocks(lines)
    issues = []
    for asset_id, start, end, block_lines in blocks:
        # キャラ系プロンプトのラベル行を探し、その直後のコードブロック/プロンプト本文を取得
        for idx, line in enumerate(block_lines):
            if not char_prompt_label.search(line):
                continue
            # ラベル行の後、空行までを「このキャラプロンプトのブロック」とみなす（最大30行）
            body_lines = []
            for j in range(idx + 1, min(idx + 31, len(block_lines))):
                nxt = block_lines[j]
                if char_prompt_label.search(nxt):
                    break
                # 「背景プロンプト」「SE:」「編集者指示:」「シーン:」が来たら終了
                if re.search(r'^\s*(背景プロンプト|SE:|編集者指示:|シーン:|→\s*\*\*Google Flow)', nxt):
                    break
                body_lines.append(nxt)
            body_text = ' '.join(body_lines)
            if not body_text.strip():
                continue
            missing = [kw for kw in required_keywords if kw not in body_text]
            if missing:
                actual_line = start + idx + 1
                issues.append((actual_line, asset_id, line.strip()[:50], missing))
    return issues


def check_one_character_per_image_clause(lines):
    """
    Generate指示の使い分けを検証（リファレンス羅臼岳準拠）:
    - CHAR基準画像定義（### CHAR-XX: 直下のキャラプロンプト）: `each showing only this one character` 必須
    - 本編ASSETのキャラ系プロンプト: 不要（`Generate N separate images.` のみで可）
    - バリエーション指示文（`Generate N images with variations` / `image 1..., image 2...` 列挙）: 全プロンプトで禁止
    """
    char_prompt_label = re.compile(r'^\s*(キャラプロンプト|キャラアニメーション|キャラ流用|キャラ静止画)[①②③④⑤1-5]?[（(]?')
    char_definition_header = re.compile(r'^###\s+CHAR-\d+')
    required_phrase = 'each showing only this one character'
    forbidden_variation_pattern = re.compile(
        r'Generate\s+\d+\s+separate\s+images?\s+with\s+(subtle\s+)?variations?\s*[\(（]', re.I
    )
    forbidden_enumeration = re.compile(
        r'(Vary[^.]*across\s+the\s+\d+\s+images?\s*[:：]|image\s*1\b[^.]*?image\s*2\b)', re.I
    )

    # CHAR基準画像定義の行範囲を特定（### CHAR-XX: から次の ### or ASSET- まで）
    char_def_ranges = []
    for i, line in enumerate(lines):
        if char_definition_header.search(line):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if lines[j].startswith('### ') or '【制作メモ】ASSET-' in lines[j]:
                    end = j
                    break
            char_def_ranges.append((i, end))

    def is_in_char_definition(line_idx):
        return any(s <= line_idx < e for s, e in char_def_ranges)

    blocks = split_into_asset_blocks(lines)
    issues = []
    # まず CHAR基準画像定義内のキャラプロンプトを直接走査
    for s, e in char_def_ranges:
        for idx in range(s, e):
            line = lines[idx]
            if not char_prompt_label.search(line):
                continue
            body_lines = []
            for j in range(idx + 1, min(idx + 31, e)):
                nxt = lines[j]
                if char_prompt_label.search(nxt):
                    break
                if re.search(r'^\s*(背景プロンプト|SE:|編集者指示:|シーン:|→\s*\*\*Google Flow)', nxt):
                    break
                body_lines.append(nxt)
            body_text = ' '.join(body_lines)
            if not body_text.strip():
                continue
            label = line.strip()[:50]
            if required_phrase not in body_text:
                issues.append((idx + 1, f'CHAR定義', label, "CHAR基準画像定義に必須定型句 'each showing only this one character' 欠落"))
            if forbidden_variation_pattern.search(body_text) or forbidden_enumeration.search(body_text):
                issues.append((idx + 1, f'CHAR定義', label, "禁止表現（バリエーション指示文 / image 1..., image 2... 列挙）"))

    # 本編ASSETは「禁止表現」のみチェック（必須定型句は不要）
    for asset_id, start, end, block_lines in blocks:
        for idx, line in enumerate(block_lines):
            actual_line = start + idx
            if is_in_char_definition(actual_line):
                continue
            if not char_prompt_label.search(line):
                continue
            body_lines = []
            for j in range(idx + 1, min(idx + 31, len(block_lines))):
                nxt = block_lines[j]
                if char_prompt_label.search(nxt):
                    break
                if re.search(r'^\s*(背景プロンプト|SE:|編集者指示:|シーン:|→\s*\*\*Google Flow)', nxt):
                    break
                body_lines.append(nxt)
            body_text = ' '.join(body_lines)
            if not body_text.strip():
                continue
            label = line.strip()[:50]
            if forbidden_variation_pattern.search(body_text) or forbidden_enumeration.search(body_text):
                issues.append((actual_line + 1, asset_id, label, "禁止表現（バリエーション指示文 / image 1..., image 2... 列挙）"))
    return issues


def check_no_scene_words_in_char_prompt(lines):
    """キャラ系プロンプトに場所・時間・気象等のシーン状況描写が含まれていないか検証"""
    char_prompt_label = re.compile(r'^\s*(キャラプロンプト|キャラアニメーション|キャラ流用|キャラ静止画)[①②③④⑤1-5]?[（(]?')
    # 禁止語句リスト（小文字で検出）
    forbidden_patterns = [
        re.compile(r'\boutdoors?\b', re.I),
        re.compile(r'\bindoors?\b', re.I),
        re.compile(r'\bat night\b', re.I),
        re.compile(r'\bat dawn\b', re.I),
        re.compile(r'\bin the morning\b', re.I),
        re.compile(r'\bat sunset\b', re.I),
        re.compile(r'\blate evening\b', re.I),
        re.compile(r'\bat the (police station|hospital|station|counter)\b', re.I),
        re.compile(r'\bat a reception counter\b', re.I),
        re.compile(r'\bin (the|her|his) home\b', re.I),
        re.compile(r'\bon a mountain\b', re.I),
        re.compile(r'\bin the (forest|rain|snow|wind)\b', re.I),
        re.compile(r'\bunder (snow|bright sunlight)\b', re.I),
    ]
    blocks = split_into_asset_blocks(lines)
    issues = []
    for asset_id, start, end, block_lines in blocks:
        for idx, line in enumerate(block_lines):
            if not char_prompt_label.search(line):
                continue
            body_lines = []
            for j in range(idx + 1, min(idx + 31, len(block_lines))):
                nxt = block_lines[j]
                if char_prompt_label.search(nxt):
                    break
                if re.search(r'^\s*(背景プロンプト|SE:|編集者指示:|シーン:|→\s*\*\*Google Flow)', nxt):
                    break
                body_lines.append(nxt)
            body_text = ' '.join(body_lines)
            if not body_text.strip():
                continue
            for pat in forbidden_patterns:
                m = pat.search(body_text)
                if m:
                    actual_line = start + idx + 1
                    label = line.strip()[:50]
                    issues.append((actual_line, asset_id, label, m.group(0)))
                    break  # 同じブロック内で1件検出で次へ
    return issues


def check_background_generate_clause(lines):
    """背景プロンプトの末尾に `Generate N separate images.` 定型句が含まれているか検証"""
    bg_label = re.compile(r'^\s*背景プロンプト[（(]')
    required_pattern = re.compile(r'Generate\s+\d+\s+separate\s+images?\.', re.I)
    blocks = split_into_asset_blocks(lines)
    issues = []
    for asset_id, start, end, block_lines in blocks:
        for idx, line in enumerate(block_lines):
            if not bg_label.search(line):
                continue
            body_lines = []
            for j in range(idx + 1, min(idx + 31, len(block_lines))):
                nxt = block_lines[j]
                if re.search(r'^\s*(キャラプロンプト|キャラアニメーション|キャラ流用|キャラ静止画|SE:|編集者指示:|シーン:|→\s*\*\*Google Flow)', nxt):
                    break
                body_lines.append(nxt)
            body_text = ' '.join(body_lines)
            if not body_text.strip():
                continue
            if not required_pattern.search(body_text):
                actual_line = start + idx + 1
                issues.append((actual_line, asset_id, "背景プロンプト末尾 `Generate N separate images.` 欠落"))
    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_prompts.py <台本ファイルパス> [台本Master.mdパス]")
        sys.exit(1)

    filepath = sys.argv[1]
    master_path = sys.argv[2] if len(sys.argv) >= 3 else None
    if not Path(filepath).exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    lines = load_file(filepath)

    all_pass = True
    warnings = 0

    print("=" * 60)
    print(f"Yama プロンプト品質バリデーション: {Path(filepath).name}")
    print("=" * 60)

    # 1. ナレーター:プレフィックス
    issues = check_narrator_prefix(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: ナレーター:プレフィックス欠落 ({len(issues)}件)")
        for ln, text in issues[:5]:
            print(f"   L{ln}: {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("\n✅ PASS: ナレーター:プレフィックス")

    # 2. 禁止ワード
    issues = check_forbidden_words_in_prompts(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: プロンプト内禁止ワード ({len(issues)}件)")
        for ln, cat, word, text in issues[:5]:
            print(f"   L{ln}: [{cat}] '{word}' — {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: プロンプト内禁止ワード")

    # 3. Generate表現
    issues = check_generate_wording(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 'Generate 5 images.' separateなし ({len(issues)}件)")
        for ln, text in issues[:3]:
            print(f"   L{ln}: {text}")
    else:
        print("✅ PASS: Generate表現")

    # 4. 地名チェック
    issues = check_location_in_prompts(lines)
    if issues:
        warnings += len(issues)
        print(f"\n⚠️  WARNING: 地名なし背景プロンプト ({len(issues)}件)")
        for ln, asset, text in issues[:5]:
            print(f"   L{ln} ({asset}): {text}")
    else:
        print("✅ PASS: 地名チェック")

    # 5. 安全ワード
    issues = check_safety_words(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 安全ワード違反 ({len(issues)}件)")
        for ln, word, text in issues:
            print(f"   L{ln}: '{word}' — {text}")
    else:
        print("✅ PASS: 安全ワード")

    # 6. カメラ専門用語
    issues = check_camera_terms(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: カメラ専門用語 ({len(issues)}件)")
        for ln, term, repl in issues:
            print(f"   L{ln}: '{term}' → '{repl}'")
    else:
        print("✅ PASS: カメラ専門用語")

    # 7. CHAR参照タグ
    issues = check_char_tags(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: CHAR参照タグ 初出/再利用なし ({len(issues)}件)")
        for ln, matches, text in issues[:5]:
            print(f"   L{ln}: {matches}")
    else:
        print("✅ PASS: CHAR参照タグ")

    # 8. 複数キャラCHAR矛盾チェック
    issues = check_char_multi_conflict(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 複数キャラCHARに 'only this one character' ({len(issues)}件)")
        for ln, msg, text in issues:
            print(f"   L{ln}: {msg}")
            print(f"         {text}")
    else:
        print("✅ PASS: 複数キャラCHAR整合性")

    # 9. CHAR番号1回使用（名前なし人物の可能性）
    issues = check_char_single_use(lines)
    if issues:
        warnings += len(issues)
        print(f"\n⚠️  WARNING: CHAR番号が1回しか使われていない ({len(issues)}件)")
        print(f"   名前のない人物にCHAR番号を振っていませんか？名前なし人物は [Generic group] を使用してください")
        for num, ln in issues[:5]:
            print(f"   CHAR-{num}: L{ln}のみ（再利用なし）")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: CHAR番号再利用")

    # 10. キャラプロンプト環境混入
    issues = check_char_environment(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: キャラプロンプト(1:1)に環境・構図要素 ({len(issues)}件)")
        for ln, matches, text in issues[:5]:
            print(f"   L{ln}: {matches}")
            print(f"         {text}")
    else:
        print("✅ PASS: キャラプロンプト環境要素")

    # 11. キャラプロンプト全身チェック
    issues = check_char_fullbody(lines)
    if issues:
        all_pass = False
        prohibited_count = sum(1 for x in issues if x[2] == 'prohibited')
        missing_count = sum(1 for x in issues if x[2] == 'missing_fullbody')
        print(f"\n❌ FAIL: キャラプロンプト全身ルール違反 ({len(issues)}件: 禁止語{prohibited_count}, Full body欠落{missing_count})")
        for ln, asset, kind, found, text in issues[:5]:
            if kind == 'prohibited':
                print(f"   L{ln} ({asset}): 禁止語 {found}")
            else:
                print(f"   L{ln} ({asset}): 'Full body' が含まれていません")
            print(f"         {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: キャラプロンプト全身ルール")

    # 12. 1ナレーション複数アセット
    issues = check_multi_asset_per_narration(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 1ナレーションに複数アセット紐づき ({len(issues)}件)")
        for ln, text, count, assets in issues[:5]:
            print(f"   L{ln}: {text}")
            print(f"   → {count}アセット紐づき: {', '.join(assets)}")
            print(f"   → ナレーションを分割して各アセットに1文ずつ対応させる")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 1ナレーション=1アセット")

    # 13. 孤立アセット（ナレーションなし）
    issues = check_orphan_assets(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 孤立アセット（ナレーション紐づきなし） ({len(issues)}件)")
        for ln, asset_id, text in issues[:5]:
            print(f"   L{ln}: {asset_id} — 直前にナレーター行がありません")
            print(f"   → ナレーションを追加して紐づけるか、アセットを削除する")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 孤立アセットなし")

    # 14. ナレーター行連続チェック
    # シーン単位グルーピング版ではASSET1つに複数ナレーション行が紐づくのが正常
    # → 制作メモ(ASSET)を跨いでナレーション行が連続するケースのみ検出
    is_scene_grouped = 'シーン単位グルーピング版' in ''.join(lines[:10])
    if is_scene_grouped:
        print("✅ PASS: ナレーター行配置（シーン単位グルーピング — 連続ナレーターは正常）")
    else:
        issues = check_narrator_consecutive(lines)
        if issues:
            all_pass = False
            print(f"\n❌ FAIL: ナレーター行2行以上連続 ({len(issues)}件)")
            for ln1, text1, ln2, text2 in issues[:5]:
                print(f"   L{ln1}: {text1}")
                print(f"   L{ln2}: {text2}")
                print(f"   → 各行の間に制作メモ+プロンプトを挿入して交互配置にする")
            if len(issues) > 5:
                print(f"   ...他{len(issues)-5}件")
        else:
            print("✅ PASS: ナレーター行交互配置")

    # 12. 静止画ナレーション文字数チェック
    issues = check_static_narration_length(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 静止画アセットのナレーション25文字超過 ({len(issues)}件)")
        for narr_ln, char_count, asset_id, asset_ln, text in issues[:5]:
            print(f"   L{narr_ln}: {char_count}字 → {asset_id} (L{asset_ln}) [静止画]")
            print(f"   ナレーション: {text}")
            print(f"   → キャラアニメーション or 動画に変更し制作メモも書き直す")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 静止画ナレーション文字数")

    # 13. 静止画連続
    max_cons, runs = check_static_consecutive(lines)
    if max_cons >= 3:
        all_pass = False
        print(f"\n❌ FAIL: 静止画{max_cons}連続 ({len(runs)}箇所)")
        for run in runs[:3]:
            print(f"   {run[0][1][:50]}... ({len(run)}連続)")
    else:
        print(f"✅ PASS: 静止画連続 (最大{max_cons})")

    # 14. 映像密度
    total_chars, total_assets, avg = check_density(lines)
    # シーン単位グルーピング版は1ASSET複数ナレーション行のため閾値が異なる
    density_fail = 200 if is_scene_grouped else 50
    density_warn = 150 if is_scene_grouped else 35
    if avg > density_fail:
        all_pass = False
        print(f"\n❌ FAIL: 映像密度 {avg:.1f}字/ASSET (上限{density_fail})")
    elif avg > density_warn:
        warnings += 1
        print(f"\n⚠️  WARNING: 映像密度 {avg:.1f}字/ASSET (推奨{density_warn}以下)")
    else:
        print(f"✅ PASS: 映像密度 {avg:.1f}字/ASSET ({total_chars}字/{total_assets}ASSET)")

    # 15. 台本突合チェック（第2引数に台本パスが指定された場合のみ）
    if master_path:
        missing, total_master = check_narration_coverage(lines, master_path)
        if missing:
            all_pass = False
            covered = total_master - len(missing)
            print(f"\n❌ FAIL: 台本突合チェック — {len(missing)}行が欠落 ({covered}/{total_master}行カバー)")
            for ln, text in missing[:10]:
                print(f"   台本L{ln}: {text[:60]}...")
            if len(missing) > 10:
                print(f"   ...他{len(missing)-10}件")
            print(f"   → fix_asset_narration.py で自動修正するか、手動で追加してください")
        else:
            print(f"✅ PASS: 台本突合チェック ({total_master}/{total_master}行カバー)")
    else:
        print("⏭️  SKIP: 台本突合チェック（第2引数に台本パスを指定すると実行）")

    # 16. ASSET構造順序チェック（ナレーター→制作メモ→プロンプト）— FAIL判定
    issues = check_asset_structure_order(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: ASSET構造順序 — {len(issues)}件で【制作メモ】の前にナレーターなし")
        for ln, aid in issues[:5]:
            print(f"   L{ln} ({aid})")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
        print(f"   → 正しい順序: ナレーター → 【制作メモ】→ シーン: → プロンプト → 編集者指示")
    else:
        print("✅ PASS: ASSET構造順序（ナレーター→制作メモ→プロンプト）")

    # 18. シーン行必須チェック — 全ASSETに「シーン:」行があるか
    scene_missing = check_scene_line_required(lines)
    if scene_missing:
        all_pass = False
        print(f"\n❌ FAIL: シーン行欠落 — {len(scene_missing)}件で「シーン:」行なし")
        for ln, aid in scene_missing[:5]:
            print(f"   L{ln} ({aid})")
        if len(scene_missing) > 5:
            print(f"   ...他{len(scene_missing)-5}件")
        print(f"   → 全ASSETに「シーン: <日本語でシーン説明>」行が必須です")
    else:
        print("✅ PASS: シーン行（全ASSETに「シーン:」あり）")

    # 19. Google Earthプロンプト禁止チェック
    ge_issues = check_google_earth_no_prompt(lines)
    if ge_issues:
        all_pass = False
        print(f"\n❌ FAIL: Google Earthプロンプト禁止 — {len(ge_issues)}件で```ブロック検出")
        for ln, aid in ge_issues[:5]:
            print(f"   L{ln} ({aid})")
        if len(ge_issues) > 5:
            print(f"   ...他{len(ge_issues)-5}件")
        print(f"   → [Google Earth]は座標+カメラ指示のみ。Lovart用プロンプト(```)は禁止")
    else:
        print("✅ PASS: Google Earthプロンプト禁止（```ブロックなし）")

    # 17. 末尾ゴミ行チェック
    issues = check_trailing_garbage(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 末尾ゴミ行 ({len(issues)}件)")
        for ln, desc in issues:
            print(f"   L{ln}: {desc}")
    else:
        print("✅ PASS: 末尾ゴミ行なし")

    # 18. 背景プロンプト人物矛盾
    issues = check_background_people_contradiction(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 背景プロンプト人物矛盾 ({len(issues)}件)")
        print(f"   「No people visible」と人物描写が同居しています")
        for ln, asset, words, text in issues[:5]:
            print(f"   L{ln} ({asset}): 検出語={words}")
            print(f"         {text}")
        if len(issues) > 5:
            print(f"   ...他{len(issues)-5}件")
    else:
        print("✅ PASS: 背景プロンプト人物矛盾なし")

    # 21. 【AI動画】2ブロック整合性
    issues = check_video_prompt_two_blocks(lines)
    if issues:
        all_pass = False
        print(f"\n❌ FAIL: 【AI動画】2ブロック構成違反 ({len(issues)}件)")
        print(f"   Google Flow動画プロンプトが欠落しているASSET:")
        for ln, asset, msg in issues[:10]:
            print(f"   L{ln} ({asset}): {msg}")
        if len(issues) > 10:
            print(f"   ...他{len(issues)-10}件")
    else:
        print("✅ PASS: 【AI動画】2ブロック構成")

    # 22. キャラ系プロンプト比率
    result = check_character_prompt_ratio(lines)
    if result[0] is not None:
        verdict, char_count, total, ratio = result
        if verdict == 'PASS':
            print(f"✅ PASS: キャラ系プロンプト比率 ({char_count}/{total} = {ratio:.1f}%)")
        elif verdict in ('WARNING', 'WARNING_STRONG'):
            warnings += 1
            label = '⚠️  WARNING' if verdict == 'WARNING' else '⚠️  WARNING(強)'
            print(f"\n{label}: キャラ系プロンプト比率 ({char_count}/{total} = {ratio:.1f}%)")
            print(f"   目標60%以上。背景静止画偏重の可能性。リファレンス羅臼岳=72.8%")
        else:  # FAIL
            all_pass = False
            print(f"\n❌ FAIL: キャラ系プロンプト比率 ({char_count}/{total} = {ratio:.1f}%)")
            print(f"   30%未満。解説調になりすぎ。台本全体の人物配置設計を見直し")

    # 23. キャラプロンプト固定スタイルヘッダー
    issues = check_character_style_header(lines)
    if issues:
        warnings += 1
        print(f"\n⚠️  WARNING: キャラプロンプト固定スタイルヘッダー欠落 ({len(issues)}件)")
        print(f"   必須6要素: Cute cartoon character design / thick black outlines / flat cel-shaded colors")
        print(f"             / large expressive eyes / slightly chibi proportions / children's animation style")
        for ln, asset, label, missing in issues[:10]:
            print(f"   L{ln} ({asset}) [{label}] 欠落: {missing}")
        if len(issues) > 10:
            print(f"   ...他{len(issues)-10}件")
    else:
        print("✅ PASS: キャラプロンプト固定スタイルヘッダー")

    # 24. Generate指示の使い分け（CHAR定義のみ必須・本編は禁止表現のみチェック）
    issues = check_one_character_per_image_clause(lines)
    if issues:
        warnings += 1
        print(f"\n⚠️  WARNING: Generate指示の使い分け違反 ({len(issues)}件)")
        print(f"   CHAR基準画像定義: 'Generate N separate images, each showing only this one character.' 必須")
        print(f"   本編ASSET: 'Generate N separate images.' のみで可")
        print(f"   禁止表現（全プロンプト共通）: バリエーション指示文 / image 1..., image 2... 列挙")
        for ln, asset, label, msg in issues[:10]:
            print(f"   L{ln} ({asset}) [{label}]: {msg}")
        if len(issues) > 10:
            print(f"   ...他{len(issues)-10}件")
    else:
        print("✅ PASS: Generate指示の使い分け")

    # 25. キャラプロンプトにシーン状況描写禁止
    issues = check_no_scene_words_in_char_prompt(lines)
    if issues:
        warnings += 1
        print(f"\n⚠️  WARNING: キャラプロンプトにシーン状況描写混入 ({len(issues)}件)")
        print(f"   禁止語例: outdoors / indoors / at night / at the police station / in the rain 等")
        print(f"   これらが white background を上書きして余計な背景が混入します")
        for ln, asset, label, word in issues[:10]:
            print(f"   L{ln} ({asset}) [{label}] 検出: '{word}'")
        if len(issues) > 10:
            print(f"   ...他{len(issues)-10}件")
    else:
        print("✅ PASS: キャラプロンプトにシーン状況描写なし")

    # 26. 背景プロンプト末尾Generate指示
    issues = check_background_generate_clause(lines)
    if issues:
        warnings += 1
        print(f"\n⚠️  WARNING: 背景プロンプト末尾Generate指示欠落 ({len(issues)}件)")
        print(f"   必須: 'Generate N separate images.' (無いと1枚しか生成されない)")
        for ln, asset, msg in issues[:10]:
            print(f"   L{ln} ({asset}): {msg}")
        if len(issues) > 10:
            print(f"   ...他{len(issues)-10}件")
    else:
        print("✅ PASS: 背景プロンプト末尾Generate指示")

    # Summary
    print("\n" + "=" * 60)
    if all_pass and warnings == 0:
        print("結果: ✅ ALL PASS")
        sys.exit(0)
    elif all_pass:
        print(f"結果: ⚠️  PASS (WARNING {warnings}件)")
        sys.exit(0)
    else:
        print("結果: ❌ FAIL — 修正が必要です")
        sys.exit(1)


if __name__ == '__main__':
    main()
