# 風不死岳ヒグマ事件 サムネイル設計

## サムネ構成案（2026-03-26 確定版）

- **メイン画像（右1/3）:** 笑顔でカメラ目線の20代イケメン男性（1970年代作業着、竹カゴ背負い）。背後からヒグマが口を開けて襲いかかろうとしている
- **上部セリフ:** 「クマなんて出ないって」（白明朝、画像上端右寄り）
- **下部オチ:** 11人中2人死亡（黄色極太、画像下端。「2人死亡」を特大サイズ）
- **枠:** 白枠で全体を囲む
- **背景:** 霧がかかった暗い森、ヒグマと人物の間に奥行き

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
┌─────────────────────────────────┐
│  「クマなんて出ないって」        │ ← 上端右寄り
│                                  │
│                          [顔]   │
│               [熊]       [顔]   │
│                                  │
│ 11人中  2人死亡                  │ ← 下端（「2人死亡」特大）
└─────────────────────────────────┘
※ 白枠で全体を囲む
```

## フォント・テキスト設定

### 上部（慢心セリフ）
- Font: Hiragino Mincho Pro W3
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside
- Shadow: なし

### 下部（犠牲者数）
- Font: Source Han Sans Heavy
- 「11人中」: やや小さめ
- 「2人死亡」: 特大サイズ
- Color: #FFD700（黄色一色）
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Spread 30%, Size 8px

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
