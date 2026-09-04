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

# --- 3点セットの強制（2026-09-02 新設）-------------------------------------
#   矛盾検査を書いたとき、1回目も2回目も「素通りする検査」を書いてしまった。
#   どちらも「止まるべき入力」しか試していなかったからではなく、
#   **通すべき入力での確認を後回しにしたまま直したつもりになっていた**のが原因。
#
#   検査が「効く」と言えるのは、次の3つが揃ったときだけ:
#     ① 事故そのもの（過去に実際に起きた形）  → FAIL する
#     ② 直した版                             → PASS する
#     ③ 出荷済みの全台本                      → 誤検知しない（check_calibration.py の担当）
#
#   ①だけなら「何でも赤くする検査」が通ってしまう。②が無いと素通りに気づけない。
#   ここでは ①と② がペアで登録されているかを機械で確かめる。
import re as _re
REGISTRY = []          # [(グループ記号, "fail"|"pass", 表示名, 検査スクリプト)]

def _group_of(name):
    # ⚠️ ①〜⑳ は U+2460〜、㉑〜㉟ は U+3251〜 で連続していない。
    #    範囲を ①-⑳ だけにしていると ㉑ 以降が対にならず、増やした瞬間に赤くなる（2026-09-03）
    m = _re.match(r"^([\u2460-\u2473\u3251-\u325f])", name.strip())
    return m.group(1) if m else name.strip()[:2]

def check(name, script, path, must_contain):
    """事故そのものを注入して、止まることを確かめる"""
    code, out = run(script, path)
    hit = must_contain in out
    REGISTRY.append((_group_of(name), "fail", name, script))
    print(f"  {'✅' if hit else '❌'} {name:<42} {script}")
    if not hit:
        print(f"      期待: 「{must_contain}」を含む出力 / 実際の末尾: {out.strip().splitlines()[-1][:70] if out.strip() else '(空)'}")
    return hit

