# js_anim — JavaScriptだけで作る図解アニメーション（試作）

動画生成AIを使わず、Canvasで描いた絵をコマ送りでPNGに落とし、ffmpegでMP4にする。
参考: [JavaScriptだけで作ったAIキャラの対戦アニメーション](https://x.com/taiyo_ai_gakuse/status/2102566868028686799)（2026-09-23）

## 位置づけ（2026-09-23 時点）

- **試作**。本編に採用するかは未決。Yamaの【AI動画】は実写風が規則なので、これは実写映像の代わりではなく **地図・時系列・退避経路の図解** の枠で使う。
- キャラはシルエットで、加害の瞬間は描かない。画面にも「再現ではなく状況の図解」と出す。
- ナレーションは **macOSの `say`（機械音声）による仮置き**。本番は本人の声。

## ファイル

| ファイル | 役割 |
|:---|:---|
| `kazuno_sample.html` | 60秒ぶんの絵。`renderFrame(f)` が f 番目のコマを描く（決定論的＝何度描いても同じ） |
| `capture.mjs` | Chrome を headless で起動し、CDP 直叩きで1コマずつPNG保存。Playwrightのブラウザ配置は不要 |
| `narration.py` | `say -v Kyoko` で行ごとに音声を作り、開始秒へ遅延させて1本のwavに合成（風の環境音つき） |

## 使い方

```bash
cd Yama_Story/System_Tools/js_anim

# 1) 絵の確認（数コマだけ書き出す）
FRAMES=250,700,1200 node capture.mjs kazuno_sample.html /tmp/preview

# 2) 全コマ（1800枚・約9分）
node capture.mjs kazuno_sample.html /tmp/frames

# 3) 音声
python3 narration.py /tmp/narr

# 4) MP4
ffmpeg -y -framerate 30 -i /tmp/frames/f_%05d.png -i /tmp/narr/narration.wav \
  -c:v libx264 -crf 18 -pix_fmt yuv420p -preset slow \
  -c:a aac -b:a 192k -shortest out/kazuno_60s.mp4
```

ブラウザで `kazuno_sample.html` を直接開くと実時間で再生される（絵の確認用）。

## 中身の作り

- **地形**: 値ノイズで標高を作り、マーチングスクエアで等高線を引く。陰影は低解像度のImageDataを拡大。
- **キャラ**: 関節位置を sin で動かす棒人間・四つ脚。`silhouette()` が縁の光つきで二度描きする。
- **尺の管理**: `SCENES` 配列が `[開始秒, 終了秒, 描画関数]`。字幕は `band()` で台形フェード。

## 事実の扱い

文字と時刻は `Scripts/2024年鹿角市大平地区クマ事件/Fact_Sheet_鹿角2024.md` の**確度Aのみ**。
地図は模式図で、実際の位置ではない（画面右上に明記）。死亡の瞬間・加害個体の同定は描かない（素材シートの不使用事項）。
