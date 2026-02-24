# 谷川岳 宙吊り事件 素材プロンプト一括リスト

> Lovartにコピペするだけの流れ作業用。生成順＝台本の登場順。

---

## 実写判定レポート（Step 0）

| # | 対象 | 種別 | 実写写真 | 判定 |
|:--|:--|:--|:--|:--|
| 1 | 小森康行 | 人物 | なし（著書あり、ポートレート未発見） | Lovart生成 |
| 2 | 青山成孝 | 人物 | なし | Lovart生成 |
| 3 | 石川三郎 | 人物 | なし（顕彰碑あり） | Lovart生成（登場微小） |
| 4 | Hさん・Nさん | 人物 | イニシャル＝実写対象外 | Lovart生成 |
| 5 | 谷川岳・一ノ倉沢・衝立岩 | 場所 | あり（Wikimedia、ストックフォト多数） | Google Earth + Lovart（統一感優先） |
| 6 | 土合駅 | 場所 | あり（Wikipedia掲載） | Lovart生成（統一感優先） |
| 7 | 沼田警察署 | 場所 | なし（現存建物は現代的） | Lovart生成 |
| 8 | 相馬原駐屯地 | 場所 | あり（自衛隊公式サイト） | Lovart生成（統一感・1960年代再現） |
| 9 | 1960年宙吊り事件報道写真 | イベント | あり（中日映画社ニュース映画、アフロストックフォト） | 参考のみ。素材はLovart生成 |

> **判定**: 実在場所の風景はGoogle Earthで対応。1960年代を再現する必要があるため、人物・建物シーンは全てLovart生成で統一。実写はフォールバックとして記録のみ。

---

## キャラアニメーション用 実写写真リクエスト（Step 0.5）

> **判定**: 全人物の実写写真が見つからなかったため、全CHARに `[実写参照: なし — テキスト情報のみ]` タグを適用。

---

## 0. キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**: キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> Lovartでは1プロンプトにつき5枚同時生成。ベスト1枚を一貫性キャラの参照画像として採用。

### CHAR-01: Hさん（20歳）— 蝸牛山岳会・若手クライマー
[実写参照: なし — テキスト情報のみ]
```
Japanese young man, age 20, slim athletic build, short black hair, youthful eager expression with a hint of nervousness. Wearing 1960s Japanese mountaineering gear: thick wool sweater, canvas rucksack, rope coiled around waist (no modern harness). Full body, white background. Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Muted vintage color palette. No text, no words, no letters. Generate 5 images.
```

### CHAR-02: Nさん（23歳）— 蝸牛山岳会・先輩クライマー
[実写参照: なし — テキスト情報のみ]
```
Japanese young man, age 23, tall and broad-shouldered build, short black hair parted to side, determined confident expression. Wearing 1960s Japanese mountaineering gear: heavy wool jacket, canvas knickers, rope coiled around waist (no modern harness), leather boots. Full body, white background. Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Muted vintage color palette. No text, no words, no letters. Generate 5 images.
```

### CHAR-03: 青山成孝（40代）— 谷川岳山岳警備隊員
[実写参照: なし — テキスト情報のみ]
```
Japanese man, early 40s, sturdy solid build, short black hair, alert serious expression. Wearing 1960s Japanese police mountain patrol uniform: dark jacket with patrol armband, heavy boots, binoculars hanging from neck. Weathered face showing years of mountain patrol experience. Full body, white background. Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Dark muted tones. No text, no words, no letters. Generate 5 images.
```

### CHAR-04: 小森康行（30代）— 日本トップクライマー・衝立岩の第一人者
[実写参照: なし — テキスト情報のみ]
```
Japanese man, early 30s, lean muscular build, weathered sun-tanned face, intense focused eyes, strong jawline. Short cropped black hair. Wearing 1960s mountaineering gear: heavy canvas jacket, climbing helmet (simple metal type), multiple rope coils over shoulders. Radiating competence and quiet authority. Full body, white background. Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Cool muted tones. No text, no words, no letters. Generate 5 images.
```

### CHAR-05: 自衛隊狙撃班員（汎用）— 相馬原駐屯地から派遣
[実写参照: なし — テキスト情報のみ]
```
Japanese military man, late 20s, athletic disciplined build, crew cut black hair, focused intense expression. Wearing 1960s Japan Ground Self-Defense Force field uniform: olive drab fatigues, helmet, rifle slung over shoulder. Standing at attention. Full body, white background. Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Military olive-green tones. No text, no words, no letters. Generate 5 images.
```

---

## 動画予算サマリー

| 項目 | 数 |
|:--|--:|
| Lovart動画（Google Flow使用） | 14本 |
| Veo Fastクレジット消費 | 14 x 20 = 280cr |
| 月間予算（4本/月） | 280 x 4 = 1,120cr |
| AIプロ月間枠 | ~2,500cr |
| 判定 | ✅ 予算内 |

---

## 1. 全素材リスト（台本順）

### 起（導入 — 2人の若手クライマー）

#### ASSET-001 [Google Earth] 台本L21-23
ナレーション: 1960年9月18日。群馬県と新潟県の県境にそびえる谷川岳。
座標: 36°50'14"N 138°55'47"E
カメラ: 宇宙空間から地球→日本列島→群馬県/新潟県県境→谷川岳へゆっくりズームイン。秋の山肌が見えるまで寄る
→ 編集者指示: テキスト追加（「1960年9月18日」「谷川岳」）

#### ASSET-002 [Lovart静止画] 台本L27-28
ナレーション: 神奈川県横浜市に拠点を置く「蝸牛山岳会」の会員、
シーン: 1960年代の横浜港が見える風景
```
1960s Yokohama harbor visible in background. Showa-era Japanese city street. Vintage black-and-white photograph aesthetic. Old wooden buildings, power lines, distant port cranes. Nostalgic somber atmosphere. Photorealistic vintage style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-003 [キャラアニメーション] [CHAR-01 reference | 初出] [CHAR-02 reference | 初出] 台本L33-35
ナレーション: Hさん（20歳）とNさん（23歳）が、谷川岳に入山。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 2人並んで秋の登山道を歩く後ろ姿

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 初出] [CHAR-02 reference | 初出] Two Japanese young male climbers walking together, seen from behind. Large canvas rucksacks on backs, climbing rope coiled over shoulders. 1960s mountaineering gear. Confident stride. Full body, rear view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Muted vintage tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Autumn mountain trail leading toward Ichinokurasawa valley. Early morning mist hanging over path. Trees with early fall colors. Rocky mountain path. Cool morning light. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を登山道に配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央下部に配置（後ろ姿で歩く構図）
- 0s〜5s: 背景をゆっくりズームイン（1.0→1.1）で山に向かっていく感覚
- キャラに微小な上下動（±2px、0.5秒周期）で歩行の動き
- 5秒

#### ASSET-004 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L39-41
ナレーション: 2人は蝸牛山岳会の中でも、腕利きとして知られる若手クライマー。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 岩場で練習する2人

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers practicing rock climbing. One gripping rock with both hands, the other managing rope below. 1960s mountaineering gear. Focused determined expressions. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Muted vintage tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Rocky outdoor climbing training area in Japan. Showa-era mountaineering training ground. Natural rock face with practice routes. Overcast sky. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Nさんを画面右上の岩面に配置、Hさんを画面左下に配置
- 0s〜5s: ゆっくり左から右に動かす（5秒）
- キャラに微揺れ（±2px、1秒周期）
- 5秒

#### ASSET-005 [Lovart静止画] 台本L45-47
ナレーション: 前年の1959年8月。同じ谷川岳の衝立岩で、
シーン: 「衝立岩初登頂成功」の新聞記事風
```
1959 Japanese newspaper front page reporting mountain climbing achievement. Bold headline text area at top. Black-and-white photograph area showing rocky cliff. Showa-era newspaper layout with vertical Japanese text columns. Aged yellowed paper texture. Photorealistic vintage newspaper style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-006 [キャラアニメーション] [Generic group] 台本L51-53
ナレーション: 東京雲稜会の2人のクライマーが、史上初の登頂に成功していました。
参照キャラ: なし（東京雲稜会の2人）
シーン: 岩の上でガッツポーズの2人

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese male climbers in their 20s, 1950s mountaineering gear, standing on rock summit doing victory fist pump. Elated triumphant expressions. Rope and canvas gear. Black-and-white photograph aesthetic. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Desaturated vintage tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Summit area of a massive vertical rock cliff (Tsuitate-iwa). Summer blue sky. Panoramic mountain view from top. Black-and-white vintage photograph tone. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を岩の上に配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央の岩の上に配置
- 0s〜5s: ゆっくりズームアウト（1.15→1.0）で岩壁の全景を見せる
- キャラに腕の上下動（±5px、0.8秒周期）でガッツポーズ
- 5秒

#### ASSET-007 [Google Earth] 台本L57-59
ナレーション: 日本最難関と言われた壁が、ついに人間の手で制された瞬間。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩を下から見上げるアングル。岩壁の垂直さが際立つカメラワーク
→ 編集者指示: テキスト追加（「日本最難関 衝立岩」）

#### ASSET-008 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L65-68
ナレーション: あの壁に、自分たちも立ちたい。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 地図を広げて岩壁を見上げる2人

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers, one holding open map, both looking upward with burning determination in eyes. 1960s mountaineering gear. Excited ambitious expressions. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing fire and ambition. Warm vintage tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley approach with massive Tsuitate-iwa rock wall looming in background through fog. Enormous dark cliff barely visible through mist. Intimidating scale. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を画面手前に配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面下1/3に配置（見上げるポーズ）
- 0s〜5s: 2人の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-009 [Lovart静止画] 台本L72-74
ナレーション: その熱意が、2人を谷川岳に向かわせたのでした。
シーン: 秋の谷川岳登山道入口
```
Autumn trail entrance to Tanigawadake mountain. Morning mist. Trees with early fall foliage in red and orange. Steep rocky wall faintly visible through fog in distance. Ominous yet beautiful atmosphere. Cool morning light. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。岩壁に向かってフォーカス移動

#### ASSET-010 [Google Earth] 台本L78-80
ナレーション: 目的地は、谷川岳の東面にそびえる「衝立岩」。
座標: 36°50'50"N 138°56'32"E → 36°50'44"N 138°56'20"E
カメラ: 一ノ倉沢出合から衝立岩を正面に見据える角度。岩壁の垂直さと圧倒的な高さが伝わるカメラワーク

#### ASSET-011 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L83-87
ナレーション: 高さおよそ300メートル、ほぼ垂直に切り立った一枚岩。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 衝立岩の基部から見上げる2人

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers tilting heads far back, looking straight up. Necks craned, mouths slightly open in awe. 1960s mountaineering gear. Full body, rear three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes wide with awe. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Looking straight up at the base of Tsuitate-iwa cliff face. Rock wall fills entire frame stretching impossibly high. Wet dark serpentinite surface. Overwhelming vertical scale. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を画面下部に小さく配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面最下部に配置（見上げる構図で岩壁の巨大さを強調）
- 0s〜5s: 2人の頭上方向にゆっくりズームイン（1.0→1.1）
- 5秒
→ 編集者指示: テキスト追加（「高さ約300m」）

#### ASSET-012 [Lovart動画] 台本L92-94
ナレーション: 何度も挑戦され、何度も退けられてきたこの壁に、2人は挑もうとしていました。
シーン: 霧に包まれた衝立岩の全景
```
Massive Tsuitate-iwa rock wall shrouded in thick fog. Camera looking up from below. Wet black serpentinite surface gleaming. Fog slowly drifting, revealing and hiding the cliff. Dark ominous atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Thick fog slowly parting to reveal massive dark vertical rock face. Fog drifting across surface. Camera slowly tilting upward along the endless cliff wall. Eerie atmospheric reveal. 5 seconds.
```

#### ASSET-013 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L98-100
ナレーション: この日、2人は一ノ倉沢の出合から岩壁の基部に取りつき、衝立岩正面の壁に挑戦。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 岩壁の基部で装備を最終確認する2人

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers checking climbing gear. One tightening rope around waist, the other checking carabiners. 1960s mountaineering equipment. Serious focused expressions. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing focus. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Base of Tsuitate-iwa massive dark rock wall towering above. Black serpentinite surface. Overcast sky barely visible at top. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央に配置（装備確認の動作）
- 0s〜5s: 装備を確認する手元からゆっくりズームアウト（1.15→1.0）
- キャラに微小な手の動き（±3px）で装備チェック表現
- 5秒

#### ASSET-014 [Lovart静止画] 台本L104-106
ナレーション: Nさんが先行、Hさんが確保役。
シーン: 先行者と確保者の役割図解
```
Diagram-style illustration of rock climbing lead-belay system. Two silhouettes of Japanese climbers connected by rope on vertical cliff face. Leader above, belayer below. Rope line clearly visible. Dark moody background. Photorealistic diagram style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。テキスト追加（「先行: Nさん」「確保: Hさん」）

#### ASSET-015 [キャラアニメーション] [CHAR-02 reference | 再利用] 台本L110-112
ナレーション: 先行するNさんがルートを切り拓き、後続のHさんがザイルで安全を確保する。
参照キャラ: CHAR-02（Nさん）
シーン: 岩壁に手をかけて登るNさん

**キャラプロンプト（CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-02 reference | 再利用] Japanese young man, age 23, gripping rock with both hands, looking upward. Rope tied around waist. 1960s mountaineering gear. Intense focused expression, perspiration on forehead. Full body, side view looking up. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing determination. Cool dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Vertical serpentinite rock face close-up. Dark wet black surface with climbing route cracks. Overcast sky above. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Nさんを画面中央の岩壁に配置（登攀中）
- 0s〜5s: 下から見上げるように背景をゆっくり上に動かす（5秒）
- キャラに微小な手の動き（±3px）で登る動作
- 5秒

#### ASSET-016 [Lovart動画] 台本L116-118
ナレーション: 2人は交互にピッチを重ね、少しずつ高度を上げていきます。
シーン: 垂直の岩壁を登る2人のクライマーシルエット
```
Two silhouettes of Japanese climbers ascending vertical dark rock face. One above securing rope, one climbing below. 1960s climbing gear. Tiny human figures against massive cliff. Dramatic scale contrast. Overcast sky. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Two small silhouette figures slowly ascending vertical rock face. One figure reaches up, the other belays from below. Subtle wind movement. Camera slowly tilting upward following climbers. 5 seconds.
```

