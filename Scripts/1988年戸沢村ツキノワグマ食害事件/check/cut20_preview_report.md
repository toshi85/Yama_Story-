# カット20単独プレビュー 実行結果

全コマンドの作業ディレクトリ: /Users/tosimasa/Desktop/Antigravity
PythonにはPYTHONDONTWRITEBYTECODE=1を指定。

## プレビュー
/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python System_Tools/edit/preview_cut.py '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件' 20
終了コード: 0（内部render.pyも0）。--overrideなし。
出力: /Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/preview/0020.mp4
尺: 4.6秒。640×360。

## ffmpeg実体取得
/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python -c "import sys;sys.path.insert(0,'System_Tools/edit');import ff;print(ff.ffmpeg())"
終了コード: 0。

## 3コマ抽出
/Users/tosimasa/Desktop/Antigravity/.venv-edit/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1 -hide_banner -nostdin -v error -y -ss 0.500000 -i '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/preview/0020.mp4' -frames:v 1 '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/frames_cut20/cut20_a.png'
終了コード: 0

/Users/tosimasa/Desktop/Antigravity/.venv-edit/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1 -hide_banner -nostdin -v error -y -ss 2.300000 -i '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/preview/0020.mp4' -frames:v 1 '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/frames_cut20/cut20_b.png'
終了コード: 0

/Users/tosimasa/Desktop/Antigravity/.venv-edit/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1 -hide_banner -nostdin -v error -y -ss 4.300000 -i '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/preview/0020.mp4' -frames:v 1 '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/frames_cut20/cut20_c.png'
終了コード: 0

## 元動画フレーム再確認
/Users/tosimasa/Desktop/Antigravity/.venv-edit/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1 -hide_banner -nostdin -v error -i '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/studio/jobs/20260908150535_c2a000ce/full_下書き.mp4' -map 0:v:0 -c:v copy -f framemd5 -
終了コード: 0。映像パケット数44943（30fps連続の既存確認結果と一致）。

## キャッシュ調査
{
  "shots_sha256": "4e12c71f9eb3115bbf3f8dfe11e45bf1772a81ccfe75389ffda9c313be4ff3ea",
  "shot_count": 298,
  "cache_clip_count": 298,
  "cache_sig_count": 298,
  "cut20": {
    "clip_0020.mp4": {
      "exists": true,
      "mtime": "2026-09-10T15:08:03.000147+09:00"
    },
    "clip_0020.mp4.sig": {
      "exists": true,
      "mtime": "2026-09-10T16:25:54.195620+09:00"
    }
  },
  "expected_clips_missing": [],
  "signature_mismatch_count": 1,
  "signature_mismatch_shots": [
    20
  ],
  "signature_note": "読み取り専用で既存の署名判定関数を使用。山岳では--draftでもクリップ署名の_draftはFalse。各キャッシュ動画の尺・破損は未検査のため追加再作成の可能性あり。全編レンダリング未実行。"
}

キャッシュ298本／カット298件。欠落0。署名の読み取り比較ではカット20だけ不一致なので、作り直し対象は1本の見込み。尺や破損による追加作成は未検査。全編処理は実行していない。

## 目視と変更確認
3コマをそれぞれ開いて確認。640×360の全画面・字幕付き、顔なし、破れた衣服、血・傷・赤い染みなし、雪なし。元画像の文字混入なし。
shots.json SHA256一致。既存.render_cacheのclip_0020.mp4と署名の更新時刻は実行前後で不変。
AI_REPLY.mdは従来の全バイトを残して追記。
指定preview_cut.pyの副生成物として素材直下.render_cache_previewにカット20の作業キャッシュを作成。本体.render_cacheは変更していない。

## 懸念
全編修正版は未作成。元画像の厳密16:9からの微差は残るが、プレビューは16:9・全画面で確認済み。音声は聴取未検査。
