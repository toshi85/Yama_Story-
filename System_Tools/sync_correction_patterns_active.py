#!/usr/bin/env python3
"""Correction_Patterns.md の執筆用要約を同期する。"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


YAMA_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = YAMA_ROOT.parent
SOURCE = YAMA_ROOT / "Correction_Patterns.md"
TARGET = YAMA_ROOT / "Correction_Patterns_Active.md"
MARKER = "\n## Patterns\n"


def render(source: str) -> str:
    if MARKER not in source:
        raise ValueError(f"区切り {MARKER.strip()!r} が正本にありません")
    summary = source.split(MARKER, 1)[0].rstrip() + "\n"
    summary_ids = set(re.findall(r"YCP-\d{3}", summary))
    promoted_ids = set()
    for block in re.split(r"(?=^### YCP-\d{3}(?::| ))", source, flags=re.MULTILINE):
        heading = re.match(r"### (YCP-\d{3})(?::| )", block)
        if heading and re.search(r"\*\*status\*\*:\s*promoted\b", block):
            promoted_ids.add(heading.group(1))
    missing = sorted(promoted_ids - summary_ids)
    if missing:
        raise ValueError("Promoted Summary に昇格済みルールがありません: " + ", ".join(missing))
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
    summary = summary.replace(
        "# Yama_Story Correction Patterns（ユーザー修正学習DB）",
        "# Yama_Story Correction Patterns（執筆用・現役ルール）",
        1,
    )
    summary = summary.replace(
        "`/learn-from-corrections` が自動更新するパターン集。",
        "執筆時に読む軽量版。正本と詳細な根拠・実例は "
        "[`Correction_Patterns.md`](Correction_Patterns.md) に保存する。\n\n"
        "> このファイルは自動生成。ルールの追加・昇格は正本で行う。\n\n"
        f"> 正本SHA256: `{source_hash}`",
        1,
    )
    summary = summary.replace("## Promoted Summary (TOP 5)", "## Promoted Summary", 1)
    summary = summary.replace(
        "> ライターはこのセクションだけ読めばOK。全文は不要。",
        "> ライターはこの一覧だけ読めばよい。詳細履歴は、根拠や過去例の確認が必要な場合だけ正本を参照する。",
        1,
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="同期状態だけ検査する")
    args = parser.parse_args()

    expected = render(SOURCE.read_text(encoding="utf-8"))
    current = TARGET.read_text(encoding="utf-8") if TARGET.exists() else None
    if current == expected:
        print(f"PASS: {TARGET.relative_to(PROJECT_ROOT)} は最新です")
        return 0
    if args.check:
        print(f"FAIL: {TARGET.relative_to(PROJECT_ROOT)} は正本と不一致です")
        return 1
    TARGET.write_text(expected, encoding="utf-8")
    print(f"UPDATED: {TARGET.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
