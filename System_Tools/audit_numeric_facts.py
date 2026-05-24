#!/usr/bin/env python3
"""
Yama台本の数値ファクト監査スクリプト

背景: 羅臼岳台本で「片道7時間/標高550m」等が事実検証なしに書かれていた事案を受けて新設。
全Master.md/Narration_Only.md/修正版_Master.md から数値ファクト（時間/距離/標高/人数/年齢）を
抽出し、根拠ソース（<!-- src: ... --> コメント等）が付いていない箇所を全件リスト化する。

使い方:
  python3 Yama_Story/System_Tools/audit_numeric_facts.py [対象ファイル or ディレクトリ]
  python3 Yama_Story/System_Tools/audit_numeric_facts.py Yama_Story/Scripts/  # 全件

出力:
  各台本ごとに未検証の数値箇所一覧（ファイル名・行番号・該当行・推奨ソース例）
"""

import re
import sys
from pathlib import Path

# 数値ファクト検出パターン（半角・全角両対応）
NUMERIC_PATTERNS = [
    (r'(\d+|[０-９]+)\s*時間', '時間'),
    (r'(\d+|[０-９]+)\s*分間?(?![値月])', '分'),
    (r'(\d+|[０-９]+)\s*合目', '合目'),
    (r'標高\s*(\d+|[０-９]+|[\d,，]+)', '標高'),
    (r'(\d+|[０-９]+|[\d,，]+)\s*(キロメートル|キロ|km)', '距離'),
    (r'(\d+|[０-９]+|[\d,，]+)\s*メートル(?!以上の)', '距離/標高'),
    (r'(\d+|[０-９]+|[\d,，]+)\s*m(?!in)', 'm'),
    (r'(\d+|[０-９]+)\s*歳', '年齢'),
    (r'(\d+|[０-９]+)\s*代(?!わり|表|理)', '世代'),
    (r'(\d+|[０-９]+)\s*[人名]中', '人数'),
    (r'体長\s*(\d+|[０-９]+|[\d.，,]+)', '体長'),
    (r'体重\s*(\d+|[０-９]+|[\d,，]+)', '体重'),
]

# ソース判定パターン
SRC_PATTERN = re.compile(
    r'(<!--\s*src:|<!--\s*ソース:|\[src:|\[ソース:|\[出典:|\[citation:)',
    re.IGNORECASE
)

# 監査対象ファイル名
TARGET_FILENAMES = {'Master.md', 'Narration_Only.md', '修正版_Master.md'}

# 監査対象行プレフィックス（ナレーション本体・制作メモ）
TARGET_LINE_PREFIX = re.compile(r'(ナレーター[:：]|制作メモ|^##\s)')

# 除外行（ソース行自体・メタデータ）
EXCLUDE_LINE = re.compile(r'^[\s]*<!--|src:|出典:|タイトル候補|YCP-|CHAR-\d+|ASSET-\d+\s+\[')


def find_target_files(target_path: Path) -> list[Path]:
    """対象ファイルを収集"""
    if target_path.is_file():
        return [target_path] if target_path.name in TARGET_FILENAMES else []

    results = []
    for filename in TARGET_FILENAMES:
        results.extend(target_path.rglob(filename))
    return sorted(results)


def has_source_within(lines: list[str], line_index: int, window: int = 3) -> bool:
    """指定行の前後 window 行以内にソースコメント/タグがあるか"""
    start = max(0, line_index - window)
    end = min(len(lines), line_index + window + 1)
    for i in range(start, end):
        if SRC_PATTERN.search(lines[i]):
            return True
    return False


def audit_file(file_path: Path) -> list[dict]:
    """ファイル単体を監査。未検証の数値箇所リストを返す"""
    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        print(f"⚠️  読み込み失敗: {file_path}: {e}", file=sys.stderr)
        return []

    lines = content.splitlines()
    unverified = []

    for idx, line in enumerate(lines):
        # 対象行プレフィックス判定
        if not TARGET_LINE_PREFIX.search(line):
            continue
        # 除外行判定
        if EXCLUDE_LINE.search(line):
            continue

        # 数値ファクト検出
        hit_categories = []
        for pattern, category in NUMERIC_PATTERNS:
            if re.search(pattern, line):
                hit_categories.append(category)

        if not hit_categories:
            continue

        # ソース有無チェック
        if has_source_within(lines, idx, window=3):
            continue

        unverified.append({
            'lineno': idx + 1,
            'line': line.strip()[:120],
            'categories': sorted(set(hit_categories)),
        })

    return unverified


def main():
    target_arg = sys.argv[1] if len(sys.argv) > 1 else 'Yama_Story/Scripts/'
    target_path = Path(target_arg)

    if not target_path.exists():
        print(f"❌ パスが存在しません: {target_path}", file=sys.stderr)
        sys.exit(1)

    files = find_target_files(target_path)
    if not files:
        print(f"❌ 対象ファイルが見つかりません: {target_path}", file=sys.stderr)
        sys.exit(1)

    print(f"📋 監査対象: {len(files)} ファイル\n")

    total_unverified = 0
    files_with_issues = 0

    for file_path in files:
        unverified = audit_file(file_path)
        if not unverified:
            continue

        files_with_issues += 1
        total_unverified += len(unverified)
        print(f"📂 {file_path}")
        print(f"   未検証の数値箇所: {len(unverified)}件")
        for item in unverified[:15]:
            cats = '/'.join(item['categories'])
            print(f"   L{item['lineno']:>5} [{cats}] {item['line']}")
        if len(unverified) > 15:
            print(f"   ...（残り{len(unverified) - 15}件は省略）")
        print()

    print("=" * 60)
    print(f"監査完了: {files_with_issues}/{len(files)} ファイルに未検証数値あり")
    print(f"未検証数値合計: {total_unverified}件")
    print()
    print("対応方法:")
    print("  各数値箇所の同一行 or 前後3行以内に以下のいずれかを追加:")
    print("    <!-- src: 環境省ビジターセンター 2026-05 -->")
    print("    <!-- src: YAMAP コースタイム 2026-05 -->")
    print("    <!-- src: 知床財団 調査報告書 2024 -->")
    print("    [src: デイリー新潮 §6]   ← インラインタグも可")

    sys.exit(0 if total_unverified == 0 else 1)


if __name__ == '__main__':
    main()
