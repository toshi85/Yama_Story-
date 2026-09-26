#!/bin/zsh
# ダブルクリックで開く。動画の見本（動画_H3/ の H3_032・058・160・178）を見たうえで、5つの資料の動画を1つずつ「承認」と打つ。
cd "${0:A:h}"
open 動画_H3
G=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/generation_gate.py
for f in Fix4 Fix5a Fix5b Fix5c Fix2; do
  python3 $G approve "Asset_Prompts_$f.md" --kind video
done
python3 $G approve "Asset_Prompts_Fix5a.md" --kind image
echo "終わりました。この画面は閉じてください。"
