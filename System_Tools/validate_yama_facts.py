#!/usr/bin/env python3
"""
Yama台本 事実・語り口バリデーター

背景: 2026-08-19 東成瀬村台本で、AIが書いた「つなぎの地の文」が出典のない主張を
生み出す事故が連続した（「限界を迎えていたのは東成瀬村だけではありませんでした」
＝村が限界だったという事実を勝手に作った／「山林だから緊急銃猟の対象外」＝推論を
断定で書いた／「同じクマの仕業だと判断されました」＝報道は断定していない）。

文章を滑らかにする作業と、1文ずつ出典を確認する作業は同時に走らない。
だから「書いた後に人間が気づく」のではなく、機械で止める。

検査項目:
  A. 答え先行     問いを立てたら6行以内に答えを出しているか（YCP-004）
  B. 権威名詞     大学の講座名・学会名・医学誌名を読み上げていないか
  C. 断定語       「〜と判断されました」等の断定に出典が付いているか  ★FAIL対象
  D. 出典カバー率 ナレーション行のうち、近傍に <!-- src: --> がある割合

使い方:
  python3 Yama_Story/System_Tools/validate_yama_facts.py <台本>
"""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _infermarks
import re
import sys
from pathlib import Path

NARR = "ナレーター: "
SRC = re.compile(r"<!--\s*src:", re.I)

# A. 問いと答え
QUESTION = re.compile(r"(なぜ|どうして|何が|本当に).*(のか|のでしょうか|でしょうか)[。？?]?\s*$")
ANSWER = re.compile(r"(理由は|答えは|原因は|それは|答えが|からです|ためでした|わけです)")

# B. 権威名詞（耳で聞いて意味を成さない固有名詞）
AUTHORITY = [
    (r"大学院", "大学院＋講座名は読み上げない。「〜の資料によると」で足りる"),
    (r"[^\s]{2,}学講座", "講座名は不要"),
    (r"[^\s]{2,}学会", "学会名は不要。発表内容だけ残す"),
    (r"医学誌|専門誌|学術誌", "掲載誌名は不要"),
    (r"に掲載され", "掲載の事実は視聴者の関心事ではない"),
    (r"研究科", "研究科名は不要"),
]

# C. 断定語（報道が断定していないのに断定すると事実誤認になる）
ASSERTION = [
    r"と判断されました", r"と断定され", r"と結論づけ", r"と確定し",
    r"ことが判明しました", r"と決まりました", r"に違いありません",
]


def near_src(lines, idx, span=3):
    """前後 span 行以内に src コメントがあるか"""
    lo, hi = max(0, idx - span), min(len(lines), idx + span + 1)
    return any(SRC.search(lines[i]) for i in range(lo, hi))


import re as _re


