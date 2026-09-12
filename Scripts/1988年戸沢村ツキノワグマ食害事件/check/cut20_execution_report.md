# カット20 実行記録

作業ディレクトリ: /Users/tosimasa/Desktop/Antigravity
PythonコマンドにはPYTHONDONTWRITEBYTECODE=1を設定し、許可外のpycache生成を抑止。

- 変更前コピー、画像保存、JSON更新・フィールド比較: 各Python処理の終了コード0。
- 標準画像生成: 1回、正常に画像返却。ユーザープロンプトは変更なし。有料API・代替生成なし。

## 区間差し替え
```sh
/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python System_Tools/edit/splice_rebuild.py '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/shots.json' --master '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/studio/jobs/20260908150535_c2a000ce/full_下書き.mp4' --shots 20 --out '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/review_revised.mp4'
```
終了コード: 直接回収できていない（エラー分岐のreturnは1）。カット20単体のrender.pyは終了コード0。元動画のフレーム検査で停止。evidence.json: status=未検証 / frame_count=44943 / expected_frames=44944。指定された完成動画は未生成。全編再レンダリングなし。

## ゲート
```sh
/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python System_Tools/edit/gate.py '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/shots.json' '/Users/tosimasa/Desktop/Antigravity/Yama_Story/Scripts/1988年戸沢村ツキノワグマ食害事件/check/review_revised.mp4'
```
終了コード1。同期中央値96%、同期OK。動画が存在せずFileNotFoundError、ゲートFAIL。

## ffmpeg実体取得
```sh
/Users/tosimasa/Desktop/Antigravity/.venv-edit/bin/python -c "import sys;sys.path.insert(0,'System_Tools/edit');import ff;print(ff.ffmpeg())"
```
終了コード0。実体: /Users/tosimasa/Desktop/Antigravity/.venv-edit/lib/python3.14/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1
指定3コマは修正版動画未生成のため未抽出。元動画や単体レンダリングのコマで代用していない。

## 目視確認
生成画像を保存先から開いて目視確認した結果:
(a) 実写風の写真表現であり、イラストではない。
(b) 顔は岩側に伏せられ、顔の造作は見えない。
(c) 肩・背中・太もも周辺の衣服が大きく破れ、布が垂れたボロボロの状態。
(d) 血・傷・赤い染みは見当たらない。
(e) 雪・霜は見当たらない。
(f) 文字は見当たらない。

厳密な16:9は未達（1672×941）。再生成なし。

## 比較結果
```
カット20の変更キー一覧: asset_file, asset_kind, background_file, base_x, drift, edit_note, motion
asset_file: "画像/ASSET-020.png" → "画像/ASSET-020_実写.png"
asset_kind: "character" → "image"
background_file: "画像/ASSET-020-1.png" → ""
base_x: -409 → 0
drift: [486, -57] → [0, 0]
edit_note: "後ろ姿だけで処理し、視線の先は一切映さない。心拍SEを立ち上げる。1〜2秒で次へ。" → "実写の倒れた男性を全画面で1〜2秒。顔は見せない。心拍SEを立ち上げる。"
motion: "lean" → "still"
PASS カット20 start_frame: キーの有無・値とも不変（2513）
PASS カット20 end_frame: キーの有無・値とも不変（2651）
PASS カット20 narration: キーの有無・値とも不変（"おそるおそる近づいてみると、それは無残な夫の姿でした。"）
PASS カット20 subtitle_segments: キーの有無・値とも不変（両方ともキーなし）
PASS カット20以外の全297カット: 全フィールド一致
PASS カット20の指定外キー: 有無・値とも一致
PASS トップレベル: 全キー一致、shots以外の全値一致（shotsはカット20の指定7キーのみ変更）
PASS カット20以外のJSON原文: 1文字も変更なし
PASS JSON体裁: インデント1スペース・ensure_ascii=False・末尾改行
```

## 残作業
元動画とカット表の1フレーム差の扱いを解決後、指定区間の書き出し、gate PASS確認、84.2/86.0/88.0秒の3コマ抽出・目視。画像の厳密な16:9も未達。許可外変更、Git操作、公開、ファイル削除の指示は実行していない。
