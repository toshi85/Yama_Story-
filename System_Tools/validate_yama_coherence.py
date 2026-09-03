#!/usr/bin/env python3
"""
辻褄検査 — 「資料を並べただけ」を機械で止める（2026-09-03 新設）

2026-09-03 に指摘された事故:
  §4 は資料を2つ引いていた。
    素材#121（文春）= 石を投げるとクマは「姿を消した」。6人は回収を断念した
    素材#2  （米田）= 発見時、クマはその場に「居座って」おり、収容は翌日になった
  本文は #121 だけを書き、#2 は <!-- src --> に名前が載っているだけで
  ナレーションに一度も出てこなかった。その結果、
    章タイトル「クマが、そこから動かなかった」（#2 の内容）
    本文       「間もなく姿を消します」        （#121 の内容）
  が正面から食い違い、「姿を消したのに、なぜ諦めたのか」が読者に分からなくなった。

  原因は一つ。**資料を並べたが、資料同士を突き合わせていない。**

検査:
  Check 1  引いたのに本文にない素材      … src に挙げた素材が、その章のナレーションに反映されていない
  Check 2  対立語の同居                   … 章タイトルと本文、または同一章の本文が反対のことを言っている
  Check 3  同じ素材の扱いの割れ           … 同じ素材を、ある章は断定し、別の章は「食い違い」として出している

使い方:
  python3 validate_yama_coherence.py <Master.md>
  （同じフォルダの Fact_Sheet_*.md を自動で探す）
"""
import sys, re, os, glob

# --- Check 2 の対立語ペア -------------------------------------------------
#   すべて、実際に台本の中で食い違っていた組み合わせ。
#   思いつきで足さないこと。**起きた事故だけを足す**（起きていない対立を足すと誤検知が増える）
ANTONYMS = [
    # 2026-09-03 §4: タイトル「動かなかった」 vs 本文「姿を消します」
    (r"居座|その場から動かな|そこから動かな|留まり続け", r"姿を消し|去っていき|いなくなりまし|逃げ去"),
    # 2026-09-03 §6: 「成果は上がらなかった」 vs 「7頭から8頭を捕らえています」
    (r"成果は上がらな|成果はありませ|何も獲れ", r"捕らえ|捕獲し|仕留め"),
    # 2026-09-03 §15/§16: 「弱っていた・病気」 vs 「空腹ではなかった・満腹」
    (r"弱っ|病気を思わせ|体に張りがな", r"空腹では|満腹|腹いっぱい"),
    # 2026-09-03 §9/§20: 「前から」 vs 「後ろから」
    (r"前から|前方から", r"後ろから|背後から|背後に"),
    # 2026-09-03 §2/§24: 「夕方に戻る」 vs 「昼までに戻る」
    (r"夕方に戻|夕方まで戻", r"昼までに戻|昼には戻"),
    # 2026-09-03 §21/§23: 「襲われた話は聞かない」 vs 「重いけがを負いました」
    (r"襲われたという話は聞かな|同じことは起きていな", r"重いけがを負|重傷を負"),
    # 2026-09-03 §14/§18: 「ここで終わります」と断定 vs 後の章「はっきりしていません」
    (r"ここで終わりま|これで終わりま|決着しま", r"はっきりしていません|分かりませんでした|決まっていません"),
]

HEDGE = re.compile(r"食い違|はっきりしていません|分かりませんでした|分かっていません|推測のまま|断定はされ|とみられ|可能性")

def norm(t):
    """表記ゆれを吸収してから比べる（km/キロ、m/メートル、全角数字など）"""
    t = t.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    t = re.sub(r"(\d+)\s*km", r"\1キロ", t)
    t = re.sub(r"(\d+)\s*m(?![a-z])", r"\1メートル", t)
    t = re.sub(r"(\d+)\s*kg", r"\1キロ", t)
    t = re.sub(r"(\d+)\s*cm", r"\1センチ", t)
    return re.sub(r"[、。「」『』（）\s]", "", t)

