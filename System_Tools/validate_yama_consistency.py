#!/usr/bin/env python3
"""
台本・プロット表・素材シートの整合性を検査する（2026-09-01 新設）

2026-09-01 の戸沢村で実際に起きた事故を機械で止めるために作った:
  1. 同じナレーション行が2箇所にそのまま入っていた（§13と§20）
  2. 素材シートの「使う章」が §22 新設で全部ズレていた（65件が誤り）
  3. プロット表の目標字数・章題が本文と食い違ったまま放置されていた
  4. プロット表の素材# が、素材シートに存在しない番号を指していた

使い方:
  python3 validate_yama_consistency.py <Master.md>
  （同じフォルダの Plot_Sheet_*.md / Fact_Sheet_*.md を自動で探す）
"""
import sys, re, glob, os

def load_master(p):
    ch, cur, dup = [], None, {}
    for i, l in enumerate(open(p, encoding="utf-8")):
        l = l.rstrip("\n")
        m = re.match(r"^## (\d+)\. (.+)", l)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(), "chars": 0}
            ch.append(cur)
        elif l.startswith("ナレーター:"):
            c = re.sub(r"\s*<!--.*?-->", "", l.split(":", 1)[1]).strip()
            if cur: cur["chars"] += len(c)
            dup.setdefault(c, []).append(i + 1)
    return ch, dup

def main():
    if len(sys.argv) < 2:
        print("usage: validate_yama_consistency.py <Master.md>"); return 2
    mp = sys.argv[1]; d = os.path.dirname(os.path.abspath(mp))
    ch, dup = load_master(mp)
    fails, warns = [], []

    print("=" * 62)
    print(f"[Yama Consistency Validator] {os.path.basename(mp)}")
    print("=" * 62)

    # 1. 完全重複ナレーション行
    for text, lines in dup.items():
        if len(lines) > 1 and len(text) >= 12:
            fails.append(f"完全重複ナレ行 行{','.join(map(str,lines))}: 「{text[:44]}」")

    # 2/3. プロット表との整合（章番号・章題・字数）
    pp = glob.glob(os.path.join(d, "Plot_Sheet_*.md"))
    plot_src = {}
    if pp:
        rows = {}
        for l in open(pp[0], encoding="utf-8"):
            m = re.match(r"^\|\s*(\d+)\s*\|([^|]+)\|[^|]+\|[^|]+\|\s*([\d,]+)\s*\|([^|]*)\|", l.strip())
            if m:
                rows[int(m.group(1))] = (m.group(2).strip(), int(m.group(3).replace(",", "")), m.group(4))
                plot_src[int(m.group(1))] = re.findall(r"\d+", m.group(4))
        mm = {c["no"]: c for c in ch}
        for n in sorted(set(rows) | set(mm)):
            if n not in rows: fails.append(f"プロット表に §{n} の行がない（本文にはある）")
            elif n not in mm: fails.append(f"本文に §{n} がない（プロット表にはある）")
            else:
                t, c, _ = rows[n]
                if t != mm[n]["title"]: fails.append(f"§{n} 章題の不一致  表『{t}』/ 本文『{mm[n]['title']}』")
                if c != mm[n]["chars"]: fails.append(f"§{n} 字数の不一致  表 {c}字 / 本文 {mm[n]['chars']}字")
    else:
        warns.append("Plot_Sheet_*.md が見つからない")

    # 4/5. 素材シートとの整合（素材#の実在・「使う章」の実在）
    fp = glob.glob(os.path.join(d, "Fact_Sheet_*.md"))
    if fp:
        body = open(fp[0], encoding="utf-8").read()
        have = set(re.findall(r"^\|\s*(\d+)\s*\|", body, re.M))
        for n, ids in plot_src.items():
            miss = [i for i in ids if i not in have]
            if miss: fails.append(f"§{n} の素材# {','.join(miss)} が素材シートに存在しない")
        used = set()
        for l in body.split("\n"):
            if l.startswith("|"):
                for s in re.findall(r"§(\d+)", l.split("|")[-2] if l.count("|") >= 3 else ""):
                    used.add(int(s))
        exist = {c["no"] for c in ch}
        bad = sorted(used - exist)
        if bad: fails.append(f"素材シートの「使う章」が本文に存在しない: {', '.join('§'+str(b) for b in bad)}")
    else:
        warns.append("Fact_Sheet_*.md が見つからない")

    for label, items in (("FAIL", fails), ("WARN", warns)):
        if items:
            print(f"\n--- {label} {len(items)}件 ---")
            for x in items: print(f"  {'x' if label=='FAIL' else '!'} {x}")
    if not fails:
        print("\n[PASS] 台本・プロット表・素材シートは整合しています")
        return 0
    print(f"\n[FAIL] {len(fails)}件。3つの資料が食い違ったままPhase2に進むと必ず事故る")
    return 1

if __name__ == "__main__":
    sys.exit(main())
