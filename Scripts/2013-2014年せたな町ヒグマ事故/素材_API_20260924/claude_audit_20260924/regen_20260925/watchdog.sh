#!/bin/zsh
# 2026-09-26: 画像が8分間1枚も保存されなければ、生成処理（run.py）を止める。run_all2.sh がすぐ立ち上げ直す。
# 本人「いま止まってたよね？」「同じミスを二度としないようにして」。記録は .imagegen/watchdog.log
cd "${0:A:h}"
while pgrep -f run_all2.sh >/dev/null; do
  newest=$(stat -f %m images/*.png 2>/dev/null | sort -n | tail -1)
  idle=$(( $(date +%s) - newest ))
  if [ $idle -gt 480 ] && pgrep -f "imagegen/run.py" >/dev/null; then
    echo "$(date +%H:%M) ${idle}秒保存なし → run.py を立ち上げ直し" >> .imagegen/watchdog.log
    pkill -f "imagegen/run.py"
    sleep 120
  fi
  sleep 30
done
echo "$(date +%H:%M) run_all2 終了で見張りも終了" >> .imagegen/watchdog.log
