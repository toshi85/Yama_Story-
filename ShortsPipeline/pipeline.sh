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
# STEP 0: サムネイル確認（なければ警告）
# ============================================================
THUMB_EXISTS=$(find "$PROJECT_DIR" -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) ! -name ".*" 2>/dev/null | /usr/bin/head -1)
if [ -z "$THUMB_EXISTS" ]; then
  echo ""
  echo "⚠️  サムネイル画像がありません"
  echo "   ショート動画にサムネイルが表示されません"
  echo "   thumbnail.jpg を $PROJECT_DIR/ に配置してください"
  echo ""
  echo "   YouTubeからダウンロードする場合:"
  echo "   yt-dlp --write-thumbnail --skip-download --convert-thumbnails jpg -o \"$PROJECT_DIR/thumbnail\" <URL>"
  echo ""
  read -p "   サムネイルなしで続行しますか？ (y/N): " CONTINUE_WITHOUT_THUMB
  if [ "$CONTINUE_WITHOUT_THUMB" != "y" ] && [ "$CONTINUE_WITHOUT_THUMB" != "Y" ]; then
    echo "   → 中止しました。サムネイルを配置してから再実行してください。"
    exit 0
  fi
fi

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
  # display_titleの存在チェック
  HAS_DISPLAY_TITLE=$(python3 -c "import json; d=json.load(open('$CUTS_JSON')); print('yes' if d.get('display_title') else 'no')" 2>/dev/null)
  if [ "$HAS_DISPLAY_TITLE" = "no" ]; then
    echo ""
    echo "⚠️  cuts.jsonに display_title がありません"
    echo "   フォルダ名「$PROJECT_NAME」がそのまま表示されます"
    echo "   cuts.jsonに display_title を追加してください（例: \"1行目\\n2行目\"）"
    echo ""
    read -p "   このまま続行しますか？ (y/N): " CONTINUE_WITHOUT_TITLE
    if [ "$CONTINUE_WITHOUT_TITLE" != "y" ] && [ "$CONTINUE_WITHOUT_TITLE" != "Y" ]; then
      echo "   → 中止しました。display_titleを追加してから再実行してください。"
      exit 0
    fi
  fi
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
# STEP 2.5: カット尺バリデーション（61秒未満をブロック）
# ============================================================
echo ""
echo "🔍 STEP 2.5: カット尺バリデーション..."

export CUTS_JSON
VALIDATION_RESULT=$(python3 << 'VALIDATE_EOF'
import json, os, sys

CUTS_JSON = os.environ["CUTS_JSON"]

with open(CUTS_JSON) as f:
    data = json.load(f)

errors = []
warnings = []
MIN_DURATION = 61
MAX_DURATION = 90

for cut in data["cuts"]:
    ep = cut["episode"]
    start = cut["start"]
    end = cut["end"]
    s_sec = float(start.split(":")[0])*3600 + float(start.split(":")[1])*60 + float(start.split(":")[2])
    e_sec = float(end.split(":")[0])*3600 + float(end.split(":")[1])*60 + float(end.split(":")[2])
    duration = e_sec - s_sec

    if duration < MIN_DURATION:
        errors.append(f"ep{ep:02d}: {duration:.0f}秒 (最低{MIN_DURATION}秒未満)")
    elif duration > MAX_DURATION:
        warnings.append(f"ep{ep:02d}: {duration:.0f}秒 (推奨{MAX_DURATION}秒超過)")

if errors:
    print("ERRORS")
    for e in errors:
        print(f"  ❌ {e}")
    for w in warnings:
        print(f"  ⚠️  {w}")
elif warnings:
    print("WARNINGS")
    for w in warnings:
        print(f"  ⚠️  {w}")
else:
    print("OK")
VALIDATE_EOF
)

VALIDATION_STATUS=$(echo "$VALIDATION_RESULT" | /usr/bin/head -1)

if [ "$VALIDATION_STATUS" = "ERRORS" ]; then
  echo "$VALIDATION_RESULT" | tail -n +2
  echo ""
  echo "❌ 61秒未満のエピソードがあります。cuts.jsonを修正してください。"
  exit 1
