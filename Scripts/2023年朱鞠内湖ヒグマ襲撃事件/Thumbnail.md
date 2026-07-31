# 2023年朱鞠内湖ヒグマ襲撃事件 サムネイル設計

> 作成: 2026-07-31
> 動画URL: https://youtu.be/kQrIDctEHVA（限定公開）
> 採用タイトル: `朱鞠内湖、5日ぶりに再開された釣りの朝…たった一人で湖の最奥へ降りた54歳の末路…2023年 朱鞠内湖ヒグマ襲撃事件`
> 準拠: `memory/yama-thumbnail-prompt-template.md` B案テンプレ（中年）／背景ヒグマ**薄く入れる**（ユーザー指示 2026-07-31）

---

## ✅ 確定版（2026-07-31 採用・実制作済み）

> ユーザーが実制作したものを採用。以下は完成物の実測記録。**下の3案は不採用**（アーカイブとして残置）。

### テキスト

| 位置 | 文言 | 体裁 |
|:--|:--|:--|
| **上部（左寄せ・上端）** | 「1人で行ってくるよ」 | 白＋黒縁・明朝・カギカッコ「」あり・1行 |
| **下部（左寄せ・下端）** | 9kgの**肉塊**となり、、 | 極太ゴシック＋黒縁。「9」特大・白／「kg」小・白／「の」中・白／**「肉塊」特大・赤**／「となり、、」中・白 |
| **右上** | チャンネルロゴ「事故ログ」（黄丸バッジ） | — |
| フッター黒帯 | **なし** | — |

### 画像

- **人物**: 50代日本人男性。歯を見せた笑顔・カメラ目線。ベージュのキャップ＋カーキのフィッシングベスト＋黒の長袖。**右1/3**配置
- **背景**: 新緑の森と湖（冬化なし ✅）。空はやや暗い曇天
- **ヒグマ**: 画面**左奥の対岸**に立つシルエット。人物と重ならず、テキスト上部の空きゾーンに収まっている

### 確定版が既存ルールと異なる点（意図的な逸脱として記録）

| 項目 | Channel_Master §7 | 確定版 | 備考 |
|:--|:--|:--|:--|
| 下部の色 | 黄→橙グラデ（#FFD700→#FFA500） | 白ベース＋キーワード「肉塊」のみ赤 | 赤の厳密なhexは未取得 |
| フッター黒帯 | 必須（地形図・アニメーションで解説） | なし | 下部テキストの面積を優先 |
| 中間テキスト（3層目） | あり（具体行動2〜3行） | なし（2段構成） | SKILL.md の2段ルール側に一致 |
| 上部セリフ | 10文字程度 | 「1人で行ってくるよ」9文字 | ✅ 準拠 |

- **反復回避**: 立山「生還者2人」（赤）・風不死岳「11人中2人死亡」（黄一色）に対し、**白地＋1語だけ赤**は新フォーマット ✅
- **タイトルとの重複**: タイトルに「たった一人」があり、上部セリフ「1人で行ってくるよ」と語が重なる。ただし視点が異なる（タイトル＝ナレーター視点の事実／サムネ＝本人のセリフ）ため許容範囲

### ⚠️ 公開前の留意点

1. **「肉塊」と台本方針の関係** — `Asset_Prompts.md` L7 は「襲撃・遺体・胃内容・駆除は**非描写**」（遺族配慮）。サムネの「9kgの肉塊」は胃内容の言語化にあたり、この方針と衝突する。西川さんは実名、父親（80代）も存命で CHAR-06 として登場するため、遺族の目に触れる可能性がある
2. **事実の粒度** — 台本 L219 は「駆除されたクマの胃の中から、およそ**9キロにのぼる肉片**が見つかった」。サムネの「9kgの肉塊となり、、」は**遺体全体が9kgになった**とも読める。数字自体は台本準拠で正確 ✅
3. **YouTube側リスク** — 画像ではなくテキストのみのため即時の制限対象になる可能性は低いが、サムネイルポリシー上のショッキング表現として年齢制限・広告制限の判断材料になりうる。**公開後に収益化ステータスを確認**すること

---

## 【不採用】A/Bテスト3案（2026-07-31 提案・アーカイブ）

## 共通要素（3案とも同一）