def main(path):
    p = Path(path)
    lines = _infermarks.strip_infer(p.read_text(encoding="utf-8")).split("\n")
    narr_idx = [i for i, l in enumerate(lines) if l.startswith(NARR)]

    fails, warns = [], []

    # --- A. 答え先行 ---
    # 起パート（イントロ）の問いは設計上あとで回収するので対象外
    ki_end = next((i for i, l in enumerate(lines) if "PART: SHO" in l), 0)
    for n, i in enumerate(narr_idx):
        if i < ki_end:
            continue
        body = lines[i][len(NARR):]
        if QUESTION.search(body):
            window = [lines[j][len(NARR):] for j in narr_idx[n + 1:n + 7]]
            if not any(ANSWER.search(w) for w in window):
                warns.append((i + 1, "A/答え先行",
                              "問いの6行以内に答えが見当たらない", body))

    # --- B. 権威名詞 ---
    for i in narr_idx:
        body = lines[i][len(NARR):]
        for pat, msg in AUTHORITY:
            if re.search(pat, body):
                warns.append((i + 1, "B/権威名詞", msg, body))
                break

    # --- C. 断定語 ---
    for i in narr_idx:
        body = lines[i][len(NARR):]
        for pat in ASSERTION:
            if re.search(pat, body):
                if near_src(lines, i):
                    warns.append((i + 1, "C/断定語",
                                  "断定している。出典が本当に断定しているか確認", body))
                else:
                    fails.append((i + 1, "C/断定語",
                                  "出典なしで断定している", body))
                break

    # --- D. 出典カバー率 ---
    covered = sum(1 for i in narr_idx if near_src(lines, i, span=2))
    rate = 100 * covered / len(narr_idx) if narr_idx else 0

    # --- 引用の改変（2026-09-03 新設・WARNのみ）-----------------------------
    #   ユーザー確定稿で、佐藤さんの証言が
    #     原文「昔は裏手の山肌は歩くけど、ここに出なかったんですよ。ここ1、2年だね」
    #     台本「昔は裏手の山肌は歩くけど、ここに出たんですよ。ここ1、2年だね」
    #   と、**否定が消えて意味が真逆**になっていた。「ここ1、2年だね」と繋がらなくなる。
    #   発言の引用は、語尾も含めて資料のまま。抜粋（部分列）はよいが、書き換えは不可。
    #
    #   判定: 本文の「」内（12字以上）を素材シートの「」内と突き合わせ、
    #         似ている（正規化して一致率0.7以上）のに一致せず、
    #         **否定語の数か、含まれる数字が食い違う**ものだけ WARN。
    #   較正: 戸沢村で誤検知2件（匿名記号A/Bを説明語へ置換した箇所・表記ゆれ）。
    #         抜粋（片方がもう片方の部分列）は除外している。
    import difflib as _dl
    _NEG = _re.compile(r"ない|なかっ|ません|ませんで|ず[、。]|ぬ[、。]")
    _NUM = _re.compile(r"\d+")
    def _nrm(t):
        return _re.sub(r"[\s\u3000\*（）()、。「」『』]", "", t)
    _fq = []
    for _fp in p.parent.glob("Fact_Sheet_*.md"):
        _fq += [m.group(1) for m in
                _re.finditer(r"[「『]([^」』\n|]{12,})[」』]", _fp.read_text(encoding="utf-8"))]
    if _fq:
        for _i, _l in enumerate(lines, 1):
            if not _l.startswith("ナレーター:"):
                continue
            _t = _re.sub(r"\s*<!--.*?-->", "", _l)
            for _m in _re.finditer(r"「([^」\n]{12,})」", _t):
                _q = _m.group(1); _nq = _nrm(_q)
                _best = max(((_dl.SequenceMatcher(None, _nq, _nrm(_f)).ratio(), _f) for _f in _fq),
                            default=(0, ""))
                if _best[0] < 0.7 or _best[0] >= 1.0:
                    continue
                _nf = _nrm(_best[1])
                if _nq in _nf or _nf in _nq:
                    continue
                if (len(_NEG.findall(_q)) != len(_NEG.findall(_best[1]))
                        or _NUM.findall(_nq) != _NUM.findall(_nf)):
                    warns.append((_i, "D/引用の改変",
                                  f"素材シートの引用と、否定か数字が食い違います（一致率{_best[0]:.2f}）\n"
                                  f"      素材: {_best[1][:60]}\n"
                                  f"      → 発言の引用は語尾まで資料のまま。抜粋は可、書き換えは不可（YCP-042）",
                                  _q[:60]))

    print("=" * 62)
    print(f"[Yama Facts Validator] {p.name}")
    print("=" * 62)
    print(f"ナレーション {len(narr_idx)}行 / 出典カバー率 {rate:.1f}%"
          f"（近傍2行以内に src があるナレーション行の割合）")
    if rate < 50:
        print("  → カバー率が低い。素材シートに無い地の文が多い可能性がある")
    print()

    for label, items in (("FAIL", fails), ("WARN", warns)):
        if not items:
            continue
        print(f"--- {label} {len(items)}件 ---")
        for ln, kind, msg, body in items:
            print(f"  L{ln:>5} [{kind}] {msg}")
            print(f"          {body[:70]}")
        print()

    if fails:
        print(f"[FAIL] 出典なしの断定 {len(fails)}件。素材シートで根拠を示すか、"
              f"推定表現（〜とみられています）に直すこと")
        return 1
    print("[PASS] 出典なしの断定はありません"
          + (f"（WARN {len(warns)}件は要確認）" if warns else ""))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_yama_facts.py <台本>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