elif [ "$VALIDATION_STATUS" = "WARNINGS" ]; then
  echo "$VALIDATION_RESULT" | tail -n +2
  echo ""
  read -p "   90秒超過がありますが続行しますか？ (y/N): " CONTINUE_WITH_WARN
  if [ "$CONTINUE_WITH_WARN" != "y" ] && [ "$CONTINUE_WITH_WARN" != "Y" ]; then
    echo "   → 中止しました。cuts.jsonを修正してから再実行してください。"
    exit 0
  fi
else
  echo "  ✅ 全エピソード 61〜90秒 OK"
fi

# ============================================================
# STEP 3: FFmpegで分割
# ============================================================
echo ""
echo "🔪 STEP 3: 動画分割中..."

SEG_DIR="$PROJECT_DIR/segments"
SEG_DIR_NOBGM="$PROJECT_DIR/segments_nobgm"
mkdir -p "$SEG_DIR" "$SEG_DIR_NOBGM"

export CUTS_JSON SOURCE_MP4 SEG_DIR SEG_DIR_NOBGM
python3 << 'SPLIT_EOF'
import json, subprocess, os, sys, shutil

CUTS_JSON = os.environ["CUTS_JSON"]
SOURCE_MP4 = os.environ["SOURCE_MP4"]
SEG_DIR = os.environ["SEG_DIR"]
SEG_DIR_NOBGM = os.environ["SEG_DIR_NOBGM"]

with open(CUTS_JSON) as f:
    data = json.load(f)

total = len(data["cuts"])

for cut in data["cuts"]:
    ep = cut["episode"]
    start = cut["start"]
    end = cut["end"]
    is_last = (ep == total)

    s_sec = float(start.split(":")[0])*3600 + float(start.split(":")[1])*60 + float(start.split(":")[2])
    e_sec = float(end.split(":")[0])*3600 + float(end.split(":")[1])*60 + float(end.split(":")[2])
    duration = e_sec - s_sec

    # --- source.mp4からそのまま切り出し ---
    out_seg = f"{SEG_DIR}/ep{ep:02d}.mp4"
    if not os.path.exists(out_seg):
        cmd = [
            "ffmpeg", "-y", "-ss", start, "-i", SOURCE_MP4,
            "-t", str(duration),
            "-c:v", "libx264", "-c:a", "aac", "-preset", "fast",
            "-avoid_negative_ts", "make_zero", out_seg
        ]
        print(f"  ✂️  Part {ep}/{total}: {start} → {end}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  ✅ {os.path.basename(out_seg)}")
        else:
            print(f"  ❌ エラー: {r.stderr[-200:]}")
            sys.exit(1)
    else:
        print(f"  ⏭️  Part {ep}: 分割済み")

    # --- BGMなし版（最終パートのみDemucs、他はコピー） ---
    out_nobgm = f"{SEG_DIR_NOBGM}/ep{ep:02d}.mp4"
    if not os.path.exists(out_nobgm):
        if is_last:
            # 最終パートのみDemucsでBGM除去
            print(f"  🎵 Part {ep} (最終): Demucsでナレーション抽出中...")
            sep_dir = f"{SEG_DIR_NOBGM}/separated"
            # pipxでインストールしたdemucsコマンドを使用
            import shutil as _sh
            demucs_bin = _sh.which("demucs") or "demucs"
            r = subprocess.run(
                [demucs_bin, "--two-stems=vocals", "-o", sep_dir, out_seg],
                capture_output=True, text=True
            )
            if r.returncode != 0:
                print(f"  ⚠️  Demucs失敗 → BGMあり版をそのまま使用")
                print(f"      ({r.stderr[-200:]})")
                shutil.copy2(out_seg, out_nobgm)
            else:
                # Demucs出力からvocals.wavを探す
                vocals = None
                for root, dirs, files in os.walk(sep_dir):
                    if "vocals.wav" in files:
                        vocals = os.path.join(root, "vocals.wav")
                        break
                if vocals:
                    # ナレーション音声を映像と再合成
                    r2 = subprocess.run([
                        "ffmpeg", "-y", "-i", out_seg, "-i", vocals,
                        "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0",
                        "-c:a", "aac", "-b:a", "192k", out_nobgm
                    ], capture_output=True, text=True)
                    if r2.returncode == 0:
                        print(f"  ✅ BGM除去完了: {os.path.basename(out_nobgm)}")
                    else:
                        print(f"  ⚠️  再合成失敗 → BGMあり版をそのまま使用")
                        shutil.copy2(out_seg, out_nobgm)
                else:
                    print(f"  ⚠️  vocals.wav未検出 → BGMあり版をそのまま使用")
                    shutil.copy2(out_seg, out_nobgm)
                # Demucs一時ファイル削除
                shutil.rmtree(sep_dir, ignore_errors=True)
        else:
            # 最終パート以外はそのままコピー
            shutil.copy2(out_seg, out_nobgm)
            print(f"  📋 Part {ep}: BGMなし版コピー")
    else:
        print(f"  ⏭️  Part {ep} (BGMなし): 済み")

