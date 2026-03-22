# 風不死岳ヒグマ事件 サムネイル設計

## サムネ構成案

- **メイン画像（右1/3）:** 笑顔でカメラ目線の20代イケメン男性（1970年代作業着、竹カゴ背負い）。背後からヒグマが口を開けて襲いかかろうとしている
- **上部セリフ:** 「クマなんて出ないって」（白明朝、画像上端）
- **中間行動:** 警報が出てるのに11人で入山 / 次々とクマに襲われ、、（白明朝60%、人物左側）
- **下部オチ:** タケノコ採りが地獄に変わった（黄橙グラデ極太、画像下端）
- **フッター:** 黒帯に白文字「地形図・アニメーションで解説」
- **背景:** 霧がかかった笹薮の山肌、不穏な曇り空

## Lovart画像プロンプト

```
Photorealistic cinematic shot. Very attractive handsome young Japanese man
in his early 20s, sharp jawline, clear skin, stylish short black hair,
model-like features, big bright toothy smile, facing the camera, looking
directly at the viewer, completely unaware of danger. Behind him, a massive
Hokkaido brown bear (higuma) with its mouth wide open showing teeth, about
to attack, lunging forward aggressively. He is wearing 1970s Japanese
outdoor clothes (olive green cotton jacket, dark work pants, rubber boots),
carrying a bamboo basket on his back. Dense bamboo grass (Chishimazasa)
and dark moody Hokkaido mountain forest background with fog. Dramatic warm
lighting on the man's face, dark shadows behind. No text, no words, no
letters. 16:9 aspect ratio. Generate 5 images.
```

## Photopea配置ガイド

```
┌──────────────────────────────┐
│「クマなんて出ないって」        │ ← 上端
│                               │
│ 警報が出てるのに11人で入山 [顔]│ ← 中間（人物の左側）
│ 次々とクマに襲われ、、   [顔] │
│                          [熊] │
│ タケノコ採りが地獄に変わった   │ ← 下端
│■■ 地形図・アニメーションで解説 ■■│
└──────────────────────────────┘
```

## フォント・テキスト設定

### 上部（慢心セリフ）
- Font: Hiragino Mincho Pro W3
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside
- Shadow: なし

### 中間（状況説明・箇条書き）
- Font: Hiragino Mincho Pro W3
- Color: #FFFFFF
- Stroke: #000000, 3px, Outside
- Shadow: なし
- サイズ: 下部の約60%
- 配置: 人物の左側

### 下部（衝撃オチ）
- Font: Source Han Sans Heavy
- Color: グラデーション #FFD700 → #FFA500（黄→オレンジ）
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Spread 30%, Size 8px
- 傾き: 右上がり3-5度

### フッター
- Font: Hiragino Mincho Pro Medium
- Color: #FFFFFF
- 背景: 黒帯
- 内容: 「地形図・アニメーションで解説」

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
