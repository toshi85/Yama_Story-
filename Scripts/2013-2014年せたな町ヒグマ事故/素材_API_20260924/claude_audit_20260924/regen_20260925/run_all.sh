#!/bin/zsh
# 2026-09-26: 生成リストの画像を全資料ぶん作り切る。1枚が2回失敗して止まったら、そのカットを後回し（defer）にして残りを続ける。
# 全資料を1周したら後回しを戻してもう1周。最大4周。飛ばす（skip_ids）は ChatGPT が描かないと確定したカット。
set -u
cd "${0:A:h}"
PY=/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python
RUN=/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen/run.py
touch .imagegen/skip_ids.txt .imagegen/defer_ids.txt
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
left() { $PY - <<'PY'
import json, pathlib
q = json.load(open('image_queue.json'))
skip = set(pathlib.Path('.imagegen/skip_ids.txt').read_text().split()) | set(pathlib.Path('.imagegen/defer_ids.txt').read_text().split())
print(sum(1 for x in q if x['id'] not in skip and not pathlib.Path('images', x['id'] + '.png').exists()))
PY
}
defer_failed() { $PY - <<'PY'
import json, pathlib
st = json.load(open('.imagegen/parallel_state.json'))
d = pathlib.Path('.imagegen/defer_ids.txt'); ids = set(d.read_text().split())
new = [i for i, n in st.get('attempts', {}).items() if n >= 2 and not pathlib.Path('images', i + '.png').exists()]
ids |= set(new); d.write_text('\n'.join(sorted(ids)) + '\n'); print('後回し:', new)
PY
}
for round in 1 2 3 4; do
  : > .imagegen/defer_ids.txt
  for fix in Fix5c Fix5b Fix5a Fix4 Fix2 Fix3; do
    python3 make_queue_for_list.py "$fix" --write >/dev/null
    stall=0
    while [ "$(left)" -gt 0 ] && [ $stall -lt 6 ]; do
      before=$(left)
      echo "===== $(date +%H:%M) 周${round} ${fix} 残り ${before}枚"
      reset_tabs
      ex=$(cat .imagegen/skip_ids.txt .imagegen/defer_ids.txt | tr '\n' ',' | sed 's/,$//')
      $PY -X utf8 "$RUN" "$PWD" --exclude "$ex" > .imagegen/last_run.log 2>&1
      grep -q "同じ項目が2回失敗" .imagegen/last_run.log && defer_failed
      [ "$(left)" -ge "$before" ] && stall=$((stall+1)) || stall=0
    done
    echo "===== $(date +%H:%M) 周${round} ${fix} おわり（残り $(left)枚・後回し $(wc -l < .imagegen/defer_ids.txt | tr -d ' ')件）"
  done
  total=$($PY -c "
import json,pathlib,importlib.util,sys
spec=importlib.util.spec_from_file_location('mq','make_queue_for_list.py'); mq=importlib.util.module_from_spec(spec); sys.argv=['x']; spec.loader.exec_module(mq)
q,_,_=mq.build(); skip=set(pathlib.Path('.imagegen/skip_ids.txt').read_text().split())
print(sum(1 for x in q if x['id'] not in skip and not pathlib.Path('images',x['id']+'.png').exists()))")
  echo "===== $(date +%H:%M) 周${round} 全体の残り ${total}枚"
  [ "$total" -eq 0 ] && break
done
echo "===== 全部終わり $(date +%m/%d\ %H:%M)"; ls images | grep -c png
