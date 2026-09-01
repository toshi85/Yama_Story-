#!/usr/bin/env python3
"""
朱鞠内湖フォーミュラ適合チェッカー
基準の根拠: Yama_Story/Winning_Formula_Shumarinai.md（朱鞠内湖 kQrIDctEHVA の実測）

使い方:
    python3 Yama_Story/System_Tools/validate_yama_intro.py <script_path>

台本側で1行だけ指定が必要:
    結末（画になる一文）の直後の行に  <!-- HOOK-IMAGE -->  を置く
"""
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
}


def narr(block):
    return [l.replace("ナレーター:", "").strip()
            for l in block.split("\n") if l.startswith("ナレーター:")]


def chars(lines):
    return sum(len(l) for l in lines)


def main(path):
    t = open(path, encoding="utf-8").read()
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
        rlo, rhi = REF["ratio"].get(name, (0, 100))
        ok = "OK " if rlo <= pct <= rhi else "NG "
        if ok == "NG ":
            fails.append(f"{name} 比率 {pct:.1f}%（許容 {rlo}-{rhi}%）")
        print(f"  {ok}{name:10} {c:6,}字 {pct:5.1f}%  許容 {rlo}-{rhi}%")

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
