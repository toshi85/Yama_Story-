#!/usr/bin/env python3
"""
Yama Story 5秒ルール物理バリデータ
==================================
Full.md / 台本.txt の映像密度を物理チェック。

チェック項目:
  1. 静止画ASSET: ナレーション ≤25文字
  2. 動画/アニメ/GE ASSET: ナレーション ≤50文字
  3. 全体平均: ≤35文字/ASSET
  4. 連続静止画: 3枚以上連続禁止
  5. 動画/アニメ/GE比率: 50%以上

使い方:
  python3 Yama_Story/System_Tools/validate_yama_density.py <file_path>
"""
import sys
import os
import re


# === 定数 ===
STATIC_LIMIT = 25       # 静止画の文字数上限
VIDEO_LIMIT = 50         # 動画/アニメ/GEの文字数上限
AVG_LIMIT = 35           # 全体平均の文字数上限
MAX_CONSECUTIVE_STATIC = 2  # 連続静止画の上限
MIN_DYNAMIC_RATIO = 0.50    # 動的素材の最低比率

# 素材タイプ分類
DYNAMIC_TYPES = {"AI動画", "キャラアニメーション", "Google Earth"}
STATIC_TYPES = {"背景静止画"}


def classify_asset(line):
    """制作メモの行からアセットタイプを判定"""
    if "Google Earth" in line or "【Google Earth】" in line:
        return "Google Earth"
    elif "AI動画" in line or "【AI動画】" in line:
        return "AI動画"
    elif "キャラアニメーション" in line or "【キャラアニメーション】" in line:
        return "キャラアニメーション"
    elif "背景静止画" in line or "【背景静止画】" in line:
        return "背景静止画"
    return None


def extract_narration_chars(text):
    """ナレーション文字数をカウント（ナレーター:プレフィックスを除く）"""
    chars = 0
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        # ナレーター: プレフィックスを除去
        if line.startswith("ナレーター:"):
            line = line[len("ナレーター:"):].strip()
        elif line.startswith("ナレーター："):
            line = line[len("ナレーター："):].strip()
        # 制作メモ・見出し・コメント・編集者指示はスキップ
        if line.startswith("【") or line.startswith("#") or line.startswith("<!--"):
            continue
        if line.startswith("→") or line.startswith("->"):
            continue
        if line.startswith("|") or line.startswith("---") or line.startswith("*"):
            continue
        if line.startswith("[CHAR-"):
            continue
        chars += len(line)
    return chars


