# 1996年星野道夫ヒグマ襲撃事件 サムネイル設計

## 方針（2026-06-27 確定）

- **メイン画像: 星野道夫さん本人の実写写真を使用**（AI生成ではなく実写）。ユーザー判断・CTR最優先。
  - ⚠️ **著作権・肖像権リスクはユーザー承知の上での決定**。写真の著作権は撮影者/出版社（文藝春秋・福音館書店等）または遺族（妻・直子さん管理）に残る。YouTube収益化動画の商用利用。
  - リスク: Content ID／著作権申し立て（当該動画の収益移転・ブロック）／繰り返しでストライキ／遺族からの削除要請の可能性。
  - **必須の保険（下記「リスク対応」参照）**: バックアップサムネ常備＋申し立て即対応。
- 表情は「口大開けクリックベイト笑い」は避け、**星野さんらしい穏やかな表情の写真**を選ぶ（実在故人への配慮・炎上回避）。

---

## 実写写真 使用ワークフロー

1. **写真選定**: 星野さん本人の、**正面〜やや正面・穏やかな表情・顔がはっきり写った高解像度**の写真を1枚選ぶ
   - カメラを持つ／フィールドでの姿が、写真家という文脈と「あの事件」の認識キューに最適
   - できれば出典・撮影者が分かるもの（万一の申し立て対応・許諾交渉のため記録）
2. **Photopea前処理**:
   - チェストアップにトリミング、**右1/3**に配置（テキストと重ねない）
   - 透かし・クレジット文字が入っていれば除去
   - 背景が明るい場合は、暗いカムチャツカ風の背景に差し替え or 周辺減光で不穏さを演出（※背景合成すると「改変コンテンツ」扱い→AI開示要）
3. **テキスト合成**（下記フォント設定）
4. **書き出し** 1280×720px

> ⚠️ **AI開示の判断**: 実写をトリミング＋テキスト配置のみ＝合成コンテンツ開示は不要。**別背景に合成・加工した場合は「改変または合成コンテンツ=はい」**を選択。

---

## サムネ構成（本命）

- **メイン画像（右1/3）**: 星野道夫さん本人の実写（穏やかな表情・カメラ/フィールド）
- **上段セリフ（白明朝・カギカッコあり・画像上端）**: 「クマと心は通じる」
- **下段オチ（黄→橙グラデ・極太・画像下端・右上3度傾き）**: 餌付けグマに、、
- **フッター（黒帯白文字）**: 地形図・アニメーションで解説
- **背景**: カムチャツカの薄暮・霧・遠景に巨大ヒグマの淡いシルエット・不穏な曇天（背景合成する場合）

## 文言A/Bテスト案（上段の信念表現で比較）

| 案 | 上段（白明朝「」） | 下段（黄橙極太） | 狙い |
|---|---|---|---|
| **A（本命・台本準拠）** | 「クマと心は通じる」 | 餌付けグマに、、 | 信念 vs 人間が変えた1頭 |
| **D（比較）** | 「クマを信じてた」 | 人が変えた1頭 | 信頼の逆説（餌付け＝人災明示） |
| B | 「銃は持たない」 | テント3mの牙 | 無銃哲学 vs 距離の恐怖 |
| C | 「サケがあるから襲わない」 | 寝袋ごと、、 | 確信の根拠 vs 現実 |

- NGワードチェック: ✅「死/死亡/遺体」不使用・問題なし
- 反復回避: 風不死岳「11人中2人死亡」/立山「生還者2人」と異なるフォーマット（信念セリフ型）

## Photopea配置ガイド（1280×720）

```
┌──────────────────────────────┐
│「クマと心は通じる」 ← 上端右寄り │
│                       [星野さん] │
│                       [星野さん] │
│   餌付けグマに、、     [星野さん] │ ← 下端（「餌付けグマに」特大）
│■ 地形図・アニメーションで解説 ■│ ← 黒帯
└──────────────────────────────┘
```

## フォント・テキスト設定

### 上段（信念セリフ）
- Font: **Hiragino Mincho Pro W3**（明朝）
- Color: #FFFFFF / Stroke: #000000, 5px, Outside
- カギカッコ「」付き・1行

### 下段（オチ）
- Font: **Source Han Sans Heavy**（極太ゴシック）
- 「餌付けグマに」やや小〜特大、「、、」余韻
- Color: 黄→橙グラデ #FFD700→#FFA500
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Size 8px
- 右上がり3〜5度傾き

### フッター
- Font: **Hiragino Mincho Pro Medium** / 白文字 / 黒帯
- 「地形図・アニメーションで解説」

> プロデザイン新仕様: 上段=LightNovelPOPv2 / 下段=Source Han Sans JP Heavy / フッター=Source Han Sans JP Medium。Photopeaは英語UIのためフォントは英語名指定。

---

## リスク対応（実写使用の保険・重要）

- **バックアップサムネを常備**: 下記AI似顔版をいつでも差し替えられるよう完成させておく。著作権申し立て/ブロックが来たら**即こちらに差し替え**て動画を生かす。
- **出典記録**: 使用写真の入手元・撮影者・URLを控えておく（許諾交渉・反論対応用）。
- **投稿後モニタリング**: 公開直後〜数日、Content ID／申し立て／コメントの遺族反応を確認。
- **許諾の事後取得**も検討余地（直子さん側に連絡が取れれば正式許可でリスク消滅）。

### バックアップ用 AI似顔プロンプト（著作権回避版・差し替え用）
```
Photorealistic cinematic close-up documentary portrait, framed from chest up. A 43-year-old Japanese male wildlife photographer with a warm gentle approachable face, soft rounded kind features (not sharp or angular), warm intelligent crinkled eyes, light unshaven stubble to short beard, slightly long natural-textured black hair tousled by cold wind, warm tan skin weathered by years living in the Alaskan and Kamchatkan wilderness, lean fit outdoorsman build. A warm gentle quiet smile, calm peaceful humble expression, facing the camera, looking directly at the viewer with kind serene fearless eyes, completely at peace and unaware of danger. He is wearing a dark khaki photographer's vest with many utility pockets over a faded blue cotton shirt, a large professional camera with a long telephoto lens hanging at his chest, one hand resting gently near the camera. Wind softly blowing his hair and the collar of his vest. Behind him, the dark moody Kamchatka wilderness at twilight, distant volcanic peaks and a misty lake, fog rising between the slopes, and a faint shadowy silhouette of a massive brown bear barely visible deep in the misty background. The sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Warm documentary lighting on his face, dark cold shadows behind. Shallow depth of field, background slightly blurred. No text, no words, no letters, no logos. 16:9 aspect ratio. Generate 5 separate images.
```

---

## AI開示ラベル
- 実写トリミング＋テキストのみ → 合成開示**不要**
- 別背景に合成・加工した場合 → YouTube Studio「改変または合成コンテンツ=はい」
- ⚠️ 実在故人の実写使用。著作権・肖像権・遺族感情に留意（投稿後モニタリング必須）
