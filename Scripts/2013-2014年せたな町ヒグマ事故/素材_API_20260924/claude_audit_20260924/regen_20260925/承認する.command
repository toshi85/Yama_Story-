#!/bin/zsh
# ダブルクリックで開く。6つの資料の画像の見本を、1つずつ「承認」と打って承認する。
cd "${0:A:h}"
G=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/generation_gate.py
for f in Fix4 Fix2 Fix3 Fix5a Fix5b Fix5c; do
  until python3 $G status "Asset_Prompts_$f.md" | sed -n 2p | grep -q "まだ見本が無い種類 なし"; do echo "$f の見本を作っています…"; sleep 20; done
  python3 $G approve "Asset_Prompts_$f.md" --kind image
done
echo "終わりました。この画面は閉じてください。"
