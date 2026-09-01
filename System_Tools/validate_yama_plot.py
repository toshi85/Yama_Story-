#!/usr/bin/env python3
"""
Yamaプロット表バリデーター（執筆前ゲート）

背景: 2026-08-19 東成瀬村台本で、構成の検査が「完成した9,000字」に対してしかできず、
転結18.5%・起3.6%・実用情報の位置ずれ・説明の連続を、書き終わってから帳尻合わせした。
谷の位置と二山構造は、書き終わってからでは章ごと動かすしかない。だから先に検査する。

対象: Plot_Sheet_<事件名>.md（`Plot_Sheet_Template.md` の形式）

検査:
  1. 合計字数 8,400〜11,300字
  2. 起承転結 5-15 : 70-90 : 5-15
  3. イントロ章 120〜380字
  4. 説明の連続（説明/データが2章連続しない・1章800字以内）
  5. 谷の帯（累計50〜55%に説明/データを置かない）
  6. 80%以降に「実用」の章がある
  7. 二山構造（前半ピーク15〜45% / 後半ピーク50〜85%）
  8. 全章に素材#がある

使い方:
  python3 Yama_Story/System_Tools/validate_yama_plot.py <プロット表>
"""

# 2026-09-01 較正: イントロ字数の基準を出荷済み7本（128-360字・中央値180）に合わせた。
# 旧値200-270は羅臼岳(128)・大千軒岳(151)・風不死岳(162)・戸沢村(180)を落としていた。
# → feedback_calibrate_audits_to_shipped_content.md
import re
import sys
from pathlib import Path

CPS = 323                       # 字/分
TOTAL_LO, TOTAL_HI = 8400, 11300
PART_RANGE = {"KI": (5, 15), "SHO": (70, 90), "TEN-KETSU": (5, 15)}
INTRO_LO, INTRO_HI = 120, 380  # 2026-09-01 較正: 出荷済み7本は128-360字・中央値180。旧値200-270は羅臼岳(128)大千軒岳(151)風不死岳(162)戸沢村(180)を落としていた → feedback_calibrate_audits_to_shipped_content.md
EXPLAIN = {"説明", "データ"}
EXPLAIN_MAX = 800
VALLEY = (50.0, 55.0)           # 谷が出やすい帯
PEAK1 = (15.0, 45.0)
# 2026-08-30 実測により 50-85% → 35-75% へ変更。
# 根拠: 朱鞠内湖（実測で当たった1本）の第二の山場「ドローン駆除（国内初）」は累計43.1%。
#       旧基準では失格になっていた。第一の山場（捜索と発見）は34.3%で、二山は34%と43%に並ぶ。
#       → Analytics/Why_Shumarinai_Hit.md §4-5
PEAK2 = (35.0, 75.0)
KINDS = {"フック", "動き", "証言", "感情", "説明", "データ", "実用"}

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*([\d,]+)\s*\|(.*?)\|\s*$")
META = re.compile(r"^-\s*(前半ピーク|後半ピーク|目標尺)\s*[:：]\s*(.+?)\s*$")


