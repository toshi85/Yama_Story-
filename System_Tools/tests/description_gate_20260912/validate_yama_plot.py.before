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
  9. 素材密度（字数÷素材数 ≤ 120）★創作の予防
 10. 主題占有率（外部素材だけで組まれた章 ≤ 15%）★他事件・全国統計での水増しの予防
 11. 設計からの乖離（設計字数 ±15%）★しきい値合わせの水増しの予防

使い方:
  python3 Yama_Story/System_Tools/validate_yama_plot.py <プロット表>
"""

# 2026-09-01 較正: イントロ字数の基準を出荷済み7本（128-360字・中央値180）に合わせた。
# 旧値200-270は羅臼岳(128)・大千軒岳(151)・風不死岳(162)・戸沢村(180)を落としていた。
# → feedback_calibrate_audits_to_shipped_content.md
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _infermarks
import glob
import os
import re
import sys
from pathlib import Path

CPS = 323                       # 字/分
TOTAL_LO, TOTAL_HI = 8400, 11300
PART_RANGE = {"KI": (0, 10), "SHO": (70, 90), "TEN-KETSU": (5, 15)}
# 起は字数で判定する（比率は上限のみ）。フック120-380 ＋ セットアップ150-500 の合成。
# 出荷済み7本の実測は 328〜929字。→ validate_yama_intro.py / validate_yama_structure.py と同値
KI_CHARS = (270, 950)
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

# --- 検査10 主題占有率（2026-09-02 追加）---------------------------------
# 「他の事件で文字を水増しするのではなく、その事件を深掘りして分量を満たす」を機械で守らせる。
# 視聴者が見に来ているのは "その事件" であって、他所の統計でも別の事件でもない。
#
# 判定は素材シートの〔外部〕印で行う。〔外部〕= 本件そのものではない行（全国統計・他事件・一般知識）。
#   章の素材のうち〔外部〕が EXT_CHAPTER 以上を占める章 = 「外部素材の章」
#   外部素材の章の合計字数が全体の EXT_BUDGET% を超えたら FAIL
#
# 較正（2026-09-02 実測・戸沢村）:
#   旧稿 = 18.4%（§19 受傷部位の統計456字 / §22 1994年 新潟県笹神村352字 / §24 月別・時間帯の統計922字）
#   新稿 =  7.8%（§3 記録の枠組み222字 / §25 5月と10月の実用575字）
#   → 上限15%は「旧稿を落とし、新稿を通す」値。統計や他事件の引用そのものを禁じてはいない。
EXT_CHAPTER = 2 / 3
EXT_BUDGET = 15.0

# 7列（設計字数／実測字数）と 旧6列（字数のみ）の両方を受ける
ROW7 = re.compile(r"^\|\s*(\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|(.*?)\|\s*$")
ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*([\d,]+)\s*\|(.*?)\|\s*$")
# 設計字数から実測がこれ以上ずれたら FAIL（2026-09-02 追加）
#   「書きながら膨らませて、あとでプロット表を本文に合わせる」を止めるための検査。
#   2026-09-02 の戸沢村で、起の5%フロアを満たすために §2 を149→232字（+56%）、
#   §3 を171→222字（+30%）に膨らませ、そのあと表を本文から再生成して差を消していた。
DRIFT = 15.0
META = re.compile(r"^-\s*(前半ピーク|後半ピーク|目標尺|ボトム)\s*[:：]\s*(.+?)\s*$")

# --- 検査12 V字（落差）2026-09-02 追加 ------------------------------------
# 出典: たちばなやすひと『「物語」の見つけ方』
#   「谷」を作ることで見かけの上がり幅が大きくなる。一度マイナスになり、そこから反転することで
#   上昇がより鮮明に認識される。時間が同じなら、人は上がり幅の大きいほうを望む。
#   坂本龍一「音楽とは緊張からの解決」／松本人志「笑いは緊張と緩和」も同じ「V」。
#
# ⚠️ ノンフィクションでは「谷を作らない」。実際に起きた落差を**省略しない**だけ。
#    プチハッピー・再起・プラスαは完全創作の型なので、Yama では採用しない。
# ⚠️ 「物語のボトム」と「維持率の谷」は別物。前者は作るべき最低点、後者は避けるべき離脱点
#    （説明の連続で生まれる）。混同しないこと。


def main(path):
    p = Path(path)
    text = p.read_text(encoding="utf-8")

    rows, meta = [], {}
    for line in text.split("\n"):
        m = META.match(line.strip())
        if m:
            meta[m.group(1)] = m.group(2)
            continue
        m7 = ROW7.match(line.strip())
        if m7:
            rows.append({
                "no": int(m7.group(1)),
                "title": m7.group(2).strip(),
                "part": m7.group(3).strip(),
                "kind": m7.group(4).strip(),
                "plan": int(m7.group(5).replace(",", "")),
                "chars": int(m7.group(6).replace(",", "")),
                "src": m7.group(7).strip(),
            })
            continue
        m = ROW.match(line.strip())
        if not m:
            continue
        rows.append({
            "no": int(m.group(1)),
            "title": m.group(2).strip(),
            "part": m.group(3).strip(),
            "kind": m.group(4).strip(),
            "plan": None,
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
    #    2026-09-02: 起は「機能」で切るので比率の下限では判定しない。
    #    起 = フック章 ＋ 最初の被害者の日常 ＋「その日常が崩れる予感」の一行。承はそこから事件の具体。
    #    下限は字数（フック120-380＋セットアップ150-500／出荷済み実測328-929字）、上限だけ比率。
    for part, (lo, hi) in PART_RANGE.items():
        c = sum(r["chars"] for r in rows if r["part"] == part)
        pct = 100 * c / total
        if part == "KI":
            ok = KI_CHARS[0] <= c <= KI_CHARS[1] and pct <= hi
            print(f"  {'OK ' if ok else 'NG '}{part:<10} {c:6,}字 {pct:5.1f}%"
                  f"  基準 {KI_CHARS[0]:,}-{KI_CHARS[1]:,}字 かつ 上限{hi}%")
            if not (KI_CHARS[0] <= c <= KI_CHARS[1]):
                fails.append(f"KI 字数 {c:,}字（基準 {KI_CHARS[0]:,}〜{KI_CHARS[1]:,}字）"
                             "＝フック120-380＋セットアップ150-500")
            if pct > hi:
                fails.append(f"KI 比率 {pct:.1f}%（上限 {hi}%）")
            continue
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
            n = int(re.search(r"\d+", v.split("#")[0]).group())
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

    # 9. 素材密度（2026-09-01 追加）— 1素材あたりの字数
    # 戸沢村の実測: 平均96字/素材。創作で埋めていた5章が全て120字/素材を超えていた。
    #   §5=298（章まるごと創作）§11=140 §7=131 §22=130（雨の予報は出典なし）§12=120
    #   逆に出典が厚い章は §18=42 §3=45 §13=57 で、いずれも創作ゼロだった。
    # 素材1つで300字書けば、残りは埋め草になる。**執筆前にここで止める。**
    DENSITY_HI = 120
    dense = []
    for r in rows:
        cnt = len([x for x in r["src"].split(",") if x.strip() and re.search(r"\d", x)])
        if cnt:
            d = r["chars"] / cnt
            if d > DENSITY_HI:
                dense.append((r["no"], r["title"][:18], r["chars"], cnt, d))
    if dense:
        for no, ti, ch, cnt, d in dense:
            fails.append(
                f"素材密度 §{no}「{ti}」= {d:.0f}字/素材（{ch}字 ÷ 素材{cnt}件・上限{DENSITY_HI}）"
                f" → 素材を足すか章を短くする。この比率を超えた章は創作で埋まる"
            )

    # 11. 設計からの乖離（2026-09-02 追加）— 書きながら膨らませるのを止める
    planned = [r for r in rows if r.get("plan")]
    if not planned:
        warns.append("プロット表に「設計字数」列がありません。"
                     "6列の旧形式では、書きながら膨らませても検知できません"
                     "（列: 章／タイトル／PART／種別／設計字数／実測字数／素材#）")
    else:
        drift = []
        for r in planned:
            d = 100 * (r["chars"] - r["plan"]) / r["plan"]
            if abs(d) > DRIFT:
                drift.append((r["no"], r["title"][:20], r["plan"], r["chars"], d))
        if drift:
            for no, ti, pl, ch, d in drift:
                fails.append(f"設計からの乖離 §{no}「{ti}」= {pl}字 → {ch}字（{d:+.0f}%・上限±{DRIFT:.0f}%）"
                             " → 本文を設計に戻すか、設計を意識して更新する。"
                             "検査を通すために行を足さない")
        print("[設計との差] 全%d章 / 上限±%.0f%% / 乖離 %d章" % (len(planned), DRIFT, len(drift)))
        print()

    # 12. V字（ボトムの宣言と位置）— 2026-09-02 追加
    bt = meta.get("ボトム")
    part_of = {r["no"]: r["part"] for r in rows}
    if not bt:
        fails.append("「- ボトム: <章番号>」の宣言がありません"
                     " → 物語がいちばん落ちる章。ここが深いほど、そこからの反転が大きく見える"
                     "（ノンフィクションでは谷を作らず、実際にあった落差を省略しない）")
    elif "なし" in bt:
        warns.append("ボトムが「なし」。落差のない構成は上がり幅が出ない。本当に無いか確認すること")
    else:
        try:
            bn = int(re.search(r"\d+", bt.split("#")[0]).group())
        except ValueError:
            fails.append(f"ボトムの章番号が読めません: {bt}")
            bn = None
        if bn is not None:
            if bn not in pos:
                fails.append(f"ボトムの §{bn} が表にありません")
            elif part_of.get(bn) != "SHO":
                fails.append(f"ボトム §{bn} が承（SHO）にありません（PART: {part_of.get(bn)}）"
                             " → ボトムは承の中。そこから転（クライマックス）へ向けて反転させる")
            else:
                print(f"[V字] ボトム §{bn}「{next(r['title'] for r in rows if r['no']==bn)[:22]}」"
                      f" 累計{pos[bn]:.1f}%")
                p2 = meta.get("後半ピーク")
                if p2:
                    try:
                        pn = int(re.search(r"\d+", p2.split("#")[0]).group())
                        if pn <= bn:
                            warns.append(f"後半ピーク §{pn} がボトム §{bn} より前にあります"
                                         "（落ちてから上げる形になっていない）")
                    except ValueError:
                        pass
                print()

    # 10. 主題占有率（2026-09-02 追加）— 他事件・全国統計での水増しを止める
    fs = sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(path)), "Fact_Sheet_*.md")))
    if not fs:
        warns.append("素材シート（Fact_Sheet_*.md）が同じフォルダに無いため、主題占有率を測れません")
    else:
        body = _infermarks.strip_infer(Path(fs[0]).read_text(encoding="utf-8"))
        ext_ids, all_ids = set(), set()
        for line in body.splitlines():
            m = re.match(r"^\|\s*(\d+)\s*\|([^|]*)\|", line)
            if not m:
                continue
            all_ids.add(m.group(1))
            if "〔外部〕" in m.group(2):
                ext_ids.add(m.group(1))
        if not ext_ids:
            warns.append(
                f"素材シート {os.path.basename(fs[0])} に〔外部〕印が1件もありません。"
                "全素材が本件由来なら正常ですが、印の付け忘れなら主題占有率の検査が空振りします")
        else:
            ext_rows, ext_chars = [], 0
            for r in rows:
                ids = [x.strip() for x in r["src"].split(",") if re.search(r"\d", x)]
                ids = [re.sub(r"\D", "", x) for x in ids]
                if not ids:
                    continue
                e = sum(1 for x in ids if x in ext_ids)
                if e / len(ids) >= EXT_CHAPTER:
                    ext_rows.append((r["no"], r["title"][:22], r["chars"], e, len(ids)))
                    ext_chars += r["chars"]
            pct = 100 * ext_chars / total
            print(f"[主題占有率] 外部素材の章 {len(ext_rows)}章 / {ext_chars:,}字 = {pct:.1f}%"
                  f"（上限 {EXT_BUDGET:.0f}%）")
            for no, ti, ch, e, n in ext_rows:
                print(f"    §{no} {ti}  {ch:,}字  外部素材 {e}/{n}")
            if pct > EXT_BUDGET:
                fails.append(
                    f"主題占有率 — 外部素材だけで組まれた章が {pct:.1f}%（上限 {EXT_BUDGET:.0f}%）。"
                    "他事件・全国統計で尺を伸ばさず、本件の未使用素材で埋めること")
            print()

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