SPLIT_EOF

echo "  ✅ 分割完了（2バージョン）"

# ============================================================
# STEP 4: FFmpegで縦型変換 + 上下装飾（2バージョン）
# ============================================================
echo ""
echo "🎨 STEP 4: 縦型変換 + 装飾中..."

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
python3 << 'STEP4_EOF'
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

# display_titleを行ごとに分割（改行対応）
title_lines = data.get("display_title", PROJECT_NAME).split("\n")

def build_title_filters(prev_label, font_path, title_lines, part_text, cta_text, text_y):
    """タイトル行 + Part + CTAのdrawtextフィルターチェーンを構築"""
    filters = ""
    label = prev_label
    y = text_y
    title_fontsize = 48 if max(len(l) for l in title_lines) > 12 else 52
    for i, line in enumerate(title_lines):
        # FFmpeg drawtextの特殊文字をエスケープ
        escaped = line.replace("'", "'\\''").replace(":", "\\:")
        next_label = f"title{i}"
        filters += (
            f"[{label}]drawtext=fontfile={font_path}:text='{escaped}'"
            f":fontsize={title_fontsize}:fontcolor=white:borderw=3:bordercolor=black"
            f":x=(w-text_w)/2:y={y}[{next_label}];"
        )
        label = next_label
        y += title_fontsize + 10
    # Part表示
    y += 5
    filters += (
        f"[{label}]drawtext=fontfile={font_path}:text='{part_text}'"
        f":fontsize=40:fontcolor=#CCCCCC:borderw=2:bordercolor=black"
        f":x=(w-text_w)/2:y={y}[parted];"
    )
    y += 50
    # CTA表示
    filters += (
        f"[parted]drawtext=fontfile={font_path}:text='{cta_text}'"
        f":fontsize=30:fontcolor=#FFD700:borderw=1:bordercolor=black"
        f":x=(w-text_w)/2:y={y}[final]"
    )
    return filters

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

    # 9:16 = 1080x1920、均等3分割（各640px）
    out_w, out_h = 1080, 1920
    section_h = out_h // 3  # 640px
    part_text = f"Part {ep} / {total_parts}"
    cta_text = "▶ フォローして続きを見る"

    # 動画を中央セクション(640px)にフィット
    scale_w = out_w
    scale_h = int(src_h * (out_w / src_w))
    if scale_h > section_h:
        scale_h = section_h
        scale_w = int(src_w * (section_h / src_h))
    video_y = section_h + (section_h - scale_h) // 2  # 中央セクション内で上下中央

    # テキストは下セクション上端から配置（上揃え）
    text_y = section_h * 2 + 20

    inputs = ["-i", input_seg]

    # サムネイルがある場合
    if THUMBNAIL_PATH and os.path.exists(THUMBNAIL_PATH):
        inputs.extend(["-i", THUMBNAIL_PATH])
        # サムネを上セクション(640px)にフィット
        thumb_w = out_w - 40
        thumb_h = int(thumb_w * 9 / 16)
        if thumb_h > section_h - 20:
            thumb_h = section_h - 20
            thumb_w = int(thumb_h * 16 / 9)
        thumb_y = (section_h - thumb_h) // 2  # 上セクション内で上下中央
        base_filter = (
            f"color=c=black:s={out_w}x{out_h}:r=30[bg];"
            f"[0:v]scale={scale_w}:{scale_h}[scaled];"
            f"[bg][scaled]overlay={(out_w - scale_w) // 2}:{video_y}[base];"
            f"[1:v]scale={thumb_w}:{thumb_h}[thumbscaled];"
            f"[base][thumbscaled]overlay=(W-w)/2:{thumb_y}[withthumb];"
        )
        title_filters = build_title_filters("withthumb", FONT_PATH, title_lines, part_text, cta_text, text_y)
        filter_complex = base_filter + title_filters
    else:
        # サムネなし: 動画を中央セクションに配置
        base_filter = (
            f"color=c=black:s={out_w}x{out_h}:r=30[bg];"
            f"[0:v]scale={scale_w}:{scale_h}[scaled];"
            f"[bg][scaled]overlay={(out_w - scale_w) // 2}:{video_y}[baseout];"
        )
        title_filters = build_title_filters("baseout", FONT_PATH, title_lines, part_text, cta_text, text_y)
        filter_complex = base_filter + title_filters

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
STEP4_EOF

