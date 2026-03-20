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
WHISPER_BIN="/Users/tosimasa/Library/Python/3.9/bin/mlx_whisper"

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
    --model mlx-community/whisper-small-mlx \
    --language ja \
    --output-format json \
    --output-dir "$PROJECT_DIR" \
    --word-timestamps True

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
# STEP 3: Demucsで音源分離（BGM除去）
# ============================================================
echo ""
echo "🎵 STEP 3: Demucsでナレーション抽出中..."

VOCALS_WAV="$PROJECT_DIR/vocals.wav"
CLEAN_MP4="$PROJECT_DIR/clean.mp4"

if [ -f "$CLEAN_MP4" ]; then
  echo "  ⏭️  音源分離済み（スキップ）"
else
  # Demucsでボーカル（ナレーション）を抽出
  python3 -m demucs --two-stems=vocals -o "$PROJECT_DIR/separated" "$SOURCE_MP4" 2>/dev/null

  # Demucs出力パスを特定（htdemucs/ファイル名/vocals.wav）
  DEMUCS_DIR=$(find "$PROJECT_DIR/separated" -name "vocals.wav" -print -quit 2>/dev/null | xargs dirname)
  if [ -z "$DEMUCS_DIR" ]; then
    echo "  ❌ Demucs出力が見つかりません"
    exit 1
  fi
  VOCALS_WAV="$DEMUCS_DIR/vocals.wav"

  # ナレーション音声を元動画の映像と再合成（BGMなし版のマスター）
  ffmpeg -y -i "$SOURCE_MP4" -i "$VOCALS_WAV" \
    -c:v copy -map 0:v:0 -map 1:a:0 \
    -c:a aac -b:a 192k \
    "$CLEAN_MP4" 2>/dev/null

  echo "  ✅ 完了: clean.mp4（ナレーションのみ）"
fi

# ============================================================
# STEP 4: FFmpegで分割（2バージョン）
# ============================================================
echo ""
echo "🔪 STEP 4: 動画分割中（BGMあり版 + BGMなし版）..."

SEG_DIR="$PROJECT_DIR/segments"
SEG_DIR_NOBGM="$PROJECT_DIR/segments_nobgm"
mkdir -p "$SEG_DIR" "$SEG_DIR_NOBGM"

# BGM楽曲の確認
BGM_FILE=""
if [ -f "$ASSETS_DIR/bgm.mp3" ]; then
  BGM_FILE="$ASSETS_DIR/bgm.mp3"
elif [ -f "$ASSETS_DIR/bgm.wav" ]; then
  BGM_FILE="$ASSETS_DIR/bgm.wav"
elif [ -f "$ASSETS_DIR/bgm.m4a" ]; then
  BGM_FILE="$ASSETS_DIR/bgm.m4a"
fi

export CUTS_JSON CLEAN_MP4 SOURCE_MP4 SEG_DIR SEG_DIR_NOBGM BGM_FILE
python3 << 'SPLIT_EOF'
import json, subprocess, os, sys

CUTS_JSON = os.environ["CUTS_JSON"]
CLEAN_MP4 = os.environ["CLEAN_MP4"]
SOURCE_MP4 = os.environ["SOURCE_MP4"]
SEG_DIR = os.environ["SEG_DIR"]
SEG_DIR_NOBGM = os.environ["SEG_DIR_NOBGM"]
BGM_FILE = os.environ.get("BGM_FILE", "")

with open(CUTS_JSON) as f:
    data = json.load(f)

for cut in data["cuts"]:
    ep = cut["episode"]
    start = cut["start"]
    end = cut["end"]
    title = cut.get("title", f"第{ep}話")

    s_sec = float(start.split(":")[0])*3600 + float(start.split(":")[1])*60 + float(start.split(":")[2])
    e_sec = float(end.split(":")[0])*3600 + float(end.split(":")[1])*60 + float(end.split(":")[2])
    duration = e_sec - s_sec

    # --- BGMなし版（clean.mp4からカット） ---
    out_nobgm = f"{SEG_DIR_NOBGM}/ep{ep:02d}.mp4"
    if not os.path.exists(out_nobgm):
        cmd = [
            "ffmpeg", "-y", "-ss", start, "-i", CLEAN_MP4,
            "-t", str(duration),
            "-c:v", "libx264", "-c:a", "aac", "-preset", "fast",
            "-avoid_negative_ts", "make_zero", out_nobgm
        ]
        print(f"  ✂️  Part {ep} (BGMなし): {start} → {end}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  ✅ {os.path.basename(out_nobgm)}")
        else:
            print(f"  ❌ エラー: {r.stderr[-200:]}")
            sys.exit(1)
    else:
        print(f"  ⏭️  Part {ep} (BGMなし): 分割済み")

    # --- BGMあり版（clean.mp4 + BGMをミックス） ---
    out_bgm = f"{SEG_DIR}/ep{ep:02d}.mp4"
    if not os.path.exists(out_bgm):
        if BGM_FILE and os.path.exists(BGM_FILE):
            # ナレーション + BGMをミックス（BGM音量を下げる）
            cmd = [
                "ffmpeg", "-y", "-ss", start, "-i", CLEAN_MP4,
                "-stream_loop", "-1", "-i", BGM_FILE,
                "-t", str(duration),
                "-filter_complex",
                "[0:a]volume=1.0[voice];[1:a]volume=0.15[music];[voice][music]amix=inputs=2:duration=first[aout]",
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "libx264", "-c:a", "aac", "-preset", "fast",
                "-avoid_negative_ts", "make_zero",
                "-shortest", out_bgm
            ]
            print(f"  ✂️  Part {ep} (BGMあり): {start} → {end}")
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0:
                print(f"  ✅ {os.path.basename(out_bgm)}")
            else:
                print(f"  ❌ エラー: {r.stderr[-200:]}")
                sys.exit(1)
        else:
            # BGMファイルがない場合はBGMなし版をコピー
            import shutil
            shutil.copy2(out_nobgm, out_bgm)
            print(f"  ⚠️  Part {ep}: BGMファイル未設定 → BGMなし版をコピー")
    else:
        print(f"  ⏭️  Part {ep} (BGMあり): 分割済み")
