#!/usr/bin/env python3
"""編集用素材台本から、プロンプトを除いた編集者用台本を書き出す。"""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


SOURCE_NAME = "編集用素材台本.md"
REPEATED_HEADING = "## 1. 全素材リスト（台本順）"
KIND_BULLET_RE = re.compile(r"^\s*-\s*【[^】]+】")
SENTENCE_RE = re.compile(r"[^。！？!?]*(?:[。！？!?]|$)")
DISCLAIMER_TERMS = ("推測", "推定", "断り書き", "但し書き", "非公表", "断定")
DISPLAY_TERMS = ("表示", "添え", "テロップ", "字幕", "画面に", "画面の", "常時")
DISCLAIMER_FORM_TERMS = ("旨", "あくまで", "断り書き", "但し書き", "注記", "資料からの")
NEGATIVE_DISPLAY_TERMS = ("出さない", "表示しない", "表示しなく", "入れない")
DEPENDENT_CLAUSE_RE = re.compile(
    r"^(?:ここから|以後|そのまま|引き続き).*(?:出し|表示|維持)"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="作品フォルダの編集用素材台本から編集者用台本を作ります。"
    )
    parser.add_argument("work_folder", type=Path, help="作品フォルダ")
    parser.add_argument("--name", required=True, help="出力フォルダに使う短い作品名")
    return parser.parse_args()


def is_display_disclaimer(clause: str) -> bool:
    return (
        any(term in clause for term in DISCLAIMER_TERMS)
        and any(term in clause for term in DISPLAY_TERMS)
        and any(term in clause for term in DISCLAIMER_FORM_TERMS)
        and not any(term in clause for term in NEGATIVE_DISPLAY_TERMS)
    )


def remove_display_disclaimers(instruction: str) -> tuple[str, int]:
    """画面に断り書きを出す部分だけを文・節単位で除去する。"""
    kept_sentences: list[str] = []
    removed_count = 0

    for sentence in SENTENCE_RE.findall(instruction):
        if not sentence:
            continue
        clauses = sentence.split("、")
        kept_clauses: list[str] = []
        removed_in_sentence = False

        for clause in clauses:
            stripped = clause.strip()
            if not stripped:
                continue
            if is_display_disclaimer(stripped):
                removed_in_sentence = True
                while kept_clauses and (
                    kept_clauses[-1].endswith(("であり", "である", "ため", "ので"))
                    or any(term in kept_clauses[-1] for term in DISCLAIMER_TERMS)
                ):
                    kept_clauses.pop()
                continue
            if removed_in_sentence and DEPENDENT_CLAUSE_RE.search(stripped):
                continue
            kept_clauses.append(stripped)

        if removed_in_sentence:
            removed_count += 1
        if kept_clauses:
            kept_sentence = "、".join(kept_clauses)
            if not re.search(r"[。！？!?]$", kept_sentence):
                if kept_sentence.endswith("置き"):
                    kept_sentence = kept_sentence[:-1] + "く"
                kept_sentence += "。"
            kept_sentences.append(kept_sentence)

    cleaned = "".join(kept_sentences).strip(" 、")
    return cleaned, removed_count


def export_text(source_text: str, work_name: str) -> tuple[str, int, int]:
    output_lines = [f"# {work_name} 編集者用台本", ""]
    in_code_block = False
    removed_disclaimers = 0
    removed_instruction_lines = 0

    for raw_line in source_text.splitlines():
        stripped = raw_line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if stripped == REPEATED_HEADING:
            continue
        if "プロンプト" in stripped:
            continue
        if KIND_BULLET_RE.match(stripped):
            continue

        if stripped.startswith("→ 編集者指示:"):
            prefix = "→ 編集者指示:"
            instruction = stripped[len(prefix) :].strip()
            instruction, removed = remove_display_disclaimers(instruction)
            removed_disclaimers += removed
            if not instruction:
                removed_instruction_lines += 1
                continue
            raw_line = f"{prefix} {instruction}"

        output_lines.append(raw_line.rstrip())

    if in_code_block:
        raise ValueError("コードブロックが閉じられていません")

    compacted: list[str] = []
    for line in output_lines:
        if line == "" and compacted and compacted[-1] == "":
            continue
        compacted.append(line)

    while compacted and compacted[-1] == "":
        compacted.pop()
    return "\n".join(compacted) + "\n", removed_disclaimers, removed_instruction_lines


def main() -> int:
    args = parse_args()
    work_folder = args.work_folder.expanduser().resolve()
    source = work_folder / SOURCE_NAME
    if not work_folder.is_dir():
        raise SystemExit(f"作品フォルダが見つかりません: {work_folder}")
    if not source.is_file():
        raise SystemExit(f"入力ファイルが見つかりません: {source}")

    source_text = source.read_text(encoding="utf-8")
    exported, removed_disclaimers, removed_lines = export_text(
        source_text, work_folder.name
    )

    output_dir = Path.home() / "Desktop" / f"{args.name}_編集者用台本_{date.today():%Y%m%d}"
    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_path = output_dir / "編集者用台本.md"
    text_path = output_dir / "編集者用台本.txt"
    markdown_path.write_text(exported, encoding="utf-8")
    text_path.write_text(exported, encoding="utf-8")

    print(f"入力: {source}")
    print(f"出力: {markdown_path}")
    print(f"出力: {text_path}")
    print(f"断り書き削除: {removed_disclaimers}件")
    print(f"断り書きだけの編集者指示を削除: {removed_lines}行")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
