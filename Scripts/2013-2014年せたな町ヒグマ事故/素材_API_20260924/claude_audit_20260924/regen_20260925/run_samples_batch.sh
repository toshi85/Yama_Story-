#!/bin/zsh
# 2026-09-25: 残り5資料の見本（種類ごとに1枚）を順番に作る。承認前は関所が種類ごと1件に絞る。
set -u
cd "${0:A:h}"
PY=/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python
RUN=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen/run.py
reset_tabs() {
  $PY - <<'PY'
import sys; sys.path.insert(0, '/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen')
import chrome_bridge as b
for t in b.tabs():
    if 'chatgpt.com/c/' in t.get('url', ''):
        b.command(t['webSocketDebuggerUrl'], 'Page.navigate', {'url': 'https://chatgpt.com/'})
PY
  sleep 8
}
for spec in "Fix2 ASSET-009_still,ASSET-017_char,ASSET-015_bg" "Fix3 ASSET-026_bg,ASSET-027_char" "Fix5a ASSET-053_bg,ASSET-058_still,ASSET-060_char" "Fix5b ASSET-101_bg,ASSET-107_char,ASSET-141_still" "Fix5c ASSET-161_bg,ASSET-161_char,ASSET-169_still"; do
  fix=${spec%% *}; ids=${spec#* }
  echo "===== $fix $ids  $(date +%H:%M)"
  python3 make_queue_for_list.py "$fix" --write --ids "$ids" 2>&1 | tail -1 || { echo "キュー作成失敗 $fix"; continue; }
  reset_tabs
  $PY -X utf8 "$RUN" "$PWD" 2>&1 | grep -v "^\s*$" | tail -6
done
echo "===== 終了 $(date +%H:%M)"; ls images | grep png