SPLIT_EOF

echo "  ✅ 分割完了（2バージョン）"

# ============================================================
# STEP 5: FFmpegで縦型変換 + 上下装飾（2バージョン）
# ============================================================
echo ""
echo "🎨 STEP 5: 縦型変換 + 装飾中..."

OUT_DIR="$PROJECT_DIR/output"
OUT_DIR_NOBGM="$PROJECT_DIR/output_nobgm"
mkdir -p "$OUT_DIR" "$OUT_DIR_NOBGM"

# フォント設定
if [ -f "$ASSETS_DIR/font.ttf" ]; then
  FONT_PATH="$ASSETS_DIR/font.ttf"
elif [ -f "$ASSETS_DIR/font.otf" ]; then
  FONT_PATH="$ASSETS_DIR/font.otf"
else
  # 日本語パスはFFmpegでエスケープ問題が出るためシンボリックリンクを使用
  ln -sf "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc" /tmp/hiragino.ttc
  FONT_PATH="/tmp/hiragino.ttc"
fi

# サムネイル確認（プロジェクト固有の画像ファイルを自動検出）
THUMBNAIL_PATH=""
if [ -f "$PROJECT_DIR/thumbnail.png" ]; then
  THUMBNAIL_PATH="$PROJECT_DIR/thumbnail.png"
elif [ -f "$PROJECT_DIR/thumbnail.jpg" ]; then
  THUMBNAIL_PATH="$PROJECT_DIR/thumbnail.jpg"
else
  # thumbnail以外の名前の画像も検出（サムネ.jpg等）
  THUMBNAIL_PATH=$(find "$PROJECT_DIR" -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) ! -name ".*" 2>/dev/null | /usr/bin/head -1)
fi

# ロゴ確認
LOGO_PATH=""
if [ -f "$ASSETS_DIR/logo.png" ]; then
  LOGO_PATH="$ASSETS_DIR/logo.png"
fi

export CUTS_JSON SEG_DIR SEG_DIR_NOBGM OUT_DIR OUT_DIR_NOBGM FONT_PATH THUMBNAIL_PATH PROJECT_NAME
python3 << 'STEP5_EOF'
import json, subprocess, os, sys

CUTS_JSON = os.environ.get("CUTS_JSON", "")
FONT_PATH = os.environ.get("FONT_PATH", "/tmp/hiragino.ttc")
THUMBNAIL_PATH = os.environ.get("THUMBNAIL_PATH", "")
PROJECT_NAME = os.environ.get("PROJECT_NAME", "")

# 2バージョン処理: (入力セグメントDir, 出力Dir, ラベル)
versions = [
    (os.environ.get("SEG_DIR", ""), os.environ.get("OUT_DIR", ""), "BGMあり"),
    (os.environ.get("SEG_DIR_NOBGM", ""), os.environ.get("OUT_DIR_NOBGM", ""), "BGMなし"),
]

with open(CUTS_JSON) as f:
    data = json.load(f)

total_parts = len(data["cuts"])