#### ASSET-017 [Lovart静止画] 台本L122-125
ナレーション: しかし、この直後、二人は悲惨な事故により命を失うことに、、
シーン: 無人の衝立岩正面。不気味な静寂
```
Deserted Tsuitate-iwa rock face, front view. No people. Fog and clouds enveloping rock wall. Complete eerie silence suggested by still misty atmosphere. Autumn overcast sky. Ominous dark tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。岩壁の巨大さが際立つように

#### ASSET-018 [キャラアニメーション] [CHAR-02 reference | 再利用] 台本L131-133
ナレーション: 後の調査で推定されたのは、こういうことでした。
参照キャラ: CHAR-02（Nさん）
シーン: 岩壁途中で体勢を崩すNさん

**キャラプロンプト（CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-02 reference | 再利用] Japanese young man losing balance on rock face. One foot slipping off ledge, arms flailing. Terror on face. 1960s climbing gear, rope around waist. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes wide with fear. Desaturated dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Vertical rock face midway up Tsuitate-iwa cliff. Deep valley below with fog. Mist drifting. Dangerous exposed position. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Nさんを画面中央に配置（足が滑るポーズ）
- 0s〜5s: Nさんの足元にゆっくりズームイン（1.0→1.15）
- キャラに微小な傾き（±5度）で体勢の崩れを表現
- 5秒

#### ASSET-019 [Lovart動画] 台本L139-141
ナレーション: その衝撃がザイルを通じてHさんに伝わり、Hさんもろとも岩壁から引き剥がされたのです。
シーン: 岩壁から引きずり落とされる2つのシルエット
```
Two small silhouettes of climbers being pulled off vertical rock face. One falls first, rope connecting them yanks the second off. Dark cliff, misty background. Faces not visible at this distance. Horrifying moment captured from far away. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
One small silhouette figure slips from rock face, rope snaps taut pulling second figure off wall. Both figures swinging into void. Camera pulls back slowly revealing massive cliff scale. 5 seconds.
```

#### ASSET-020 [キャラアニメーション] [Generic group] 台本L145-148
ナレーション: 2人は互いに繋がれたまま、空中に投げ出されてしまいました。
参照キャラ: なし（2人のシルエット）
シーン: ザイルで繋がれたまま宙に浮く2人のシルエット

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese male climbers silhouettes connected by rope, suspended in mid-air. Arms spread, flailing. 1960s climbing gear. Desperate helpless poses. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closed/terrified). Dark desaturated tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock face, 200 meters above ground. Overcast sky. Valley and mountains visible below. Fog drifting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を岩壁途中に小さく配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人のシルエットを画面中央やや上に小さめに配置
- 0s〜5s: ゆっくりズームアウト（1.15→1.0）で岩壁の中の小さなシルエットを強調
- キャラに微小な揺れ（±3px、1.5秒周期）
- 5秒

---

### 承（1. 発見 — 動かない2つの影）

#### ASSET-021 [キャラアニメーション] [CHAR-03 reference | 初出] 台本L160-162
ナレーション: 群馬県警察の谷川岳山岳警備隊に、一本の通報が入ります。
参照キャラ: CHAR-03（青山成孝）
シーン: 電話を受ける青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 初出] Japanese man in his 40s, police mountain patrol uniform. Holding old black rotary telephone receiver to ear. Furrowed brow, writing on notepad. Serious alert expression. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing concern. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Interior of 1960s Japanese mountain patrol station. Wooden cabin walls. Topographic maps pinned on wall. Old black rotary telephone on desk. Dim warm lighting. Sparse furnishings. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面中央に配置（電話を受けるポーズ）
- 0s〜5s: 青山さんの表情にゆっくりズームイン（1.0→1.15）
- キャラに微小な手の動き（±2px）でメモを取る動作
- 5秒

#### ASSET-022 [Lovart静止画] 台本L166-169
ナレーション: 「一ノ倉沢で、転落事故が起きたようだ」
シーン: 黒いダイヤル式電話機のクローズアップ
```
Close-up of old black rotary dial telephone on wooden desk. Receiver lifted. 1960s Japanese office setting. Warm dim lighting. Dramatic chiaroscuro. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-023 [キャラアニメーション] [CHAR-03 reference | 再利用] 台本L173-175
ナレーション: 警備隊員の青山成孝さんが慌てて詰所を飛び出し、一ノ倉沢に向かいます。
参照キャラ: CHAR-03（青山成孝）
シーン: 詰所から走り出す青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 再利用] Japanese man in his 40s, police mountain patrol uniform. Bursting through doorway, running. Equipment in hand. Urgent determined expression. Full body, side view running. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing urgency. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Exterior of 1960s Japanese mountain patrol station. Rustic wooden building. Mountain cabin style. Morning light. Mountain scenery in background. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面中央やや左に配置（走り出すポーズ）
- 0s〜5s: 扉を開ける動作にゆっくりズームアウト（1.15→1.0）
- キャラを左から右に移動（30px、5秒）で走る動き
- 5秒

#### ASSET-024 [Lovart動画] 台本L179-181
ナレーション: 通報者と合流し、約1時間半かけて岩壁の基部にたどり着くと、
シーン: 険しい岩場を登る警備隊員の後ろ姿
```
Japanese mountain patrol officer in 1960s uniform climbing steep rocky terrain. Rear view. Morning mist. Massive Ichinokurasawa rock walls gradually becoming visible through fog. Officer stops and looks up. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Man in dark uniform climbing rocky path, seen from behind. Fog slowly clearing to reveal enormous cliff wall ahead. Officer pauses and looks upward in shock. Camera slowly tilting up following his gaze. 5 seconds.
```

#### ASSET-025 [キャラアニメーション] [CHAR-03 reference | 再利用] 台本L185-187
ナレーション: そこには信じがたい光景が広がっていました。
参照キャラ: CHAR-03（青山成孝）
シーン: 愕然として上を見上げる青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 再利用] Japanese man in his 40s, police mountain patrol uniform. Standing on rocky ground, looking straight up in shock. Mouth agape, eyes wide. Frozen in disbelief. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing shock. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Base of Ichinokurasawa valley looking up at massive Tsuitate-iwa rock face. Overcast sky. Intimidating vertical cliff. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面下部に配置（見上げるポーズ）
- 0s〜5s: 青山さんの表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-026 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L193-195
ナレーション: 地上からおよそ200メートルの高さに、2つの人影がザイルでぶら下がっていたのです。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 岩壁中腹で宙吊りの2人（図解風）

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese male climbers hanging limply from rope on cliff. Upper figure (CHAR-01) and lower figure (CHAR-02) connected by red rope. Bodies motionless, arms dangling. 1960s gear. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closed). Somber desaturated tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Full front view of Tsuitate-iwa rock face. Diagram-like composition showing entire cliff from base to top. Overcast sky. Dark serpentinite surface. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで2人を岩壁の中腹に配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Hさんを画面中央やや上、Nさんをその下方に配置（上下約50m離れた位置）
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- キャラに微小な揺れ（±2px、2秒周期）で風に揺れる動き
- 5秒
→ 編集者指示: テキスト追加（「約200m」の高さ表示）

#### ASSET-027 [キャラアニメーション] [CHAR-01 reference | 再利用] 台本L199-201
ナレーション: 上方にいたのはHさん。第二ハングと呼ばれる張り出しを越えたあたりで、宙吊りになっていました。
参照キャラ: CHAR-01（Hさん）
シーン: 宙吊りのHさん

**キャラプロンプト（CHAR-01）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] Japanese young man, age 20, hanging limply from rope around waist. Arms dangling, completely motionless. 1960s climbing gear. Eyes closed. Full body, front view, suspended vertically. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closed). Somber cold tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock face at second overhang area. Vertical dark serpentinite surface. Fog drifting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Hさんを画面中央に配置（宙吊り状態）
- 0s〜5s: ゆっくりズームイン（1.0→1.15）
- キャラに微小な揺れ（±2px、2秒周期）
- 5秒
→ 編集者指示: テキスト追加（「Hさん 第二ハング付近」）

#### ASSET-028 [キャラアニメーション] [CHAR-02 reference | 再利用] 台本L205-207
ナレーション: そこから約50メートル下方、第一ハング付近にNさん。
参照キャラ: CHAR-02（Nさん）
シーン: 宙吊りのNさん

**キャラプロンプト（CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-02 reference | 再利用] Japanese young man, age 23, hanging from rope around waist, body tilted at angle. Arms dangling, completely motionless. 1960s climbing gear. Eyes closed. Full body, front view, suspended. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closed). Somber cold tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock face at first overhang area. Red climbing rope visible extending upward. Vertical dark serpentinite surface. Fog. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- Nさんを画面中央に配置（宙吊り状態、やや傾いた体）
- 0s〜5s: ゆっくりズームアウト（1.15→1.0）で2人の距離感を見せる
- キャラに微小な揺れ（±2px、2秒周期）
- 5秒
→ 編集者指示: テキスト追加（「Nさん 第一ハング付近」「約50m」）

#### ASSET-029 [Google Earth] 台本L211-213
ナレーション: 2人を繋ぐ赤いザイルが、岩壁に沿って垂れ下がっている状態。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の3D地形を横から見た断面図。地上から200m地点に発見位置をマーク。岩壁の傾斜角度を強調
→ 編集者指示: テキスト追加（「発見位置 約200m」）

#### ASSET-030 [Lovart動画] 台本L219-221
ナレーション: 双眼鏡で確認しても、手足の動きは一切見られず、声をかけても、反応はありません。
シーン: 双眼鏡越しの視界
```
Binocular view (circular vignette frame). Distant vertical rock face visible through shaky circular viewport. Two tiny human figures hanging from rope on cliff, barely discernible. Wind-blown, slightly swaying. Far away, out of reach. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Shaky binocular circular view slowly focusing on distant rock face. Two tiny hanging figures gradually come into focus. Subtle wind sway. Binocular view trembles slightly. Eerie distant observation. 5 seconds.
```

#### ASSET-031 [キャラアニメーション] [CHAR-03 reference | 再利用] 台本L227-229
ナレーション: 「もう2人はダメだろう」 誰が見てもそう判断せざるを得ない状況でした。
参照キャラ: CHAR-03（青山成孝）
シーン: 双眼鏡を下ろし苦渋の表情の青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 再利用] Japanese man in his 40s, police mountain patrol uniform. Lowering binoculars with one hand, eyes closed, head shaking slowly side to side. Pained anguished expression. Another man standing behind. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing grief. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Base of Ichinokurasawa valley. Tsuitate-iwa rock wall towering in background. Overcast sky. Another man standing nearby. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面中央に配置
- 0s〜5s: 青山さんの表情にゆっくりズームイン（1.0→1.15）
- 首を横に振る微小な動き（±5px、1.5秒周期）
- 5秒

---

### 承（2. 腹巻き式の致命的弱点）

#### ASSET-032 [キャラアニメーション] [Generic group] 台本L237-239
ナレーション: 当時の登山装備は、現在と比べて危険だらけでした。
参照キャラ: なし（1960年代の登山者）
シーン: 1960年代の装備を点検する登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s mountaineering clothing. Kneeling and inspecting climbing gear laid out on ground: khaki anorak, knickers, leather boots, ice axe, hemp rope. Careful focused expression. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Vintage sepia tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Japanese mountain hut exterior. Climbing gear spread on ground: canvas anorak, leather boots, hemp rope, ice axe. Black-and-white vintage photograph aesthetic. No people visible. Photorealistic vintage style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置
- 0s〜5s: ゆっくり左から右に動かす（5秒）
- キャラに微小な手の動き（±3px）で装備チェック
- 5秒

