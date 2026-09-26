#!/bin/zsh
# 2026-09-25 夜: 承認済みの資料から、生成リストの画像を全部作る。上限に当たったら解除時刻まで待って続ける。
# 順番は Fix4 が先（CHAR-05〜07 の基準画像を作り、以後のキャラに添えるため）。承認がまだの資料は承認されるまで待つ。
set -u
cd "${0:A:h}"
PY=/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python
RUN=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen/run.py
GATE=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/generation_gate.py
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
left() { $PY - "$1" <<'PY'
import json, sys, pathlib
q = json.load(open('image_queue.json'))
skip = set(pathlib.Path('.imagegen/skip_ids.txt').read_text().split()) if pathlib.Path('.imagegen/skip_ids.txt').exists() else set()
print(sum(1 for x in q if x['id'] not in skip and not pathlib.Path('images', x['id'] + '.png').exists()))
PY
}
# 見本づくりが終わるのを待つ（同じ作業フォルダで二重に回さない）
for fix in ${=FIXES:-Fix4 Fix2 Fix3 Fix5a Fix5b Fix5c}; do
  until python3 $GATE status "Asset_Prompts_$fix.md" | sed -n 2p | grep -q "見本承認=済"; do
    echo "$(date +%H:%M) $fix は承認待ち"; sleep 300
  done
  python3 make_queue_for_list.py "$fix" --write | tail -1
  tries=0
  while [ "$(left $fix)" -gt 0 ] && [ $tries -lt 8 ]; do
    tries=$((tries+1))
    echo "===== $(date +%H:%M) $fix 残り $(left ${fix})枚（${tries}回目）"
    reset_tabs
    skip=$(tr '\n' ',' < .imagegen/skip_ids.txt 2>/dev/null | sed 's/,$//')
    $PY -X utf8 "$RUN" "$PWD" --exclude "$skip" 2>&1 | grep -v "^\s*$" | tail -8
    code=${pipestatus[1]}
    if [ -f .imagegen/limit_until.json ]; then
      until_ts=$(python3 -c "import json; print(int(json.load(open('.imagegen/limit_until.json'))['until']))")
      now=$(date +%s); wait=$(( until_ts - now + 120 ))
      if [ $wait -gt 0 ]; then echo "$(date +%H:%M) 上限。$(date -r $until_ts +%m/%d\ %H:%M) まで待つ"; sleep $wait; tries=$((tries-1)); fi
      rm -f .imagegen/limit_until.json
    fi
  done
  echo "===== $(date +%H:%M) $fix 完了（残り $(left ${fix})枚）"
done
echo "===== 全部終わり $(date +%m/%d\ %H:%M)"; ls images | grep -c png
