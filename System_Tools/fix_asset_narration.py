#!/usr/bin/env python3
"""
Asset_Prompts.mdに欠落しているナレーション行を台本から自動補完するスクリプト。

使い方:
  python3 fix_asset_narration.py <asset_prompts.md> <master_script.md>

処理:
1. Master台本から全ナレーション行を行番号付きで抽出
2. Asset_Promptsの各ASSETの「台本Lxx-Lyy」範囲を解析
3. 範囲内のナレーション行が欠落していれば、ASSETの最初のナレーター行の直後に挿入
4. 修正後のファイルを上書き保存
"""

import sys
import re


def extract_narration_lines(master_path):
    """台本から全ナレーション行を {行番号: テキスト} で返す"""
    with open(master_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    narrations = {}
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("ナレーター:"):
            narrations[i + 1] = stripped  # 1-indexed
    return narrations


def parse_asset_ranges(asset_lines):
    """Asset_Promptsの各ASSETの位置と台本L範囲を解析"""
    # Pattern: 【制作メモ】ASSET-XXX [...] 台本Lxx-Lyy or 台本Lxx
    range_pattern = re.compile(r'【制作メモ】(ASSET-\d+)\s+\[.*?\]\s+台本L(\d+)(?:-L(\d+))?')

    assets = []
    for i, line in enumerate(asset_lines):
        match = range_pattern.search(line)
        if match:
            asset_id = match.group(1)
            l_start = int(match.group(2))
            l_end = int(match.group(3)) if match.group(3) else l_start
            assets.append({
                'id': asset_id,
                'line_idx': i,  # 0-indexed line in asset file
                'l_start': l_start,
                'l_end': l_end,
            })
    return assets


def find_narration_insert_point(asset_lines, asset_line_idx):
    """ASSETの制作メモ行の直前にあるナレーター行群の位置を特定し、
    挿入すべき位置（制作メモ行の直前）を返す"""
    # 制作メモの直前を探す（ナレーター行があるはず）
    # 挿入位置 = 制作メモ行の直前（空行の前）
    insert_idx = asset_line_idx
    # 制作メモ行の上を遡って、最初の空行またはナレーター行を見つける
    for j in range(asset_line_idx - 1, -1, -1):
        stripped = asset_lines[j].strip()
        if stripped.startswith("ナレーター:"):
            # このナレーター行の直前に挿入点がある
            # さらに上にナレーター行がないか確認
            insert_idx = j
            continue
        elif stripped == '':
            # 空行 = このASSETブロックの始まり
            insert_idx = j + 1
            break
        else:
            # 他のコンテンツ（前のASSETの一部）
            insert_idx = j + 1
            break
    return insert_idx


def get_existing_narrations_in_asset(asset_lines, asset_start_idx, next_asset_idx):
    """ASSETブロック内に既に存在するナレーション行のテキストセットを返す"""
    existing = set()
    for i in range(asset_start_idx, next_asset_idx):
        stripped = asset_lines[i].strip()
        if stripped.startswith("ナレーター:"):
            existing.add(stripped)
    return existing


def fix_asset_narrations(asset_path, master_path):
    """メイン処理: 欠落ナレーション行を補完"""
    # 1. 台本のナレーション行を全抽出
    master_narrations = extract_narration_lines(master_path)
    print(f"台本ナレーション行数: {len(master_narrations)}")

    # 2. Asset_Promptsを読み込み
    with open(asset_path, 'r', encoding='utf-8') as f:
        asset_lines = f.readlines()

    # 3. ASSET範囲を解析
    assets = parse_asset_ranges(asset_lines)
    print(f"ASSET数: {len(assets)}")

    # 4. 各ASSETの境界を設定（次のASSETの制作メモ行まで or ファイル末尾）
    for i, asset in enumerate(assets):
        if i + 1 < len(assets):
            # 次のASSETの制作メモの前にあるナレーター行も含めるため、
            # 次のASSETブロックの開始位置を探す
            next_memo_idx = assets[i + 1]['line_idx']
            # 次の制作メモの上にあるナレーター行は次のASSETに属する
            # → 次のASSETの最初のナレーター行の位置を見つける
            boundary = next_memo_idx
            for j in range(next_memo_idx - 1, asset['line_idx'], -1):
                stripped = asset_lines[j].strip()
                if stripped.startswith("ナレーター:"):
                    boundary = j
                elif stripped == '':
                    continue
                else:
                    break
            asset['end_idx'] = boundary
        else:
            asset['end_idx'] = len(asset_lines)

    # 5. 欠落チェック & 挿入リスト作成
    insertions = []  # (挿入位置, 挿入テキスト) のリスト
    total_missing = 0

    for asset in assets:
        l_start = asset['l_start']
        l_end = asset['l_end']

        # この範囲のナレーション行を取得
        range_narrations = []
        for line_num in sorted(master_narrations.keys()):
            if l_start <= line_num <= l_end:
                range_narrations.append((line_num, master_narrations[line_num]))

        # 既存のナレーション行を取得
        existing = get_existing_narrations_in_asset(
            asset_lines, asset['line_idx'] - 20, asset['end_idx']
        )
        # もっと広い範囲で探す（制作メモの前のナレーター行も含む）
        search_start = max(0, asset['line_idx'] - 30)
        existing = set()
        for i in range(search_start, min(len(asset_lines), asset['end_idx'])):
            stripped = asset_lines[i].strip()
            if stripped.startswith("ナレーター:"):
                existing.add(stripped)

        # 欠落行を特定
        missing = []
        for line_num, text in range_narrations:
            if text not in existing:
                missing.append((line_num, text))

        if missing:
            total_missing += len(missing)
            print(f"  {asset['id']} (台本L{l_start}-L{l_end}): {len(missing)}行欠落")
            for ln, txt in missing:
                print(f"    L{ln}: {txt[:50]}...")

            # 挿入位置 = 制作メモ行の直前
            insert_at = asset['line_idx']
            # 制作メモ行の直前に空行があればその前に
            if insert_at > 0 and asset_lines[insert_at - 1].strip() == '':
                insert_at = insert_at - 1

            # 挿入テキストを構築（既存のナレーター行の後に追加）
            insert_text = ""
            for ln, txt in missing:
                insert_text += f"\n{txt}\n"

            insertions.append((insert_at, insert_text))

    print(f"\n合計欠落行: {total_missing}")

    if total_missing == 0:
        print("欠落なし。修正不要です。")
        return

    # 6. 挿入を後ろから実行（インデックスがずれないように）
    insertions.sort(key=lambda x: x[0], reverse=True)

    for insert_at, insert_text in insertions:
        # 挿入位置にテキストを追加
        asset_lines.insert(insert_at, insert_text)

    # 7. 保存
    with open(asset_path, 'w', encoding='utf-8') as f:
        f.writelines(asset_lines)

    print(f"\n修正完了: {total_missing}行を追加しました。")

    # 8. 検証
    verify_coverage(asset_path, master_path)


def verify_coverage(asset_path, master_path):
    """修正後の検証: 全ナレーション行がカバーされているか"""
    master_narrations = extract_narration_lines(master_path)

    with open(asset_path, 'r', encoding='utf-8') as f:
        asset_content = f.read()

    missing = []
    for line_num, text in sorted(master_narrations.items()):
        if text not in asset_content:
            missing.append((line_num, text))

    print(f"\n=== 検証結果 ===")
    print(f"台本ナレーション行: {len(master_narrations)}")
    print(f"Asset内に存在: {len(master_narrations) - len(missing)}")
    print(f"欠落: {len(missing)}")

    if missing:
        print("\n欠落行:")
        for ln, txt in missing:
            print(f"  L{ln}: {txt[:60]}...")
    else:
        print("✅ 全ナレーション行がカバーされています。")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 fix_asset_narration.py <asset_prompts.md> <master_script.md>")
        sys.exit(1)

    fix_asset_narrations(sys.argv[1], sys.argv[2])