#### ASSET-033 [Lovart静止画] 台本L243-245
ナレーション: ハーネスはまだ普及しておらず、ザイルは直接、腰や腹に巻きつける腹巻式。
シーン: 腹巻き式ザイルの図解
```
Diagram-style close-up of 1960s climbing rope wrapped directly around a Japanese man's torso and waist (belly-wrap method). Rope coiled tightly around abdomen. No harness. Clear detail of wrapping technique. Dark moody background. Photorealistic diagram style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。テキスト追加（「腹巻き式」）

#### ASSET-034 [キャラアニメーション] [Generic group] 台本L249-251
ナレーション: 実は、この「腹巻き式」の方法には、致命的な弱点がありました。
参照キャラ: なし（図解用の登山者）
シーン: 腹巻きザイルの弱点の図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s climbing gear, standing upright. Rope wrapped around waist area highlighted in red glow to show danger zone. Neutral expression. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Highlighted red rope area. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark grey solid background for diagram use. Clean minimal backdrop. No texture. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置
- 0s〜5s: ザイルの巻きつけ部分にゆっくりズームイン（1.0→1.2）
- 5秒

#### ASSET-035 [キャラアニメーション] [Generic group] 台本L255-258
ナレーション: 万が一、宙吊りの状態になると、ザイルが腹部を締めつけ、内臓を圧迫。
参照キャラ: なし（図解用の登山者）
シーン: 宙吊りで腹部圧迫の図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s climbing gear, hanging from rope wrapped around abdomen. Body weight compressing on rope at waist. Red highlighted pressure area on abdomen. Pained expression. Full body, side view suspended. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing pain. Dark tones with red highlights. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark grey solid background for medical diagram use. Clean minimal backdrop. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置（宙吊り図解）
- 0s〜5s: ゆっくりズームイン（1.0→1.15）
- 5秒
→ 編集者指示: テキスト追加（「腹部を圧迫」「内臓への負荷」の矢印）

#### ASSET-036 [Google Earth] 台本L262-264
ナレーション: そのまま血流が止まり、意識が薄れ、やがて心臓が停止する恐れがあります。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の3D地形。岩壁の基部から見上げる角度で、200m上空の宙吊り位置までの垂直距離を強調。孤立した壁の中で動けない状況が伝わるカメラワーク
→ 編集者指示: テキスト追加（「宙吊り位置 200m」）

#### ASSET-037 [キャラアニメーション] [Generic group] 台本L270-273
ナレーション: 宙吊りになってから意識を失うまで、わずか数分の出来事とされています。
参照キャラ: なし（図解用の登山者）
シーン: 時間経過で力が抜けていく図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s climbing gear, hanging from rope. Progressive loss of consciousness: body going limp, arms dropping, head tilting. Time-lapse diagram feel. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (gradually closing). Dark somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background with subtle clock/time icon silhouette. Time-passage atmosphere. Minimal dark design. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- キャラをゆっくり下に沈ませる（-10px、5秒）で力が抜ける表現
- 5秒
→ 編集者指示: テキスト追加（「サスペンション・トラウマ」「数分で意識喪失」）

#### ASSET-038 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L277-279
ナレーション: 1960年当時、この知識は一般の登山者にはほとんど知られていませんでした。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 入山前の笑顔の2人

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers smiling, tying rope around waists carelessly. No concern, no awareness of danger. Happy eager expressions. 1960s mountaineering gear. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing happiness. Warm bright tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain trailhead area in early morning light. Bright warm atmosphere. Autumn colors. Contrast to later dark scenes. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央に配置（笑顔で装備中）
- 0s〜5s: ゆっくりズームイン（1.0→1.1）。腰のザイル部分にフォーカス
- 5秒

---

### 承（3. 誰も近づけない壁）

#### ASSET-039 [キャラアニメーション] [CHAR-03 reference | 再利用] 台本L287-289
ナレーション: 2人の姿は確認できた。しかし、回収する手段がなかったのです。
参照キャラ: CHAR-03（青山成孝）
シーン: 絶望的な表情で岩壁を見上げる青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 再利用] Japanese man in his 40s, police mountain patrol uniform. Looking up at cliff with desperate hopeless expression. Clenching fists. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing despair. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Full view of Tsuitate-iwa rock face looking up. Two tiny dots (human figures) visible midway up the massive cliff. Overwhelming scale. Overcast sky. No people at base visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面下部に配置（見上げるポーズ）
- 0s〜5s: 青山さんの表情から岩壁にゆっくりズームイン（1.0→1.1）
- 5秒

#### ASSET-040 [キャラアニメーション] [CHAR-03 reference | 再利用] 台本L293-295
ナレーション: しかもこの日の天候は不安定。
参照キャラ: CHAR-03（青山成孝）
シーン: 空を見上げて険しい表情の青山さん

**キャラプロンプト（CHAR-03）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-03 reference | 再利用] Japanese man in his 40s, police mountain patrol uniform. Looking up at sky with stern worried expression. Clothes and hair ruffling in wind. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing worry. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley. Low heavy clouds. Strong wind. Rock wall upper portion hidden in fog. Threatening weather. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 青山さんを画面下部に配置
- 0s〜5s: 青山さんから空へゆっくりズームアウト（1.1→1.0）
- キャラに微揺れ（±3px）で風の強さを表現
- 5秒

#### ASSET-041 [Lovart静止画] 台本L299-301
ナレーション: 回収のために岩壁に取りついた場合、救助隊員が事故に遭う危険も高い。
シーン: 雨に濡れた蛇紋岩のクローズアップ
```
Close-up of wet serpentinite rock surface. Water droplets running down black-green glistening stone. Dangerously slippery texture. Dark moody lighting. Photorealistic macro photography, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。岩の質感が伝わるように

#### ASSET-042 [Google Earth] 台本L305-306
ナレーション: つまり、目の前に2人がいるのに、誰も近づけない状況でした。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の3D地形。基部から宙吊り地点までのルートを見せるが、オーバーハング部分が立ちはだかっている様子。到達不可能な状況が伝わるカメラワーク

---

### 承（4. 代替案の模索）

#### ASSET-043 [キャラアニメーション] [Generic group] 台本L314-317
ナレーション: 翌日、9月20日。蝸牛山岳会から、11人の仲間が現場に駆けつけます。
参照キャラ: なし（山岳会メンバー）
シーン: 登山道を歩く仲間たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Five Japanese male hikers in their 20s-40s, 1960s mountaineering gear, heavy packs. Walking in line, grim serious expressions. Full body, front view walking toward camera. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing grief. Muted dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain trail leading to Ichinokurasawa valley. Autumn overcast sky. Heavy clouds. Dark somber atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 5人を画面中央に配置（正面歩行）
- 0s〜5s: 正面から歩いてくる一行をゆっくりズームイン（1.0→1.1）
- キャラに微小な上下動（±2px、0.5秒周期）で歩行表現
- 5秒

#### ASSET-044 [Lovart動画] 台本L321-323
ナレーション: しかし、この日は朝からガスと雨。
シーン: 雨に煙る衝立岩
```
Tsuitate-iwa rock wall obscured by heavy rain and fog. Thick cloud cover pressing down. Rain streaming down rock surface. Midway up cliff completely invisible in mist. Dark ominous atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Heavy rain falling on massive rock face. Fog banks rolling in from left. Cliff gradually disappearing into cloud and rain. Rain drops running down rock surface. Camera slowly tilting upward into nothingness of fog. 5 seconds.
```

#### ASSET-045 [Lovart静止画] 台本L327-329
ナレーション: 谷川岳の岩壁は「蛇紋岩」という特殊な岩石でできています。
シーン: 蛇紋岩のクローズアップ
```
Extreme close-up of serpentinite rock surface, wet and glistening black-green. Rain water streaming down polished stone. Distinctive serpentine pattern visible. Dark moody lighting, high contrast. Photorealistic macro, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。岩の表面の質感が伝わるように

#### ASSET-046 [Google Earth] 台本L335-337
ナレーション: しかも日本海側と太平洋側の気候がぶつかる位置にあるため、天候が恐ろしいスピードで急変。
座標: 36°50'14"N 138°55'47"E
カメラ: 谷川岳の広域表示。日本海側と太平洋側の分水嶺の位置を示す。雲が山にぶつかる気象の仕組みが伝わるカメラワーク
→ 編集者指示: テキスト追加（「日本海側」「太平洋側」「気候の衝突点」）

#### ASSET-047 [キャラアニメーション] [Generic group] 台本L343-345
ナレーション: とても救助に向かえる状況ではありません。
参照キャラ: なし（テント内の登山者たち）
シーン: テントの中で悔しがる仲間たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Three Japanese male hikers in their 20s-40s, 1960s mountaineering gear, sitting inside tent. Stern frustrated expressions. One clenching fists. Damp clothing. Full body, front view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing frustration. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Interior of simple canvas tent. Dim lighting. Rain visible through tent fabric. Gear scattered inside. Heavy rain sounds implied by wet surfaces. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人をテント内に配置
- 0s〜5s: 各人の手元と表情を交互にゆっくりズームイン（1.0→1.1）
- 5秒

#### ASSET-048 [キャラアニメーション] [Generic group] 台本L351-353
ナレーション: 「長い棒の先にナイフを付けて、ザイルを切れないか」
参照キャラ: なし（テント内の登山者）
シーン: スケッチを描く登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s mountaineering gear, sitting cross-legged. Drawing sketch on paper with pencil. Serious concentrated expression. Full body, three-quarter view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing concentration. Warm lamp-lit tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Interior of canvas tent. Map and gear spread out. Sketch of long pole with knife on paper. Lamp lighting. Rain sounds. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置
- 0s〜5s: スケッチを描く手元にゆっくりズームイン（1.0→1.2）
- キャラに微小な手の動き（±3px）で描画表現
- 5秒

#### ASSET-049 [キャラアニメーション] [Generic group] 台本L357-359
ナレーション: 「油に浸した布を巻いた松明で、焼き切れないか」
参照キャラ: なし（テント内の登山者たち）
シーン: 松明のスケッチを描く登山者と首を振る仲間

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese men in their 30s, 1960s mountaineering gear, inside tent. One drawing torch sketch on paper, the other shaking head negatively. Tense expressions. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Warm lamp-lit tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Interior of canvas tent. Lamp flame. Rain pattering on canvas. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人をテント内に配置
- 0s〜5s: スケッチから首を振る男性にゆっくりフォーカス移動
- 首を横に振る微小な動き（±5px、1秒周期）
- 5秒

#### ASSET-050 [Lovart静止画] 台本L363-366
ナレーション: どの作戦も、300メートルもの壁には通用しないものでした。
シーン: 検討作戦の図解
```
Dark dramatic background with subtle mountain silhouette. Three failed rescue plans shown as diagram elements with X marks. Space for text overlay. Dark moody atmosphere. Photorealistic dark background. Documentary infographic style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「ナイフ付き棒→到達不可能」「松明→到達不可能」「登攀→天候不良で断念」）。ゆっくりズームイン（5秒）

---

### 承（5. 決死の接近 — あと3メートル）

#### ASSET-051 [Lovart静止画] 台本L372-374
ナレーション: 翌日9月21日。わずかに天候が回復。
シーン: 雲の切れ間から光が差す一ノ倉沢
```
Ichinokurasawa valley after rain. Clouds breaking apart, thin sunlight streaming through gaps. Still damp atmosphere. Tsuitate-iwa faintly visible in distance. Cautious hope atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.1）。雲の切れ間に向かって

#### ASSET-052 [キャラアニメーション] [CHAR-04 reference | 初出] 台本L380-382
ナレーション: 小森康行さん。
参照キャラ: CHAR-04（小森康行）
シーン: 立ち上がり衝立岩を見上げる小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 初出] Japanese man, early 30s, lean muscular build. Standing up with resolve, looking upward. Holding climbing helmet in one hand. Determined expression. 1960s mountaineering gear: heavy canvas jacket, rope coils. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing determination. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley approach. Overcast but brighter than previous day. Tsuitate-iwa rock wall towering in background. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央に配置
- 0s〜5s: 小森さんの表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-053 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L386-388
ナレーション: 日本を代表するトップクライマーの1人であり、衝立岩に誰よりも精通した人物。
参照キャラ: CHAR-04（小森康行）
シーン: 装備を整える小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, lean muscular build. Putting on climbing helmet, adjusting rope on shoulder. Surrounded by watching companions (4 figures in background). Focused preparation expression. 1960s mountaineering gear. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing focus. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley staging area. Climbing gear laid out. Four other climbers standing in background watching. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央に配置
- 0s〜5s: 装備を整える手元にゆっくりズームイン（1.0→1.15）
- キャラに微小な手の動き（±3px）
- 5秒

#### ASSET-054 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L392-394
ナレーション: 小森さんを含む5名のパーティーが、2人の回収のために動き出したのです。
参照キャラ: CHAR-04（小森康行）
シーン: 5人が一列で岩壁に向かう

**キャラプロンプト（CHAR-04 + Generic group）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] [Generic group] Five Japanese male climbers walking in single file. Lead figure (CHAR-04) in front with helmet and rope. Four others following behind. 1960s mountaineering gear. Determined stride. Full body, rear view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley with Tsuitate-iwa rock face directly ahead. Five-person climbing party would be approaching. Massive dark cliff. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 5人を画面下部に配置（後ろ姿、岩壁に向かう）
- 0s〜5s: 5人の後ろ姿にゆっくりズームイン（1.0→1.1）
- キャラに微小な上下動（±2px、0.5秒周期）で歩行
- 5秒

#### ASSET-055 [Google Earth] 台本L400-402
ナレーション: しかし、衝立岩の正面には巨大なオーバーハングが張り出しています。真下から直接登って2人に近づくことは、不可能でした。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩を横から見た3D地形。正面のオーバーハングを強調し、正面ルートが使えないことが伝わるカメラワーク
→ 編集者指示: テキスト追加（「正面ルート 登攀不可能」）

#### ASSET-056 [Google Earth] 台本L406-408
ナレーション: 小森さんたちは、隣接するルートから回り込むように高度を上げ、
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の3D地形。迂回ルートを矢印で示す。側面から登り、横移動でNさんの位置に近づく計画
→ 編集者指示: テキスト追加（「迂回ルート」の矢印）

#### ASSET-057 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L412-414
ナレーション: 横移動でNさんの位置に近づいていく計画を立てました。
参照キャラ: CHAR-04（小森康行）
シーン: 地図でルートを確認する小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, lean muscular build. Holding open map, tracing route with finger. Discussing with companion. 1960s mountaineering gear. Full body, three-quarter view looking down at map. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing concentration. Cool muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Base of rock cliff. Climbing gear spread out. Map laid on rock. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央に配置
- 0s〜5s: 地図の上で指が動くのにゆっくりズームイン（1.0→1.2）
- キャラに微小な手の動き（±3px）
- 5秒

#### ASSET-058 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L418-420
ナレーション: 垂直に近い岩壁を、一歩一歩。
参照キャラ: CHAR-04（小森康行）
シーン: 岩壁に張りつき登る小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, lean muscular build. Clinging to vertical rock face, carefully searching for next foothold. Sweat on forehead. Intense focused expression. 1960s climbing gear, helmet. Full body, side view climbing. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing intense focus. Cool dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Side face of Tsuitate-iwa cliff. Near-vertical dark serpentinite rock surface. Wet black stone. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央の岩壁に配置
- 0s〜5s: 小森さんの手足の動きにゆっくりズームイン（1.0→1.15）
- キャラに微小な上方移動（+5px、5秒）で登攀表現
- 5秒

#### ASSET-059 [Lovart動画] 台本L424-426
ナレーション: 風化してもろくなった岩の突起。いつ崩れてもおかしくありません。
シーン: 岩をつかんだ瞬間に崩れる手元のアップ
```
Close-up of gloved hand gripping dark serpentinite rock protrusion. Rock suddenly crumbles and breaks apart under grip. Climber's hand recoiling, desperately grabbing another hold. Water seeping from rock cracks. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Close-up of hand gripping rock protrusion. Rock suddenly crumbles apart. Hand slips and quickly grabs another hold nearby. Rock debris falling downward. Tense dramatic moment. 5 seconds.
```

#### ASSET-060 [Lovart静止画] 台本L430-432
ナレーション: 前日の雨の湿気がまだ残る蛇紋岩は、手をかけるたびに嫌な滑りを見せます。
シーン: 濡れた岩を掴む手のクローズアップ
```
Extreme close-up of bare hand gripping wet serpentinite rock. Water seeping between fingers. White-knuckled grip showing tension. Slippery wet surface. Dark moody macro photography. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。手の震えを感じさせるように

