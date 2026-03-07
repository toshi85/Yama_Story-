# 谷川岳宙吊り事件 サムネイル設計

## 確定キャッチコピー（A/Bテスト3案）

上部を固定、下部の訴求軸を変えてCTR比較する。

| 案 | 上部 | 下部 | 訴求軸 |
|:--|:--|:--|:--|
| 1 | これくらい大丈夫でしょ | 宙吊りで7日間、、 | 時間の恐怖 |
| 2 | これくらい大丈夫でしょ | 宙吊りで目撃 | 第三者視点の不気味さ |
| 3 | これくらい大丈夫でしょ | 300m宙吊り、、 | 高さの恐怖 |

## Lovart画像プロンプト（3案共通）

```
Photorealistic portrait of a young Japanese male climber in his early 20s, short black hair, slim athletic build, wearing 1960s vintage wool sweater and canvas rucksack with rope coiled over shoulder. Big bright toothy smile, eyes squinting with joy, radiating youthful excitement and overconfidence, looking upward at an unseen cliff. Dark dramatic mountain landscape background with massive vertical rock wall and ominous storm clouds. Natural warm lighting on face contrasting cold dark blue-grey background. High detail. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

## Photopea配置ガイド

```
┌──────────────────────────┐
│ これくらい大丈夫でしょ ← 上端│
│                           │
│                    [人物]  │
│                           │
│ 宙吊りで7日間、、  [人物]  │
│■■ 地形図・アニメーションで解説 ■■│
└──────────────────────────┘
```

## フォント・テキスト設定

### 上部（慢心セリフ）
- Font: Zen Maru Gothic Bold
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside
- Shadow: なし

### 下部（衝撃オチ）
- Font: Source Han Sans JP Heavy
- Color: グラデーション #FFD700 → #FFA500（黄→オレンジ）
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Spread 30%, Size 8px
- 傾き: 右上がり3-5度

### フッター
- Font: Source Han Sans JP Medium
- Color: #FFFFFF
- 背景: 黒帯
- 内容: 「地形図・アニメーションで解説」

## テスト設計
- 画像: 3案とも同一（上記プロンプトで生成した1枚）
- 変数: 下部テキストのみ変更
- 勝者確定後 → タイトルのA/Bテストに移行

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