# ============================================================
# STEP 5: BGMミックス（YouTube用 output/ にBGMを合成）
# ============================================================
echo ""
echo "🎵 STEP 5: BGMミックス中..."

BGM_FILE="$ASSETS_DIR/bgm.mp3"
BGM_VOLUME="0.15"

if [ ! -f "$BGM_FILE" ]; then
  echo "  ⚠️  BGMファイルがありません: $BGM_FILE"
  echo "  → BGMなしのまま完了します"
else
  BGM_TMP_DIR="$OUT_DIR/tmp_bgm"
  mkdir -p "$BGM_TMP_DIR"

  for f in "$OUT_DIR"/ep*_short.mp4; do
    BASE=$(basename "$f")
    TMP_OUT="$BGM_TMP_DIR/$BASE"

    if [ -f "$TMP_OUT" ]; then
      echo "  ⏭️  $BASE: BGMミックス済み"
      continue
    fi

    echo "  🎵 $BASE"
    ffmpeg -y -i "$f" -stream_loop -1 -i "$BGM_FILE" \
      -filter_complex "[1:a]volume=${BGM_VOLUME}[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=3[aout]" \
      -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k \
      "$TMP_OUT" 2>/dev/null

    if [ $? -eq 0 ]; then
      echo "  ✅ $BASE"
    else
      echo "  ⚠️  BGMミックス失敗 → 元ファイルを維持: $BASE"
      cp "$f" "$TMP_OUT"
    fi
  done

  # 差し替え
  for f in "$BGM_TMP_DIR"/ep*_short.mp4; do
    mv "$f" "$OUT_DIR/$(basename "$f")"
  done
  rm -rf "$BGM_TMP_DIR"
  echo "  ✅ BGMミックス完了（volume=${BGM_VOLUME}）"
fi

echo ""
echo "=========================================="
echo "🎉 パイプライン完了！"
echo "📁 BGMあり版（YouTube用）: $OUT_DIR/"
echo "📁 BGMなし版（TikTok用）: $OUT_DIR_NOBGM/"
echo "=========================================="
echo "BGMあり版（YouTube用）:"
ls -la "$OUT_DIR/" 2>/dev/null || echo "  (出力ファイルなし)"
echo "BGMなし版（TikTok用）:"
ls -la "$OUT_DIR_NOBGM/" 2>/dev/null || echo "  (出力ファイルなし)"
echo ""
echo "📱 投稿先:"
echo "   YouTube       → BGMあり版（$OUT_DIR/） + BGM自動合成済み"
echo "   TikTok        → BGMなし版（$OUT_DIR_NOBGM/） + アプリ内楽曲後付け"
echo "   LINE VOOM     → BGMあり版（$OUT_DIR/）そのまま"