def main(path):
    p = Path(path)
    text = p.read_text(encoding="utf-8")

    rows, meta = [], {}
    for line in text.split("\n"):
        m = META.match(line.strip())
        if m:
            meta[m.group(1)] = m.group(2)
            continue
        m = ROW.match(line.strip())
        if not m:
            continue
        rows.append({
            "no": int(m.group(1)),
            "title": m.group(2).strip(),
            "part": m.group(3).strip(),
            "kind": m.group(4).strip(),
            "chars": int(m.group(5).replace(",", "")),
            "src": m.group(6).strip(),
        })

    if not rows:
        print("章の行が1つも読めません。Plot_Sheet_Template.md の表形式を確認してください")
        return 2

    total = sum(r["chars"] for r in rows)
    cum, acc = [], 0
    for r in rows:
        acc += r["chars"]
        cum.append(100 * acc / total)

    fails, warns = [], []

    print("=" * 68)
    print(f"[Yama Plot Validator] {p.name}")
    print("=" * 68)
    print(f"全{len(rows)}章 / 合計 {total:,}字 / 想定尺 {total/CPS:.1f}分\n")
    print(f"{'章':>3} {'種別':<5} {'PART':<10} {'字数':>6} {'累計%':>7}  タイトル")
    for r, c in zip(rows, cum):
        flag = "  ←谷帯" if VALLEY[0] <= c <= VALLEY[1] and r["kind"] in EXPLAIN else ""
        print(f"{r['no']:>3} {r['kind']:<5} {r['part']:<10} {r['chars']:>6,} {c:>6.1f}%  {r['title'][:28]}{flag}")
    print()

    # 1. 合計字数
    if not (TOTAL_LO <= total <= TOTAL_HI):
        fails.append(f"合計 {total:,}字（基準 {TOTAL_LO:,}〜{TOTAL_HI:,}字＝26〜35分）")

    # 2. 起承転結
    for part, (lo, hi) in PART_RANGE.items():
        c = sum(r["chars"] for r in rows if r["part"] == part)
        pct = 100 * c / total
        ok = lo <= pct <= hi
        print(f"  {'OK ' if ok else 'NG '}{part:<10} {c:6,}字 {pct:5.1f}%  許容 {lo}-{hi}%")
        if not ok:
            fails.append(f"{part} 比率 {pct:.1f}%（許容 {lo}-{hi}%）")
    print()

    # 3. イントロ章
    intro = next((r for r in rows if r["kind"] == "フック"), None)
    if intro is None:
        fails.append("種別「フック」の章がありません（イントロ未設計）")
    elif not (INTRO_LO <= intro["chars"] <= INTRO_HI):
        fails.append(f"イントロ {intro['chars']}字（基準 {INTRO_LO}〜{INTRO_HI}字）")

    # 4. 説明の連続・上限
    for i, r in enumerate(rows):
        if r["kind"] in EXPLAIN and r["chars"] > EXPLAIN_MAX:
            warns.append(f"§{r['no']}「{r['title'][:20]}」が{r['chars']:,}字（説明は{EXPLAIN_MAX}字が上限）")
        if i and rows[i - 1]["kind"] in EXPLAIN and r["kind"] in EXPLAIN:
            fails.append(f"説明が連続: §{rows[i-1]['no']} → §{r['no']}（間に動き/証言/感情を挟む）")

    # 5. 谷の帯
    for r, c in zip(rows, cum):
        if VALLEY[0] <= c <= VALLEY[1] and r["kind"] in EXPLAIN:
            fails.append(f"谷の帯（累計{VALLEY[0]:.0f}〜{VALLEY[1]:.0f}%）に説明を配置: §{r['no']}「{r['title'][:20]}」")

    # 6. 80%以降の実用情報
    if not any(r["kind"] == "実用" and c >= 80 for r, c in zip(rows, cum)):
        fails.append("累計80%以降に種別「実用」の章がありません（持ち帰れる知識を後半に置く）")

    # 7. 二山構造
    pos = {r["no"]: c for r, c in zip(rows, cum)}
    for key, (lo, hi) in (("前半ピーク", PEAK1), ("後半ピーク", PEAK2)):
        v = meta.get(key)
        if not v:
            fails.append(f"「- {key}: <章番号>」の宣言がありません（二山構造）")
            continue
        try:
            n = int(re.sub(r"\D", "", v))
        except ValueError:
            fails.append(f"{key} の章番号が読めません: {v}")
            continue
        if n not in pos:
            fails.append(f"{key} の§{n} が表にありません")
        elif not (lo <= pos[n] <= hi):
            warns.append(f"{key} §{n} が累計{pos[n]:.1f}%（推奨 {lo:.0f}〜{hi:.0f}%）")

    # 8. 素材の紐づけ
    nosrc = [r["no"] for r in rows if not re.search(r"\d", r["src"])]
    if nosrc:
        fails.append(f"素材#が空の章: {', '.join('§'+str(n) for n in nosrc)}（素材シートに無い章は作れない）")

    # 種別の語彙
    bad = {r["kind"] for r in rows} - KINDS
    if bad:
        warns.append(f"未知の種別: {', '.join(sorted(bad))}（使えるのは {', '.join(sorted(KINDS))}）")

    for label, items in (("FAIL", fails), ("WARN", warns)):
        if items:
            print(f"--- {label} {len(items)}件 ---")
            for x in items:
                print(f"  {'x' if label=='FAIL' else '!'} {x}")
            print()

    if fails:
        print("[FAIL] プロットを直してから執筆に入ること。9,000字書いてから直すより安い")
        return 1
    print("[PASS] プロットは基準を満たしています。執筆に進んでよい"
          + (f"（WARN {len(warns)}件は確認）" if warns else ""))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_yama_plot.py <プロット表>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
