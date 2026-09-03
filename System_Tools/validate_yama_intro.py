#!/usr/bin/env python3
"""
朱鞠内湖フォーミュラ適合チェッカー
基準の根拠: Yama_Story/Winning_Formula_Shumarinai.md（朱鞠内湖 kQrIDctEHVA の実測）

使い方:
    python3 Yama_Story/System_Tools/validate_yama_intro.py <script_path>

台本側で1行だけ指定が必要:
    結末（画になる一文）の直後の行に  <!-- HOOK-IMAGE -->  を置く
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import _infermarks
import re
import sys

CPS = 323 / 60.0  # 実測 323字/分

# 朱鞠内湖の実測値
REF = {
    # 2026-09-01 較正: 旧値 (200,270)/(37,50) は出荷済み7本のうち4本を落としていた。
    #   羅臼岳128 / 大千軒岳151 / 風不死岳162 / 戸沢村180 / 東成瀬村216 / 朱鞠内湖243 / 星野道夫360
    #   中央値180字。リファレンス台本の羅臼岳(128字)も、維持率2位の風不死岳(162字)も落ちていた。
    #   → feedback_calibrate_audits_to_shipped_content.md（出荷済みが通る値に較正する）
    #   目標値は朱鞠内湖の実測 243字・44秒。下記は「明らかに短すぎ／長すぎ」だけを止める幅。
    "intro_chars": (120, 380),   # 目標240字（実測レンジ 128-360）
    "intro_secs": (20, 72),      # 目標44秒
    "hook_image_secs": 35,       # 27秒
    "questions": 2,
    "closing": "地形図とともに解説します。",
    "ratio": {"KI": (5, 15), "SHO": (70, 90), "TEN-KETSU": (5, 15)},
    "total_chars": (8400, 11300),  # 26〜35分
    "explain_chars": 800,          # 説明セクションの上限
    # --- 起（KI）の定義 2026-09-02 ユーザー確定 ---
    # 起は比率ではなく「機能」で切る。
    #   起 = フック章 ＋ 最初の被害者の日常 ＋ 「その日常が崩れる予感」の一行（承の直前）
    #   承 = そこから先の、事件の具体
    # 例（戸沢村）: 「…ふつうの一日のはずでした。」→「ところが、この日は戻りません。」で起が終わる。
    #
    # ⚠️ これは実測されたパターンではなく、2026-09-02 に決めた設計ルール。
    #    出荷済み7本のうちこの形で終わっているのは 戸沢村 と 朱鞠内湖 の2本だけ
    #    （朱鞠内湖は実測トップの1本）。既存5本は calibration_baseline.json に登録して除外する。
    "ki_chars": (270, 950),        # 起の字数（フック120-380＋セットアップ150-500／出荷済み実測328-929）
    "ki_ratio_max": 10,            # 起の比率は上限だけ見る（下限なし）。
    # 2026-09-02 ユーザー指示:「起は短ければ短いほどいい。離脱を防げるから。1割未満に抑える」
    # 出荷済み7本の実測は 3.61〜8.31%（最大は朱鞠内湖 8.31%）で、全本が10%未満に収まる。
}


# 起の最終行が「日常が崩れる予感」か（2026-09-02 新設）
# 逆接、または「戻らない／現れない／応答がない」系の不在で終わっていること。
# 結の上限字数（2026-09-02）。結は「テーマの定着と余韻」で、ワンシーンかツーシーン。
# 戸沢村の実測は192字。朱鞠内湖の最終章685字は『転＋結が1章になっている』状態。
KETSU_MAX = 400

KI_TURN = re.compile(
    # ① 逆接で日常が折れる
    r"(ところが|しかし|ですが|それが|だが)"
    # ② 帰らない・現れない・応じない（不在で異変を示す）
    r"|(戻りません|戻ってきません|帰りません|帰ってきません|現れません|来ませんでした"
    r"|姿はありません|応答はありません|連絡が取れません|返事はありません|戻らないまま)"
    # ③ 「このあと何かが起きるとは、誰も思っていなかった」型の前振り
    #    2026-09-02 較正: 実測トップの朱鞠内湖がこの形だった。
    #    「そんな人物が、この日、命を落とすことになるとは、湖にいた誰一人、想像していなかったはずです。」
    r"|(想像していなかった|思っていなかった|思ってもみなかった|知る由もなかった"
    r"|予想していなかった|考えてもいなかった|誰も気づいていません)")


def narr(block):
    return [l.replace("ナレーター:", "").strip()
            for l in block.split("\n") if l.startswith("ナレーター:")]


def chars(lines):
    return sum(len(l) for l in lines)


def main(path):
    t = _infermarks.strip_infer(open(path, encoding="utf-8").read())
    fails, warns = [], []

    # ---- パート比率 ----
    parts = re.split(r"<!-- PART: (\w[\w-]*) -->", t)
    pdata, total = [], 0
    for i in range(1, len(parts), 2):
        c = chars(narr(parts[i + 1]))
        pdata.append((parts[i], c))
        total += c
    if not total:
        print("[ERROR] ナレーション行が見つかりません")
        return 1

    print("=" * 62)
    print(f"[朱鞠内湖フォーミュラ] {path}")
    print("=" * 62)
    print(f"\n総字数 {total:,}字 / 想定尺 {total/CPS/60:.1f}分")
    lo, hi = REF["total_chars"]
    if not lo <= total <= hi:
        fails.append(f"尺が範囲外: {total:,}字（基準 {lo:,}〜{hi:,}字＝26〜35分）")

    print("\n[構成比]")
    for name, c in pdata:
        pct = c / total * 100
        if name == "KI":
            # 2026-09-02: 起は「機能」で切るので、比率の下限では判定しない。
            #   下限は字数（フック120-380 ＋ セットアップ150-500 の合成）、上限だけ比率で見る。
            klo, khi = REF["ki_chars"]
            ok_c = klo <= c <= khi
            ok_r = pct < REF["ki_ratio_max"]
            if not ok_c:
                fails.append(f"KI 字数 {c:,}字（基準 {klo:,}〜{khi:,}字）"
                             "＝フック120-380＋セットアップ150-500。出荷済み実測は328-929字")
            if not ok_r:
                fails.append(f"KI 比率 {pct:.1f}%（10%未満に抑える。短いほど離脱が減る）")
            print(f"  {'OK ' if ok_c and ok_r else 'NG '}{name:10} {c:6,}字 {pct:5.1f}%"
                  f"  基準 {klo:,}-{khi:,}字 かつ 上限{REF['ki_ratio_max']}%")
            continue
        rlo, rhi = REF["ratio"].get(name, (0, 100))
        ok = "OK " if rlo <= pct <= rhi else "NG "
        if ok == "NG ":
            fails.append(f"{name} 比率 {pct:.1f}%（許容 {rlo}-{rhi}%）")
        print(f"  {ok}{name:10} {c:6,}字 {pct:5.1f}%  許容 {rlo}-{rhi}%")

    # ---- 起の切り方（2026-09-02 確定・設計ルール）----
    # 起 = フック章 ＋ 最初の被害者の日常 ＋「その日常が崩れる予感」の一行。
    # 承 = そこから先の、事件の具体。
    ki_block = None
    for i in range(1, len(parts), 2):
        if parts[i] == "KI":
            ki_block = parts[i + 1]
    if ki_block is not None:
        kl = narr(ki_block)
        if not kl:
            fails.append("起にナレーション行がありません")
        elif KI_TURN.search(kl[-1]):
            print("\n[起の切り方] OK  最終行が『日常が崩れる予感』で終わっています")
            print(f"    → 「{kl[-1][:48]}」")
        else:
            fails.append(
                f"起の最後が「日常が崩れる予感」で終わっていません: 「{kl[-1][:44]}」"
                " → 起＝フック＋最初の被害者の日常＋『ところが、この日は戻りません。』のような一行。"
                "承はそこから事件の具体に入る")

    # ---- 転・結の切り方（2026-09-02 確定・設計ルール）----
    # 『シナリオ・センター式 物語のつくり方／物語のみがき方』（新井一樹・日本実業出版社）より:
    #   転 = 物語のクライマックス。主人公にとって最大の障害をぶつけ、そこでテーマを伝える
    #   結 = テーマの定着と余韻。ワンシーンかツーシーンで短く。「結はオチではない」
    #   割合 起1割強 : 承7〜8割 : 転・結1割強
    # よって TEN-KETSU パートは「転（長い・山場）→ 結（短い・余韻）」の順で、最低2章必要。
    #
    # ⚠️ 設計ルールであって実測パターンではない。出荷済み6本は転結を1章で書いており、
    #    中身は実質「結」だけで転が入っていない。calibration_baseline.json に導入前として登録済み。
    tk = None
    for i in range(1, len(parts), 2):
        if parts[i] == "TEN-KETSU":
            tk = parts[i + 1]
    if tk is not None:
        tk_secs = re.split(r"\n## (?:§|第)?\d+[\.．][^\n]*\n", "\n" + tk)
        tk_lens = [chars(narr(x)) for x in tk_secs if chars(narr(x)) > 0]
        if len(tk_lens) < 2:
            fails.append(
                "転結が1章しかありません（転と結が分かれていない）"
                " → 転＝クライマックス（最大の障害・テーマを伝える）／結＝テーマの定着と余韻。"
                "結は短く、ワンシーンかツーシーン")
        else:
            ten, ketsu = sum(tk_lens[:-1]), tk_lens[-1]
            ok = ketsu <= KETSU_MAX and ketsu < ten
            print(f"\n[転・結] 転 {ten:,}字 / 結 {ketsu:,}字  "
                  f"{'OK' if ok else 'NG'}（結は{KETSU_MAX}字以内、かつ転より短い）")
            if ketsu > KETSU_MAX:
                fails.append(f"結が {ketsu:,}字（上限 {KETSU_MAX}字）"
                             " → 結はテーマの定着と余韻。ワンシーンかツーシーンで短く")
            if ketsu >= ten:
                fails.append(f"結（{ketsu:,}字）が転（{ten:,}字）以上あります"
                             " → 山場は転。結はその余韻で、必ず短くする")

    # ---- セクション分解 ----
    # 2026-08-30: 見出しの「§」「第」を許容。朱鞠内湖（実測で当たった1本）は "## §1. フック" 形式で、
    # 旧正規表現（数字始まりのみ）ではセクションが1つも取れず IndexError で落ちていた。
    # → Analytics/Why_Shumarinai_Hit.md §5
    secs = re.split(r"\n## (?:§|第)?(\d+[\.．][^\n]+)\n", t)
    sections = []
    for i in range(1, len(secs), 2):
        sections.append((secs[i], narr(secs[i + 1]), secs[i + 1]))
    if not sections:
        print("[ERROR] セクション見出しが読めません。'## 1. タイトル' または '## §1. タイトル' 形式にしてください")
        return 1

    # ---- イントロ ----
    title, lines, body = sections[0]
    ic = chars(lines)
    isec = ic / CPS
    print(f"\n[イントロ] {title}")
    print(f"  {ic}字 / {isec:.0f}秒   （朱鞠内湖 240字 / 44秒）")
    lo, hi = REF["intro_chars"]
    if not lo <= ic <= hi:
        fails.append(f"イントロ長 {ic}字（基準 {lo}〜{hi}字）")
    lo, hi = REF["intro_secs"]
    if not lo <= isec <= hi:
        fails.append(f"イントロ秒 {isec:.0f}秒（基準 {lo}〜{hi}秒）")

    # 結末（画）到達
    if "<!-- HOOK-IMAGE -->" in body:
        upto = body.split("<!-- HOOK-IMAGE -->")[0]
        hc = chars(narr(upto))
        hs = hc / CPS
        ok = hs <= REF["hook_image_secs"]
        print(f"  結末（画）到達: {hc}字 / {hs:.0f}秒 {'OK' if ok else 'NG'}"
              f"   （朱鞠内湖 27秒・上限 {REF['hook_image_secs']}秒）")
        if not ok:
            fails.append(f"結末（画）到達 {hs:.0f}秒（上限 {REF['hook_image_secs']}秒）")
    else:
        warns.append("<!-- HOOK-IMAGE --> マーカーが無いため結末到達時刻を測定できません")

    # 問いの数
    # 「〜のか。」「〜のか？」の両方を問いとして数える（2026-08-17 追加）
    q = [l for l in lines if l.rstrip().endswith(("のか。", "のか？", "のか?", "でしょうか。", "でしょうか？"))]
    ok = len(q) == REF["questions"]
    print(f"  問いの数: {len(q)}  {'OK' if ok else 'NG'}   （基準 {REF['questions']}つ固定）")
    if not ok:
        fails.append(f"問いの数 {len(q)}（基準 {REF['questions']}つ）")

    # ---- CQ（セントラルクエスチョン）の回収位置（2026-09-02 新設）----
    # 出典: たちばなやすひと『「物語」の見つけ方』（CQ＝物語を最後まで見届けさせる問い。
    #       CQの結果はクライマックスで出る）。Yama では「フックの問い2つ」＝CQ。
    # よって **各CQは転（TEN-KETSU）で受ける**。承の途中で言い切って終わらせない。
    if tk is not None and q:
        tk_text = "".join(narr(tk))
        for n, qq in enumerate(q, 1):
            body_q = re.sub(r"(そして|なぜ|どうして|一体|いったい)", "", qq)
            # ありふれた語で「回収したこと」にできてしまうため除外する
            GENERIC = {"のか", "でしょうか", "クマ", "ヒグマ", "ツキノワグマ", "事件", "事故",
                       "男性", "女性", "現場", "場所"}
            # 2026-09-02: 「3度」のような算用数字＋助数詞も語として拾う。
            #   漢数字を算用数字に統一したとき、「三度」は拾えるのに「3度」が拾えず、
            #   中身は同じなのに CQ 未回収と誤判定した（表記ゆれで検査が壊れた）。
            terms = [w for w in re.findall(r"[0-9０-９]+[一-龥ァ-ヶー]+|[一-龥ァ-ヶー]{2,}", body_q)
                     if w not in GENERIC]
            terms.sort(key=len, reverse=True)
            hit = [w for w in terms if w in tk_text]
            if hit:
                print(f"  CQ{n} 回収: OK  転に「{hit[0]}」が出てきます")
            else:
                fails.append(
                    f"CQ{n}「{qq[:32]}」が転で回収されていません（探した語: {'/'.join(terms[:6])}）"
                    " → CQの答えはクライマックス＝転で出す。承の途中で言い切って終わらせない")

    for x in q:
        print(f"      - {x}")

    # 締め
    ok = lines and lines[-1].strip() == REF["closing"]
    print(f"  締めの一文: {'OK' if ok else 'NG'}   「{REF['closing']}」")
    if not ok:
        fails.append(f"締めが「{REF['closing']}」でない（実際:「{lines[-1] if lines else ''}」）")

    # ---- 説明の連続 / 80%以降 ----
    print("\n[セクション別]")
    cum = 0
    rows = []
    for title, lines, _ in sections:
        c = chars(lines)
        cum += c
        rows.append((title, c, cum / total * 100))
        print(f"  {title[:34]:36} {c:5,}字 {c/CPS:4.0f}秒  累計{cum/total*100:5.1f}%")

    lim = REF["explain_chars"]
    for i in range(len(rows) - 1):
        if rows[i][1] > lim and rows[i + 1][1] > lim:
            warns.append(
                f"長いセクションが連続（谷のリスク）: 「{rows[i][0]}」{rows[i][1]:,}字 → "
                f"「{rows[i+1][0]}」{rows[i+1][1]:,}字。間に人の動き／証言を挟むこと")

    tail = [r for r in rows if r[2] >= 80]
    print(f"\n[80%以降のセクション] {len(tail)}件（最大の実用情報をここに置く）")
    for r in tail:
        print(f"  - {r[0]}  (累計{r[2]:.1f}%)")
    if not tail:
        warns.append("累計80%以降にセクションがありません")

    # ---- 判定 ----
    print("\n" + "=" * 62)
    if fails:
        print(f"[FAIL] {len(fails)}件")
        for f in fails:
            print(f"  ❌ {f}")
    else:
        print("[PASS] 朱鞠内湖フォーミュラの必須項目をすべて満たしています")
    for w in warns:
        print(f"  ⚠️  {w}")
    print("=" * 62)
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