#### ASSET-061 [キャラアニメーション] [Generic group] 台本L436-439
ナレーション: 掴んだ岩が突然崩れ落ちることもありました。
参照キャラ: なし（クライマー）
シーン: 岩が砕けて落ちる瞬間

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s climbing gear, clinging to rock face. Hand-hold breaking apart, rock crumbling. Panicked expression, grabbing for new hold. Full body, side view on wall. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing panic. Dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Vertical rock face of Tsuitate-iwa side wall. Deep valley below. Dark serpentinite surface. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央の岩壁に配置
- 0s〜5s: 岩が崩れる瞬間にゆっくりズームイン（1.0→1.15）
- キャラに体の傾き変化（±8度、0.5秒）で体勢の崩れ
- 5秒

#### ASSET-062 [キャラアニメーション] [CHAR-04 reference | 再利用] [Generic group] 台本L445-447
ナレーション: 5人の命が、常に危険にさらされる状況。作業開始から数時間。午後2時半。
参照キャラ: CHAR-04（小森康行）
シーン: 岩壁途中の疲労したクライマーたち

**キャラプロンプト（CHAR-04 + Generic group）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] [Generic group] Three Japanese male climbers pressed against rock face, exhausted. Sweating heavily. Fatigue visible. Late afternoon weak light on faces. 1960s climbing gear. Full body, side view clinging to wall. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing exhaustion. Warm-dark late afternoon tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock wall midway up. Valley visible far below. Late afternoon light. Elevation sense. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人を岩壁に配置
- 0s〜5s: ゆっくりズームアウト（1.1→1.0）で高度感を強調
- 5秒

#### ASSET-063 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L451-455
ナレーション: 小森さんのパーティーは、ついにNさんの姿まであと3メートル、という地点に到達しました。
参照キャラ: CHAR-04（小森康行）
シーン: あと3mの位置で上を見上げる小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, lean muscular build. Clinging to rock face, looking upward. Sweat and tension on face. Above him a faint silhouette of hanging figure just meters away. Desperate reaching expression. 1960s climbing gear, helmet. Full body, side view on wall looking up. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing desperation. Dark twilight tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Rock face midway up Tsuitate-iwa. Twilight weak light. Deep valley below. Faint silhouette of hanging figure visible few meters above. No people at close range visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央やや下に配置（見上げるポーズ）
- 0s〜5s: 小森さんの視線の先（上方のシルエット）にゆっくりフォーカス移動
- 5秒
→ 編集者指示: テキスト追加（「あと3m」）

#### ASSET-064 [Lovart静止画] 台本L461-463
ナレーション: 手を伸ばせば、もう少しで届く。
シーン: 届きそうで届かない指先とザイルの端
```
Close-up of outstretched climber's hand reaching upward. Rope end visible just above fingertips. Almost touching but not quite reaching. Rocky cliff background. Dramatic tension. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: 指先にゆっくりズームイン（5秒で1.0→1.2）

#### ASSET-065 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L467-469
ナレーション: しかし、すでにあたりは暗くなりかけていました。
参照キャラ: CHAR-04（小森康行）
シーン: 暗さに気づく小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, clinging to rock face. Looking around at darkening surroundings, expression clouding with worry. Helmet, 1960s climbing gear. Full body, three-quarter view on wall. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing concern. Dark twilight tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock face at twilight. Sky transitioning from orange to purple. Darkness closing in. Dramatic fading light. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央の岩壁に配置
- 0s〜5s: 空の色の変化にゆっくりズームアウト（1.1→1.0）
- 5秒

#### ASSET-066 [キャラアニメーション] [CHAR-04 reference | 再利用] 台本L475-477
ナレーション: 小森さんは、この至近距離からNさんの様子を目視で確認し、生存していないことを確認。
参照キャラ: CHAR-04（小森康行）
シーン: 苦渋の表情で上方を見つめる小森さん

**キャラプロンプト（CHAR-04）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-04 reference | 再利用] Japanese man, early 30s, clinging to rock face. Looking up with grief-stricken expression, biting lip. Eyes closing, taking deep breath. Painful decision moment. 1960s climbing gear, helmet. Full body, side view on wall. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing deep sorrow. Dark twilight tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Rock face of Tsuitate-iwa at twilight. Faint silhouette of hanging figure above in fading light. Dark atmosphere. No people at close range visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 小森さんを画面中央に配置
- 0s〜5s: 小森さんの表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-067 [Lovart動画] 台本L481-483
ナレーション: 仕方なく安全のため小森さん含む5名は、撤退を開始することに。
シーン: 夕暮れの岩壁を降りる5人のシルエット
```
Silhouettes of five climbers slowly descending dark rock face at sunset. One figure turns back to look up. Faint hanging figure visible high above on cliff. Dramatic sunset sky transitioning to dark. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Five silhouette figures slowly climbing down rock face. One figure pauses and looks back upward. Sunset light fading to darkness. Wind sound. Solemn slow retreat. Camera slowly pulling back. 5 seconds.
```

#### ASSET-068 [Lovart静止画] 台本L487-489
ナレーション: 日本屈指のトップクライマーが命を賭けて挑んでも、あと3メートルが届かない。
シーン: 夕暮れの衝立岩全景
```
Tsuitate-iwa rock face at sunset. Darkening sky. Two tiny silhouettes hanging at cliff midway, barely visible. Overwhelming scale of wall. Somber majestic atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。岩壁の巨大さが際立つように

#### ASSET-069 [Google Earth] 台本L493-495
ナレーション: それが、衝立岩という壁でした。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の夕暮れの3D地形。岩壁を横から見せて、垂直さとスケール感を強調するカメラワーク
→ 編集者指示: テキスト追加（「衝立岩 高さ約300m」）

---

### 承（6. 苦渋の決断 — 「撃て」）

#### ASSET-070 [キャラアニメーション] [Generic group] 台本L503-506
ナレーション: 小森さんの報告を受け、蝸牛山岳会は緊急の対策会合を開きました。
参照キャラ: なし（山岳会メンバー）
シーン: 夜の山小屋で激論する男たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Five Japanese men in their 20s-40s, sitting facing each other in intense discussion. One slamming fist on table. Grim angry expressions. 1960s mountaineering clothing. Full body, three-quarter view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing anger and grief. Warm lamp-lit tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Interior of 1960s mountain hut at night. Dim oil lamp on table. Maps and documents scattered. Dark window showing night outside. Tense heavy atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 5人をテーブル周りに配置
- 0s〜5s: ゆっくり左から右にパン（5秒）。各人の表情を映す
- 5秒

#### ASSET-071 [キャラアニメーション] [Generic group] 台本L512-514
ナレーション: 仲間を、あのまま壁に残すのか。それとも、別の方法を探すのか。
参照キャラ: なし（苦悩する男たち）
シーン: 両手で顔を覆う男性

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s mountaineering clothing. Sitting with face buried in hands. Deep anguish. Another man beside him placing hand on shoulder consolingly. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (hidden behind hands). Dark warm tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain hut interior. Oil lamp light. Heavy oppressive atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- うつむく男性を画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-072 [キャラアニメーション] [Generic group] 台本L520-522
ナレーション: 夜通し続いた議論の末、残された選択肢は、ひとつだけでした。
参照キャラ: なし（窓際の登山者）
シーン: 窓から夜空を見つめる男性

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s mountaineering clothing. Sitting by window, exhausted expression, staring outside into night sky. Oil lamp glow on face. Full body, side view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing exhaustion. Dark warm tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain hut interior at night. Window showing stars and dark night sky. Oil lamp. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを窓際に配置
- 0s〜5s: 窓の外の夜空にゆっくりフォーカス移動
- 5秒

#### ASSET-073 [Lovart静止画] 台本L526-529
ナレーション: 銃で、ザイルを撃ち切る。
シーン: 検討された回収方法の図解
```
Dark dramatic background with mountain silhouette. Four rescue method diagrams: three with X marks (crossed out), fourth (gunfire) remaining highlighted. Space for large text overlay. Dark moody infographic design. Photorealistic dark background. Documentary infographic style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「ナイフ→不可能」「火→不可能」「登攀→あと3mで断念」「銃撃→唯一の手段」）。1つずつ順番に表示

#### ASSET-074 [キャラアニメーション] [Generic group] 台本L535-537
ナレーション: 銃弾でザイルを切断し、2人を岩壁から引き離す。そして、落下した先で、回収する。
参照キャラ: なし（山岳会幹部）
シーン: 立ち上がって説明する幹部

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 40s, 1960s clothing, standing and gesturing with hands (drop-and-recover gesture). Explaining plan to seated men. Authoritative serious expression. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Dark warm tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain hut interior. All men looking at speaker. Maps and sketches pinned on wall. Oil lamp lighting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 説明する男性を画面中央に配置
- 0s〜5s: 説明する男性から聞く側の表情にゆっくりパン
- 5秒

#### ASSET-075 [キャラアニメーション] [Generic group] 台本L543-545
ナレーション: しかしそれ以外に、2人を家族のもとへ帰す手段は、もうなかったのです。
参照キャラ: なし（月明かりの登山者）
シーン: 夜の屋外で岩壁を見上げる男性

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s mountaineering clothing. Standing alone outside at night, looking up at cliff. Moonlit profile. Resigned determined expression. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing resolve mixed with sorrow. Moonlight blue tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Night view of Tsuitate-iwa rock face under moonlight. Two small shadows visible on cliff midway. Moonlit mountain landscape. No people at ground visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面左下に配置（横顔）
- 0s〜5s: 登山者の横顔から岩壁にゆっくりフォーカス移動
- 5秒

#### ASSET-076 [キャラアニメーション] [Generic group] 台本L549-552
ナレーション: 最も辛い決断を迫られたのはHさん、Nさんの家族でした。
参照キャラ: なし（遺族の夫婦）
シーン: 書類の前に座る中年夫婦

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Middle-aged Japanese couple in their 50s. Father in dark suit, mother in traditional Japanese clothing (kimono). Sitting at low table. Mother pressing hand to eyes, crying quietly. Father sitting rigidly beside her. Grief-stricken expressions. Documents on table. Full body, front view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing deep grief. Dark somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dim traditional Japanese room (washitsu). Low table (chabudai) with documents. Heavy oppressive atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 夫婦をちゃぶ台に配置
- 0s〜5s: 手元の書類から夫婦の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-077 [Lovart静止画] 台本L556-558
ナレーション: 銃弾がロープではなく、体に命中するかもしれない。
シーン: 銃弾の軌道図解
```
Dark background diagram. Silhouette of person hanging from rope on cliff. Bullet trajectory lines drawn: one hitting rope (green), one missing (red). Risk visualization. Dark moody infographic. Photorealistic dark background. Documentary diagram style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「ザイルに命中」「外れた場合...」）。ゆっくりズームイン（5秒）

#### ASSET-078 [キャラアニメーション] [Generic group] 台本L562-564
ナレーション: ロープに当たり切断できても、300メートルの岩壁をゴロゴロと落下することになる。
参照キャラ: なし（遺族の父親）
シーン: 拳を握りしめる父親

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Middle-aged Japanese man in his 50s, dark suit. Sitting at low table, staring at documents, clenching fists tightly. Jaw clenched, trembling with emotion. Full body, close-up of upper body and fists. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing anguish. Dark somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Traditional Japanese room. Low table. Dark dim lighting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 父親を画面中央に配置
- 0s〜5s: 握りしめた拳にゆっくりズームイン（1.0→1.2）
- キャラに微小な震え（±2px、0.3秒周期）
- 5秒

#### ASSET-079 [キャラアニメーション] [Generic group] 台本L570-572
ナレーション: それでもHさん、Nさんのご家族は同意しました。
参照キャラ: なし（うなずく夫婦）
シーン: 覚悟を決めてうなずく夫婦

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Middle-aged Japanese couple in their 50s. Father slowly nodding. Mother holding back tears, also nodding. Resolved determined expressions through grief. Documents and seal stamp on table. Full body, front view sitting at low table. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing painful resolve. Dark somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Traditional Japanese room. Low table with documents and red seal stamp. Dim lighting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 夫婦をちゃぶ台に配置
- 0s〜5s: うなずく2人の表情にゆっくりズームイン（1.0→1.15）
- うなずき動き（-5px→0px、1秒）
- 5秒

#### ASSET-080 [Lovart静止画] 台本L578-581
ナレーション: 「このまま、あの壁に置き去りにはできない」 その一心で、承諾したのです。
シーン: 押印された書類のクローズアップ
```
Close-up of stamped official document on low Japanese table. Red seal stamp (inkan) impressed on paper. Seal stamp placed beside document. Showa-era Japanese room atmosphere. Dim warm lighting. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: 印鑑から書類にゆっくりズームアウト（5秒で1.15→1.0）

---

### 承（7. 自衛隊出動要請）

#### ASSET-081 [Google Earth] 台本L589-591
ナレーション: 蝸牛山岳会の代表者3名が、群馬県沼田警察署を訪れました。
座標: 36°39'08"N 139°04'00"E → 36°50'14"N 138°55'47"E
カメラ: 沼田警察署の位置を表示。谷川岳との距離感がわかる広域表示。2地点を結ぶラインを入れる
→ 編集者指示: テキスト追加（「沼田警察署」「谷川岳」の2地点名）

#### ASSET-082 [キャラアニメーション] [Generic group] 台本L595-597
ナレーション: 手には、山岳会代表と家族代表の連名で書かれた、一通の要請書。
参照キャラ: なし（山岳会代表3名）
シーン: 警察署の廊下を歩く3人

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Three Japanese men in their 30s-40s, mountaineering clothing. Walking down hallway with tense expressions. Lead man holding envelope with both hands reverently. Full body, front view walking. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing tension. Muted institutional tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Japanese police station hallway. Linoleum floor. Fluorescent lights. Institutional atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人を画面中央に配置（廊下を歩く）
- 0s〜5s: 封筒を持つ手元にゆっくりズームイン（1.0→1.15）
- キャラに微小な上下動（±2px、0.5秒周期）で歩行
- 5秒

#### ASSET-083 [Lovart静止画] 台本L601-603
ナレーション: 「自衛隊出動要請書」
シーン: 公文書のクローズアップ
```
1960s Japanese official document close-up. Bold title text area at center. Multiple signature blocks at bottom with red seal stamps. Aged official paper texture. Formal government document aesthetic. Photorealistic vintage document style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-084 [キャラアニメーション] [Generic group] 台本L607-609
ナレーション: 宛先は、沼田警察署長。
参照キャラ: なし（署長と代表者たち）
シーン: 署長が書類を受け取る瞬間

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese police chief in his 50s, wearing glasses, formal police uniform. Receiving document from three mountaineers across desk. Stern serious expression. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Dark institutional tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Japanese police station reception room. Leather sofa. Clock and photos on wall. Formal institutional atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 署長と3人をデスク越しに配置
- 0s〜5s: 書類を受け取る手元にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-085 [キャラアニメーション] [Generic group] 台本L615-618
ナレーション: 日本の登山史上、前例のない作戦が、動き出しました。
参照キャラ: なし（警察署を出る3人）
シーン: 警察署の玄関を出る3人

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Three Japanese men in their 30s-40s, mountaineering clothing. Walking out through police station entrance. Tense determined expressions. Rear view walking away. Full body, rear view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Muted institutional tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Exterior of 1960s Japanese police station. Sign reading "Numata Police Station" area. Police car parked. Showa-era architecture. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人を画面中央に配置（後ろ姿）
- 0s〜5s: 3人の後ろ姿にゆっくりズームアウト（1.1→1.0）
- キャラに微小な上下動（±2px、0.5秒周期）で歩行
- 5秒

