#!/usr/bin/env python3
"""Master.md → Googleドキュメント 貼り付け用テキストを作る（2026-09-03 新設）

使い方:
    python3 sync_script_to_gdoc.py <Master.md> [--doc-dump 現在のドキュメント全文.txt]
    → クリップボードに入るので、ドキュメント側で ⌘A → 編集 > マークダウンから貼り付け

なぜこの道具が要るか（2026-09-03 に3回貼り直した）:
  ① 「書式なしで貼り付け（⌘⇧V）」だと ** が文字のまま残る。太字にならない
  ② 「マークダウンから貼り付け」だと太字にはなるが、**改行が全部つながって段落が壊れる**
     （Markdown では単一改行は改行にならない）→ 全行の末尾に半角スペース2つを付けて防ぐ
  ③ 閉じの ** の直前が読点だと強調として解釈されない（CommonMark の右フランキング規則）
     例: **家族に伝え、**午前10時 → 太字にならない。**家族に伝え**、午前10時 に直す

前提: ドキュメント側で ツール > 設定 > 「マークダウンを有効にする」が ON（2026-09-03 にユーザーが設定済み）
"""
import re
import subprocess
import sys

CLOSE_AFTER_PUNCT = re.compile(r"\*\*([^*]*?)([、。，．])\*\*")


def fix_bold_punctuation(text):
    """閉じ ** の直前の読点を、印の外へ出す。行末の 。** はそのままでよい"""
    fixed, n = [], 0
    for line in text.split("\n"):
        new = line
        for m in list(CLOSE_AFTER_PUNCT.finditer(line)):
            # 行末で閉じているものは Markdown が正しく解釈するので触らない
            if m.end() == len(line.rstrip()):
                continue
            new = new.replace(m.group(0), f"**{m.group(1)}**{m.group(2)}")
            n += 1
        fixed.append(new)
    return "\n".join(fixed), n


def narration(path):
    out = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("ナレーター:"):
            out.append(re.sub(r"\s*<!--.*?-->", "", line).rstrip())
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    master = sys.argv[1]
    lines = narration(master)
    body = "\n".join(lines)
    body, fixed = fix_bold_punctuation(body)
    if fixed:
        print(f"⚠️ 閉じ ** の直前の読点を {fixed} 箇所直しました。"
              f"Master.md 側も同じ形に直してください（そうしないと次回また出ます）")
    lines = body.split("\n")

    # ドキュメントの段落グループを保つ: 現在のドキュメント全文があれば、その空行配置に載せる
    dump = None
    if "--doc-dump" in sys.argv:
        dump = sys.argv[sys.argv.index("--doc-dump") + 1]
    if dump:
        doc = open(dump, encoding="utf-8").read().split("\n")
        idx = [i for i, l in enumerate(doc) if l.strip()]
        if len(idx) != len(lines):
            print(f"❌ 行数が違います: ドキュメント {len(idx)}行 / Master {len(lines)}行\n"
                  f"   章の増減があったときは、空行の入れ方を人が決める必要があります")
            return 1
        out = list(doc)
        for k, p in enumerate(idx):
            out[p] = lines[k] + "  "   # ← Markdown のハード改行
    else:
        out = [l + "  " for l in lines]

    text = "\n".join(out)
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
    bold = text.count("**") // 2
    print(f"✅ {len(out)}行 / 本文{len(lines)}行 / 太字{bold}箇所 をクリップボードへ")
    print("   ドキュメントで ⌘A → 編集 > マークダウンから貼り付け")
    print("   ⚠️ ⌘V も ⌘⇧V も駄目（** が文字のまま残る）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