def check_pass(name, script, path, must_not_contain):
    """直した版を通して、余計に止めないことを確かめる"""
    code, out = run(script, path)
    hit = must_not_contain not in out
    REGISTRY.append((_group_of(name), "pass", name, script))
    print(f"  {'✅' if hit else '❌'} {name:<42} {script}")
    if not hit:
        print(f"      「{must_not_contain}」が出てはいけない場面で出ています（誤検知）")
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
    ok.append(check_pass("①b 証言導入を誤検出しない", "validate_yama_narrative.py",
                         p, "❌ [メタ語り禁止"))

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
    ok.append(check_pass("③b 遺体が本文なら通る", "validate_yama_safety.py",
                         p, "タイトル/サムネのみ"))

    # ④ 完全重複ナレ行
    d = os.path.join(tmp, "dup"); os.makedirs(d)
    p = os.path.join(d, "Master.md")
    open(p, "w", encoding="utf-8").write(HEAD + "\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n\n## 2. 別の章\n\nナレーター: クマは二人に出会った場合、動いているほうの人を襲う。\n")
    ok.append(check("④ 完全重複ナレ行", "validate_yama_consistency.py", p, "完全重複ナレ行"))

    # ⑰ 辻褄検査（2026-09-03 新設）— 章タイトルと本文が反対
    d17 = os.path.join(tmp, "coh1"); os.makedirs(d17)
    p = os.path.join(d17, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 4. クマが、そこから動かなかった\n\n"
        "ナレーター: ブナの木の下にいたクマは、間もなく姿を消します。\n\n"
        "ナレーター: しかし6人は、男性を運び出すことを諦めました。\n")
    ok.append(check("⑰ 章タイトルと本文が反対", "validate_yama_coherence.py", p, "章タイトルと本文が反対"))
    d17b = os.path.join(tmp, "coh1b"); os.makedirs(d17b)
    p = os.path.join(d17b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 4. クマが、そこから動かなかった\n\n"
        "ナレーター: 6人は声を上げ、石を投げつけます。\n\n"
        "ナレーター: しかし、それでもクマはその場に居座り続けました。\n")
    ok.append(check_pass("⑰b 直した版は通る", "validate_yama_coherence.py", p, "章タイトルと本文が反対"))

    # ⑱ 同じ章の中で反対のことを言う（説明なし）
    d18 = os.path.join(tmp, "coh2"); os.makedirs(d18)
    p = os.path.join(d18, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n\n"
        "ナレーター: 新聞は、成果は上がらなかった、と書いています。\n\n"
        "ナレーター: ただし、新聞に載らなかったことがあります。\n\n"
        "ナレーター: 猟友会は1週間に7頭から8頭のクマを捕らえています。\n")
    ok.append(check("⑱ 同じ章で反対（成果なし↔捕獲）", "validate_yama_coherence.py", p, "同じ章の中で反対"))
    d18b = os.path.join(tmp, "coh2b"); os.makedirs(d18b)
    p = os.path.join(d18b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n\n"
        "ナレーター: 新聞は、成果は上がらなかった、と書いています。\n\n"
        "ナレーター: 猟友会は7頭から8頭のクマを捕らえています。\n\n"
        "ナレーター: それでも「成果なし」でした。探していたのは男性を襲った1頭で、"
        "捕らえたどれがそれなのか、記録は食い違ったままです。\n")
    ok.append(check_pass("⑱b 食い違いを明示すれば通る", "validate_yama_coherence.py", p, "同じ章の中で反対"))

    # ⑲ 資料に無い部分を埋めたのに、太字で示していない（2026-09-03 新設）
    d19 = os.path.join(tmp, "coh3"); os.makedirs(d19)
    p = os.path.join(d19, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n"
        "<!-- src: 素材#75。⚠️「胃の内容物を確認」は資料に無い＝人間側の確定判断 -->\n\n"
        "ナレーター: 7頭から8頭のクマを捕らえ胃の内容物を確認しました。\n")
    ok.append(check("⑲ 推測を埋めたのに太字が無い", "validate_yama_coherence.py", p, "太字が1つも無い"))
    d19b = os.path.join(tmp, "coh3b"); os.makedirs(d19b)
    p = os.path.join(d19b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n"
        "<!-- src: 素材#75。⚠️「胃の内容物を確認」は資料に無い＝人間側の確定判断 -->\n\n"
        "ナレーター: 7頭から8頭のクマを捕らえ**胃の内容物を確認しました**。\n")
    ok.append(check_pass("⑲b 太字で示せば通る", "validate_yama_coherence.py", p, "太字が1つも無い"))

    # ⑳ 太字の閉じ方がドキュメントで壊れる（2026-09-03 新設）
    d20 = os.path.join(tmp, "coh4"); os.makedirs(d20)
    p = os.path.join(d20, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 2. 最初に山へ入った人\n"
        "<!-- src: 素材#120。⚠️ 資料に無い＝人間側の確定判断 -->\n\n"
        "ナレーター: **家族にタケノコを採りにいくと伝え、**午前10時ごろに出発。\n")
    ok.append(check("⑳ 太字の閉じ方がドキュメントで壊れる", "validate_yama_coherence.py", p, "太字の閉じ方"))
    d20b = os.path.join(tmp, "coh4b"); os.makedirs(d20b)
    p = os.path.join(d20b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 2. 最初に山へ入った人\n"
        "<!-- src: 素材#120。⚠️ 資料に無い＝人間側の確定判断 -->\n\n"
        "ナレーター: **家族にタケノコを採りにいくと伝え**、午前10時ごろに出発。\n")
    ok.append(check_pass("⑳b 読点を印の外へ出せば通る", "validate_yama_coherence.py", p, "太字の閉じ方"))

    # ㉑ 素材シートがあるのに src の無い章（2026-09-03 新設）
    d21 = os.path.join(tmp, "coh5"); os.makedirs(d21)
    open(os.path.join(d21, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(
        "| # | 事実 | 出典 | 確認 | 使う章 |\n|--:|:--|:--|:--|:--|\n| 1 | テスト素材 | X | Y | §2 |\n")
    p = os.path.join(d21, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 2. 結論を先に出す章\n\n"
        "ナレーター: 日本クマネットワークの報告書にも、こう書かれています。\n\n"
        "ナレーター: 同じ1頭だった可能性が考えられる。\n\n"
        "ナレーター: 2016年の十和利山でも、クマは移動しています。\n")
    ok.append(check("㉑ 素材シートがあるのに src の無い章", "validate_yama_coherence.py", p, "src がありません"))
    d21b = os.path.join(tmp, "coh5b"); os.makedirs(d21b)
    open(os.path.join(d21b, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(
        "| # | 事実 | 出典 | 確認 | 使う章 |\n|--:|:--|:--|:--|:--|\n| 1 | テスト素材 | X | Y | §2 |\n")
    open(os.path.join(d21b, "Plot_Sheet_test.md"), "w", encoding="utf-8").write(
        "| 章 | タイトル | PART | 種別 | 設計 | 実測 | 素材# |\n|--:|:--|:--|:--|--:|--:|:--|\n"
        "| 2 | 結論を先に出す章 | SHO | 説明 | 60 | 60 | 1 |\n")
    p = os.path.join(d21b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 2. 結論を先に出す章\n"
        "<!-- src: 報告書＝素材#1 -->\n\n"
        "ナレーター: 日本クマネットワークの報告書にも、こう書かれています。\n\n"
        "ナレーター: 同じ1頭だった可能性が考えられる。\n\n"
        "ナレーター: 2016年の十和利山でも、クマは移動しています。\n")
    ok.append(check_pass("㉑b src を書けば通る", "validate_yama_coherence.py", p, "src がありません"))

    # ㉒ 時間が飛ぶのに、飛んだと分かる行が無い（2026-09-03 新設）
    d22 = os.path.join(tmp, "coh6"); os.makedirs(d22)
    p = os.path.join(d22, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n\n"
        "ナレーター: 1988年5月27日。\n\n"
        "ナレーター: 猟友会が緊急許可を取ります。\n\n"
        "## 7. クルミを拾いに\n\n"
        "ナレーター: 1988年10月6日。\n\n"
        "ナレーター: 59歳の女性が、クルミを拾いに出かけました。\n")
    ok.append(check("㉒ 132日飛ぶのに飛んだと分かる行が無い", "validate_yama_coherence.py", p,
                    "が飛びますが"))
    d22b = os.path.join(tmp, "coh6b"); os.makedirs(d22b)
    p = os.path.join(d22b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 6. 1週間の山狩り\n\n"
        "ナレーター: 1988年5月27日。\n\n"
        "ナレーター: 猟友会が緊急許可を取ります。\n\n"
        "## 7. クルミを拾いに\n\n"
        "ナレーター: それから4か月半、村は静かでした。\n\n"
        "ナレーター: 1988年10月6日。\n\n"
        "ナレーター: 59歳の女性が、クルミを拾いに出かけました。\n")
    ok.append(check_pass("㉒b 空いた時間を1行で言えば通る", "validate_yama_coherence.py", p, "が飛びますが"))

    # ㉓ 書籍の著者名を本文に出す（2026-09-03 新設）
    d23 = os.path.join(tmp, "author"); os.makedirs(d23)
    p = os.path.join(d23, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n<!-- src: 米田一彦『熊が人を襲うとき』p.206 -->\n\n"
        "ナレーター: 米田さんは、そう書いています。\n")
    ok.append(check("㉓ 書籍の著者名を本文に出す", "validate_yama_safety.py", p, "書籍の著者名"))
    d23b = os.path.join(tmp, "authorb"); os.makedirs(d23b)
    p = os.path.join(d23b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n<!-- src: 米田一彦『熊が人を襲うとき』p.206 -->\n\n"
        "ナレーター: 研究者は、そう見ています。\n")
    ok.append(check_pass("㉓b 名前を出さなければ通る", "validate_yama_safety.py", p, "書籍の著者名"))

    # ㉔ 本を出典として明かす言い回し（2026-09-03 新設）
    d24 = os.path.join(tmp, "book"); os.makedirs(d24)
    p = os.path.join(d24, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: ただし同じ本の別のページには、前から咬まれたと書かれています。\n")
    ok.append(check("㉔ 本を出典として明かす言い回し", "validate_yama_safety.py", p, "本を出典として明かす"))
    d24b = os.path.join(tmp, "bookb"); os.makedirs(d24b)
    p = os.path.join(d24b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: ただし同じ研究者は、別のところで、前から咬まれたと書いています。\n")
    ok.append(check_pass("㉔b 本だと分からない形なら通る", "validate_yama_safety.py", p, "本を出典として明かす"))

    # ㉕ 助数詞・標本・日本などを誤検知しない／SAFETY_OK 宣言で外せる（2026-09-03 新設）
    d25 = os.path.join(tmp, "bookfp"); os.makedirs(d25)
    p = os.path.join(d25, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 刃渡り5センチのナイフ一本で、ヒグマと向き合いました。\n\n"
        "ナレーター: 標本にしてみると、頭の骨に古い傷が残っていたのです。\n\n"
        "ナレーター: 日本では、こうした事故は多くありません。\n\n"
        "ナレーター: 星野さん自身、著書の中でこう書いています。"
        " <!-- SAFETY_OK: 本人がこの回の題材で、その人自身の著書を引くのは出典を隠す話とは別 -->\n")
    ok.append(check_pass("㉕ 助数詞・標本・日本とSAFETY_OK宣言を誤検知しない",
                         "validate_yama_safety.py", p, "本を出典として明かす"))
    d25b = os.path.join(tmp, "bookfpb"); os.makedirs(d25b)
    p = os.path.join(d25b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 星野さん自身、著書の中でこう書いています。\n")
    ok.append(check("㉕b 宣言が無ければ止まる", "validate_yama_safety.py", p, "本を出典として明かす"))

    # ㉖ 同じ数字を資料を変えて二度言う（2026-09-03 新設）
    d26 = os.path.join(tmp, "dupnum"); os.makedirs(d26)
    p = os.path.join(d26, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 20. 44年で、三人だけ\n\n"
        "ナレーター: 山形県は、1977年から2020年までの人身事故を一覧にしています。\n\n"
        "ナレーター: そのなかで、命が失われたと記録されているのは、1988年の3件だけ。\n\n"
        "ナレーター: 日本クマネットワークの報告書も、同じことを書いています。\n\n"
        "ナレーター: 記録が残る1977年から2008年までで、命が失われた事故は、この3件だけです。\n")
    ok.append(check("㉖ 同じ数字を資料を変えて二度言う", "validate_yama_coherence.py", p, "＋限定語を"))
    d26b = os.path.join(tmp, "dupnumb"); os.makedirs(d26b)
    p = os.path.join(d26b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 20. 44年で、三人だけ\n\n"
        "ナレーター: 山形県は、1977年から2020年までの人身事故を一覧にしています。\n\n"
        "ナレーター: そのなかで、命が失われたと記録されているのは、1988年の3件だけ。\n\n"
        "ナレーター: 日本クマネットワークの報告書も、同じ3件を挙げています。\n")
    ok.append(check_pass("㉖b 二つ目を畳めば通る", "validate_yama_coherence.py", p, "＋限定語を"))

    # ㉗ 発言に「」が付いていない（2026-09-03 新設・WARN）
    d27 = os.path.join(tmp, "quote"); os.makedirs(d27)
    p = os.path.join(d27, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 佐藤浩人さんは、こう話しています。\n\n"
        "ナレーター: 3件目のあと、この村で同じことは起きていない。\n")
    ok.append(check("㉗ 発言に「」が付いていない", "validate_yama_narrative.py", p, "発言に「」が付いていません"))
    d27b = os.path.join(tmp, "quoteb"); os.makedirs(d27b)
    p = os.path.join(d27b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 佐藤浩人さんは、こう話しています。\n\n"
        "ナレーター: 「3件目のあと、この村で同じことは起きていない」\n")
    ok.append(check_pass("㉗b 「」で囲めば通る", "validate_yama_narrative.py", p, "発言に「」が付いていません"))

    # ㉘ 発言の帰属が前に出ている（2026-09-03 新設・WARN）
    d28 = os.path.join(tmp, "attr"); os.makedirs(d28)
    p = os.path.join(d28, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 小林室長は、こう話しています。\n\n"
        "ナレーター: 「事件の前か後かは不明です」\n")
    ok.append(check("㉘ 発言の帰属が前に出ている", "validate_yama_narrative.py", p, "帰属が前に出ています"))
    d28b = os.path.join(tmp, "attrb"); os.makedirs(d28b)
    p = os.path.join(d28b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 小林室長は、「事件の前か後かは不明ですが、\n\n"
        "ナレーター: 農家に居ついていたようです」と話しています。\n")
    ok.append(check_pass("㉘b セリフの後に帰属を置けば通る", "validate_yama_narrative.py", p, "帰属が前に出ています"))

    # ㉙ 列挙の前に個数を宣言（2026-09-03 新設・WARN）
    d29 = os.path.join(tmp, "cnt"); os.makedirs(d29)
    p = os.path.join(d29, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 1頭だと考える根拠は、三つ。\n\n"
        "ナレーター: 傷の場所が、よく似ていること。\n")
    ok.append(check("㉙ 列挙の前に個数を宣言", "validate_yama_narrative.py", p, "列挙の前に個数を宣言"))
    d29b = os.path.join(tmp, "cntb"); os.makedirs(d29b)
    p = os.path.join(d29b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n\n"
        "ナレーター: 1頭だと考える根拠としては、\n\n"
        "ナレーター: 傷の場所が、よく似ていること。\n\n"
        "ナレーター: また、最初の2件の現場が、200メートルしか離れていないこと。\n\n"
        "ナレーター: 湖の中でも、最も奥まった場所のひとつです。\n")
    ok.append(check_pass("㉙b 数を出さず「また」で継げば通る／「〜のひとつ」は誤検知しない",
                         "validate_yama_narrative.py", p, "列挙の前に個数を宣言"))

    # ㉚ 引用の改変（否定が消えて意味が逆になる）2026-09-03 新設
    d30 = os.path.join(tmp, "quotemod"); os.makedirs(d30)
    open(os.path.join(d30, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(
        "| # | 事実 | 出典 | 確認 | 使う章 |\n|--:|:--|:--|:--|:--|\n"
        "| 1 | 佐藤さん「昔は裏手の山肌は歩くけど、ここに出なかったんですよ。ここ1、2年だね」 | note | 実物 | §1 |\n")
    p = os.path.join(d30, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n<!-- src: 素材#1 -->\n\n"
        "ナレーター: 「昔は裏手の山肌は歩くけど、ここに出たんですよ。ここ1、2年だね」と話しています。\n")
    ok.append(check("㉚ 引用の改変（否定が消える）", "validate_yama_facts.py", p, "引用の改変"))
    d30b = os.path.join(tmp, "quotemodb"); os.makedirs(d30b)
    open(os.path.join(d30b, "Fact_Sheet_test.md"), "w", encoding="utf-8").write(
        "| # | 事実 | 出典 | 確認 | 使う章 |\n|--:|:--|:--|:--|:--|\n"
        "| 1 | 佐藤さん「昔は裏手の山肌は歩くけど、ここに出なかったんですよ。ここ1、2年だね」 | note | 実物 | §1 |\n")
    p = os.path.join(d30b, "Master.md")
    open(p, "w", encoding="utf-8").write(
        "# T\n\n## 1. テスト\n<!-- src: 素材#1 -->\n\n"
        "ナレーター: 「昔は裏手の山肌は歩くけど、ここに出なかったんですよ」と話しています。\n")
    ok.append(check_pass("㉚b 抜粋なら通る（書き換えでなければよい）",
                         "validate_yama_facts.py", p, "引用の改変"))

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
    ok.append(check_pass("⑧b 「」で囲めば通る", "validate_yama_narrative.py",
                         p, "話し言葉が括弧の外"))

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

    # ⑬ 設計からの乖離（2026-09-02 追加）— しきい値を満たすための水増しを止める
    #    2026-09-02 の戸沢村で、起が5%フロアぎりぎりだったため §2 を149→232字（+56%）に膨らませた。
    #    そのあとプロット表を本文から再生成したので差が消えていた。同じ形を注入して、止まるか確かめる。
    import os as _os3
    def mkdrift(dirname, plan, real):
        d = _os3.path.join(tmp, dirname); _os3.makedirs(d, exist_ok=True)
        open(_os3.path.join(d, "Fact_Sheet_d.md"), "w", encoding="utf-8").write(
            "# 素材シート\n\n| # | 事実 | 出典 | 確認方法 | 使う章 |\n|:--|:--|:--|:--|:--|\n"
            "| 1 | 事実A | X | 実物 | §1 |\n| 2 | 事実B | X | 実物 | §2 |\n")
        f = _os3.path.join(d, "Plot_Sheet_d.md")
        open(f, "w", encoding="utf-8").write(
            "# プロット表\n\n- 目標尺: 28分\n- 前半ピーク: 1\n- 後半ピーク: 1\n\n"
            "| 章 | タイトル | PART | 種別 | 設計字数 | 実測字数 | 素材# |\n|--:|:--|:--|:--|--:|--:|:--|\n"
            "| 1 | 本編 | SHO | 動き | 9000 | 9000 | 1 |\n"
            f"| 2 | 膨らませた章 | KI | 説明 | {plan} | {real} | 2 |\n")
        return f

    ok.append(check("⑬ 設計149字を本文で232字に膨らませた", "validate_yama_plot.py",
                    mkdrift("drift_ng", 149, 232), "設計からの乖離"))

    f = mkdrift("drift_ok", 149, 160)   # +7%
    ok.append(check_pass("⑬ b ±15%以内なら通す", "validate_yama_plot.py",
                         f, "設計からの乖離"))

    d = _os3.path.join(tmp, "drift_old"); _os3.makedirs(d, exist_ok=True)
    open(_os3.path.join(d, "Plot_Sheet_d.md"), "w", encoding="utf-8").write(
        "# プロット表\n\n- 目標尺: 28分\n- 前半ピーク: 1\n- 後半ピーク: 1\n\n"
        "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |\n|--:|:--|:--|:--|--:|:--|\n"
        "| 1 | 本編 | SHO | 動き | 9000 | 1 |\n")
    ok.append(check("⑬ c 6列の旧形式は検知できないと告げる", "validate_yama_plot.py",
                    _os3.path.join(d, "Plot_Sheet_d.md"), "「設計字数」列がありません"))

    # ⑭ 起の切り方（2026-09-02 確定の設計ルール）
    #    起 = フック ＋ 最初の被害者の日常 ＋「その日常が崩れる予感」の一行。承はそこから事件の具体。
    import os as _os4
    def mkki(name, last):
        f = _os4.path.join(tmp, name + ".md")
        sho = "ナレーター: " + ("日が暮れます。山の中は、もう何も見えません。" * 120)
        ten = "ナレーター: " + ("その後、村は変わりました。" * 20)
        body = HEAD + "\nナレーター: 1988年5月25日。山形県の戸沢村。\nナレーター: 深夜、男性が遺体で発見。\nナレーター: なぜ、三度も繰り返されたのか。\nナレーター: そしてなぜ、満腹なのに人を食べたのか？\nナレーター: 地形図とともに解説します。\n\n## 2. 最初に山へ入った人\nナレーター: 戸沢村は、山形県の北にあります。人口はおよそ4,300人。\nナレーター: この村に住む61歳の男性が、タケノコを採りに山へ入りました。\nナレーター: 農業を営む人でした。家を出たのは午前十時ごろでした。\nナレーター: 何十年も繰り返されてきた、ふつうの一日のはずでした。\n{LAST}\n\n<!-- PART: SHO -->\n## 3. 戻らなかった一日\nナレーター: {SHO}\n\n<!-- PART: TEN-KETSU -->\n## 4. その後\nナレーター: {TEN}\n"
        body = body.replace("{LAST}", "ナレーター: " + last)
        body = body.replace("ナレーター: {SHO}", sho).replace("ナレーター: {TEN}", ten)
        open(f, "w", encoding="utf-8").write(body)
        return f

    ok.append(check("⑭ 起が舞台説明で終わっている", "validate_yama_intro.py",
                    mkki("ki_ng", "それほど自然との距離が近い環境でした。"),
                    "「日常が崩れる予感」で終わっていません"))

    f = mkki("ki_ok", "ところが、この日は戻りません。")
    ok.append(check_pass("⑭ b 逆接＋不在で終わっていれば通す", "validate_yama_intro.py",
                         f, "「日常が崩れる予感」で終わっていません"))

    f = mkki("ki_ok2", "そんな人物が、この日、命を落とすことになるとは、誰一人、想像していなかったはずです。")
    ok.append(check_pass("⑭ c 前振り型（朱鞠内湖の形）も通す", "validate_yama_intro.py",
                         f, "「日常が崩れる予感」で終わっていません"))

    # ㉛ CQ（イントロの問い2つ）の回収位置と、その見送り宣言（2026-09-04 新設）
    #    転にも本文にも答えが無いなら止める。本人が「本文の中で答えているので転では言い直さない」
    #    と決めた回は `<!-- CQ_OK: 理由（8字以上） -->` で外せる。理由が短ければ止める。
    f = mkki("cq_ng", "ところが、この日は戻りません。")
    ok.append(check("㉛ CQが転で回収されていない", "validate_yama_intro.py",
                    f, "が転で回収されていません"))

    f2 = mkki("cq_ok", "ところが、この日は戻りません。")
    _s = open(f2, encoding="utf-8").read()
    open(f2, "w", encoding="utf-8").write(
        "<!-- CQ_OK: 答えは本文の中で語っているので転では言い直さない -->\n" + _s)
    ok.append(check_pass("㉛b CQ_OK 宣言があれば見送る", "validate_yama_intro.py",
                         f2, "が転で回収されていません"))

    f3 = mkki("cq_short", "ところが、この日は戻りません。")
    _s = open(f3, encoding="utf-8").read()
    open(f3, "w", encoding="utf-8").write("<!-- CQ_OK: 不要 -->\n" + _s)
    ok.append(check("㉛c CQ_OK の理由が短ければ止める", "validate_yama_intro.py",
                    f3, "CQ_OK の理由が短すぎます"))

    # ⑮ V字（ボトムの宣言）2026-09-02
    #    出典: たちばなやすひと『「物語」の見つけ方』。落差を省略しないための宣言。
    import os as _os5
    _FS_V = ("# 素材シート\n\n| # | 事実 | 出典 | 確認方法 | 使う章 |\n"
             "|:--|:--|:--|:--|:--|\n| 1 | 事実A | X | 実物 | §1 |\n")
    _ROWS_V = ("| 章 | タイトル | PART | 種別 | 設計字数 | 実測字数 | 素材# |\n"
               "|--:|:--|:--|:--|--:|--:|:--|\n"
               "| 1 | 本編 | SHO | 動き | 8000 | 8000 | 1 |\n"
               "| 2 | 山場 | TEN-KETSU | 動き | 1000 | 1000 | 1 |\n")

    def mkbottom(name, bottom_line):
        d = _os5.path.join(tmp, name)
        _os5.makedirs(d, exist_ok=True)
        open(_os5.path.join(d, "Fact_Sheet_v.md"), "w", encoding="utf-8").write(_FS_V)
        f = _os5.path.join(d, "Plot_Sheet_v.md")
        head = ("# プロット表\n\n- 目標尺: 28分\n- 前半ピーク: 1\n- 後半ピーク: 2\n"
                + bottom_line + "\n")
        open(f, "w", encoding="utf-8").write(head + _ROWS_V)
        return f

    ok.append(check("⑮ ボトムの宣言が無い", "validate_yama_plot.py",
                    mkbottom("v_none", ""), "「- ボトム: <章番号>」の宣言がありません"))

    ok.append(check("⑮b ボトムが承の外にある", "validate_yama_plot.py",
                    mkbottom("v_bad", "- ボトム: 2"), "承（SHO）にありません"))

    ok.append(check_pass("⑮c 承の中なら通す", "validate_yama_plot.py",
                         mkbottom("v_ok", "- ボトム: 1"), "承（SHO）にありません"))

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
    ok.append(check_pass("⑪ b 外部素材が9.1%なら通す", "validate_yama_plot.py",
                         f, "主題占有率 —"))

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

    # ⑯ 台本内の相互矛盾（2026-09-02）
    #    出典: 戸沢村 §9「二人目は前から」と §19「三件とも後ろから」を両方断定していた。
    #    米田 p.206 と p.208 で記述が割れているのに、割れていると書かなかった。
    import os as _os6
    def mkcontra(name, line19):
        d = _os6.path.join(tmp, name)
        _os6.makedirs(d, exist_ok=True)
        p = _os6.path.join(d, "Master.md")
        open(p, "w", encoding="utf-8").write(
            "<!-- PART: KI -->" + chr(10) +
            "## 9. 200メートル" + chr(10) +
            "ナレーター: 一人目は背後から。二人目は前から。" + chr(10) +
            "## 19. 防ぎ方" + chr(10) + line19 + chr(10))
        return p

    ok.append(check("⑯ 全称の断定が個別章と矛盾している", "validate_yama_consistency.py",
                    mkcontra("contra_bad",
                             "ナレーター: 三件とも、クマは身を伏せて、後ろから襲ってきました。"),
                    "台本内の矛盾"))

    ok.append(check_pass("⑯b 食い違いを当の章で明示すれば通す", "validate_yama_consistency.py",
                         mkcontra("contra_ok",
                                  "ナレーター: 三件とも後ろからとされますが、記録は食い違ったままです。"),
                         "台本内の矛盾"))

    # ---- 「通すべきケース」の補完（2026-09-02）--------------------------
    #   メタチェックを入れたら、②④⑤⑥⑦⑨⑫ は「止まる」しか試していなかった。
    #   正常な入力で余計に止めないことを、ここで1件ずつ確かめる。
    import os as _os7
    dn = _os7.path.join(tmp, "normal"); _os7.makedirs(dn, exist_ok=True)

    # 正常な3点セット。§1=9字 / §2=9字 でプロット表・素材シートと一致させる
    open(_os7.path.join(dn, "Master.md"), "w", encoding="utf-8").write(
        HEAD + chr(10) + "ナレーター: ダミーの一行です。" + chr(10) * 2 +
        "## 2. 二章目" + chr(10) + "ナレーター: もう一行のダミー。" + chr(10))
    open(_os7.path.join(dn, "Plot_Sheet_n.md"), "w", encoding="utf-8").write(
        "# プロット表" + chr(10) * 2 +
        "| 章 | タイトル | PART | 種別 | 設計字数 | 実測字数 | 素材# |" + chr(10) +
        "|--:|:--|:--|:--|--:|--:|:--|" + chr(10) +
        "| 1 | フック | KI | フック | 9 | 9 | 1 |" + chr(10) +
        "| 2 | 二章目 | SHO | 動き | 9 | 9 | 2 |" + chr(10))
    open(_os7.path.join(dn, "Fact_Sheet_n.md"), "w", encoding="utf-8").write(
        "# 素材シート" + chr(10) * 2 +
        "| # | 事実 | 出典 | 確認方法 | 使う章 |" + chr(10) +
        "|:--|:--|:--|:--|:--|" + chr(10) +
        "| 1 | 事実A | X | 実物 | §1 |" + chr(10) +
        "| 2 | 事実B | X | 実物 | §2 |" + chr(10))
    _mn = _os7.path.join(dn, "Master.md")

    ok.append(check_pass("④b 重複が無ければ通す", "validate_yama_consistency.py",
                         _mn, "完全重複ナレ行"))
    ok.append(check_pass("⑤b 表と本文の字数が一致すれば通す", "validate_yama_consistency.py",
                         _mn, "字数の不一致"))
    ok.append(check_pass("⑥b 使う章が本文にあれば通す", "validate_yama_consistency.py",
                         _mn, "「使う章」が本文に存在しない"))
    ok.append(check_pass("⑫b 素材#と使う章が双方向で合えば通す", "validate_yama_consistency.py",
                         _mn, "「使う章」に §2 が無い"))

    # ② 固有名詞が2回以上出ていれば孤立ではない
    p = _os7.path.join(tmp, "orphan_ok.md")
    open(p, "w", encoding="utf-8").write(
        "ナレーター: 村の真ん中を、最上川が西へ流れています。" + chr(10) +
        "ナレーター: その最上川の岸に、集落があります。" + chr(10))
    ok.append(check_pass("②b 2回以上出る固有名詞は通す", "validate_yama_narrative.py",
                         p, "[孤立した固有名詞] Line"))

    # ⑨ 引用先を先に置き、述語を後ろに回した正しい形
    p = _os7.path.join(tmp, "attr_ok.md")
    open(p, "w", encoding="utf-8").write(
        "ナレーター: 米田さんは、こう記しています。" + chr(10) +
        "ナレーター: 満腹の状態でありながら、人を食べていた。" + chr(10))
    ok.append(check_pass("⑨b 引用先が先にあれば通す", "validate_yama_narrative.py",
                         p, "帰属だけの単独行"))

    # ⑦ 素材密度が 120字/素材 以下なら通す
    p = _os7.path.join(tmp, "Plot_Sheet_sparse.md")
    open(p, "w", encoding="utf-8").write(
        "- 前半ピーク: 1" + chr(10) + "- 後半ピーク: 1" + chr(10) * 2 +
        "| 章 | タイトル | PART | 種別 | 目標字数 | 素材# |" + chr(10) +
        "|--:|:--|:--|:--|--:|:--|" + chr(10) +
        "| 1 | フック | KI | フック | 220 | 2,3 |" + chr(10))
    ok.append(check_pass("⑦b 110字/素材なら通す", "validate_yama_plot.py",
                         p, "素材密度"))

    shutil.rmtree(tmp)

    # --- メタチェック: 3点セットが揃っているか ---------------------------
    print()
    print("-" * 74)
    print("メタチェック — 各検査に「止まるべき」と「通すべき」が両方あるか")
    print("-" * 74)
    groups = {}
    for g, kind, name, script in REGISTRY:
        groups.setdefault(g, {"fail": [], "pass": [], "script": script})[kind].append(name)
    lonely = []
    for g in sorted(groups, key=lambda x: (len(x), x)):
        v = groups[g]
        both = v["fail"] and v["pass"]
        mark = "✅" if both else "❌"
        miss = "" if both else ("  ← 通すべきケースが無い" if not v["pass"] else "  ← 止まるべきケースが無い")
        print(f"  {mark} {g}  止まる{len(v['fail'])}件 / 通す{len(v['pass'])}件  {v['script']}{miss}")
        if not both:
            lonely.append(g)
    meta_ok = not lonely
    ok.append(meta_ok)
    if lonely:
        print()
        print(f"  片側だけの検査が {len(lonely)}件: {' '.join(lonely)}")
        print("  → 「止まる」しか試していない検査は、素通りしていても気づけない。")
        print("     矛盾検査では実際にそれで2回、素通りする検査を書いた（YCP-033）。")

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