- **メイン画像**: 50代日本人男性、口を大きく開けて笑うカメラ目線、胸まであるオリーブ色の胴長（ウェーダー）＋カーキのフィッシングベスト＋ベージュのキャップ、釣り竿を肩に担ぐ
- **背景**: 新緑（5月中旬）の湖畔。対岸は鮮やかな緑、水面は濃紺、低く霧。空は重い曇天
- **背景ヒグマ**: 奥の木立に**薄いシルエットのみ**（小さく・ピント外・動的表現なし）
- **配置**: 人物は右1/3。テキストは左2/3。テキストと人物を重ねない
- **フッター**: 黒帯に白文字「地形図・アニメーションで解説」
- **サイズ**: 1280×720px

---

## A/Bテスト3案

| 枠 | 上部セリフ（白＋黒縁） | 下部オチ（黄→橙 極太） | 狙う感情 | 構図 |
|:--|:--|:--|:--|:--|
| **A（本命）** | 「やっと再開だ」 | 胴長だけが | 好奇心 | 人物=右 / テキスト=左 |
| **B** | 「奥まで行くわ」 | クマが隠した | 恐怖 | 人物=右 / テキスト=左 |
| **C** | 「もう大丈夫でしょ」 | たった3歳 | 驚き | **人物=左 / テキスト=右**（左右反転） |

- **テスト変数**: 上下テキストのコンセプト（人物画像は3枠とも同一を使用）
- **C案の反転**: Channel_Master §7「直近3本と異なる構図を1案入れる」への対応。同一画像を左右反転して使うため、画像は統一のまま構図バリエーションを確保
- **判定**: 1〜2週間

### 各案の設計意図

**A案（好奇心型・本命）**
「やっと再開だ」= 5日間の遊漁自粛が明けた朝の、誰でも言いそうな一言。下部「胴長だけが」は台本 L115-117 の事実（水辺に胴長だけが残っていた）。**何が起きたか説明せずに映像だけが浮かぶ**構造で、続きを見に来させる。

**B案（恐怖型）**
下部「クマが隠した」は台本 L151 の事実（仕留めたものに草や土をかけて隠し、そばを離れない習性）。「隠した」という**主語がクマ側にある動詞**が不気味さを生む。上部の「奥まで行くわ」= 湖の最奥へ降りた行動と対応。

**C案（驚き型）**
下部「たった3歳」は加害個体が推定3歳・オスの亜成獣・体長1.5m（CHAR-03定義）という**意外性の数字**。「巨大なクマではなかった」というギャップが「え、3歳で？」を生む。SKILL.md「数字を使うなら規模ではなく意外性」に準拠。

### タイトルとの重複チェック

タイトル既出ワード: 朱鞠内湖 / 5日ぶり / 釣りの朝 / たった一人 / 湖の最奥 / 54歳 / 末路
→ **3案とも重複なし**。サムネ=感情的インパクト、タイトル=知的好奇心の役割分担が成立。

---

## Lovart画像プロンプト（3枠共通・1枚のみ生成して使い回す）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. Fresh green season, mid-May. A Japanese male fashion model in his mid-50s (54 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with rugged refined mature features. Sharp strong defined V-shaped jawline tapering to a firm pointed chin, high prominent commanding cheekbones, very high straight strong nose bridge, deep-set double-eyelid intense piercing dark eyes with steady gaze, well-shaped full lips, smooth handsome tan skin with mature masculine appeal, glossy perfectly styled short greying black hair gently blown by the lakeside wind. Tall broad-shouldered sturdy powerful model build with elegant proportions. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fishing vest. He is wearing chest-high olive-green fishing waders over a dark long-sleeve shirt, a khaki fishing vest with many small pockets, and a beige cap, with a fishing rod resting on his shoulder. Behind him, the lush green shoreline of a vast quiet lake in rural Japan in full fresh leaf, vivid green birch and fir trees covering the far shore, open dark blue water, thin mist drifting low over the surface, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Deep in the misty treeline far behind him, a faint shadowy silhouette of a brown bear barely visible among the trunks, small, dark and out of focus. Dramatic warm lighting on his face like a fashion magazine cover, fresh green tones glowing warmly, dark deep shadows behind. Shallow depth of field, background slightly blurred. Absolutely no snow, no ice, no frozen water, no bare leafless trees, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

### プロンプト設計メモ

