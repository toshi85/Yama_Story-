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
    r = subprocess.run([PY, os.path.join(HERE, script), path], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

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
    print("検査の自己試験 — 2026-09-01 のミスを注入して、止まるか確かめる")
    print("=" * 74)

    # ① メタ語り（Gate 6）
    p = os.path.join(tmp, "meta.md")
    open(p, "w").write("ナレーター: ここで一度、山形県が残している資料を開きます。\nナレーター: 見つかった場所を、地図で見てみます。\n")
    ok.append(check("① メタ語り「ここで〜を開きます」", "validate_yama_narrative.py", p, "❌ [メタ語り禁止"))

    # ①b 証言導入は誤検出しないこと
    p = os.path.join(tmp, "quote.md")
    open(p, "w").write("ナレーター: 佐藤さんは、こう振り返ります。\nナレーター: ひどかったな、あれは。\n")
    code, out = run("validate_yama_narrative.py", p)
    hit = "❌ [メタ語り禁止" not in out and code == 0
    print(f"  {'✅' if hit else '❌'} {'①b 証言導入を誤検出しない':<42} validate_yama_narrative.py")
    ok.append(hit)

    # ② 孤立した固有名詞（Gate 7・警告）
    p = os.path.join(tmp, "orphan.md")
    open(p, "w").write("ナレーター: 村の真ん中を、最上川が西へ流れています。\nナレーター: 山に入りました。\n")
    ok.append(check("② 孤立した固有名詞（最上川）", "validate_yama_narrative.py", p, "[孤立した固有名詞] Line"))

    # ③ 遺体はタイトルで止まり、本文では止まらない
    p = os.path.join(tmp, "title.md")
    open(p, "w").write("# 遺体で発見された事件\n\nナレーター: 山で見つかりました。\n")
    ok.append(check("③ 遺体がタイトルにあると止まる", "validate_yama_safety.py", p, "タイトル/サムネのみ"))
    p = os.path.join(tmp, "body.md")
    open(p, "w").write("# ふつうのタイトル\n\nナレーター: 深夜、男性が遺体で発見。\n")
    code, out = run("validate_yama_safety.py", p)
    hit = code == 0
    print(f"  {'✅' if hit else '❌'} {'③b 遺体が本文なら通る':<42} validate_yama_safety.py")
    ok.append(hit)

    # ④ 完全重複ナレ行
    d = os.path.join(tmp, "dup"); os.makedirs(d)
    p = os.path.join(d, "Master.md")
    open(p, "w").write(HEAD + "\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n\n## 2. 別の章\n\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n")
    ok.append(check("④ 完全重複ナレ行", "validate_yama_consistency.py", p, "完全重複ナレ行"))

    # ⑤ プロット表の字数ズレ
    d2 = os.path.join(tmp, "stale"); os.makedirs(d2)
    open(os.path.join(d2, "Master.md"), "w").write(HEAD + "\nナレーター: 十文字ちょうどの行。\n")
    open(os.path.join(d2, "Plot_Sheet_test.md"), "w").write(
        "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n| 1 | フック | KI | フック | 999 | 1 |\n")
    ok.append(check("⑤ プロット表の字数が本文とズレ", "validate_yama_consistency.py", os.path.join(d2, "Master.md"), "字数の不一致"))

    # ⑥ 素材シートの「使う章」が本文に無い
    d3 = os.path.join(tmp, "chap"); os.makedirs(d3)
    open(os.path.join(d3, "Master.md"), "w").write(HEAD + "\nナレーター: ダミー。\n")
    open(os.path.join(d3, "Fact_Sheet_test.md"), "w").write(
        "| # | 事実 | 出典 | 確認方法 | 使う章 |\n|:--|:--|:--|:--|:--|\n| 1 | ダミー | 米田 | 同上 | §99 |\n")
    ok.append(check("⑥ 素材シートの使う章が本文に無い", "validate_yama_consistency.py", os.path.join(d3, "Master.md"), "「使う章」が本文に存在しない"))

    # ⑦ 素材密度（字数÷素材数）— 創作の予防
    p = os.path.join(tmp, "Plot_Sheet_dense.md")
    open(p, "w").write(
        "- 前半ピーク: 1\n- 後半ピーク: 1\n\n| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
        "| 1 | フック | KI | フック | 298 | 2 |\n")
    ok.append(check("⑦ 素材1つで298字（創作の温床）", "validate_yama_plot.py", p, "素材密度"))

    # ⑧ 証言が「」の外（ナレーターが一人称で話す）
    p = os.path.join(tmp, "colloq.md")
    open(p, "w").write("ナレーター: 俺、持ったけど。甥っ子が背負って。\nナレーター: 嫌だったよな。\n")
    ok.append(check("⑧ 話し言葉が括弧の外（俺／よな）", "validate_yama_narrative.py", p, "話し言葉が括弧の外"))

    # ⑧b 正しく「」で囲めば通る
    p = os.path.join(tmp, "quoted.md")
    open(p, "w").write("ナレーター: 佐藤さんは、取材にこう話しています。\nナレーター: 「俺、持ったけど。嫌だったよな」\n")
    code, out = run("validate_yama_narrative.py", p)
    hit = "❌ [話し言葉が括弧の外" not in out and code == 0
    print(f"  {'✅' if hit else '❌'} {'⑧b 「」で囲めば通る':<42} validate_yama_narrative.py")
    ok.append(hit)

    # ⑨ 帰属だけの単独行を後ろに置く
    p = os.path.join(tmp, "attr.md")
    open(p, "w").write("ナレーター: 満腹の状態でありながら、人を食べていた。\nナレーター: 米田さんは、そう記しています。\n")
    ok.append(check("⑨ 後置の「そう記しています。」単独行", "validate_yama_narrative.py", p, "帰属だけの単独行"))

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
        print("[PASS] 2026-09-01 のミスは、すべて機械で止まります")
        return 0
    print("[FAIL] 止まらないミスが残っています")
    return 1

if __name__ == "__main__":
    sys.exit(main())
