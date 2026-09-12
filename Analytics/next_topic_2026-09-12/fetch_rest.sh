#!/bin/bash
cd /Users/tosimasa/Desktop/Antigravity/Yama_Story/Analytics/next_topic_2026-09-12
tail -n +2 channel_2_all.csv | cut -d, -f1 > ids_ch2.txt
cat ids_ch1.txt ids_ch2.txt | sort -u > ids_all.txt
n=0
while read -r id; do
  [ -z "$id" ] && continue
  f="video_full_default_${id}.json"
  if [ -s "$f" ]; then continue; fi
  yt-dlp --quiet --no-warnings --skip-download --dump-single-json "https://www.youtube.com/watch?v=${id}" > "$f" 2>/dev/null || rm -f "$f"
  n=$((n+1))
  sleep 2
done < ids_all.txt
echo "FETCH_DONE $n"
