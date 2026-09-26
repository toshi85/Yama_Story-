#!/bin/zsh
# 2026-09-26: 指定した資料・IDだけを生成する（本人の修正指示分）。全部そろうか5回やり直したら終わる。
# 使い方: ./gen_batch.sh Fix5a "CHAR-11" && ./gen_batch.sh Fix5a "ASSET-063_char,..."
set -u
cd "${0:A:h}"
PY=/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python
fix=$1; ids=$2
for id in ${(s:,:)ids}; do [ -f images/$id.png ] && mv images/$id.png rejected/${id}_before_$(date +%H%M).png && rm -f .imagegen/receipts/$id.json; done
# 2026-09-26: 止めた回の送信中の結果を次の回が拾わないよう、前回の送信状態を片付けてから始める
#   （写実寄りの見本で描いた 074 が、止めた後の再開で「保存済み」として残った）
[ -f .imagegen/parallel_state.json ] && mv .imagegen/parallel_state.json rejected/parallel_state_$(date +%H%M%S).json
python3 make_queue_for_list.py "$fix" --write --ids "$ids" | tail -1
for t in 1 2 3 4 5; do
  miss=$(python3 -c "import json,pathlib; print(sum(1 for q in json.load(open('image_queue.json')) if not pathlib.Path('images',q['id']+'.png').exists()))")
  [ "$miss" -eq 0 ] && break
  echo "$(date +%H:%M) $fix 残り ${miss}枚（${t}回目）"
  $PY - <<'PY'
import sys; sys.path.insert(0, '/Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen')
import chrome_bridge as b
for t in b.tabs():
    if 'chatgpt.com/c/' in t.get('url', ''):
        b.command(t['webSocketDebuggerUrl'], 'Page.navigate', {'url': 'https://chatgpt.com/'})
PY
  sleep 8
  $PY -X utf8 /Users/tosimasa/Desktop/Antigravity/Yama_Story/System_Tools/imagegen/run.py "$PWD" > .imagegen/gen_batch_last.log 2>&1
  # 2026-09-26: 合格票と一致しない等で run.py が止めたときは、やり直さず理由を出して終える（黙って 0/14 で終わっていた）
  if grep -q "^❌" .imagegen/gen_batch_last.log; then
    echo "$(date +%H:%M) $fix 止まった理由:"; grep -A1 "^❌" .imagegen/gen_batch_last.log | cut -c1-300
    exit 2
  fi
done
echo "$(date +%H:%M) $fix おわり: $(python3 -c "import json,pathlib; q=json.load(open('image_queue.json')); print(sum(1 for x in q if pathlib.Path('images',x['id']+'.png').exists()),'/',len(q))")"