---

### 承（8. 銃器12丁、弾薬2,000発）

#### ASSET-086 [Google Earth] 台本L626-628
ナレーション: 要請を受けた陸上自衛隊は、相馬原駐屯地から、第1偵察中隊の狙撃班を派遣しました。
座標: 36°26'05"N 138°57'11"E → 36°50'50"N 138°56'32"E
カメラ: 相馬原駐屯地から谷川岳一ノ倉沢へルートを描く。距離約45km
→ 編集者指示: テキスト追加（「相馬原駐屯地」「約45km」「谷川岳」）

#### ASSET-087 [キャラアニメーション] [Generic group] 台本L637-640
ナレーション: 投入された装備は、軽機関銃、2丁。ライフル銃、5丁。カービン銃、5丁。合計12丁。
参照キャラ: なし（自衛隊員）
シーン: 銃器を並べる自衛隊員

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese JGSDF soldier in his 30s, 1960s olive drab uniform. Carefully placing military rifles in a row. Disciplined focused expression. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background with 1960s military firearms arranged in neat row: two light machine guns, five rifles, five carbines. Ammunition boxes stacked beside them. Cold metallic military atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 隊員を画面右に配置
- 0s〜5s: 左から右にゆっくりパン（5秒）で銃器を映す
- 5秒
→ 編集者指示: テキスト追加（「軽機関銃x2 / ライフル銃x5 / カービン銃x5 / 合計12丁」）

#### ASSET-088 [キャラアニメーション] [Generic group] 台本L644-646
ナレーション: そして弾薬、2,000発。
参照キャラ: なし（自衛隊員2人）
シーン: 弾薬箱を運ぶ自衛隊員

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese JGSDF soldiers in their 30s, 1960s olive drab uniform. Carrying heavy wooden ammunition box together. Straining with weight. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing effort. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Military truck bed. Wooden crates stacked. 1960s military transport. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人をトラック荷台に配置
- 0s〜5s: 弾薬箱にゆっくりズームイン（1.0→1.15）
- 5秒
→ 編集者指示: テキスト追加（「弾薬 2,000発」）

#### ASSET-089 [キャラアニメーション] [Generic group] 台本L650-652
ナレーション: 標高1,500メートルの山岳地帯に持ち込まれた、戦場のような装備。
参照キャラ: なし（自衛隊員5人）
シーン: 山道を登る自衛隊員の隊列

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Five Japanese JGSDF soldiers in 1960s olive drab uniforms, marching in line up mountain trail. Rifles on shoulders, ammunition boxes on backs. Disciplined stride. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Autumn mountain trail. Fall foliage. Tanigawadake ridgeline visible in distance. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 5人の隊列を画面中央に配置
- 0s〜5s: ゆっくり横にパン（5秒）
- キャラに微小な上下動（±2px、0.5秒周期）で行軍
- 5秒

#### ASSET-090 [Lovart静止画] 台本L656-658
ナレーション: ターゲットは、直径わずか1センチのナイロン製ザイル。
シーン: ナイロンザイルの断面クローズアップ
```
Extreme close-up cross-section of nylon climbing rope, diameter 1cm. Fine nylon fibers visible in cross-section. Scale reference coin beside it. Dark dramatic macro lighting. Photorealistic macro photography. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.2）。テキスト追加（「直径わずか1cm」）

#### ASSET-091 [キャラアニメーション] [Generic group] 台本L664-666
ナレーション: 同日、石川三郎医師による確認も実施。双眼鏡越しではあるものの、HさんとNさんがすでに帰らぬ人であることが、正式に確認されました。
参照キャラ: なし（石川医師）
シーン: 双眼鏡を覗く医師

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Elderly Japanese doctor in his 60s, wearing white coat over dark overcoat. Looking through binoculars with stern expression. Nodding slowly with grave confirmation. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing solemnity. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley approach. Tsuitate-iwa rock wall in background. Overcast sky. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 医師を画面中央に配置
- 0s〜5s: 双眼鏡を下ろす医師の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-092 [キャラアニメーション] [CHAR-05 reference | 初出] [Generic group] 台本L672-676
ナレーション: 自衛隊の部隊が、谷川岳の玄関口である土合駅前の広場に集結。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 土合駅前に整列する自衛隊員たち

**キャラプロンプト（CHAR-05 + Generic group）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 初出] [Generic group] Japanese JGSDF soldiers, five visible, standing in formation. Lead soldier (CHAR-05) at attention with rifle on shoulder. 1960s olive drab uniforms, helmets. Disciplined formation. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing focus. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Doai station plaza at sunset. Military trucks parked. Local Japanese civilians watching from distance. Dramatic sunset sky. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 隊員たちを画面中央に配置
- 0s〜5s: 広場全体からゆっくり隊員たちにズームイン（1.1→1.0→1.05）
- 5秒

#### ASSET-093 [Lovart静止画] 台本L680-682
ナレーション: 翌日の作戦に備え、待機を開始しました。
シーン: 夕暮れの土合駅前広場
```
Sunset view of 1960s Doai station plaza. Military trucks lined up. Soldiers in formation in distance. Orange-tinted sky. Tense calm-before-storm atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。広場全体が見える構図に

---

### 承（9. 射撃作戦 — 1,300発の銃弾）

#### ASSET-094 [Lovart静止画] 台本L690-692
ナレーション: 午前3時。一ノ倉沢の全域を封鎖。
シーン: 暗闘のバリケード
```
Pre-dawn darkness. Makeshift barricade with "No Entry" sign (space for Japanese text). Police flashlight beams cutting through darkness. Ominous atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.1）

#### ASSET-095 [キャラアニメーション] [CHAR-05 reference | 再利用] [Generic group] 台本L698-700
ナレーション: 午前4時半、部隊が出発。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 暗闇の中を出発する隊員たち

**キャラプロンプト（CHAR-05 + Generic group）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] [Generic group] Five Japanese JGSDF soldiers marching in darkness. Only headlamp lights visible on faces. Rifles shouldered, silent disciplined march. 1960s uniforms. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes glowing in lamp light. Dark night tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark mountain trail at night. Stars visible. Tree silhouettes. Only faint headlamp glow. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 隊員たちを画面中央に配置
- 0s〜5s: ヘッドライトの光にゆっくりズームイン（1.0→1.1）
- キャラに微小な上下動（±2px、0.5秒周期）で行軍
- 5秒

#### ASSET-096 [Lovart動画] 台本L704-706
ナレーション: 暗闇の山道を、重い銃器と弾薬を背負って登っていきます。
シーン: 暗闇の行軍
```
Dark mountain trail. Silhouettes of soldiers marching with rifles and ammunition. Only headlamp lights visible in pitch darkness. Dawn beginning to break on eastern horizon. Dramatic documentary atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Silhouettes of soldiers marching up dark mountain path. Headlamp beams bouncing. Dawn light slowly appearing on horizon behind mountains. Steady rhythmic march. Camera slowly following from behind. 5 seconds.
```

#### ASSET-097 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L710-712
ナレーション: そして午前8時半。射撃地点に到着。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 射撃地点を確認する狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Setting down rifle, surveying surroundings. Looking up at cliff face. Assessing shooting position. 1960s uniform, helmet. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing assessment. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa valley opening. Morning light. Tsuitate-iwa rock face towering directly ahead. Shooting position area. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面下部に配置
- 0s〜5s: 狙撃手の視線の先（衝立岩）にゆっくりフォーカス移動
- 5秒

#### ASSET-098 [キャラアニメーション] [Generic group] 台本L716-718
ナレーション: 現場には、自衛隊員47名、警察官40名、地元山岳会員約30名。
参照キャラ: なし（大群衆）
シーン: 各グループに分かれた群衆

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Large group of Japanese men in three distinct clusters: soldiers in olive uniforms, police in dark uniforms, climbers in mountaineering gear. Standing in organized groups. Morning light. Full body, wide view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Mixed military/civilian tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Wide open area at Ichinokurasawa valley approach. Morning light. Mountain setting. Large gathering space. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 群衆を3グループに分けて配置
- 0s〜5s: 左から右にゆっくりパン（5秒）で各グループを映す
- 5秒

#### ASSET-099 [キャラアニメーション] [Generic group] 台本L722-724
ナレーション: さらに家族や関係者200名、報道関係者100名以上。
参照キャラ: なし（報道陣と家族）
シーン: カメラを構える報道陣と家族

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Mixed group of Japanese people: suited journalists with cameras, women in traditional kimono (family members). All looking upward. Cameras on tripods, reporters taking notes. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing tension. Mixed formal tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting point vicinity. Journalists with 1960s cameras and tripods. Mountain backdrop. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 群衆を画面全体に配置
- 0s〜5s: 群衆の横顔にゆっくりズームイン（1.0→1.1）
- 5秒

#### ASSET-100 [Google Earth] 台本L728-730
ナレーション: 合わせて400人を超える人々が、衝立岩を見上げていました。
座標: 36°50'50"N 138°56'32"E → 36°50'44"N 138°56'20"E
カメラ: 射撃地点（一ノ倉沢出合付近）から衝立岩を見上げる角度。射撃距離約140mの距離感を強調
→ 編集者指示: テキスト追加（「射撃距離 約140m」）

#### ASSET-101 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L734-736
ナレーション: 隊員たちが銃を構え、見上げた先。射撃距離、約140メートル。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: ライフルを構えてスコープを覗く狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Aiming rifle upward, looking through scope. Concentrated intense expression. 1960s uniform, helmet. Full body, side view aiming. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing intense focus. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Rock face filling upper portion of frame. Narrow sky above. Tense atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置（射撃姿勢）
- 0s〜5s: スコープ部分にゆっくりズームイン（1.0→1.2）
- 5秒

#### ASSET-102 [Lovart静止画] 台本L740-742
ナレーション: 狙うべきは、岩壁の途中で風に揺れる、直径1センチのナイロンのザイル。
シーン: 射撃地点から見た衝立岩とザイル
```
View looking up at Tsuitate-iwa rock face from shooting position. Single thin red rope visible hanging on cliff midway. Extremely small target against massive rock. Dramatic perspective showing impossible difficulty. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「ターゲット: 直径1cm」）。赤いザイルにゆっくりズームイン（5秒）

#### ASSET-103 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L746-748
ナレーション: しかもそのザイルは、風を受けて絶えず回転している状況。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 照準が定まらない狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Looking through rifle scope, making micro-adjustments tracking a moving target. Concentrated frustrated expression, scope hand trembling slightly. 1960s uniform. Full body, side view aiming. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing frustration. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Scope view (circular vignette). Rope visible on cliff face, swaying and rotating in wind. Cross-hairs trying to track. Blurred rock background. No people visible. Photorealistic scope view. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面左に配置
- 0s〜5s: スコープ視界風のエフェクトでゆっくりズームイン（1.0→1.15）
- キャラに微小な銃口の動き（±3px）で追従表現
- 5秒

#### ASSET-104 [Lovart静止画] 台本L752-755
ナレーション: 前代未聞の作戦が、まもなく始まろうとしていました。
シーン: 射撃地点の全景（緊迫の瞬間）
```
Wide shot of shooting position. Soldiers with rifles in foreground, their backs to camera. Massive Tsuitate-iwa rock face in background. 400+ people gathered behind. Tense atmosphere before action. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。全体の緊迫感が伝わるように

#### ASSET-105 [Lovart動画] 台本L761-763
ナレーション: 射撃、開始。
シーン: 発砲の瞬間
```
Japanese JGSDF soldier firing rifle upward at cliff face. Muzzle flash visible. Shell casing ejecting. Smoke rising. Mountain valley backdrop. 1960s military uniform. Dramatic moment of first shot. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Soldier fires rifle upward. Muzzle flash. Shell casing flying out. Gunshot echoing through valley. Smoke drifting. Camera pulls back from shooter to reveal cliff face above. 5 seconds.
```

#### ASSET-106 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L769-771
ナレーション: 続いて、ライフル銃。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: ライフルを撃つ狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Firing rifle upward, slight recoil. Immediately chambering next round. 1960s uniform. Full body, side view shooting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing focus. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Gun smoke drifting. Tsuitate-iwa rock face in background. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: 発砲の瞬間にゆっくりズームイン（1.0→1.1）
- キャラに微小な反動（±4px、0.2秒周期）で射撃振動
- 5秒

#### ASSET-107 [Lovart静止画] 台本L775-778
ナレーション: 銃声が、一ノ倉沢の岩壁に響きます。
シーン: 谷間の閉塞感
```
Ichinokurasawa valley panorama showing rock walls enclosing narrow space. Sound reverberating atmosphere implied by enclosed rocky canyon. Dramatic echo-suggesting composition. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。谷間の閉塞感を強調

#### ASSET-108 [キャラアニメーション] [Generic group] 台本L782-784
ナレーション: 10発。50発。100発。
参照キャラ: なし（射撃する自衛隊員3人）
シーン: 次々と発砲する自衛隊員たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Three Japanese JGSDF soldiers, each with different firearm, firing simultaneously. Shell casings scattered on ground. Concentrated expressions. 1960s uniforms. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing intense focus. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Gun smoke. Tsuitate-iwa rock wall in background. Shell casings on ground. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人を画面中央に配置
- 0s〜5s: 地面に増えていく薬莢にゆっくりズームイン（1.0→1.1）
- キャラに微小な反動（±3px）
- 5秒
→ 編集者指示: テキスト追加（「10発...50発...100発...」）

