#!/bin/sh
cd /Users/tosimasa/Desktop/Antigravity || exit 125
export PYTHONDONTWRITEBYTECODE=1
.venv-edit/bin/python System_Tools/edit/splice_rebuild.py '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/shots.json' --master '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/studio/jobs/20260908150535_c2a000ce/full_下書き.mp4' --shots 7,8 --out '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/review_revised.mp4'
splice_rc=$?
printf "%s\n" "$splice_rc" > '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/splice_exit_20260910.txt'
exit "$splice_rc"
