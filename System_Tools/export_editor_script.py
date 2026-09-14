#!/usr/bin/env python3
"""Asset_Prompts_Full.md から編集者向けの日本語台本を出力する。"""

from __future__ import annotations

import argparse
from pathlib import Path
import re


CHARACTER_SECTION = "## キャラ基準画像"
ASSET_LIST_SECTION = "## 1. 全素材リスト"
EARTH_PREFIXES = (
    "検索座標:",
    "カメラ高度:",
    "カメラ角度:",
    "向き:",
    "構図:",
    "書き出し:",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="画像プロンプトを除いた編集者用台本を生成します。"
    )
    parser.add_argument("input", type=Path, help="Asset_Prompts_Full.md のパス")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力先（省略時は入力と同じフォルダの 編集者用台本.md）",
    )
    return parser.parse_args()


def collapse_blank_lines(lines: list[str]) -> list[str]:
    collapsed: list[str] = []
    previous_was_blank = False
    for line in lines:
        is_blank = not line.strip()
        if is_blank and previous_was_blank:
            continue
        collapsed.append("" if is_blank else line)
        previous_was_blank = is_blank
    while collapsed and not collapsed[-1]:
        collapsed.pop()
    return collapsed


def export_editor_script(source: str) -> str:
    lines = source.splitlines()
    character_index = next(
        (i for i, line in enumerate(lines) if line.startswith(CHARACTER_SECTION)), None
    )
    asset_list_index = next(
        (i for i, line in enumerate(lines) if line.startswith(ASSET_LIST_SECTION)), None
    )
    if character_index is None or asset_list_index is None:
        raise ValueError("必須見出し（キャラ基準画像／全素材リスト）が見つかりません。")
    if character_index >= asset_list_index:
        raise ValueError("必須見出しの順序が不正です。")

    output_lines = lines[:character_index]
    output_lines.append(lines[asset_list_index])

    in_fence = False
    for line in lines[asset_list_index + 1 :]:
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        keep = (
            not line.strip()
            or line == "---"
            or line.startswith("ナレーター:")
            or line.startswith("【制作メモ】")
            or line.startswith("シーン:")
            or line.startswith("→ ")
            or line.startswith(EARTH_PREFIXES)
        )
        if keep:
            output_lines.append(line)

    if in_fence:
        raise ValueError("閉じられていないコードフェンスがあります。")

    result = "\n".join(collapse_blank_lines(output_lines)) + "\n"
    result = result.replace("画像プロンプト（結合版）", "編集者用台本（プロンプトなし）")
    result = result.replace(
        "ナレーション1行 = 1アセット ／ ASSET-001〜298",
        "ナレーション1行 = 1アセット ／ ASSET-001〜298\n"
        "素材ファイル名はアセット番号（ASSET-NNN.png / .mp4）と一致。生成用の英文プロンプトはこの台本から省いてある。",
    )
    return result


def main() -> None:
    args = parse_args()
    output_path = args.output or args.input.with_name("編集者用台本.md")
    source = args.input.read_text(encoding="utf-8")
    result = export_editor_script(source)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(result, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