for seg_dir, out_dir, label in versions:
  print(f"\n  --- {label}版 ---")
  for cut in data["cuts"]:
    ep = cut["episode"]
    input_seg = f"{seg_dir}/ep{ep:02d}.mp4"
    output_file = f"{out_dir}/ep{ep:02d}_short.mp4"

    if not os.path.exists(input_seg):
        print(f"  ⚠️  スキップ（ファイルなし）: ep{ep:02d}.mp4")
        continue

    if os.path.exists(output_file):
        print(f"  ⏭️  Part {ep}: 装飾済み（スキップ）")
        continue

    # 元動画の解像度を取得
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_streams", input_seg],
        capture_output=True, text=True
    )
    streams = json.loads(probe.stdout)
    video_stream = [s for s in streams["streams"] if s["codec_type"] == "video"][0]
    src_w = int(video_stream["width"])
    src_h = int(video_stream["height"])

    # 9:16 = 1080x1920、動画を横幅1080にフィット
    out_w, out_h = 1080, 1920
    scale_w = out_w
    scale_h = int(src_h * (out_w / src_w))
    part_text = f"Part {ep} / {total_parts}"
    cta_text = "▶ フォローして続きを見る"

    inputs = ["-i", input_seg]

    # サムネイルがある場合
    if THUMBNAIL_PATH and os.path.exists(THUMBNAIL_PATH):
        inputs.extend(["-i", THUMBNAIL_PATH])
        # サムネを上部に小さく配置、動画をその直下に詰める
        thumb_h = 160
        thumb_w = int(thumb_h * 16 / 9)
        if thumb_w > out_w - 40:
            thumb_w = out_w - 40
            thumb_h = int(thumb_w * 9 / 16)
        video_y = thumb_h + 15  # サムネ直下に詰める
        bottom_text_y = video_y + scale_h + 20
        filter_complex = (
            f"color=c=black:s={out_w}x{out_h}:r=30[bg];"
            f"[0:v]scale={scale_w}:{scale_h}[scaled];"
            f"[bg][scaled]overlay=0:{video_y}[base];"
            f"[1:v]scale={thumb_w}:{thumb_h}[thumbscaled];"
            f"[base][thumbscaled]overlay=(W-w)/2:5[withthumb];"
            f"[withthumb]drawtext=fontfile={FONT_PATH}:text='{PROJECT_NAME}'"
            f":fontsize=52:fontcolor=white:borderw=3:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y}[titled];"
            f"[titled]drawtext=fontfile={FONT_PATH}:text='{part_text}'"
            f":fontsize=40:fontcolor=#CCCCCC:borderw=2:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y + 65}[parted];"
            f"[parted]drawtext=fontfile={FONT_PATH}:text='{cta_text}'"
            f":fontsize=30:fontcolor=#FFD700:borderw=1:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y + 120}[final]"
        )
    else:
        # サムネなし: 動画を上端に詰める
        video_y = 10
        bottom_text_y = video_y + scale_h + 20
        filter_complex = (
            f"color=c=black:s={out_w}x{out_h}:r=30[bg];"
            f"[0:v]scale={scale_w}:{scale_h}[scaled];"
            f"[bg][scaled]overlay=0:{video_y}[base];"
            f"[base]drawtext=fontfile={FONT_PATH}:text='{PROJECT_NAME}'"
            f":fontsize=52:fontcolor=white:borderw=3:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y}[titled];"
            f"[titled]drawtext=fontfile={FONT_PATH}:text='{part_text}'"
            f":fontsize=40:fontcolor=#CCCCCC:borderw=2:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y + 65}[parted];"
            f"[parted]drawtext=fontfile={FONT_PATH}:text='{cta_text}'"
            f":fontsize=30:fontcolor=#FFD700:borderw=1:bordercolor=black"
            f":x=(w-text_w)/2:y={bottom_text_y + 120}[final]"
        )

    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", filter_complex,
        "-map", "[final]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "fast",
        "-r", "30",
        "-shortest",
        output_file
    ]

    print(f"  🎨 Part {ep}/{total_parts}: {PROJECT_NAME}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(output_file) // 1024 // 1024
        print(f"  ✅ 完成: ep{ep:02d}_short.mp4 ({size}MB)")
    else:
        print(f"  ⚠️  装飾エラー → フォールバック（パディングのみ）")
        simple_cmd = [
            "ffmpeg", "-y", "-i", input_seg,
            "-vf", f"scale={out_w}:-2,pad={out_w}:{out_h}:(ow-iw)/2:(oh-ih)/2:black",
            "-c:a", "aac", "-preset", "fast",
            output_file
        ]
        subprocess.run(simple_cmd, capture_output=True)
        print(f"  ✅ フォールバック完成: ep{ep:02d}_short.mp4")
STEP5_EOF

echo ""
echo "=========================================="
echo "🎉 パイプライン完了！"
echo "📁 BGMあり版: $OUT_DIR/"
echo "📁 BGMなし版: $OUT_DIR_NOBGM/"
echo "=========================================="
echo "BGMあり版（YouTube用）:"
ls -la "$OUT_DIR/" 2>/dev/null || echo "  (出力ファイルなし)"
echo "BGMなし版（TikTok/Instagram/Facebook/LINE VOOM用）:"
ls -la "$OUT_DIR_NOBGM/" 2>/dev/null || echo "  (出力ファイルなし)"
echo ""
echo "📱 投稿先:"
echo "   YouTube       → BGMあり版（$OUT_DIR/） + URL申請"
echo "   TikTok        → BGMなし版（$OUT_DIR_NOBGM/） + アプリ内楽曲後付け"
echo "   Instagram     → BGMなし版 + アプリ内楽曲後付け"
echo "   Facebook      → BGMなし版 + アプリ内楽曲後付け"
echo "   LINE VOOM     → BGMなし版そのまま"
