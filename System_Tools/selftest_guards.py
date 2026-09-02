#!/usr/bin/env python3
"""
検査の自己試験（2026-09-01 新設）

**2026-09-01 に実際に起きたミスを1件ずつ注入して、検査が捕まえるかを確かめる。**
「検査を足した」と言うだけでは、効いている証拠にならない。ここが全部 OK になって初めて
「同じミスは機械で止まる」と言える。

  python3 selftest_guards.py
"""
import subprocess, sys, os, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

HEAD = """# テスト用タイトル

## リサーチ出典一覧（Tier順）
- ダミー

## 競合との差別化要因レポート
### 競合動画Top 3
| 順位 | タイトル | チャンネル | 再生数 | 尺 | 公開 |
|:--|:--|:--|--:|--:|:--|
| 1 | ダミー | ダミー | 1回 | 1分 | 2025-01-01 |
### 情報の穴（Information Holes）
- 穴①

## サムネイル競合分析
| チャンネル | テキスト | 構図 | 色調 |
|:--|:--|:--|:--|
| ダミー | ダミー | ダミー | ダミー |

<!-- PART: KI -->

## 1. フック
"""

def run(script, path):
    # Windows の既定エンコーディング（cp932）だと日本語の出力で落ちるため UTF-8 を明示する
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([PY, os.path.join(HERE, script), path],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def check(name, script, path, must_contain):
    code, out = run(script, path)
    hit = must_contain in out
    print(f"  {'✅' if hit else '❌'} {name:<42} {script}")
    if not hit:
        print(f"      期待: 「{must_contain}」を含む出力 / 実際の末尾: {out.strip().splitlines()[-1][:70] if out.strip() else '(空)'}")
    return hit

def main():
    tmp = tempfile.mkdtemp()
    ok = []
    print("=" * 74)
    print("検査の自己試験 — 過去に実際に起きたミスを注入して、止まるか確かめる")
    print("=" * 74)

    # ① メタ語り（Gate 6）
    p = os.path.join(tmp, "meta.md")
    open(p, "w", encoding="utf-8").write("ナレーター: ここで一度、山形県が残している資料を開きます。\nナレーター: 見つかった場所を、地図で見てみます。\n")
    ok.append(check("① メタ語り「ここで〜を開きます」", "validate_yama_narrative.py", p, "❌ [メタ語り禁止"))

    # ①b 証言導入は誤検出しないこと
    p = os.path.join(tmp, "quote.md")
    open(p, "w", encoding="utf-8").write("ナレーター: 佐藤さんは、こう振り返ります。\nナレーター: ひどかったな、あれは。\n")
    code, out = run("validate_yama_narrative.py", p)
    hit = "❌ [メタ語り禁止" not in out and code == 0
    print(f"  {'✅' if hit else '❌'} {'①b 証言導入を誤検出しない':<42} validate_yama_narrative.py")
    ok.append(hit)

    # ② 孤立した固有名詞（Gate 7・警告）
    p = os.path.join(tmp, "orphan.md")
    open(p, "w", encoding="utf-8").write("ナレーター: 村の真ん中を、最上川が西へ流れています。\nナレーター: 山に入りました。\n")
    ok.append(check("② 孤立した固有名詞（最上川）", "validate_yama_narrative.py", p, "[孤立した固有名詞] Line"))

    # ③ 遺体はタイトルで止まり、本文では止まらない
    p = os.path.join(tmp, "title.md")
    open(p, "w", encoding="utf-8").write("# 遺体で発見された事件\n\nナレーター: 山で見つかりました。\n")
    ok.append(check("③ 遺体がタイトルにあると止まる", "validate_yama_safety.py", p, "タイトル/サムネのみ"))
    p = os.path.join(tmp, "body.md")
    open(p, "w", encoding="utf-8").write("# ふつうのタイトル\n\nナレーター: 深夜、男性が遺体で発見。\n")
    code, out = run("validate_yama_safety.py", p)
    hit = code == 0
    print(f"  {'✅' if hit else '❌'} {'③b 遺体が本文なら通る':<42} validate_yama_safety.py")
    ok.append(hit)

    # ④ 完全重複ナレ行
    d = os.path.join(tmp, "dup"); os.makedirs(d)
    p = os.path.join(d, "Master.md")
    open(p, "w", encoding="utf-8").write(HEAD + "\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n\n## 2. 別の章\n\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n")
    ok.append(check("④ 完全重複ナレ行", "validate_yama_consistency.py", p, "完全重複ナレ行"))

    # ⑤ プロット表の字数ズレ
    d2 = os.path.join(tmp, "stale"); os.makedirs(d2)
    open(os.path.join(d2, "Master.md"), "w", encoding="utf-8").write(HEAD + "\nナレーター: 十文字ちょうどの行。\n")
    open(os.path.join(d2, "Plot_Sheet_test.md"), "w", encoding="utf-8").write(
        "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n| 1 | フック | KI | フック | 999 | 1 |\n")
    ok.append(check("⑤ プロット表の字数が本文とズレ", "validate_yama_consistency.py", os.path.join(d2, "Master.md"), "字数の不一致"))

    # ⑥ 素材シートの「使う章」が本文に無い
    d3 = os.path.join(tmp, "chap"); os.makedirs(d3)
    open(os.path.join(d3, "Master.md"), "w", encoding="utf-8").write(HEAD + "\nナレーター: ダミー。\n")
    open(os.path.join(d3, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(
        "| # | 事実 | 出典 | 確認方法 | 使う章 |\n|:--|:--|:--|:--|:--|\n| 1 | ダミー | 米田 | 同上 | §99 |\n")
    ok.append(check("⑥ 素材シートの使う章が本文に無い", "validate_yama_consistency.py", os.path.join(d3, "Master.md"), "「使う章」が本文に存在しない"))

    # ⑦ 素材密度（字数÷素材数）— 創作の予防
    p = os.path.join(tmp, "Plot_Sheet_dense.md")
    open(p, "w", encoding="utf-8").write(
        "- 前半ピーク: 1\n- 後半ピーク: 1\n\n| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
        "| 1 | フック | KI | フック | 298 | 2 |\n")
    ok.append(check("⑦ 素材1つで298字（創作の温床）", "validate_yama_plot.py", p, "素材密度"))

    # ⑧ 証言が「」の外（ナレーターが一人称で話す）
    p = os.path.join(tmp, "colloq.md")
    open(p, "w", encoding="utf-8").write("ナレーター: 俺、持ったけど。甥っ子が背負って。\nナレーター: 嫌だったよな。\n")
    ok.append(check("⑧ 話し言葉が括弧の外（俺／よな）", "validate_yama_narrative.py", p, "話し言葉が括弧の外"))

    # ⑧b 正しく「」で囲めば通る
    p = os.path.join(tmp, "quoted.md")
    open(p, "w", encoding="utf-8").write("ナレーター: 佐藤さんは、取材にこう話しています。\nナレーター: 「俺、持ったけど。嫌だったよな」\n")
    code, out = run("validate_yama_narrative.py", p)
    hit = "❌ [話し言葉が括弧の外" not in out and code == 0
    print(f"  {'✅' if hit else '❌'} {'⑧b 「」で囲めば通る':<42} validate_yama_narrative.py")
    ok.append(hit)

    # ⑨ 帰属だけの単独行を後ろに置く
    p = os.path.join(tmp, "attr.md")
    open(p, "w", encoding="utf-8").write("ナレーター: 満腹の状態でありながら、人を食べていた。\nナレーター: 米田さんは、そう記しています。\n")
    ok.append(check("⑨ 後置の「そう記しています。」単独行", "validate_yama_narrative.py", p, "帰属だけの単独行"))

    # ⑫ 素材#と「使う章」の双方向一致（2026-09-02 追加）
    #    2026-09-01 の戸沢村で §22 を新設したのに素材シートの「使う章」を振り直さず65件ズレていた。
    import os as _os2
    d4 = _os2.path.join(tmp, "usech"); _os2.makedirs(d4, exist_ok=True)
    open(_os2.path.join(d4, "Master.md"), "w", encoding="utf-8").write(
        HEAD + "\nナレーター: ダミーの一行です。\n\n## 2. 二章目\nナレーター: もう一行のダミー。\n")
    open(_os2.path.join(d4, "Plot_Sheet_t.md"), "w", encoding="utf-8").write(
        "# プロット表\n\n| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
        "| 1 | フック | KI | フック | 10 | 1 |\n"
        "| 2 | 二章目 | SHO | 動き | 9 | 1 |\n")
    open(_os2.path.join(d4, "Fact_Sheet_t.md"), "w", encoding="utf-8").write(
        "# 素材シート\n\n| # | 事実 | 出典 | 確認方法 | 使う章 |\n|:--|:--|:--|:--|:--|\n"
        "| 1 | 事実A | X | 実物 | §1 |\n")   # §2 が抜けている
    ok.append(check("⑫ 素材#と「使う章」のズレ", "validate_yama_consistency.py",
                    _os2.path.join(d4, "Master.md"), "「使う章」に §2 が無い"))

    # ⑪ 主題占有率（2026-09-02 追加）— 他事件・全国統計での水増しを止める
    #    旧稿の戸沢村は §19 受傷部位統計 / §22 1994年 新潟県笹神村 / §24 月別・時間帯統計 で
    #    外部素材だけの章が18.4%あった。同じ形を注入して、止まるかを確かめる。
    import os as _os
    fs_body = (
        "# 素材シート: テスト\n\n"
        "| # | 事実 | 出典 | 確認方法 | 使う章 |\n|:--|:--|:--|:--|:--|\n"
        "| 1 | 本件の事実A | X | 実物 | §1 |\n"
        "| 2 | 本件の事実B | X | 実物 | §1 |\n"
        "| 3 | 〔外部〕全国統計A | Y | 実物 | §2 |\n"
        "| 4 | 〔外部〕別の事件B | Y | 実物 | §2 |\n"
    )

    def mk(dirname, ext_chars):
        d = _os.path.join(tmp, dirname)
        _os.makedirs(d, exist_ok=True)
        open(_os.path.join(d, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(fs_body)
        pl = (
            "# プロット表: テスト\n\n- 目標尺: 28分\n- 前半ピーク: 1\n- 後半ピーク: 1\n\n"
            "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
            "| 1 | 本件の章 | SHO | 動き | 5000 | 1,2 |\n"
            f"| 2 | 他事件の章 | SHO | データ | {ext_chars} | 3,4 |\n"
        )
        f = _os.path.join(d, "Plot_Sheet_test.md")
        open(f, "w", encoding="utf-8").write(pl)
        return f

    ok.append(check("⑪ 外部素材だけの章が28.6%（旧稿の形）", "validate_yama_plot.py",
                    mk("ext_ng", 2000), "主題占有率 —"))

    f = mk("ext_ok", 500)
    code, out = run("validate_yama_plot.py", f)
    hit = "主題占有率 —" not in out
    print(f"  {'✅' if hit else '❌'} {'⑪ b 外部素材が9.1%なら通す':<42} validate_yama_plot.py")
    ok.append(hit)

    d = _os.path.join(tmp, "ext_nosheet")
    _os.makedirs(d, exist_ok=True)
    open(_os.path.join(d, "Plot_Sheet_test.md"), "w", encoding="utf-8").write(
        "# プロット表: テスト\n\n- 目標尺: 28分\n- 前半ピーク: 1\n- 後半ピーク: 1\n\n"
        "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
        "| 1 | 本件の章 | SHO | 動き | 9000 | 1,2 |\n")
    ok.append(check("⑪ c 素材シートが無ければ空振りを告げる", "validate_yama_plot.py",
                    _os.path.join(d, "Plot_Sheet_test.md"), "主題占有率を測れません"))

    # ⑩ リファレンス未読で Master.md を書こうとするとブロックされるか
    proj = os.path.abspath(os.path.join(HERE, "..", ".."))
    hook = os.path.join(proj, ".claude", "hooks", "guard-yama-script-reference.sh")
    if os.path.exists(hook):
        st = os.path.join(proj, ".claude", ".state", "yama_reads_selftest.log")
        if os.path.exists(st): os.remove(st)
        env = {**os.environ, "CLAUDE_PROJECT_DIR": proj}
        import json as _json
        cases = [
            ({"tool_name": "Write", "tool_input": {"file_path": "/x/Yama_Story/Scripts/e/Master.md"}}, 2, "Write"),
            ({"tool_name": "Bash", "tool_input": {"command": "python3 -c \"open('/x/Master.md','w').write(s)\""}}, 2, "Bash経由の書き込み"),
            ({"tool_name": "Bash", "tool_input": {"command": "grep -n x /x/Master.md"}}, 0, "読み取りは素通り"),
        ]
        for payload, want, label in cases:
            payload["session_id"] = "selftest"
            r = subprocess.run(["bash", hook], input=_json.dumps(payload), capture_output=True, text=True, env=env)
            hit = r.returncode == want
            print(f"  {'✅' if hit else '❌'} {'⑩ 未読ガード: ' + label:<42} guard-yama-script-reference.sh")
            ok.append(hit)

    shutil.rmtree(tmp)
    print()
    n, t = sum(ok), len(ok)
    print(f"{n}/{t} 件が期待どおり動作")
    if n == t:
        print("[PASS] 過去に起きたミスは、すべて機械で止まります")
        return 0
    print("[FAIL] 止まらないミスが残っています")
    return 1

if __name__ == "__main__":
    sys.exit(main())