#### ASSET-109 [キャラアニメーション] [Generic group] 台本L788-790
ナレーション: 弾丸は次々と発射されるが、直径わずか1センチのナイロンザイルは、風に揺れて回転し、なかなか命中しません。
参照キャラ: なし（ザイルの図解モデル）
シーン: 風に揺れるザイルと弾丸の図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Close-up diagram-style illustration of nylon rope swaying in wind. Bullet trajectory lines passing close but missing. Rope rotating. Impact marks on rock beside rope. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Dark analytical tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background. Tsuitate-iwa cliff diagram on left side. Bullet trajectory arrows and rock impact marks. Analytical documentary style. No people visible. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- ザイルモデルを画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.15）
- ザイルに左右揺れ（±5px、1秒周期）で風の回転
- 5秒
→ 編集者指示: テキスト追加（「直径1cm」「風で回転」「命中せず」）

#### ASSET-110 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L796-798
ナレーション: それを銃弾で正確に撃ち抜くことは腕のいい狙撃手でも難しいことでした。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 唇を噛む狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Pulling away from rifle scope momentarily, biting lip in frustration. Then returning to scope with renewed focus. 1960s uniform. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing frustration turning to determination. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Smoke drifting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: 狙撃手の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-111 [Lovart静止画] 台本L802-804
ナレーション: 1時間が経過。弾数は、すでに500発を超えていました。
シーン: 大量の薬莢が散乱する地面
```
Ground covered with hundreds of spent brass shell casings. Open ammunition boxes, some empty. 1960s military setting. Devastating quantity visible. Photorealistic macro, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: 薬莢の山にゆっくりズームイン（5秒で1.0→1.15）。テキスト追加（「1時間経過 500発以上消費」）

#### ASSET-112 [キャラアニメーション] [Generic group] 台本L810-812
ナレーション: そこで、軽機関銃が投入されることに。
参照キャラ: なし（自衛隊員2人）
シーン: 軽機関銃を設置する隊員

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese JGSDF soldiers setting up light machine gun on tripod mount on rock surface. Loading ammunition belt. Serious focused expressions. 1960s uniforms. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing focus. Military olive-green tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Rocky shooting position. Light machine gun on tripod on rock. Tsuitate-iwa cliff in background. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央に配置
- 0s〜5s: 軽機関銃の設置にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-113 [Lovart動画] 台本L816-818
ナレーション: 連射の轟音が、谷間を埋め尽くす。
シーン: 軽機関銃の連射
```
Light machine gun firing rapid bursts. Shell casings flying. Thick gun smoke. Mountain valley backdrop. Deafening barrage suggested by scene composition. Rock face visible through smoke. 1960s military equipment. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Light machine gun firing rapid continuous bursts. Shell casings ejecting rapidly. Gun smoke billowing. Camera shakes slightly with recoil. Looking up at cliff through smoke, rope still hanging uncut. 5 seconds.
```

#### ASSET-114 [キャラアニメーション] [Generic group] 台本L824-826
ナレーション: 2時間で、消費した弾薬は1,000発以上。それでも、ザイルは切れませんでした。
参照キャラ: なし（ザイルの図解モデル）
シーン: 弾痕だらけだが切れていないザイル

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Close-up diagram of nylon climbing rope with multiple bullet marks and damage, but still intact and connected. Frayed fibers visible. Swaying in wind. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Analytical documentary tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa cliff face midway up, telephoto lens perspective. Rope visible with damage. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- ザイルモデルを画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.15）
- ザイルに微小な揺れ（±3px、1.5秒周期）
- 5秒
→ 編集者指示: テキスト追加（「2時間 1,000発以上 切断できず」）

#### ASSET-115 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L830-833
ナレーション: 午前11時15分。射撃は、一時中断。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 銃を下ろし疲労の表情の狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Lowering rifle, wiping sweat from forehead. Exhausted frustrated expression. Looking at fellow soldier. Shell casings scattered at feet. 1960s uniform. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing exhaustion and frustration. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Shell casings scattered on ground. Gun smoke drifting. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: 地面の薬莢から隊員の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-116 [キャラアニメーション] [Generic group] 台本L839-841
ナレーション: 所持していた2,000発の弾薬のうち、すでに半分以上を消費。しかし、いまだに切ることができない状況。
参照キャラ: なし（弾薬確認する隊員）
シーン: 弾薬箱の残りを確認する隊員

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese JGSDF soldier in his 30s, 1960s uniform. Opening ammunition box and checking remaining rounds. Worried anxious expression. Empty boxes beside him. Full body, three-quarter view kneeling. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing worry. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Empty and half-full ammunition boxes. More than half empty. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 隊員を画面中央に配置
- 0s〜5s: 弾薬箱からゆっくりズームアウト（1.15→1.0）
- 5秒
→ 編集者指示: テキスト追加（「消費: 1,000発以上 / 残: 約1,000発」）

#### ASSET-117 [キャラアニメーション] [Generic group] 台本L845-847
ナレーション: 400人の視線が集まる現場に、焦りと絶望が広がり始めていました。
参照キャラ: なし（不安な群衆）
シーン: 岩壁を見上げる不安そうな群衆

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Group of Japanese people: soldiers, climbers, families looking up anxiously. Some whispering, some standing with arms crossed in silence. Mixed uniforms and civilian clothing. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing anxiety. Mixed muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting point area. 400-person crowd. Tsuitate-iwa cliff in background. Tense atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 群衆を画面全体に配置
- 0s〜5s: 群衆の表情をゆっくり横にパン（5秒）
- 5秒

#### ASSET-118 [キャラアニメーション] [Generic group] 台本L851-853
ナレーション: 見守る家族の表情は、もはや正視できるものではなかったと言います。
参照キャラ: なし（泣く母親と支える父親）
シーン: 目を覆う遺族の女性

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Middle-aged Japanese woman in her 50s, traditional clothing, covering eyes with hand, crying. Japanese man beside her placing hand on her shoulder consolingly. Grief-stricken. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing deep grief. Dark somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Area slightly away from shooting position. Other family members and officials standing around. Somber atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 女性と男性を画面中央に配置
- 0s〜5s: 女性の横顔にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-119 [キャラアニメーション] [Generic group] 台本L857-859
ナレーション: 仲間の遺体に向けて銃弾が放たれている。それだけでも耐えがたい光景なのに、その銃弾すら届きません。
参照キャラ: なし（涙をこらえる山岳会メンバー）
シーン: 涙をこらえながら岩壁を見上げる登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, mountaineering clothing. Holding back tears, looking up at cliff. Jaw clenched, eyes glistening. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing restrained tears. Dark muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa full view. Bullet impact marks scattered on cliff. Rope still uncut. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面左下に配置
- 0s〜5s: 登山者の表情から岩壁にゆっくりフォーカス移動
- 5秒

---

### 承（10. 作戦転換 — 岩に接する部分を狙え）

#### ASSET-120 [キャラアニメーション] [Generic group] 台本L867-869
ナレーション: これまでは、空中に垂れているザイルの「宙に浮いた部分」を狙っていました。
参照キャラ: なし（ザイル図解）
シーン: 空中ザイルを狙撃する失敗の図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Diagram illustration: rope hanging in mid-air from cliff, swaying in wind. Bullet trajectory line passing close but missing. Arrow showing wind direction causing rotation. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Analytical dark tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background with Tsuitate-iwa cliff diagram on left half. Bullet trajectory arrows. Analytical documentary infographic style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 図解を画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- ザイルに揺れ（±5px、1秒周期）
- 5秒
→ 編集者指示: テキスト追加（「失敗: 空中のザイルを狙撃→風で揺れて命中せず」）

#### ASSET-121 [キャラアニメーション] [Generic group] 台本L875-877
ナレーション: 当たっても弾の力が逃げてしまい、切断には至りません。
参照キャラ: なし（指揮官）
シーン: 地面に図を描いて説明する指揮官

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese JGSDF commander in his 40s, 1960s uniform. Kneeling, drawing diagram on ground with stick. Explaining to subordinates gathered around. Urgent authoritative expression. Full body, three-quarter view kneeling. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing authority. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Soldiers gathered in circle. Emergency tactical meeting. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 指揮官を画面中央に配置
- 0s〜5s: 地面の図にゆっくりズームイン（1.0→1.2）
- 5秒

#### ASSET-122 [キャラアニメーション] [Generic group] 台本L883-885
ナレーション: であれば、ザイルが「岩に接している部分」を狙えばどうか。岩に固定された箇所なら、風の影響を受けません。
参照キャラ: なし（ザイル図解 - 新戦術）
シーン: 岩との接点を狙う新戦術の図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Diagram illustration: rope pressed against rock surface at contact point. Bullet trajectory line hitting rope at rock contact. Impact force transmitted through rock and rope. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Analytical bright tones with green highlight. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background with Tsuitate-iwa cliff diagram on right half. New bullet trajectory arrows aimed at rock-rope contact point. Analytical documentary infographic style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 図解を画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- 5秒
→ 編集者指示: テキスト追加（「変更: 岩との接点を狙撃→固定されているため力が伝わる」）

#### ASSET-123 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L889-892
ナレーション: 弾丸の力が、逃げずにザイルに伝わります。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 新しい照準位置を確認する狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Looking through rifle scope, adjusting aim to new target point. Determined resolute expression. 1960s uniform. Full body, side view aiming. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing renewed determination. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Rifle aimed upward. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: スコープ部分にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-124 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L896-898
ナレーション: 午後12時51分。戦術を変更し、射撃を再開。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 再び銃を構え照準を合わせる狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Carefully aiming rifle, finger on trigger. Extreme concentration, holding breath. 1960s uniform. Full body, close side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing razor-sharp focus. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Tense atmosphere. Surrounding soldiers holding breath. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: トリガーにかかる指にゆっくりズームイン（1.0→1.2）
- 5秒

#### ASSET-125 [キャラアニメーション] [Generic group] 台本L904-906
ナレーション: 岩肌にめり込む弾丸が、今度はザイルの繊維を確実に削り始める。
参照キャラ: なし（ザイル切断進行の図解）
シーン: 繊維がほつれていくザイル

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Extreme close-up diagram of nylon rope at rock contact point. Bullet impact marks on rope and rock. Rope fibers fraying, unraveling one by one. Progressive damage visible. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Analytical tones with red damage highlights. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Cliff face close-up, telephoto perspective. Bullet marks embedded in rock. Rope at contact point. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- ザイル図解を画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.2）
- 5秒
→ 編集者指示: テキスト追加（「繊維がほつれ始める」）

#### ASSET-126 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L912-914
ナレーション: そして、38発目。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 集中して連続発砲する狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Firing rifle in rapid succession, sweat on forehead. Nodding slightly after each hit. Counting shots. 1960s uniform. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing intense concentration. Military tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Smoke. Tension. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: 発砲のリズムに合わせてゆっくりズームイン（1.0→1.1）
- キャラに微小な反動（±3px、0.3秒周期）
- 5秒
→ 編集者指示: テキスト追加（「10発...20発...30発...38発目」）

#### ASSET-127 [Lovart動画] 台本L920-922
ナレーション: Nさんを吊り下げていたザイルが、ついに断ち切れたのです。
シーン: ザイルが切れる瞬間（スローモーション）
```
Extreme close-up of nylon rope at rock contact point. Final bullet impact. Remaining fibers snapping one by one. Rope separating in slow motion. Cut end fraying. Dramatic decisive moment. Photorealistic macro, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Close-up of rope being struck by bullet at rock surface. Final fibers stretching and snapping. Rope separating in slow motion. Two halves falling apart. Dramatic slow-motion decisive moment. 5 seconds.
```

#### ASSET-128 [Lovart静止画] 台本L928-930
ナレーション: Nさんの姿が、岩壁を滑り落ちていきます。100メートル以上の落下。
シーン: 落下ラインを示す衝立岩
```
Tsuitate-iwa rock face. Fall trajectory line drawn from midway point down to snow field at base. Massive cliff showing 100+ meter drop distance. No human figures shown. Dark somber atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「100m以上の落下」のライン）。上から下にゆっくり動かす（5秒）

#### ASSET-129 [Google Earth] 台本L934-937
ナレーション: 岩肌に体を何度もぶつかりながら、下の雪渓へと消えていきました。
座標: 36°50'44"N 138°56'20"E
カメラ: 衝立岩の3D地形。宙吊り位置から岩壁の基部までの落下ルートを見せる。雪渓の位置を示す
→ 編集者指示: テキスト追加（「落下ルート」「雪渓」）

#### ASSET-130 [キャラアニメーション] [Generic group] 台本L941-943
ナレーション: その光景を見つめていた400人の中から、目を背ける者。涙をこらえきれない者も。
参照キャラ: なし（様々な反応の群衆）
シーン: それぞれ異なる反応の群衆

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Group of Japanese people showing different emotional reactions: one turning away, one wiping tears, one staring blankly at sky. Mixed clothing: climbers, police, families. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing various grief. Somber autumn tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Autumn afternoon light. Silence after gunfire. Still atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 群衆を画面全体に配置
- 0s〜5s: 群衆の中をゆっくり横にパン（5秒）。各人の表情を映す
- 5秒

#### ASSET-131 [キャラアニメーション] [Generic group] 台本L950-952
ナレーション: 仲間を帰すために、こうするしかなかった。誰もが、それを分かっていました。
参照キャラ: なし（天を仰ぐ山岳会メンバー）
シーン: 目を閉じて天を仰ぐ登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, mountaineering clothing. Biting lip, eyes closed, head tilted back toward sky. Enduring grief with dignity. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closed). Somber autumn tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Tsuitate-iwa in background. Autumn afternoon. Quiet solemn atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面中央に配置
- 0s〜5s: 表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-132 [キャラアニメーション] [Generic group] 台本L958-960
ナレーション: Hさんを繋いでいたザイルも、同じく切断されました。
参照キャラ: なし（ザイル切断位置の図解）
シーン: 2本のザイル切断位置を示す衝立岩図解

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Diagram illustration of Tsuitate-iwa rock face showing two rope cut points marked with red circles. Upper cut and lower cut positions. Cliff profile view. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Analytical documentary tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa full cliff face. Two marked positions where ropes were cut. No people visible. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 図解を画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- 5秒
→ 編集者指示: テキスト追加（「午後1時27分 2本目切断」）

