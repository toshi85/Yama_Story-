# 谷川岳宙吊り事件 サムネイル設計

## 確定キャッチコピー（3層テキスト構成）

CTR TOP5分析（2026-03-07）により、2層→3層構成に変更。
中間テキストで「どう舐めたか→何が起きたか→被害拡大」を箇条書きで追加。

| 層 | テキスト | 役割 |
|:--|:--|:--|
| 上部 | 「これくらい大丈夫でしょ」 | 慢心セリフ |
| 中間1 | 憧れだけで無謀な登山 | 舐めた理由 |
| 中間2 | 悪天候で崖から転落 | 事故の展開 |
| 中間3 | 仲間も巻き添えに、、 | 被害拡大 |
| 下部 | 宙吊りで7日間、、 | 衝撃の結末 |

## Lovart画像プロンプト（3案共通）

```
Photorealistic portrait of a young Japanese male climber in his early 20s, short black hair, slim athletic build, wearing 1960s vintage wool sweater and canvas rucksack with rope coiled over shoulder. Big bright toothy smile, eyes squinting with joy, radiating youthful excitement and overconfidence, looking upward at an unseen cliff. Dark dramatic mountain landscape background with massive vertical rock wall and ominous storm clouds. Natural warm lighting on face contrasting cold dark blue-grey background. High detail. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

## Photopea配置ガイド

```
┌──────────────────────────────┐
│「これくらい大丈夫でしょ」      │ ← 上端
│                               │
│ 憧れだけで無謀な登山      [顔] │ ← 中間（人物の左側）
│ 悪天候で崖から転落        [顔] │
│ 仲間も巻き添えに、、     [顔] │
│                               │
│ 宙吊りで7日間、、         [顔] │ ← 下端
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
- 配置: 人物の左側、3行

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

## テスト設計
- 画像: 同一（上記プロンプトで生成した1枚）
- 現在は1案のみ（3層構成の効果を検証後、中間テキスト違いでA/Bテスト展開）

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