def parse_assets(file_path):
    """
    Full.md/台本.txtからアセットとナレーションの対応を抽出。

    Returns:
        list of dict: [{type, narration_chars, narration_text, line_num}, ...]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    assets = []
    current_narration = []
    current_asset_type = None
    in_production_note = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 制作メモブロック開始
        if stripped == "【制作メモ】":
            in_production_note = True
            continue

        # 制作メモブロック内のアセットタイプ検出
        if in_production_note:
            asset_type = classify_asset(stripped)
            if asset_type:
                # 前のナレーション蓄積をこのアセットに紐付け
                narr_text = '\n'.join(current_narration)
                narr_chars = extract_narration_chars(narr_text)
                assets.append({
                    'type': asset_type,
                    'narration_chars': narr_chars,
                    'narration_text': narr_text.strip(),
                    'line_num': i,
                })
                current_narration = []
                current_asset_type = asset_type
                continue

            # 制作メモブロック内の他の行（編集者指示、音効など）はスキップ
            if stripped.startswith("→") or stripped.startswith("【音効】") or stripped.startswith("【演出】") or stripped.startswith("【SE】") or stripped.startswith("【画面エフェクト】"):
                continue
            # 空行で制作メモブロック終了
            if not stripped:
                in_production_note = False
                continue
            # 制作メモ内のその他行はスキップ
            continue

        # 通常のナレーション行を蓄積
        if stripped and not stripped.startswith("#") and not stripped.startswith("<!--") and not stripped.startswith("|") and not stripped.startswith("---") and not stripped.startswith("*"):
            current_narration.append(stripped)
        elif not stripped:
            # 空行は区切りだが蓄積は継続
            pass

    return assets


def validate(file_path):
    """5秒ルールのバリデーション実行"""
    print(f"[5秒ルール] Validating: {os.path.basename(file_path)}")
    print("=" * 60)

    assets = parse_assets(file_path)

    if not assets:
        print("  ASSET が見つかりません。Full.md形式で制作メモが含まれていますか？")
        sys.exit(1)

    total_assets = len(assets)
    total_chars = sum(a['narration_chars'] for a in assets)
    avg_chars = total_chars / total_assets if total_assets > 0 else 0

    # --- 集計 ---
    type_counts = {}
    for a in assets:
        type_counts[a['type']] = type_counts.get(a['type'], 0) + 1

    dynamic_count = sum(type_counts.get(t, 0) for t in DYNAMIC_TYPES)
    static_count = sum(type_counts.get(t, 0) for t in STATIC_TYPES)
    dynamic_ratio = dynamic_count / total_assets if total_assets > 0 else 0

    # --- 表示: 概要 ---
    print(f"\n  総ASSET数: {total_assets}")
    print(f"  総ナレーション文字数: {total_chars}")
    print(f"  平均文字数/ASSET: {avg_chars:.1f} (上限: {AVG_LIMIT})")
    print(f"  推定動画長: {total_chars / 6:.0f}〜{total_chars / 4.5:.0f}秒 ({total_chars / 6 / 60:.1f}〜{total_chars / 4.5 / 60:.1f}分)")
    print()

    for t, c in sorted(type_counts.items()):
        pct = c / total_assets * 100
        print(f"  {t}: {c} ({pct:.0f}%)")
    print(f"  動的素材合計: {dynamic_count}/{total_assets} = {dynamic_ratio:.0%} (基準: 50%以上)")
    print()

    # === チェック1: 個別ASSET文字数 ===
    errors = []
    warnings = []

    for idx, a in enumerate(assets):
        limit = STATIC_LIMIT if a['type'] in STATIC_TYPES else VIDEO_LIMIT
        if a['narration_chars'] > limit:
            severity = "ERROR" if a['narration_chars'] > limit * 1.5 else "WARN"
            msg = f"  [{severity}] ASSET#{idx+1} (L{a['line_num']}) {a['type']}: {a['narration_chars']}字 > {limit}字上限"
            if severity == "ERROR":
                errors.append(msg)
            else:
                warnings.append(msg)

    # === チェック2: 全体平均 ===
    if avg_chars > AVG_LIMIT:
        errors.append(f"  [ERROR] 全体平均 {avg_chars:.1f}字/ASSET > {AVG_LIMIT}字上限 (不足ASSET数: 約{int(total_chars / AVG_LIMIT - total_assets)})")

    # === チェック3: 連続静止画 ===
    consecutive_static = 0
    max_consecutive = 0
    for a in assets:
        if a['type'] in STATIC_TYPES:
            consecutive_static += 1
            max_consecutive = max(max_consecutive, consecutive_static)
        else:
            consecutive_static = 0

    if max_consecutive > MAX_CONSECUTIVE_STATIC:
        errors.append(f"  [ERROR] 連続静止画 {max_consecutive}枚 (上限: {MAX_CONSECUTIVE_STATIC}枚)")

    # === チェック4: 動的素材比率 ===
    if dynamic_ratio < MIN_DYNAMIC_RATIO:
        errors.append(f"  [ERROR] 動的素材比率 {dynamic_ratio:.0%} < {MIN_DYNAMIC_RATIO:.0%}")

    # === 結果表示 ===
    if warnings:
        print(f"  --- 警告 ({len(warnings)}件) ---")
        for w in warnings:
            print(w)
        print()

    if errors:
        print(f"  --- エラー ({len(errors)}件) ---")
        for e in errors:
            print(e)
        print()
        print("[FAILED] 5秒ルール違反が検出されました。")
        sys.exit(1)
    else:
        if warnings:
            print(f"[PASSED with {len(warnings)} warnings] 5秒ルール基本チェック通過。")
        else:
            print("[PASSED] 5秒ルールチェック全項目通過。")
        sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_yama_density.py <file_path>")
        print("  file_path: Yama_Story Full.md or 台本.txt")
        sys.exit(1)

    fp = sys.argv[1]
    if not os.path.exists(fp):
        print(f"File not found: {fp}")
        sys.exit(1)

    validate(fp)