#### ASSET-133 [キャラアニメーション] [CHAR-05 reference | 再利用] 台本L966-968
ナレーション: 作戦終了。
参照キャラ: CHAR-05（自衛隊狙撃手）
シーン: 銃を下ろし深く息をつく狙撃手

**キャラプロンプト（CHAR-05）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-05 reference | 再利用] Japanese JGSDF soldier, late 20s. Lowering rifle, closing eyes, taking deep breath. Complex expression of relief, exhaustion, and solemnity. Shell casings covering ground at feet. 1960s uniform. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes (closing). Military tones mixed with somber mood. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Shooting position. Massive shell casing coverage on ground. Drifting smoke. Silence. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 狙撃手を画面中央に配置
- 0s〜5s: 狙撃手の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-134 [Lovart静止画] 台本L972-975
ナレーション: 消費された弾薬は合計約1,300発にも及びました。
シーン: 作戦の時系列記録
```
Dark background with timeline design. Space for chronological text entries. Solemn documentary infographic aesthetic. Dark moody atmosphere. Photorealistic dark background. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「午前9:15 射撃開始」「午後1:02 1本目切断」「午後1:27 2本目切断」「消費弾薬: 約1,300発」）。1行ずつ順番に表示

---

### 承（11. 帰還 — 7日目）

#### ASSET-135 [キャラアニメーション] [Generic group] 台本L981-984
ナレーション: その後、蝸牛山岳会の仲間たちが雪渓を降り、2人のなきがらを回収。
参照キャラ: なし（担架を運ぶ登山者たち）
シーン: 担架を運ぶ仲間たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Four Japanese male hikers in their 20s-40s, 1960s mountaineering gear. Carefully carrying stretcher. Heavy slow steps. Downcast grief-stricken expressions. Full body, side view walking. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing deep sorrow. Soft somber tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Snow field (yukikei) in mountain valley. Autumn afternoon. Tsuitate-iwa visible in distance. Soft diffused light. Solemn quiet atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 4人を画面中央に配置（担架を運ぶ）
- 0s〜5s: 担架を運ぶ一行をゆっくりズームアウト（1.1→1.0）。雪渓の広さを見せる
- キャラに微小な上下動（±2px、0.8秒周期）で歩行
- 5秒

#### ASSET-136 [キャラアニメーション] [Generic group] 台本L990-992
ナレーション: HさんとNさんは、ようやく家族のもとへ帰ることができたのです。
参照キャラ: なし（泣く家族）
シーン: 涙の再会

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Middle-aged Japanese couple in their 50s. Mother covering face, crying. Father beside her with eyes downcast. Stretcher visible behind them. Autumn light. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing grief. Warm somber autumn tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Mountain trailhead descent area. Autumn sunset. Climbers and officials in background. Solemn atmosphere. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 家族を画面中央に配置
- 0s〜5s: 家族の姿にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-137 [Lovart静止画] 台本L996-999
ナレーション: 入山から数えて、ちょうど7日目のことでした。
シーン: 秋の夕暮れの一ノ倉沢出合
```
Autumn sunset at Ichinokurasawa valley approach. Climbers descending in far distance. Tsuitate-iwa lit by golden sunset light. Peaceful yet solemn atmosphere. Silence. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームアウト（5秒で1.1→1.0）。衝立岩の全景が広がっていく。テキスト追加（「入山から7日目」）

---

### 転結

#### ASSET-138 [キャラアニメーション] [Generic group] 台本L1009-1011
ナレーション: この前代未聞の作戦は、当時のニュース映画として記録され、全国の映画館で本編の上映前に放映されました。
参照キャラ: なし（映画館の観客）
シーン: 昭和の映画館の内部

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese audience in 1960s movie theater, mix of ages 20s-50s, traditional and Western clothing. Sitting in dark theater, faces lit by screen light. Stunned shocked expressions. Full body, three-quarter view sitting. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes wide with shock. Dark theater tones with screen glow. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Japanese movie theater interior. Movie screen showing black-and-white newsreel footage. Dark auditorium seats. Screen glow. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 観客を客席に配置
- 0s〜5s: スクリーンから客席にゆっくりズームアウト（1.15→1.0）
- 5秒

#### ASSET-139 [Lovart静止画] 台本L1015-1017
ナレーション: 日本中がこの事件を目の当たりにし、
シーン: 昭和の新聞紙面
```
1960s Japanese newspaper front pages stacked. Bold headline about Tanigawadake Tsuitate-iwa shooting operation. Black-and-white photo area. Multiple newspapers overlapping. Aged yellowed paper. Photorealistic vintage newspaper style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）。見出しにフォーカス

#### ASSET-140 [Google Earth] 台本L1021-1023
ナレーション: 谷川岳は「魔の山」と呼ばれるようになり、衝立岩は恐怖の象徴となったのです。
座標: 36°50'14"N 138°55'47"E
カメラ: 谷川岳全景。上空から衝立岩に向かってゆっくり近づいていく。険しい岩壁が徐々にクローズアップ
→ 編集者指示: テキスト追加（「魔の山 谷川岳」）

#### ASSET-141 [Lovart静止画] 台本L1029-1032
ナレーション: この事件から6年後の1966年。
シーン: 不穏なトーンの「1966年」
```
Dark ominous background with subtle Tsuitate-iwa rock silhouette. Space for large year text. Foreboding atmosphere. Dark deep tones. Photorealistic dark background. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.1）

#### ASSET-142 [キャラアニメーション] [Generic group] 台本L1038-1040
ナレーション: 同じ谷川岳で、再び宙吊りの事故が発生。20代の若い登山者2人が、またしても岩壁の途中で帰らぬ人となりました。
参照キャラ: なし（宙吊りシルエット）
シーン: 繰り返される悲劇の構図

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two small human silhouettes hanging from rope on cliff midway. Same composition as 1960 incident. Eerie repetition. Full body, distant view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Dark ghostly desaturated tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Tsuitate-iwa rock face in fog. 1966 autumn. Same cliff, same tragedy. Eerie atmospheric similarity. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人のシルエットを岩壁中腹に小さく配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）。不安感を強調
- 5秒

#### ASSET-143 [Lovart静止画] 台本L1044-1046
ナレーション: あの悲劇が、繰り返された。
シーン: 霧に包まれた衝立岩
```
Tsuitate-iwa rock face shrouded in thick fog. Same cliff where tragedy repeats. Dark ominous atmosphere. Haunting. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.1）

#### ASSET-144 [キャラアニメーション] [Generic group] 台本L1052-1054
ナレーション: この「2度目の宙吊り」により、根本的に制度を見直す動きが始まります。1967年、「群馬県谷川岳遭難防止条例」が施行。
参照キャラ: なし（年表図解モデル）
シーン: 因果関係を結ぶ年表

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Timeline diagram model with three event nodes connected by arrows showing cause and effect. Each node has a date marker. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Clean analytical design. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background for timeline infographic. Clean documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 年表モデルを画面中央に配置
- 0s〜5s: 年表を左から右にゆっくりパン
- 5秒
→ 編集者指示: テキスト追加（「1960年 宙吊り事件」→「1966年 2度目の宙吊り」→「1967年 遭難防止条例施行」）。1つずつ順番に表示

#### ASSET-145 [キャラアニメーション] [Generic group] 台本L1058-1060
ナレーション: 一ノ倉沢を含む危険地区への立ち入りには、
参照キャラ: なし（警察官と登山者）
シーン: 登山計画書を確認する場面

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese police officer in his 40s, 1960s uniform, standing at checkpoint. Checking papers from young Japanese hiker in mountaineering gear. Formal interaction. Full body, side view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Official institutional tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Entrance to Ichinokurasawa restricted zone. "Danger Area" sign. 1960s mountain landscape. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 警察官と登山者を画面中央に配置
- 0s〜5s: 2人のやりとりにゆっくりズームイン（1.0→1.1）
- 5秒

#### ASSET-146 [Lovart静止画] 台本L1064-1067
ナレーション: 登山計画書の事前提出と、警察の指導を受けることが義務付けられたのです。
シーン: 登山計画書のクローズアップ
```
Close-up of 1960s Japanese climbing registration form. Showa-era official document with multiple entry fields. Pen placed beside form. Photorealistic vintage document style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-147 [キャラアニメーション] [Generic group] 台本L1071-1073
ナレーション: 行政が「山に登る自由」に法的な制限をかけた、日本初の条例です。
参照キャラ: なし（県議会の職員）
シーン: 議場で条例案を読み上げる職員

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese government official in his 40s, dark suit. Standing at podium reading from document in legislative chamber. Seated council members in background. Formal serious atmosphere. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Formal institutional tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Japanese prefectural assembly chamber. Wooden podium. Seated council members. Formal government setting. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 職員を画面中央に配置
- 0s〜5s: 職員の手元の書類にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-148 [Lovart静止画] 台本L1079-1081
ナレーション: 「個人の趣味に、なぜ行政が口を出すのか」 当時、批判の声もありました。
シーン: 昭和の新聞社説
```
1960s Japanese newspaper editorial page. "Debate over climbing regulations" headline area. Multiple opinion columns with vertical Japanese text. Aged yellowed paper texture. Photorealistic vintage newspaper style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.1）

#### ASSET-149 [キャラアニメーション] [Generic group] 台本L1085-1087
ナレーション: 登山は自由意志で行うもの。危険を承知で挑むのが登山であり、それを法律で規制するのは過剰ではないか、と。
参照キャラ: なし（不満な若い登山者）
シーン: 看板の前で腕を組む登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 20s, 1960s mountaineering gear. Standing with arms crossed, dissatisfied annoyed expression. Looking at sign. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing displeasure. Muted outdoor tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Entrance to Ichinokurasawa zone. "Mandatory climbing registration" sign. 1960s mountain landscape. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面中央に配置
- 0s〜5s: 登山者の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-150 [Lovart静止画] 台本L1091-1093
ナレーション: しかし条例施行後、谷川岳の遭難による犠牲者は明確に減少しています。
シーン: 遭難者数推移の棒グラフ
```
Dark background with bar graph design showing accident statistics decline. Two distinct periods with clear decrease after regulation. Space for text and numbers. Clean documentary infographic style. Photorealistic dark background. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「条例施行前」「条例施行後」の棒グラフ。矢印で「減少」）。ゆっくりズームイン（5秒）

#### ASSET-151 [キャラアニメーション] [Generic group] 台本L1097-1099
ナレーション: 2度の宙吊り事故。4人の若い命。それだけの代償を払って、ようやくたどり着いた答えでした。
参照キャラ: なし（現代の登山者）
シーン: 現代の登山届提出所

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Modern Japanese hiker in his 30s, latest mountaineering gear. Writing on climbing registration form at desk. Focused responsible expression. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Bright modern tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Modern Ichinokurasawa entrance. Climbing registration building. Peaceful autumn day. Maintained trail. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面中央に配置
- 0s〜5s: 登山届を記入する手元にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-152 [キャラアニメーション] [Generic group] 台本L1107-1109
ナレーション: そしてもうひとつ、この事件がきっかけで変わったものがあります。それは登山装備です。
参照キャラ: なし（1960年代と現代の装備比較）
シーン: 装備の比較構図

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Two Japanese men in their 30s standing side by side. Left: 1960s climbing gear with belly-wrap rope around waist. Right: modern climbing gear with proper harness. Comparison pose. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Split vintage/modern tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background split design for comparison. Left half darker vintage, right half brighter modern. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面左右に配置
- 0s〜5s: ゆっくり左から右にパン（5秒）
- 5秒

#### ASSET-153 [キャラアニメーション] [Generic group] 台本L1113-1115
ナレーション: 2人の命を奪った「腹巻き式」のザイルは、この事件を境に急速に消えていきました。
参照キャラ: なし（腹巻きザイルの登山者、フェードアウト）
シーン: フェードアウトする腹巻き式

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, 1960s climbing gear, with rope wrapped around waist (belly-wrap). Standing pose, becoming faded/transparent. Disappearing into past. Full body, front view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Faded desaturated vintage tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark grey background for transition. Historical fade-out atmosphere. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置
- 0s〜5s: ゆっくりフェードアウト（透明度100%→30%）
- 5秒

#### ASSET-154 [Lovart静止画] 台本L1119-1121
ナレーション: 代わりに普及したのが、現在のハーネス。
シーン: 現代のクライミングハーネス
```
Close-up of modern climbing harness. Colorful nylon webbing, metal buckles. Waist and leg loop design clearly visible. Bright clean product-style photography. Latest safety equipment. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: ゆっくりズームイン（5秒で1.0→1.15）

#### ASSET-155 [キャラアニメーション] [Generic group] 台本L1125-1127
ナレーション: 腰と太ももの2点で体重を分散する構造により、万が一宙吊りになっても、すぐに命が奪われることはありません。
参照キャラ: なし（ハーネス装着の登山者）
シーン: ハーネスの荷重分散テスト

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Japanese man in his 30s, modern climbing gear, wearing harness. Hanging safely in harness for suspension test. Weight distributed at waist and thigh points. Arrows showing force distribution. Safe comfortable expression. Full body, front view suspended. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing calm. Bright modern tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Indoor climbing gym. Safe controlled environment. Modern equipment. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- キャラを画面中央に配置（ハーネスで安全に吊り下がり）
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- 5秒
→ 編集者指示: テキスト追加（「腰」「太もも」「荷重分散」の矢印）

#### ASSET-156 [キャラアニメーション] [Generic group] 台本L1131-1133
ナレーション: HさんとNさん、そしてその後の若い登山者2人の尊い犠牲が、日本の登山の安全を変えたのです。
参照キャラ: なし（現代の笑顔の登山者）
シーン: 現代の谷川岳を歩く登山者たち

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Three modern Japanese hikers in their 20s-30s, latest mountaineering gear with proper harnesses. Smiling, walking happily. Full body, three-quarter view walking. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing joy. Bright warm autumn tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Modern Tanigawadake mountain trail. Beautiful autumn foliage. Peaceful sunny day. Gentle mountain scenery. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 3人を画面中央に配置
- 0s〜5s: 登山者たちからゆっくりズームアウト（1.1→1.0）。山の全景が広がっていく
- キャラに微小な上下動（±2px、0.5秒周期）で歩行
- 5秒

#### ASSET-157 [Google Earth] 台本L1141-1143
ナレーション: 谷川岳。標高わずか1,977メートル。富士山の半分にも届きません。
座標: 36°50'14"N 138°55'47"E
カメラ: 谷川岳全景。上空からゆっくり近づいていく。秋の紅葉に包まれた穏やかな山容。低さが際立つアングル
→ 編集者指示: テキスト追加（「標高1,977m」）

#### ASSET-158 [Lovart静止画] 台本L1149-1152
ナレーション: 遭難者数、世界一。
シーン: 「遭難者数 世界一」のビジュアル
```
Dark dramatic background with subtle Tanigawadake mountain silhouette. Space for large impactful text. Heavy solemn atmosphere. Dark cinematic tones. Photorealistic dark background. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「遭難者数 世界一」）。ゆっくりズームイン（5秒）

