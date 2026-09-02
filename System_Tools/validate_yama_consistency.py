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
import sys, re, glob, os, itertools

NEWLINE = chr(10)

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
            dup.setdefault(c, []).append((i + 1, cur["no"] if cur else 0))
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
            fails.append(f"完全重複ナレ行 行{','.join(str(n) for n, _ in lines)}: 「{text[:44]}」")

    # 1b. 近似重複ナレーション行（2026-09-02 追加）
    #     完全一致だけを見ていたため「言い換えただけの水増し」がすり抜けていた。
    #     実例: §3「山形県は、44年ぶんの人身事故の記録を残しています。」
    #           §3「一覧が始まるのは、1977年。／そこから2020年まで、書き足されてきた記録です。」
    #           §18「山形県は、1977年から2020年までの人身事故を一覧にしています。／44年ぶんです。」
    #           §3「夏のあいだは、少なくなります。」 vs §7「クマに襲われる事故は、夏のあいだは少なくなります。」
    #     較正: 文字bigramのJaccard係数。出荷済み6本での検出は 0.65 で大千軒岳2件のみ（0.55だと5件に増える）。
    #     引用行（「で始まる）は語り口が似るため対象外。
    SIM = 0.65
    def _bg(t):
        t = re.sub(r"[、。「」（）\s]", "", t)
        return set(t[i:i + 2] for i in range(len(t) - 1))
    #     近い場所での言い換え＝水増し（FAIL）／離れた場所での再提示＝聞き手のための再説明（WARN）。
    #     出荷済みの大千軒岳は「22歳。北海道大学水産学部…」（§冒頭）と追悼（§末尾）、
    #     武田主幹の肩書きを2章で再提示していた。どちらも章が大きく離れており、水増しではない。
    NEAR = 2
    cand = [(ls[0][0], ls[0][1], t) for t, ls in dup.items()
            if len(t) >= 12 and not t.startswith("「")]
    for (l1, c1, t1), (l2, c2, t2) in itertools.combinations(cand, 2):
        a, b = _bg(t1), _bg(t2)
        if not (a | b):
            continue
        j = len(a & b) / len(a | b)
        if j < SIM:
            continue
        msg = (f"近似重複ナレ行 類似度{j:.2f} §{c1}行{l1} / §{c2}行{l2}: "
               f"「{t1[:30]}」/「{t2[:30]}」")
        if abs(c1 - c2) <= NEAR:
            fails.append(msg + " → 近い場所で同じことを言い換えている。どちらかを削る")
        else:
            warns.append(msg + " → 章が離れているので再提示かもしれない（判断は人間）")

    # 2/3. プロット表との整合（章番号・章題・字数）
    pp = glob.glob(os.path.join(d, "Plot_Sheet_*.md"))
    plot_src = {}
    if pp:
        rows = {}
        for l in open(pp[0], encoding="utf-8"):
            m7 = re.match(r"^\|\s*(\d+)\s*\|([^|]+)\|[^|]+\|[^|]+\|\s*[\d,]+\s*\|\s*([\d,]+)\s*\|([^|]*)\|", l.strip())
            m = m7 or re.match(r"^\|\s*(\d+)\s*\|([^|]+)\|[^|]+\|[^|]+\|\s*([\d,]+)\s*\|([^|]*)\|", l.strip())
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

        # 6. 素材# と「使う章」の双方向一致（2026-09-02 追加）
        #    2026-09-01 の戸沢村で、§22 を新設したのに素材シートの「使う章」を振り直さず 65件がズレていた。
        #    「使う章」は プロット表の素材# から一意に決まるので、機械で突き合わせる。
        row_use = {}
        for l in body.split(NEWLINE):
            m = re.match(r"^\|\s*(\d+)\s*\|", l)
            if not m or l.count("|") < 3:
                continue
            row_use[m.group(1)] = set(re.findall(r"§(\d+)", l.split("|")[-2]))
        miss = []
        for n, ids in sorted(plot_src.items()):
            for sid in ids:
                if sid in row_use and str(n) not in row_use[sid]:
                    miss.append(f"素材#{sid} を §{n} で使っているが、素材シートの「使う章」に §{n} が無い")
        if miss:
            fails.append(f"素材#と「使う章」の食い違い {len(miss)}件: " + " / ".join(miss[:6])
                         + (" ..." if len(miss) > 6 else ""))
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
