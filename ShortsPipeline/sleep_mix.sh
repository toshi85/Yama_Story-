#!/bin/bash
# ============================================================
# Yama_Story 睡眠用まとめ動画生成
# 使い方: ./sleep_mix.sh <動画ファイル> [動画ファイル] ...
#
# 編集者からもらったSE・BGMなし動画を:
#   1. 音量均一化
#   2. 複数本を結合（間に3秒の無音）
#   3. 1本の睡眠用動画として出力
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/sleep-output"
WORK_DIR="$OUTPUT_DIR/work"

# --- 引数チェック ---
if [ $# -eq 0 ]; then
  echo "❌ エラー: 動画ファイルを1つ以上指定してください"
  echo "使い方: ./sleep_mix.sh <ファイル1> [ファイル2] [ファイル3] ..."
  echo "例:     ./sleep_mix.sh ~/Downloads/ep01_no_se.mp4 ~/Downloads/ep02_no_se.mp4"
  exit 1
fi

# --- 入力ファイル存在チェック ---
for FILE in "$@"; do
  if [ ! -f "$FILE" ]; then
    echo "❌ エラー: ファイルが見つかりません: $FILE"
    exit 1
  fi
done

# --- ディレクトリ準備 ---
mkdir -p "$WORK_DIR"

NORM_FILES=()
INDEX=0

for FILE in "$@"; do
  INDEX=$((INDEX + 1))
  echo "=========================================="
  echo "[$INDEX/${#@}] 処理中: $(basename "$FILE")"
  echo "=========================================="

  # --- 音量均一化 ---
  echo "🔊 音量均一化中..."
  NORM_FILE="$WORK_DIR/norm_${INDEX}.wav"
  ffmpeg -y -i "$FILE" -filter:a loudnorm=I=-16:TP=-1.5:LRA=11 "$NORM_FILE" 2>/dev/null
  echo "✅ 完了"

  NORM_FILES+=("$NORM_FILE")
done

# --- 結合 ---
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ ${#NORM_FILES[@]} -eq 1 ]; then
  FINAL="$OUTPUT_DIR/sleep_${TIMESTAMP}.wav"
  cp "${NORM_FILES[0]}" "$FINAL"
else
  echo "=========================================="
  echo "🔗 ${#NORM_FILES[@]}本を結合中..."
  echo "=========================================="

  CONCAT_LIST="$WORK_DIR/concat_list.txt"
  SILENCE="$WORK_DIR/silence_3s.wav"

  # 3秒の無音ファイル生成
  ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t 3 "$SILENCE" 2>/dev/null

  > "$CONCAT_LIST"
  for i in "${!NORM_FILES[@]}"; do
    echo "file '${NORM_FILES[$i]}'" >> "$CONCAT_LIST"
    if [ $i -lt $((${#NORM_FILES[@]} - 1)) ]; then
      echo "file '$SILENCE'" >> "$CONCAT_LIST"
    fi
  done

  FINAL="$OUTPUT_DIR/sleep_${TIMESTAMP}.wav"
  ffmpeg -y -f concat -safe 0 -i "$CONCAT_LIST" -c copy "$FINAL" 2>/dev/null
fi

echo "=========================================="
echo "✅ 完成！"
echo "📁 出力: $FINAL"

# ファイルサイズと長さ表示
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL" 2>/dev/null)
HOURS=$(echo "$DURATION / 3600" | bc)
MINS=$(echo "($DURATION % 3600) / 60" | bc)
SIZE=$(du -h "$FINAL" | cut -f1)
echo "⏱️  長さ: ${HOURS}時間${MINS}分"
echo "💾 サイズ: $SIZE"
echo "=========================================="

# --- クリーンアップ ---
echo "🧹 作業ファイル削除中..."
rm -rf "$WORK_DIR"
echo "✅ 完了"