#### ASSET-159 [キャラアニメーション] [Generic group] 台本L1156-1158
ナレーション: 1931年から数えて、800人以上がこの山で命を落としている。
参照キャラ: なし（データビジュアライゼーション）
シーン: カウントアップ演出

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] 3D silhouette model of Tanigawadake mountain with numerical counter overlay design. Data visualization aesthetic. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Dark analytical tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background for data visualization. Mountain silhouette backdrop. Documentary infographic style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 山のシルエットを画面中央に配置
- 0s〜5s: カウントアップ演出
- 5秒
→ 編集者指示: テキスト追加（「1931年〜 800人以上」）。カウントアップ演出

#### ASSET-160 [キャラアニメーション] [Generic group] 台本L1162-1164
ナレーション: エベレストを含むヒマラヤの8,000メートル峰14座、その全ての犠牲者を足し合わせても、637人。
参照キャラ: なし（棒グラフモデル）
シーン: 対比棒グラフ

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Bar graph model with two bars growing upward. Taller bar exceeding shorter bar dramatically. Data comparison visualization. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Dark analytical tones with red highlight. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background for data comparison infographic. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 棒グラフモデルを画面中央に配置
- 0s〜5s: ゆっくりズームイン（1.0→1.1）
- 5秒
→ 編集者指示: テキスト追加（「谷川岳 800人以上」vs「8,000m峰14座 合計637人」の棒グラフ）

#### ASSET-161 [キャラアニメーション] [Generic group] 台本L1168-1170
ナレーション: つまり谷川岳は、世界最高峰のエベレストより、はるかに多くの命を奪ってきた山なのです。
参照キャラ: なし（高さ比較モデル）
シーン: 谷川岳とエベレストの高さ比較

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Height comparison model: small mountain silhouette (Tanigawadake 1,977m) next to towering mountain silhouette (Everest 8,849m). Dramatic size difference but inverted danger. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors. Dark analytical tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Dark background for height comparison infographic. Documentary data visualization style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 比較モデルを画面中央に配置
- 0s〜5s: ゆっくりズームアウト（1.1→1.0）
- 5秒
→ 編集者指示: テキスト追加（「谷川岳 1,977m」「エベレスト 8,849m」「しかし犠牲者は...」）

#### ASSET-162 [Google Earth] 台本L1176-1178
ナレーション: 1931年に上越線の清水トンネルが開通し、東京から日帰りできるようになった。
座標: 35°42'48"N 139°46'36"E → 36°49'53"N 138°58'03"E
カメラ: 上野駅から土合駅へラインで結ぶ。上越線のルートを辿る
→ 編集者指示: テキスト追加（「東京(上野駅)→ 土合駅 日帰り可能」）

#### ASSET-163 [キャラアニメーション] [Generic group] 台本L1182-1184
ナレーション: 週末になれば、経験の浅い若い登山者たちが大量に押し寄せた。
参照キャラ: なし（昭和の登山者たち）
シーン: 土合駅に降り立つ大量の登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Large group of young Japanese hikers in their 20s, 1960s mountaineering gear, large rucksacks. Stepping off train onto platform, smiling excited. Crowded energetic scene. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing excitement. Vintage warm tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
1960s Doai station platform. Wooden station building. Crowded with hikers pouring off train. Showa-era atmosphere. No people visible. Photorealistic vintage style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 大量の登山者を画面全体に配置
- 0s〜5s: ゆっくり横にパン（5秒）で大量の登山者を映す
- 5秒

#### ASSET-164 [Lovart静止画] 台本L1190-1192
ナレーション: その油断が、エベレストを超える犠牲者を生んだのです。
シーン: 美しさと危険の対比
```
Beautiful peaceful Tanigawadake in autumn. Gorgeous red and orange foliage. Serene mountain landscape. Deceptively gentle appearance hiding deadly danger. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「この程度の山なら...」→「800人以上の犠牲」）。ゆっくりズームアウト（5秒）

#### ASSET-165 [Lovart動画] 台本L1196-1198
ナレーション: 低い山ほど人を油断させ、油断した人間ほど山に足をすくわれる。
シーン: 朝靄の衝立岩が姿を現す
```
Morning mist at Ichinokurasawa valley. Tsuitate-iwa rock wall slowly emerging from fog. Beautiful yet terrifying. Soft autumn light illuminating massive cliff. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Thick morning fog slowly clearing to reveal massive dark Tsuitate-iwa rock face. Beautiful and terrifying simultaneously. Soft autumn light. Camera slowly pulling back as cliff emerges. 5 seconds.
```

#### ASSET-166 [Lovart静止画] 台本L1202-1204
ナレーション: もし、HさんとNさんが、現代のハーネスを装着していたら。
シーン: 腹巻きとハーネスの左右分割比較
```
Split composition: left side shows 1960s belly-wrap rope, right side shows modern climbing harness. Dark dramatic lighting. Question posed visually. Photorealistic comparison style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: テキスト追加（「もし...」）。ゆっくりズームイン（5秒）

#### ASSET-167 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L1208-1210
ナレーション: もし天候が悪化した時点で、撤退を選んでいたら。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 引き返す2人の後ろ姿（if の世界）

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers walking away from mountain, heading back down trail. Rucksacks on backs. Retreating safely. Rain beginning. Full body, rear view walking away. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. Soft muted tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Ichinokurasawa mountain trail. Rain starting to fall. Retreat path. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央に配置（後ろ姿、引き返す）
- 0s〜5s: 2人の後ろ姿にゆっくりズームアウト（1.1→1.0）
- キャラに微小な上下動（±2px、0.5秒周期）で歩行
- 5秒

#### ASSET-168 [キャラアニメーション] [Generic group] 台本L1216-1218
ナレーション: 山岳遭難の悲劇を振り返るたびに、教訓はいつも同じ言葉に行き着きます。
参照キャラ: なし（現代の登山者）
シーン: 衝立岩を見上げる現代の登山者

**キャラプロンプト（Generic group）** — Lovart 1:1で生成（背景透過用）
```
[Generic group] Modern Japanese hiker in his 30s, latest gear. Standing alone on trail, looking up at Tsuitate-iwa with expression of respect and contemplation. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing quiet respect. Warm autumn tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Modern Tanigawadake Ichinokurasawa trail. Peaceful autumn day. Fall colors. Tsuitate-iwa towering in silence. No people visible. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 登山者を画面下部に配置
- 0s〜5s: 登山者からゆっくりズームアウト（1.1→1.0）。全景が広がっていく
- 5秒

#### ASSET-169 [キャラアニメーション] [CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] 台本L1222-1224
ナレーション: 1960年、Hさん、Nさんは、あの岩壁で亡くなってしまった。
参照キャラ: CHAR-01（Hさん）、CHAR-02（Nさん）
シーン: 入山前の笑顔の2人（回想）

**キャラプロンプト（CHAR-01 + CHAR-02）** — Lovart 1:1で生成（背景透過用）
```
[CHAR-01 reference | 再利用] [CHAR-02 reference | 再利用] Two Japanese young male climbers smiling with hope. Rucksacks on backs, looking up at rock wall ahead. Eager youthful faces full of ambition. 1960s mountaineering gear. Full body, three-quarter view. White background. Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes showing hope and excitement. Warm nostalgic tones. No text, no words, no letters. 1:1 aspect ratio. Generate 5 images.
```

**背景プロンプト** — Lovart 16:9で生成（フォトリアル）
```
Autumn Ichinokurasawa approach. Morning light. Tsuitate-iwa towering ahead. Beautiful yet fateful morning. No people visible. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```

**制作手順**: Lovartでキャラ(1:1)→背景透過書き出し→Lovartで背景(16:9)→CapCutで配置→下記メモに沿って動かす

**動かし方メモ（CapCut編集指示）:**
- 2人を画面中央に配置（笑顔で岩壁を見上げる）
- 0s〜5s: 2人の表情にゆっくりズームイン（1.0→1.15）
- 5秒

#### ASSET-170 [Lovart静止画] 台本L1228-1230
ナレーション: そして2人を家族のもとへ帰すために、1,300発の銃弾が必要だった。
シーン: 薬莢と衝立岩の遠景
```
Scattered spent brass shell casings covering ground in foreground. Tsuitate-iwa rock face visible in far background. Symbolic composition connecting the operation to the mountain. Somber atmospheric light. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ 編集者指示: 薬莢から衝立岩にゆっくりフォーカス移動（5秒）

#### ASSET-171 [Lovart動画] 台本L1234-1236
ナレーション: この事実だけは、どうか忘れないでいてください。
シーン: 夕暮れの衝立岩（エンディング）
```
Tsuitate-iwa rock face at sunset. Cliff lit by red-golden sunset light. Camera slowly pulling back to reveal wider Ichinokurasawa valley, then full Tanigawadake mountain view. Final fade to black. Majestic, somber, memorial atmosphere. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 5 images.
```
→ **Google Flow動画プロンプト:**
```
Sunset light on massive rock face gradually turning golden-red. Camera slowly, continuously pulling back: rock face detail → full cliff → valley → mountain panorama. Final slow fade to black. Solemn memorial atmosphere. Wind sound fading. 5 seconds.
```

#### ASSET-172 [Google Earth] — 追加分（台本L675に含まれるGE指示）
ナレーション: （ASSET-092と同一タイミング）土合駅位置の補助表示
座標: 36°49'53"N 138°58'03"E
カメラ: 土合駅の位置を表示。自衛隊集結地点

> **注記**: 台本L675の【Google Earth】はASSET-092のキャラアニメーションと同じ【制作メモ】ブロック内に記載されており、ASSET-092の背景として土合駅のGoogle Earth映像を組み合わせて使用する。単独のGE素材としても使用可能。

---

## Google Earth 座標・カメラ設定まとめ

| 素材ID | 座標 | カメラ指示 |
|--------|------|-----------|
| ASSET-001 | 36°50'14"N 138°55'47"E | 宇宙空間→日本列島→群馬県/新潟県県境→谷川岳へズームイン |
| ASSET-007 | 36°50'44"N 138°56'20"E | 衝立岩を下から見上げる。垂直さが際立つ |
| ASSET-010 | 36°50'50"N→36°50'44"N | 一ノ倉沢出合から衝立岩を正面に見据える |
| ASSET-029 | 36°50'44"N 138°56'20"E | 衝立岩の3D断面図。200m地点マーク |
| ASSET-036 | 36°50'44"N 138°56'20"E | 岩壁基部から見上げ。宙吊り位置の垂直距離強調 |
| ASSET-042 | 36°50'44"N 138°56'20"E | 基部から宙吊り地点ルート。オーバーハング |
| ASSET-046 | 36°50'14"N 138°55'47"E | 広域表示。日本海/太平洋分水嶺 |
| ASSET-055 | 36°50'44"N 138°56'20"E | 横からの3D。オーバーハング。正面ルート不可 |
| ASSET-056 | 36°50'44"N 138°56'20"E | 迂回ルートを矢印で表示 |
| ASSET-069 | 36°50'44"N 138°56'20"E | 夕暮れの3D地形。垂直さとスケール感 |
| ASSET-081 | 36°39'08"N→36°50'14"N | 沼田警察署と谷川岳の距離感。2地点ライン |
| ASSET-086 | 36°26'05"N→36°50'50"N | 相馬原駐屯地→谷川岳。距離約45km |
| ASSET-100 | 36°50'50"N→36°50'44"N | 射撃地点から衝立岩。距離約140m |
| ASSET-129 | 36°50'44"N 138°56'20"E | 宙吊り位置から基部への落下ルート。雪渓表示 |
| ASSET-140 | 36°50'14"N 138°55'47"E | 谷川岳全景→衝立岩へズームイン |
| ASSET-157 | 36°50'14"N 138°55'47"E | 谷川岳全景。紅葉。低さが際立つ |
| ASSET-162 | 35°42'48"N→36°49'53"N | 上野駅→土合駅。上越線ルート |
| ASSET-172 | 36°49'53"N 138°58'03"E | 土合駅位置表示 |

---

## 素材カテゴリ別サマリー

| カテゴリ | 件数 | 自分の作業 | 編集者の作業 |
|----------|------|-----------|------------|
| Lovart生成（静止画） | 27枚 | コピペ→選ぶ | 動き指示に従いズーム/パン追加 |
| Lovart生成（動画→Flow） | 14本 | コピペ→選ぶ→Google Flow | なし |
| キャラアニメーション（一貫性生成） | 101箇所 | キャラ(1:1)+背景(16:9)コピペ→選ぶ | CapCutでキーフレームアニメーション |
| Lovart＋編集者（図解系） | 12件 | コピペ→選ぶ | テキスト追加 |
| Google Earth | 18箇所 | なし | 座標見て録画+テキスト追加 |
| **合計** | **172件** | **Lovart 154回** | **図解12件 + GE18箇所** |
| **動画/アニメ比率** | **77%** | **目標: 50%以上 ✅** | — |

> ⚠️ **5秒ルール確認**: 全体平均 ナレーション文字数/ASSET ≒ 35文字（目標: 35文字以下 ✅）。キャラアニメーション101件（59%）が動的素材のベースとなり、AI動画14本と合わせて動的素材133/172 = 77%で基準50%以上を大きく達成。

> **注記**: 静止画27枚中12枚はLovart＋編集者（テキスト追加が必要な図解系）を含む。全静止画に編集者向けの動き指示（ゆっくりズームイン等）を付記済み。