def tokens(t):
    """文字bigram。
    ⚠️ 「漢字2字以上」方式は日本語の混ぜ書き（太もも・咬まれ・見つかり）を1つも拾えず、
       重なり率が実態と無関係になった（2026-09-03 実測）。形態素解析を入れずに済ませるため
       bigram でそろえる（validate_yama_consistency.py の近似重複判定と同じ方式）。"""
    t = norm(t)
    return set(t[i:i + 2] for i in range(len(t) - 1))

def load_master(p):
    """章ごとに タイトル / ナレーション / 引いた素材# を集める"""
    chapters, cur = [], None
    for i, line in enumerate(open(p, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        m = re.match(r"^## (\d+)\. (.+)", line)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(),
                   "narr": [], "srcs": set(), "line": i, "ok": None}
            chapters.append(cur)
            continue
        if cur is None:
            continue
        if "COHERENCE_OK:" in line:
            cur["ok"] = line.split("COHERENCE_OK:", 1)[1].split("-->")[0].strip()
        if line.lstrip().startswith("<!--"):
            # ⚠️ src は「＝素材#1 #4 #8」のように2件目以降が裸の #n で書かれる。
            #    「素材#(\d+)」だけを見ると2件目以降を全部落とす（2026-09-03 実測で21件の誤検知）
            # 「＝素材#121 #122」のまとまりだけを取る。
            # ⚠️ 行全体から #数字 を拾うと、出典名の「文春オンライン風来堂#1」まで
            #    素材#1 として拾ってしまう（2026-09-03 実測で14件の誤検知）
            for grp in re.findall(r"素材[#＃]\s*\d+(?:\s*[#＃]\s*\d+)*", line):
                for n in re.findall(r"\d+", grp):
                    cur["srcs"].add(int(n))
        elif line.startswith("ナレーター:"):
            cur["narr"].append(re.sub(r"\s*<!--.*?-->", "", line.split(":", 1)[1]).strip())
    return chapters

def load_facts(d):
    """素材シートの 番号 → 本文"""
    facts = {}
    for fp in glob.glob(os.path.join(d, "Fact_Sheet_*.md")):
        for line in open(fp, encoding="utf-8"):
            if not line.lstrip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or not cells[0].isdigit():
                continue
            facts[int(cells[0])] = re.sub(r"\*\*|⚠️", "", cells[1])
    return facts

def main():
    if len(sys.argv) < 2:
        print("usage: validate_yama_coherence.py <Master.md>")
        return 2
    mp = sys.argv[1]
    d = os.path.dirname(os.path.abspath(mp))
    chapters = load_master(mp)
    facts = load_facts(d)
    fails, warns = [], []

    print("=" * 62)
    print(f"[Yama Coherence Validator] {os.path.basename(mp)}")
    print("=" * 62)

    # 章ごとの内容語（Check 1 の「珍しい語」を決めるのに使う）
    ch_tokens = [tokens(norm("".join(c["narr"]))) for c in chapters]
    df = {}
    for ts in ch_tokens:
        for t in ts:
            df[t] = df.get(t, 0) + 1

    # --- Check 1: 引いたのに本文にない素材 ---------------------------------
    #   素材の内容語のうち、その章のナレーションに現れる割合を測る。
    #   ⚠️ 「珍しい語だけを見る」方式は誤検知だらけだった（2026-09-03 実測 28件中ほぼ全部）。
    #      素材シートの言い回しと台本の言い回しは違うのが普通で、
    #      「太もも」「61歳」のような一致している語ほど df が大きく、珍しい語から外れてしまうため。
    #   重なりが 1割未満なら、その素材はその章で使われていないとみなす。
    #   較正: 戸沢村で手検証したところ、この基準で残るのは実際に未反映の素材だけになる。
    #   ⚠️ 素材シートを持つ出荷済み台本がまだ1本しかない（＝③の較正ができない）。
    #      そのため FAIL ではなく WARN で出す。台本が2本以上そろったら FAIL へ上げる。
    # ⚠️ 当初は「素材と本文の語の重なり率」で未使用を判定しようとしたが、失敗した。
    #    素材シートの言い回しと台本の言い回しは違うのが普通で（言い換えが仕事なので）、
    #    実際に使っている素材でも一致率は25〜32%にしかならず、未使用のものと分離できなかった。
    #    → 判定は「プロット表と台本の素材#がそろっているか」という**厳密に測れるもの**に置き、
    #      一致率は判定に使わず、**読み合わせを促す一覧**として低い順に出すだけにする。
    plot_srcs = {}
    for pp in glob.glob(os.path.join(d, "Plot_Sheet_*.md")):
        for line in open(pp, encoding="utf-8"):
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(cells) >= 7 and cells[0].isdigit():
                plot_srcs[int(cells[0])] = set(
                    int(x) for x in re.findall(r"\d+", cells[6]))
    if plot_srcs:
        for c in chapters:
            ps = plot_srcs.get(c["no"])
            if ps is None:
                continue
            only_master = c["srcs"] - ps
            only_plot = ps - c["srcs"]
            if only_master:
                fails.append(
                    f"台本にあってプロット表に無い素材 §{c['no']}「{c['title']}」: "
                    f"素材#{','.join(str(x) for x in sorted(only_master))} "
                    f"→ 使うならプロット表に足す。使わないなら src から外す")
            if only_plot:
                fails.append(
                    f"プロット表にあって台本に無い素材 §{c['no']}「{c['title']}」: "
                    f"素材#{','.join(str(x) for x in sorted(only_plot))} "
                    f"→ 本文に反映するか、プロット表から外す")

    # 読み合わせ一覧（判定しない）
    low = []
    if facts:
        for c in chapters:
            ts = tokens("".join(c["narr"]))
            for n in sorted(c["srcs"]):
                ftext = facts.get(n)
                if not ftext:
                    continue
                clauses = [x for x in re.split(r"[。／/]", ftext) if len(x) >= 10] or [ftext]
                best = 0.0
                for cl in clauses:
                    ft = tokens(cl)
                    if len(ft) < 5:
                        continue
                    best = max(best, len(ft & ts) / len(ft))
                if best:
                    low.append((best, c["no"], c["title"], n, ftext))
    low.sort()

    # --- Check 2: 対立語の同居 ---------------------------------------------
    #   ⚠️ 反対のことが並ぶこと自体は事故ではない。事故は**並べたまま説明しないこと**。
    #      YCP-033「資料が割れているなら、割れているまま出す」と同じ考え方で、
    #      章の中で対比・食い違いを明示していれば通す。
    #   ⚠️ 2026-09-03 実測: 当初は「ただし|それでも|一方|違いました」も“明示”に数えていたが、
    #      これらは普通の接続詞でどの章にもあるため、§6（成果なし↔7〜8頭捕獲）と
    #      §9（前から↔背後から）が素通りした。**資料の食い違いを名指しした語だけ**に絞る。
    RECONCILED = re.compile(r"食い違|割れて|一致していません|記録は、そこで|両方の記録")
    for c in chapters:
        body = norm("".join(c["narr"]))
        title = norm(c["title"])
        # 章に <!-- COHERENCE_OK: 理由 --> があれば「書き手が両立を説明した」とみなす。
        # ⚠️ 理由が空のものは認めない。宣言はすべて出力の末尾に並べるので、隠して通すことはできない。
        declared = RECONCILED.search(body) or (c["ok"] and len(c["ok"]) >= 8)
        for a, b in ANTONYMS:
            ta, tb = re.search(a, title), re.search(b, title)
            ba, bb = re.search(a, body), re.search(b, body)
            if (ta and bb) or (tb and ba):
                # タイトルと本文の食い違いは、明示していても直す（章題は言い切りだから）
                fails.append(
                    f"章タイトルと本文が反対 §{c['no']}「{c['title']}」: "
                    f"「{(ta or tb).group(0)}」↔「{(bb or ba).group(0)}」 → どちらが正しいかを本文で示す")
            elif ba and bb and not declared:
                fails.append(
                    f"同じ章の中で反対 §{c['no']}「{c['title']}」: "
                    f"「{ba.group(0)}」↔「{bb.group(0)}」 → 両立する理由を書くか、片方を落とす")
    # 章をまたぐ対立は警告（後の章で覆す構成もあるため）
    for a, b in ANTONYMS:
        hit_a = [c["no"] for c in chapters if re.search(a, norm("".join(c["narr"])))]
        hit_b = [c["no"] for c in chapters if re.search(b, norm("".join(c["narr"])))]
        cross = [(x, y) for x in hit_a for y in hit_b if x != y]
        if cross and not (set(hit_a) & set(hit_b)):
            x, y = cross[0]
            warns.append(f"章をまたぐ対立 §{x} ↔ §{y}: 「{a.split('|')[0]}」系 と「{b.split('|')[0]}」系（判断は人間）")

    # ⚠️ 年号の逆行検査は作ったが外した（2026-09-03）。
    #    §25→§26（1998→1994）は拾えたが、正しい台本でも4件鳴った
    #    （§11→§12 2016→1988 / §21→§22 2020→2017 / §23→§24 2026→2016 / §26→§27 1998→1988）。
    #    振り返りや比較事例で年が戻るのは普通の構成で、本物と区別がつかない。
    #    **鳴りすぎる検査は無視されるので、置かない。**

    # --- Check 3: 同じ素材の扱いの割れ -------------------------------------
    by_src = {}
    for c in chapters:
        for n in c["srcs"]:
            by_src.setdefault(n, []).append(c)
    for n, cs in sorted(by_src.items()):
        if len(cs) < 2:
            continue
        hedged = [c["no"] for c in cs if HEDGE.search("".join(c["narr"]))]
        plain = [c["no"] for c in cs if c["no"] not in hedged]
        if hedged and plain:
            warns.append(
                f"同じ素材の扱いが割れている 素材#{n}: §{plain[0]} は断定 / §{hedged[0]} は留保 "
                f"→ 先に出す章で留保を付けるか、後の章で言い直す（判断は人間）")

    # --- 出力 ---------------------------------------------------------------
    for label, items in (("FAIL", fails), ("WARN", warns)):
        if items:
            print(f"{os.linesep}--- {label} {len(items)}件 ---")
            for s in items:
                print(("  ✗ " if label == "FAIL" else "  ! ") + s)
    decl = [(c["no"], c["title"], c["ok"]) for c in chapters if c["ok"]]
    if decl:
        print(f"{os.linesep}--- 両立の宣言（COHERENCE_OK）{len(decl)}件 ---")
        print("    ⚠️ 宣言は検査を黙らせる。**中身が本当に書かれているかは人が読む**")
        for no, title, why in decl:
            print(f"    §{no}「{title[:24]}」: {why}")

    if low:
        print(f"{os.linesep}--- 読み合わせ推奨（本文との重なりが小さい素材・上位10件／判定はしない）---")
        print("    ⚠️ 一致率が低い＝未使用とは限らない（言い換えれば下がる）。**その章を音読して、素材の中身が本当に入っているかを目で見る**")
        for r, no, title, n, ftext in low[:10]:
            print(f"    {r:4.0%}  §{no:>2}「{title[:22]}」 素材#{n}: {ftext[:40]}")

    if not fails and not warns:
        print(f"{os.linesep}[PASS] 資料同士の突き合わせに問題はありません")
    elif not fails:
        print(f"{os.linesep}[PASS with warnings] FAIL はありません")
    else:
        print(f"{os.linesep}[FAIL] {len(fails)}件。資料を並べただけになっている箇所があります")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