- **B案テンプレ（中年）準拠**。7必須要素すべてを1回目から内包（職業2つ／顔骨格／中年肌 tan／カメラ目線／口大開け／風の動き／暗い山岳背景＋不穏な空）
- **冬化対策**（`yama-lovart-failure-patterns.md` §5・朱鞠内湖で3回発生した既知の罠）:
  - 文頭に `Fresh green season, mid-May.` を宣言
  - 固有地名（`Shumarinai` / `Hokkaido`）を**書かない** → `a vast quiet lake in rural Japan` に匿名化
  - 新緑を面で描写 `in full fresh leaf, vivid green birch and fir trees covering the far shore`
  - 末尾に `Absolutely no snow, no ice, no frozen water, no bare leafless trees, no winter scenery`
  - 地名削除で外国人化する副作用 → 人物側に `A Japanese male...` を付与して打ち消し
  - `cold` の語を空・影から排除（`dark deep shadows`）
- **ヒグマシルエット**: `faint shadowy silhouette ... barely visible ... small, dark and out of focus` のみ。`lunging forward aggressively` / `mouth wide open` / `motion blur` は**使わない**（人物を食うため。§5既知失敗）
- **motion blur は1要素のみ**（風で髪と襟）。落ち葉・霧の渦・ストラップ揺れの併用はしない

---

## Photopea配置ガイド

### A案・B案（人物=右）

```
┌──────────────────────────────────┐
│「やっと再開だ」                  │ ← 上端・左寄せ
│                          [顔]    │
│                          [顔]    │
│              [クマ影]    [胴]    │
│ 胴長だけが                       │ ← 下端・左寄せ
│■■ 地形図・アニメーションで解説 ■■│ ← 黒帯
└──────────────────────────────────┘
```

### C案（人物=左・左右反転）

```
┌──────────────────────────────────┐
│                「もう大丈夫でしょ」│ ← 上端・右寄せ
│    [顔]                          │
│    [顔]                          │
│    [胴]    [クマ影]              │
│                        たった3歳 │ ← 下端・右寄せ
│■■ 地形図・アニメーションで解説 ■■│ ← 黒帯
└──────────────────────────────────┘
```

---

## フォント・テキスト設定

> **正本: `Channel_Master_Prompt_Yama.md` §7**（2026-07-31 ユーザー確認）。
> SKILL.md / `memory/yama-thumbnail-prompt-template.md` の「プロデザイン新仕様」（LightNovelPOPv2 / Source Han Sans JP 系）は**使わない**。

### 上部（慢心セリフ）
- Font: **Hiragino Mincho Pro W3**（明朝）
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside
- カギカッコ「」**あり** / 1行表示・改行禁止
- 画像**上端に接する**位置

### 下部（衝撃オチ）
- Font: **Source Han Sans Heavy**（極太ゴシック）
- Color: 黄→オレンジ グラデーション（#FFD700 → #FFA500）
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Spread 30%, Size 8px
- 傾き: 右上がり 3〜5度
- カギカッコ**なし** / 上部より大きいサイズ / 1行表示
- 画像**下端に接する**位置

### フッター（黒帯）
- Font: **Hiragino Mincho Pro Medium**
- Color: #FFFFFF
- 文言: 地形図・アニメーションで解説

---

## 【NGワードチェック】

✅ 問題なし

| 案 | テキスト | 判定 |
|:--|:--|:--|
| A | やっと再開だ / 胴長だけが | 死・遺体・殺 いずれも不使用 |
| B | 奥まで行くわ / クマが隠した | 同上。「隠した」は状況描写 |
| C | もう大丈夫でしょ / たった3歳 | 同上 |

## 【画像生成ブロック回避チェック】

✅ 問題なし — 未成年 / 暴力・身体的苦痛 / 血液・身体内部 / 紙幣 / 恐怖表情 いずれも不使用。ヒグマは遠景の静的シルエットのみで襲撃描写なし

---

## AI開示ラベル

- YouTube Studio: 「改変または合成コンテンツ」→ **「はい」** を選択

---

## 制作フロー

1. Lovartで上記プロンプトを実行 → 5枚から1枚選定（テキストなし）
2. 前処理: ロゴ・文字の写り込みがあれば消去（服装・人物は維持）
3. Photopeaで1280×720pxに配置。C案は同一画像を左右反転
4. 3案をYouTube StudioのA/Bテスト（サムネテスト＝タイトル固定）へ投入
5. 1〜2週間で勝敗判定 → 勝ちパターンを次作へ展開
