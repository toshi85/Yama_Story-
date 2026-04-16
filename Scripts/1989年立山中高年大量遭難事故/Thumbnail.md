# 1989年立山中高年大量遭難事故 サムネイル設計

## タイトル
10人中8人が帰らぬ人に、、生き残った2人だけが持っていた"あるもの"、、1989年 立山中高年大量遭難事故

## サムネ構成（2026-04-16 確定）

### 共通要素
- **メイン画像:** 50代日本人男性、セルフィー風正面、口を大きく開けて笑う、秋のハイキング軽装（チェック柄コットンフランネルシャツ・ベージュベスト）
- **背景:** 紅葉の山（赤・橙・金）、空はやや暗い曇天
- **下部オチ:** 生還者2人、、（赤極太）
- **チャンネルロゴ:** 右上「事故ログ」

### A/Bテスト
| 枚 | 上部セリフ | 下部 | テスト変数 |
|---|---|---|---|
| 1（本命） | 「10人で行こう！」 | 生還者2人、、 | — |
| 2 | 「いい天気だな」 | 生還者2人、、 | 上段コピー |

- テスト目的: 誘い文句型（10人で行こう！）vs 状況描写型（いい天気だな）のCTR比較
- 下段固定で上段のみ変えるクリーンテスト

## Lovart画像プロンプト

```
Photorealistic cinematic close-up portrait shot, framed from chest
up. Extremely attractive handsome Japanese man in his mid-50s,
strikingly good-looking, sharp jawline, high cheekbones, clear
smooth skin, stylish silver-streaked black hair gently blown by
wind, deep expressive eyes, mouth wide open laughing joyfully
showing perfect white teeth, ecstatic exhilarated expression,
facing the camera, looking directly at the viewer, completely
relaxed and carefree. Wind gently blowing his plaid cotton flannel
shirt collar and hair. He is wearing a plaid cotton flannel shirt
with the collar open, thin beige vest. Behind him, a stunning
Japanese mountain landscape in peak autumn foliage, vibrant red
and orange maple trees covering the mountainside, golden larch
trees, but the sky above is dark and overcast with heavy grey
clouds rolling in ominously. Dramatic warm lighting on the man's
face, autumn colors glowing warmly, but the sky hints at
approaching danger. Shallow depth of field, background slightly
blurred. No text, no words, no letters. 16:9 aspect ratio.
Generate 5 images.
```

## フォント・テキスト設定

### 上部（セリフ）
- Font: Hiragino Mincho Pro W3
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside

### 下部（生還者数）
- Font: Source Han Sans Heavy
- 「生還者」: やや小さめ
- 「2人」: 特大サイズ
- Color: 赤
- Stroke: #000000, 5px, Outside
- Shadow: あり

## 設計意図
- **画像とテキストの役割分担:** 画像（笑顔+紅葉）= 安全・楽しい / テキスト（生還者2人）= 死の結末 → 情報重複を避け、ギャップ最大化
- **タイトルとの補完:** タイトルが「あるもの」の謎かけ → サムネの「生還者2人」が「なぜこの2人だけ？」のクリック導線
- **反復回避:** 風不死岳「11人中2人死亡」とフォーマットが異なる

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
