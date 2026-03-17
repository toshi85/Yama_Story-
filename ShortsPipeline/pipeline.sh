#!/bin/bash
# ============================================================
# Yama_Story ショート動画自動生成パイプライン
# 使い方: ./pipeline.sh projects/三毛別羆事件/
#
# プロジェクトフォルダ構造:
#   projects/動画名/
#     ├── source.mp4       ← 元動画（必須）
#     ├── thumbnail.png    ← サムネイル（任意）
#     ├── transcript.json  ← Whisper出力（自動生成）
#     ├── cuts.json        ← カットポイント（自動生成）
#     ├── segments/        ← 分割素材（自動生成）
#     └── output/          ← 完成ショート動画（自動生成）
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/assets"
WHISPER_BIN="/Users/tosimasa/Library/Python/3.9/bin/whisper"

# --- 引数チェック ---
if [ $# -eq 0 ]; then
  echo "❌ エラー: プロジェクトフォルダを指定してください"
  echo "使い方: ./pipeline.sh projects/動画名/"
  echo ""
  echo "📁 利用可能なプロジェクト:"
  for d in "$SCRIPT_DIR"/projects/*/; do
    [ -d "$d" ] && echo "   $(basename "$d")"
  done
  exit 1
fi

PROJECT_DIR="$(cd "$1" && pwd)"
PROJECT_NAME="$(basename "$PROJECT_DIR")"

# 元動画を探す
SOURCE_MP4="$PROJECT_DIR/source.mp4"
if [ ! -f "$SOURCE_MP4" ]; then
  # source.mp4以外のMP4も探す
  SOURCE_MP4=$(find "$PROJECT_DIR" -maxdepth 1 -name "*.mp4" | sort | /usr/bin/head -1)
  if [ -z "$SOURCE_MP4" ]; then
    echo "❌ エラー: MP4ファイルが見つかりません: $PROJECT_DIR/"
    echo "   source.mp4 を配置してください"
    exit 1
  fi
fi

echo "=========================================="
echo "🎬 Yama Shorts Pipeline"
echo "📁 プロジェクト: $PROJECT_NAME"
echo "🎥 元動画: $(basename "$SOURCE_MP4")"
echo "=========================================="

# ============================================================
# STEP 1: Whisperで文字起こし
# ============================================================
echo ""
echo "📝 STEP 1: Whisperで文字起こし中..."
TRANSCRIPT_JSON="$PROJECT_DIR/transcript.json"

if [ -f "$TRANSCRIPT_JSON" ]; then
  echo "  ⏭️  文字起こし済み（スキップ）"
else
  "$WHISPER_BIN" "$SOURCE_MP4" \
    --model medium \
    --language ja \
    --output_format json \
    --output_dir "$PROJECT_DIR" \
    --word_timestamps True

  # Whisperはファイル名ベースで出力するのでリネーム
  WHISPER_OUTPUT="$PROJECT_DIR/$(basename "$SOURCE_MP4" .mp4).json"
  if [ -f "$WHISPER_OUTPUT" ] && [ "$WHISPER_OUTPUT" != "$TRANSCRIPT_JSON" ]; then
    mv "$WHISPER_OUTPUT" "$TRANSCRIPT_JSON"
  fi
  echo "  ✅ 完了: transcript.json"
fi

# ============================================================
# STEP 2: カットポイント判断（Claude Codeが実行）
# ============================================================
CUTS_JSON="$PROJECT_DIR/cuts.json"

if [ -f "$CUTS_JSON" ]; then
  echo ""
  echo "✂️  STEP 2: カットポイント済み（スキップ）"
else
  echo ""
  echo "✂️  STEP 2: カットポイント判断が必要です"
  echo ""
  echo "  👉 Claude Codeで以下を実行してください:"
  echo "     /yama-shorts-cut $TRANSCRIPT_JSON"
  echo ""
  echo "  カットポイントJSONを保存したら、再度実行してください:"
  echo "     ./pipeline.sh projects/$PROJECT_NAME/"
  exit 0
fi

# ============================================================
# STEP 3: FFmpegで分割
# ============================================================
echo ""
echo "🔪 STEP 3: FFmpegで動画分割中..."

SEG_DIR="$PROJECT_DIR/segments"
mkdir -p "$SEG_DIR"

python3 -c "
import json, subprocess, sys, os

with open('$CUTS_JSON') as f:
    data = json.load(f)

for cut in data['cuts']:
    ep = cut['episode']
    start = cut['start']
    end = cut['end']
    title = cut.get('title', f'第{ep}話')
    output = f'$SEG_DIR/ep{ep:02d}.mp4'

    if os.path.exists(output):
        print(f'  ⏭️  Part {ep}: 分割済み（スキップ）')
        continue

    cmd = [
        'ffmpeg', '-y',
        '-ss', start,
        '-i', '$SOURCE_MP4',
        '-to', str(float(end.split(':')[0])*3600 + float(end.split(':')[1])*60 + float(end.split(':')[2]) - float(start.split(':')[0])*3600 - float(start.split(':')[1])*60 - float(start.split(':')[2])),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-avoid_negative_ts', 'make_zero',
        output
    ]
    print(f'  ✂️  Part {ep}: {start} → {end} ({title})')
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'  ✅ 保存: ep{ep:02d}.mp4')
    else:
        print(f'  ❌ エラー: {result.stderr[-200:]}')
        sys.exit(1)
"

echo "  ✅ 分割完了"

# ============================================================
# STEP 4: FFmpegで縦型変換 + 上下装飾
# ============================================================
echo ""
echo "🎨 STEP 4: 縦型変換 + 装飾中..."

OUT_DIR="$PROJECT_DIR/output"
mkdir -p "$OUT_DIR"

# フォント設定
if [ -f "$ASSETS_DIR/font.ttf" ]; then
  FONT_PATH="$ASSETS_DIR/font.ttf"
elif [ -f "$ASSETS_DIR/font.otf" ]; then
  FONT_PATH="$ASSETS_DIR/font.otf"
else
  FONT_PATH="/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
fi

# サムネイル確認（プロジェクト固有 → 共通assets）
THUMBNAIL_PATH=""
if [ -f "$PROJECT_DIR/thumbnail.png" ]; then
  THUMBNAIL_PATH="$PROJECT_DIR/thumbnail.png"
elif [ -f "$PROJECT_DIR/thumbnail.jpg" ]; then
  THUMBNAIL_PATH="$PROJECT_DIR/thumbnail.jpg"
fi

# ロゴ確認
LOGO_PATH=""
if [ -f "$ASSETS_DIR/logo.png" ]; then
  LOGO_PATH="$ASSETS_DIR/logo.png"
fi

python3 -c "
import json, subprocess, os, sys

CUTS_JSON = '$CUTS_JSON'
SEG_DIR = '$SEG_DIR'
OUT_DIR = '$OUT_DIR'
FONT_PATH = '$FONT_PATH'
THUMBNAIL_PATH = '$THUMBNAIL_PATH'
LOGO_PATH = '$LOGO_PATH'
PROJECT_NAME = '$PROJECT_NAME'

with open(CUTS_JSON) as f:
    data = json.load(f)

total_parts = len(data['cuts'])

for cut in data['cuts']:
    ep = cut['episode']
    title = cut.get('title', PROJECT_NAME)
    input_seg = f'{SEG_DIR}/ep{ep:02d}.mp4'
    output_file = f'{OUT_DIR}/ep{ep:02d}_short.mp4'

    if not os.path.exists(input_seg):
        print(f'  ⚠️  スキップ（ファイルなし）: ep{ep:02d}.mp4')
        continue

    if os.path.exists(output_file):
        print(f'  ⏭️  Part {ep}: 装飾済み（スキップ）')
        continue

    # 元動画の解像度を取得
    probe = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-print_format', 'json',
         '-show_streams', input_seg],
        capture_output=True, text=True
    )
    streams = json.loads(probe.stdout)
    video_stream = [s for s in streams['streams'] if s['codec_type'] == 'video'][0]
    src_w = int(video_stream['width'])
    src_h = int(video_stream['height'])

    # 9:16 = 1080x1920
    out_w = 1080
    out_h = 1920

    # 動画を横幅1080にフィット
    scale_w = out_w
    scale_h = int(src_h * (out_w / src_w))
    if scale_h > out_h:
        scale_h = out_h
        scale_w = int(src_w * (out_h / src_h))

    video_y = (out_h - scale_h) // 2
    top_margin = video_y
    bottom_margin = out_h - video_y - scale_h

    font_escaped = FONT_PATH.replace(':', r'\:').replace(\"'\", r\"\\'\")

    inputs = ['-i', input_seg]
    filter_parts = []

    # ベース: 黒背景 + 動画スケール + 中央配置
    filter_parts.append(
        f'color=c=black:s={out_w}x{out_h}:r=30[bg];'
        f'[0:v]scale={scale_w}:{scale_h}[scaled];'
        f'[bg][scaled]overlay=(W-w)/2:(H-h)/2[base]'
    )

    current_label = 'base'
    input_idx = 1

    # 上余白: サムネイル画像
    if THUMBNAIL_PATH:
        inputs.extend(['-i', THUMBNAIL_PATH])
        thumb_h = max(top_margin - 20, 100)
        thumb_w = int(thumb_h * 16 / 9)
        if thumb_w > out_w - 40:
            thumb_w = out_w - 40
            thumb_h = int(thumb_w * 9 / 16)
        next_label = f'thumb{ep}'
        filter_parts.append(
            f';[{input_idx}:v]scale={thumb_w}:{thumb_h}[thumbscaled];'
            f'[{current_label}][thumbscaled]overlay=(W-w)/2:10[{next_label}]'
        )
        current_label = next_label
        input_idx += 1

    # 下余白: タイトル（= プロジェクト名）+ Part表記
    bottom_text_y = video_y + scale_h + 20
    part_text = f'Part {ep} / {total_parts}'

    next_label = f'titled{ep}'
    filter_parts.append(
        f\";[{current_label}]drawtext=\"
        f\"fontfile='{font_escaped}'\"
        f\":text='{PROJECT_NAME}'\"
        f\":fontsize=52:fontcolor=white\"
        f\":borderw=3:bordercolor=black\"
        f\":x=(w-text_w)/2:y={bottom_text_y}\"
        f\"[{next_label}]\"
    )
    current_label = next_label

    final_label = f'final{ep}'
    filter_parts.append(
        f\";[{current_label}]drawtext=\"
        f\"fontfile='{font_escaped}'\"
        f\":text='{part_text}'\"
        f\":fontsize=40:fontcolor=#CCCCCC\"
        f\":borderw=2:bordercolor=black\"
        f\":x=(w-text_w)/2:y={bottom_text_y + 70}\"
        f\"[{final_label}]\"
    )

    filter_complex = ''.join(filter_parts)

    cmd = ['ffmpeg', '-y'] + inputs + [
        '-filter_complex', filter_complex,
        '-map', f'[{final_label}]',
        '-map', '0:a?',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-r', '30',
        '-shortest',
        output_file
    ]

    print(f'  🎨 Part {ep}/{total_parts}: {PROJECT_NAME}')
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'  ✅ 完成: ep{ep:02d}_short.mp4')
    else:
        print(f'  ⚠️  装飾エラー → フォールバック（パディングのみ）')
        simple_cmd = [
            'ffmpeg', '-y', '-i', input_seg,
            '-vf', f'scale={out_w}:-2,pad={out_w}:{out_h}:(ow-iw)/2:(oh-ih)/2:black',
            '-c:a', 'aac', '-preset', 'fast',
            output_file
        ]
        subprocess.run(simple_cmd, capture_output=True)
        print(f'  ✅ フォールバック完成: ep{ep:02d}_short.mp4')
"

echo ""
echo "=========================================="
echo "🎉 パイプライン完了！"
echo "📁 出力: $OUT_DIR/"
echo "=========================================="
ls -la "$OUT_DIR/" 2>/dev/null || echo "(出力ファイルなし)"
echo ""
echo "📱 YouTube Shorts / TikTok / Instagram Reels"
echo "   → 全て9:16縦型。そのままアップロード可能です。"
