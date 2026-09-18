#!/usr/bin/env python3
"""〔場面〕素材の量から、無駄なく書けるYama台本の長さを見積もる。

較正（2026-09-18）:
  - せたな町の本人確定範囲（§1〜§11前半）は本文1,381字 / 使用した〔場面〕20行
    = 69.05字/素材。
  - Fact_Sheetがある出荷済み台本は、本文字数 / 使用素材数（〔外部〕を除く）が
    八幡平 8,651/126=68.66字、戸沢村 8,869/106=83.67字。
  - 3値のうち低い八幡平の68.66字を、尺を過大評価しない値として採用した。

無印・〔細部〕・〔外部〕は数えない。8,100字（323字/分で約25分）未満はFAIL。
"""
import re
import sys
from dataclasses import dataclass
from pathlib import Path

CHARS_PER_SCENE = 8651 / 126
CPS = 323
MIN_CHARS = 8100
ROW = re.compile(r"^\|\s*(\d+)\s*\|([^|]*)\|")


@dataclass(frozen=True)
class Estimate:
    scene_count: int
    chars: int
    minutes: float


def estimate(path: Path) -> Estimate:
    text = path.read_text(encoding="utf-8")
    scene_count = sum(
        1 for line in text.splitlines()
        if (match := ROW.match(line)) and "〔場面〕" in match.group(2)
    )
    chars = int(scene_count * CHARS_PER_SCENE)
    return Estimate(scene_count, chars, chars / CPS)


def format_result(path: Path, result: Estimate) -> str:
    status = "PASS" if result.chars >= MIN_CHARS else "FAIL"
    return (
        f"[{status}] {path.name}: 〔場面〕{result.scene_count}行 × "
        f"{CHARS_PER_SCENE:.2f}字 = {result.chars:,}字 / {result.minutes:.1f}分 "
        f"（基準 {MIN_CHARS:,}字・約{MIN_CHARS / CPS:.1f}分）"
    )


def main(path_arg: str) -> int:
    path = Path(path_arg)
    if not path.is_file():
        print(f"[ERROR] 素材シートが見つかりません: {path}")
        return 2
    result = estimate(path)
    print(format_result(path, result))
    if result.chars < MIN_CHARS:
        print("追加で資料を探す（standard_sources.txt の必須先、北海道の事件は北海道新聞データベース）か、題材を見送る")
        return 1
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: estimate_script_length.py <Fact_Sheet>")
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
