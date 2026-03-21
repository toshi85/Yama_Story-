# 羅臼岳ヒグマ襲撃事件（2025年8月） 素材プロンプト一括リスト

> Lovartにコピペするだけの流れ作業用。生成順＝台本の登場順。
> **シーン単位グルーピング版**: 1シーン = 場面転換までの連続ナレーション。1アセットで30〜60秒分をカバー。

---

## 0. キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**: キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> Lovartでは1プロンプトにつき5枚同時生成。ベスト1枚を一貫性キャラの参照画像として採用。

### CHAR-01: 曽田圭亮（26歳）— 被害者・登山者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 26-year-old Japanese man, athletic build, short black hair, medium skin tone. Wearing a bright blue hiking jacket, dark gray hiking pants, brown hiking boots, and a green daypack. Cheerful determined expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-02: 友人（20代）— 曽田さんの登山仲間

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A Japanese man in his mid-20s, average build, slightly longer black hair swept to the side, medium skin tone. Wearing an orange hiking jacket, black hiking pants, gray hiking shoes, and a red daypack. Calm steady expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-03: 母グマ「SH」（11歳メス）— 加害個体ヒグマ

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A large female Hokkaido brown bear (Ursus arctos yesoensis), 140cm body length, muscular heavy build weighing 117kg, dark brown fur with lighter brown muzzle area, small rounded ears, powerful shoulders and thick limbs, intense watchful eyes. Standing on all fours. Generate 5 separate images, each showing only this one character.
```

---

## 1. 全素材リスト（台本順）

<!-- PART: KI -->

### 起（イントロ — セクション1: フック）

ナレーター: 2025年夏。

【制作メモ】ASSET-001 [Lovart動画] 台本L11-L13
シーン: 2025年夏の知床半島・羅臼岳の遠景。朝霧に包まれた威圧的な山容。ヒグマが何度も接近した夏の始まり
```
Photorealistic, shot on RED camera. Documentary drama style. Aerial view of Mount Rausu (1,661m) in Shiretoko Peninsula, Hokkaido, Japan, shrouded in morning mist during summer 2025. Dense green forests covering the lower slopes, rocky peaks emerging above clouds. Dramatic golden hour lighting. Ominous atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Slow aerial flyover approaching Mount Rausu through morning mist. Camera slowly pushes forward revealing the mountain peak emerging from clouds. Soft golden light. 5 seconds.
```
→ 編集者指示: ゆっくり山に近づく（5秒）

ナレーター: クマスプレーを浴びてもなお、人間を襲う事実が報告されました。

【制作メモ】ASSET-002 [Lovart動画] 台本L15-L17
シーン: クマスプレーの噴射が空中に広がる様子。登山口の閉鎖されていない看板が続けて映る
```
Photorealistic, shot on RED camera. Documentary drama style. Close-up of a bear spray canister being discharged in a Hokkaido mountain forest setting, bright orange-red capsaicin cloud spreading through the air. The spray can is held by a Japanese male hand. Dense green bamboo grass in the blurred background. Urgent tense mood. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Bear spray canister held by a Japanese male hand fires a burst of bright orange capsaicin cloud spreading rapidly through the air. Dense green bamboo grass in background. Camera holds steady as spray dissipates. 5 seconds.
```

ナレーター: なぜクマは、人間を襲ったのか。

【制作メモ】ASSET-003 [キャラアニメーション] 台本L19-L21
シーン: 母グマが子グマ2頭を背後に、登山道でこちらを睨む。なぜ閉鎖されなかったかの問いかけ
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 初出] Full body. A large female Hokkaido brown bear, 140cm body length, dark brown fur, muscular heavy build, standing on all fours in aggressive posture with two small bear cubs behind her. Fierce protective expression, ears forward. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A narrow hiking trail on Mount Rausu, Hokkaido, Japan, lined with dense bamboo grass (sasa) over 2 meters tall on both sides. Overcast sky, diffused light filtering through clouds. Ominous somber atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 母グマキャラを中央に配置、子グマ2頭を背後に配置。ゆっくりズームイン（4秒）

ナレーター: 地形図とともに解説します。

【制作メモ】ASSET-004 [Google Earth] 台本L23
シーン: 知床半島と羅臼岳の全景を俯瞰
座標: 44°04'30"N, 145°07'30"E（羅臼岳山頂）
カメラ: 高度15kmから知床半島全景を表示。ゆっくり羅臼岳にズームイン（高度15km→3km、10秒）

---

### 起（イントロ — セクション2: 人物と舞台）

ナレーター: 2025年8月14日。

【制作メモ】ASSET-005 [Lovart静止画 + 編集者] 台本L28
シーン: 日付テロップ用の背景。知床の夏の朝の風景
```
Photorealistic, shot on RED camera. Documentary style. Early morning landscape of Shiretoko Peninsula, Hokkaido, Japan in August. Soft dawn light over green forests and distant mountain ridges. Warm summer atmosphere. No people visible. Peaceful calm mood. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 中央に大きく「2025年8月14日」のテロップ追加。ゆっくり右から左に動かす（5秒）

ナレーター: 26歳、会社員の曽田圭亮（そた けいすけ）さんは友人と二人で、羅臼岳へと向かいます。

【制作メモ】ASSET-006 [キャラアニメーション] 台本L30-L34
シーン: 曽田さんと友人が登山口に向かって並んで歩く姿。日本百名山を巡る若き登山家の紹介
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 初出] Full body. A 26-year-old Japanese man in a blue hiking jacket, dark gray hiking pants, brown boots, green daypack, walking forward with excited smile. [CHAR-02 reference | 初出] Full body. A Japanese man in his mid-20s in an orange hiking jacket, black hiking pants, red daypack, walking alongside with a calm smile. Two friends side by side. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Forest road leading to Iwaobetsu trailhead, Shiretoko, Hokkaido, Japan. Summer morning, bright green deciduous trees lining the road. Warm sunlight filtering through leaves. Adventurous optimistic atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 2人のキャラを背景道路の中央に配置。キーフレームで手前から奥に歩かせる（5秒）

ナレーター: 羅臼岳（らうすだけ）は、標高1,661メートル。

【制作メモ】ASSET-007 [Google Earth] 台本L36-L44
シーン: 羅臼岳の地形説明。岩尾別ルートの全景。標高230m→1,661mの高低差
座標: 44°04'30"N, 145°07'30"E（羅臼岳山頂）
カメラ: 高度5kmから岩尾別ルートを俯瞰。登山口から山頂までのルートをなぞるように移動（10秒）

ナレーター: 曽田さんと友人の二人は、まだまだ若いこともあり、そのルートで進むことに。

【制作メモ】ASSET-008 [キャラアニメーション] 台本L46-L48
シーン: 二人が意気揚々と登山道を歩き出す。しかし忘れてはならないことがある、と示唆
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, dark gray pants, green daypack, striding forward with confident expression. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, walking with determined expression. Two friends hiking together. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Lush green hiking trail ascending through mixed forest on Mount Rausu, Shiretoko, Hokkaido, Japan. Morning sunlight filtering through canopy. Fresh summer air feeling. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 2人のキャラを登山道に配置。キーフレームで奥に向かって歩かせる（4秒）

ナレーター: それは、羅臼岳がある知床半島は、2005年にユネスコの世界自然遺産に登録されるほど自然豊かで、

【制作メモ】ASSET-009 [Lovart動画] 台本L50-L52
シーン: 知床半島の豊かな自然。森、海、野生動物が共存する世界遺産の風景
```
Photorealistic, shot on RED camera. Documentary style. Pristine wilderness of Shiretoko Peninsula, Hokkaido, Japan. Dense virgin forests of Sakhalin fir and Yezo spruce, flowing streams, and the Sea of Okhotsk visible in the distance. Rich green summer landscape. UNESCO World Heritage site atmosphere. Majestic untouched nature. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Sweeping aerial view over pristine wilderness of Shiretoko Peninsula, dense virgin forests below, Sea of Okhotsk glimmering in the distance. Camera slowly glides forward over the treetops. 5 seconds.
```

ナレーター: そして、その中にヒグマもいます。

【制作メモ】ASSET-010 [Lovart動画] 台本L54-L56
シーン: 知床の森の中にいるヒグマのシルエット。目撃情報の多さを暗示
```
Photorealistic, shot on RED camera. Documentary style. A wild Hokkaido brown bear standing in a forest clearing in Shiretoko National Park, Hokkaido, Japan. The bear is partially hidden behind dense bamboo grass and trees. Dappled sunlight. Watchful alert atmosphere. Natural wild setting. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A wild Hokkaido brown bear in a forest clearing in Shiretoko, partially hidden behind bamboo grass. The bear slowly turns its head, looking toward the camera. Dappled sunlight shifts through trees. 5 seconds.
```

---

<!-- PART: SHO -->

### 承（本編 — セクション3: 登頂と下山）

ナレーター: 8月14日　早朝。

【制作メモ】ASSET-011 [キャラアニメーション] 台本L63-L69
シーン: 早朝、2人が岩尾別温泉の登山口から出発。天候は晴れ、夜明けの光
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, looking ahead with determined morning energy. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, stretching arms with early morning alertness. Two friends ready to start hiking. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Iwaobetsu hot spring trailhead at the base of Mount Rausu, Shiretoko, Hokkaido, Japan. Early morning before sunrise, sky transitioning from dark blue to pale orange. Wooden trailhead sign visible. Summer vegetation. Quiet anticipatory atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 2人のキャラを登山口に配置。歩き出すアニメーション（4秒）

ナレーター: 東京タワーの大きさが333ｍなので、約4倍以上の高さに匹敵します。

【制作メモ】ASSET-012 [Lovart動画] 台本L71-L73
シーン: 山麓から山頂へのスケール感を動画で表現
```
Photorealistic, shot on RED camera. Documentary style. Side view of Mount Rausu, Hokkaido, Japan, showing the full elevation from forested base at 230 meters to rocky summit at 1,661 meters. Clear summer day, the mountain fills the entire frame. Massive imposing scale. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Slow vertical camera movement starting from the forested base of Mount Rausu at 230 meters, gradually tilting upward to reveal the rocky summit at 1,661 meters against clear blue sky. 5 seconds.
```
→ 編集者指示: 山の横に「230m」「1,661m」「標高差 約1,400m（東京タワー約4倍）」のテキスト追加

ナレーター: しかし2人は若さもあり、順調に歩みを進めていきます。

【制作メモ】ASSET-013 [キャラアニメーション] 台本L75-L85
シーン: 登山の道中。弥三吉水で水を補給し、銀冷水を過ぎ、残雪帯を歩く。順調な登山
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, filling a water bottle with happy expression. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, standing nearby looking at the scenery with a smile. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A mountain stream water point (Yasayoshi-mizu) along the Iwaobetsu trail on Mount Rausu, Shiretoko, Hokkaido, Japan. Clear cool water flowing from rocks. Lush green subalpine vegetation. Summer morning light. Refreshing peaceful atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 2人のキャラを水場に配置。水を汲む動作のアニメーション（5秒）

ナレーター: 2人は慎重に歩みを進め、ついに山頂に到達。

【制作メモ】ASSET-014 [キャラアニメーション] 台本L87-L97
シーン: 山頂到達の喜び。知床半島の全容、オホーツク海と太平洋の絶景を満喫する二人
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, standing with arms raised in triumph, huge joyful smile. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, giving thumbs up with a relieved happy expression. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Summit of Mount Rausu (1,661m), Shiretoko, Hokkaido, Japan. Panoramic view of the Shiretoko Peninsula stretching between the Sea of Okhotsk and the Pacific Ocean. Rocky summit area, clear blue sky, distant ocean visible on both sides. Triumphant majestic atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 2人のキャラを山頂に配置。腕を上げるポーズ。ゆっくりズームアウトして背景の絶景を見せる（5秒）

ナレーター: その後、しばらくして下山を開始。

【制作メモ】ASSET-015 [キャラアニメーション] 台本L99-L101
シーン: 下山開始。ここから事態が変わることを暗示する雰囲気
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, walking downhill with a relaxed but slightly tired expression. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, following behind at a distance. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Descending trail from the upper slopes of Mount Rausu, Shiretoko, Hokkaido, Japan. The trail narrows as it enters denser vegetation. Clouds beginning to gather. Foreshadowing ominous atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんを手前、友人を奥に配置（距離感を出す）。曽田さんが速く歩くアニメーション（4秒）

---

### 承（本編 — セクション4: 遭遇）

ナレーター: 午前11時ごろ。

【制作メモ】ASSET-016 [キャラアニメーション] 台本L106-L112
シーン: 下山中の曽田さん。友人より200m先を走りながら下山している
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, jogging downhill at a fast pace, slightly forward-leaning posture. Energetic but unaware expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Descending trail on Mount Rausu near Okhotsk Observation Point, Shiretoko, Hokkaido, Japan, at approximately 550 meters elevation. Dense bamboo grass (sasa) over 2 meters tall lining both sides. Narrow winding path with poor visibility ahead. Midday overcast light. Tense uneasy atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんキャラを登山道に配置。走るアニメーション。背景を流して速度感を出す（4秒）

ナレーター: 二人はちょうどオホーツク展望台付近、標高550メートル付近にさしかかりました。

【制作メモ】ASSET-017 [Google Earth] 台本L114-L116
シーン: オホーツク展望台付近の地形。見通しの悪いカーブの道
座標: 44°05'50"N, 145°04'50"E（オホーツク展望台付近、標高550m）
カメラ: 高度1kmから現場付近を表示。地形のカーブと笹藪の密生エリアを示す（8秒）

ナレーター: 笹や低い木が登山道の両脇に密生し、3メートル先が見えません。

【制作メモ】ASSET-018 [Lovart動画] 台本L118-L126
シーン: 背丈を超える笹藪の壁に囲まれた登山道。先が見えないカーブ。ヒグマの食事場所
```
Photorealistic, shot on RED camera. Documentary drama style. First-person perspective walking through a narrow hiking trail on Mount Rausu, Shiretoko, Hokkaido, Japan, at 550 meters elevation. Dense bamboo grass (sasa) towering over 2 meters on both sides, creating a tunnel-like corridor. A sharp blind curve ahead. Impossible to see beyond 3 meters. Humid summer air. Suffocating claustrophobic atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
First-person perspective moving forward through a narrow trail tunnel formed by towering bamboo grass over 2 meters tall on Mount Rausu, Hokkaido. Camera slowly advances toward a blind curve. Leaves rustling. Claustrophobic tense feeling. 5 seconds.
```

ナレーター: 曽田さんは走りながら、このカーブを曲がることに。

【制作メモ】ASSET-019 [キャラアニメーション] 台本L128-L132
シーン: 曽田さんがカーブを曲がった瞬間、目の前にヒグマが。最悪の遭遇
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, suddenly frozen mid-stride with wide terrified eyes, mouth open in shock. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. A narrow trail blind curve on Mount Rausu, Shiretoko, Hokkaido, Japan, surrounded by dense bamboo grass over 2 meters tall. Just around the curve, a dark massive shape looms — a large brown bear silhouette barely visible through the vegetation. Harsh midday light. Horrifying sudden confrontation atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんキャラを手前に配置、背景のカーブ先にクマのシルエットが見える構図。曽田さんが急停止するアニメーション（3秒）

ナレーター: よく見ると子グマ2頭を連れた母グマでした。

【制作メモ】ASSET-020 [キャラアニメーション] 台本L134-L138
シーン: 子グマ2頭を連れた母グマとの至近距離での対峙。逃げる間もない
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear standing on all fours, aggressive defensive posture, fur bristled, baring teeth. Two small bear cubs cowering behind her. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Narrow trail on Mount Rausu, Shiretoko, Hokkaido, Japan, hemmed in by dense bamboo grass. A few meters of open space on the trail. Harsh overhead sun creating stark shadows. Deadly confrontation atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 母グマと子グマ2頭を登山道中央に配置。母グマが前に出る動き（3秒）

ナレーター: 子連れの母グマにとって、突然目の前に現れた人間は敵とみなします。自分の子供が襲われると感じるからです。

【制作メモ】ASSET-021 [Lovart動画] 台本L140-L142
シーン: 母グマの襲撃の瞬間。叫び声が響き渡る（直接的な暴力描写は避け、森全体に響く叫び声の余韻で表現）
```
Photorealistic, shot on RED camera. Documentary drama style. Dense bamboo grass forest on Mount Rausu, Shiretoko, Hokkaido, Japan. Birds scattering from treetops in alarm. Violent rustling in the undergrowth. Leaves and branches shaking. Chaotic disturbing atmosphere without showing any violence or injury. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Birds suddenly scatter from treetops in a bamboo grass forest on Mount Rausu, Hokkaido. Branches shake violently in the dense undergrowth below. Chaotic alarming movement. Camera holds steady on the disturbed canopy. 5 seconds.
```

---

### 承（本編 — セクション5: 友人の闘い）

ナレーター: 200メートル後ろにいた友人にもその叫び声は届きました。友人は必死に曽田さんの元へ走ります。

【制作メモ】ASSET-022 [キャラアニメーション] 台本L147-L149
シーン: 友人が叫び声を聞いて全力で駆けつける。現場に到着してヒグマに襲われる曽田さんを目撃
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, red daypack, sprinting forward with panicked desperate expression, arms pumping. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. A hiking trail on Mount Rausu, Shiretoko, Hokkaido, Japan, at 550 meters elevation. Dense bamboo grass on both sides. Midday light. Frantic urgent atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを登山道に配置。全力疾走のアニメーション（4秒）

ナレーター: 咄嗟に友人はクマスプレーを取り出しましたが、なぜか噴射はできませんでした。

【制作メモ】ASSET-023 [キャラアニメーション] 台本L151-L161
シーン: 友人がスプレーを取り出すが噴射できない。スプレーは使用済みで、しかもヒグマ非対応の防犯用だった
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, desperately holding a small spray canister with both hands, pressing the trigger with frustrated panicked expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Narrow trail in dense bamboo grass forest on Mount Rausu, Shiretoko, Hokkaido, Japan. Chaotic scene with trampled vegetation. Harsh midday light. Desperate helpless atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラがスプレーを構えて押す動作。噴射できずに焦るアニメーション（5秒）

ナレーター: ヒグマ専用のクマスプレーは、噴射距離が約9メートル。

【制作メモ】ASSET-024 [Lovart動画] 台本L163-L171
シーン: ヒグマ用スプレーの噴射力を動画で表現
```
Photorealistic, shot on RED camera. Documentary style. Two bear spray canisters side by side on a wooden surface in Hokkaido, Japan. Left: a large professional bear spray canister with safety clip. Right: a small pocket-sized personal defense spray. Clear size difference visible. Neutral informative atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Camera slowly dollies in toward two bear spray canisters on a wooden table. Focus shifts from the small personal defense spray on the right to the large professional bear spray on the left. 5 seconds.
```
→ 編集者指示: 左に「ヒグマ用 噴射距離 約9m」右に「防犯用 噴射距離 2-3m」のテキスト追加

ナレーター: スプレーが使えない。武器はない。道具もない。

【制作メモ】ASSET-025 [キャラアニメーション] 台本L173-L181
シーン: 友人が素手でヒグマに向かっていく。何度も拳を叩きつける壮絶な抵抗
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, fists clenched, lunging forward with fierce determined expression, jaw set. Brave fighting stance. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Trampled trail area in dense bamboo grass on Mount Rausu, Shiretoko, Hokkaido, Japan. Broken vegetation, disturbed earth. Harsh midday sunlight. Violent desperate atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを手前に配置、拳を振りかぶるポーズ。殴る動作のアニメーション（4秒）

ナレーター: しかし、人間の拳がヒグマに通じることはありませんでした。

【制作メモ】ASSET-026 [キャラアニメーション] 台本L183-L191
シーン: ヒグマは友人を無視して曽田さんを襲い続ける。太ももの大量出血の深刻さ（直接描写なし）
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, on his knees with devastated helpless expression, fists bruised, looking down in anguish. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Dense bamboo grass thicket on Mount Rausu, Shiretoko, Hokkaido, Japan. Thick vegetation swaying. Dark shadows between the stalks. Somber devastating atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを手前に配置。膝をつく絶望のアニメーション（4秒）

ナレーター: ヒグマは友人の攻撃を1ミリも気にすることなく、曽田さんをくわえたまま、藪の中へと消えていきました。

【制作メモ】ASSET-027 [Lovart動画] 台本L193-L195
シーン: 藪が揺れながら静まっていく。ヒグマが曽田さんを連れ去った後の静寂。成人男性2人でも歯が立たない現実
```
Photorealistic, shot on RED camera. Documentary drama style. Dense bamboo grass thicket on Mount Rausu, Shiretoko, Hokkaido, Japan. The tall grass sways violently then gradually settles to stillness. A trail of trampled vegetation leading deep into the undergrowth. Eerie quiet after violence. Devastating somber atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Dense bamboo grass on Mount Rausu, Hokkaido, swaying violently then gradually settling into eerie stillness. A visible trail of crushed vegetation leads into the dark thicket. Camera holds steady. 5 seconds.
```

---

### 承（本編 — セクション6: 通報と捜索）

ナレーター: 午前11時10分ごろ。

【制作メモ】ASSET-028 [キャラアニメーション] 台本L200-L204
シーン: 友人が110番通報。「仲間がヒグマに襲われた」と必死に電話する姿
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, holding a smartphone to his ear with trembling hands, tears in eyes, desperate pleading expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Hiking trail near Okhotsk Observation Point on Mount Rausu, Shiretoko, Hokkaido, Japan, at 550 meters elevation. Dense bamboo grass. Midday sun. Lonely isolated atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを登山道の脇に配置。電話する動作、体が震えるアニメーション（5秒）

ナレーター: 通報を受け、北海道警察と消防が出動。

【制作メモ】ASSET-029 [Google Earth] 台本L206-L210
シーン: 現場の標高550mまでの距離感。車が入れない山中。登山口から2時間以上の距離
座標: 44°05'50"N, 145°04'50"E（事件現場付近）
カメラ: 登山口（標高230m）から現場（標高550m）までのルートを表示。距離と険しさを示す（8秒）

ナレーター: さらに大きな問題がありました。

【制作メモ】ASSET-030 [キャラアニメーション] 台本L212-L222
シーン: ヒグマがまだ付近にいるため捜索隊が近づけない。翌日の早朝まで待つ判断。友人は一人で待つ
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, sitting alone on the trail, hugging his knees, looking down with exhausted anguished expression. Alone and helpless. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Hiking trail near Okhotsk Observation Point on Mount Rausu, Shiretoko, Hokkaido, Japan. Late afternoon light fading. Dense vegetation. Empty trail stretching both directions. Lonely despairing atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを登山道脇に座らせる。夕暮れへの光変化。ゆっくりズームアウト（5秒）

ナレーター: また、救助を待つ間、友人はオホーツク展望台付近で、あるものを目撃しています。

【制作メモ】ASSET-031 [キャラアニメーション] 台本L224-L232
シーン: 友人がヒグマが登山道を下っていく姿を目撃。人間を恐れないクマ
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-02 reference | 再利用] Full body. A Japanese man in his mid-20s in orange jacket, black pants, standing rigid with wide shocked fearful eyes, hand covering mouth. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear walking calmly on all fours, completely unfazed, moving away at a leisurely pace. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Descending hiking trail on Mount Rausu near Okhotsk Observation Point, Shiretoko, Hokkaido, Japan. Late afternoon fading light. Dense bamboo grass on both sides. Chilling eerie atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 友人キャラを手前の端に、母グマを奥の登山道上に配置。母グマがゆっくり歩いて遠ざかるアニメーション（5秒）

ナレーター: 事件の連絡を受け、近隣の町と環境省は羅臼岳の登山道と、知床五湖（しれとこごこ）に利用制限をかけることに。

【制作メモ】ASSET-032 [Lovart動画] 台本L234-L238
シーン: お盆シーズンの知床五湖に利用制限。多くの観光客がいた場所の緊急閉鎖
```
Photorealistic, shot on RED camera. Documentary style. Shiretoko Five Lakes (Shiretoko Goko), Hokkaido, Japan, during summer Obon holiday season. Elevated wooden boardwalk over marshland with a lake reflecting mountains. A temporary barrier blocking the entrance. Japanese tourists standing outside looking disappointed. Bright summer afternoon. Uneasy disrupted atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Elevated wooden boardwalk at Shiretoko Five Lakes, Hokkaido, with a temporary barrier blocking the entrance. Japanese tourists in summer clothing standing near the barrier, some looking at phones. Bright afternoon light. Camera slowly sweeps from barrier to the lake beyond. 5 seconds.
```

---

### 承（本編 — セクション7: 翌日の発見）

ナレーター: 翌日、8月15日。早朝から捜索開始。

【制作メモ】ASSET-033 [Lovart動画] 台本L243-L247
シーン: 大規模な捜索隊が山に入る。警察、消防、知床財団、ハンター、警察犬。ハンターが先頭
```
Photorealistic, shot on RED camera. Documentary drama style. A large search party entering the trailhead of Mount Rausu, Iwaobetsu, Shiretoko, Hokkaido, Japan at dawn. Japanese police officers in uniform, firefighters, wildlife foundation staff in outdoor gear, and a hunter carrying a rifle at the front. A police dog on a leash. Early morning golden light. Grim determined atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A large search party of Japanese police, firefighters, a hunter with a rifle at the front, and a police dog moving into the forested trailhead of Mount Rausu, Hokkaido, at dawn. Golden morning light. Camera follows from behind as they enter the forest. 5 seconds.
```

ナレーター: 午後1時ごろ。

【制作メモ】ASSET-034 [キャラアニメーション] 台本L249-L257
シーン: 捜索隊が3頭のクマに遭遇。母グマは捜索隊を見ても逃げず、子グマのそばから離れない
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear standing protectively over two small bear cubs, facing forward with defiant unwavering gaze. Refusing to retreat. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary drama style. Dense bamboo grass clearing near the attack site on Mount Rausu, Shiretoko, Hokkaido, Japan. Trampled vegetation. Afternoon light. Tense standoff atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 母グマと子グマ2頭を中央に配置。母グマが動かずに正面を見据える。ゆっくりズームイン（4秒）

ナレーター: すかさずハンターが母グマを銃撃。

【制作メモ】ASSET-035 [Lovart動画] 台本L259-L263
シーン: ハンターが銃撃。母グマを仕留め、子グマ2頭も駆除される
```
Photorealistic, shot on RED camera. Documentary drama style. A Japanese hunter in outdoor camouflage gear, aiming a rifle in a dense bamboo grass forest on Mount Rausu, Shiretoko, Hokkaido, Japan. Focused intense expression. Afternoon light. A puff of gun smoke in the air. Grave decisive atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A Japanese hunter in camouflage gear with short black hair, weathered face, aiming a rifle forward in a dense bamboo grass forest on Mount Rausu, Hokkaido. He steadies his aim and fires. A puff of smoke rises. Camera holds steady. 5 seconds.
```

ナレーター: 子グマは生後わずか数ヶ月。まだ自力で生きていける段階ではありませんでした。

【制作メモ】ASSET-036 [Lovart動画] 台本L265-L267
シーン: 幼い子グマの儚さ。母グマを失った子グマが生き延びることの困難さ
```
Photorealistic, shot on RED camera. Documentary style. Two very young Hokkaido brown bear cubs, only a few months old, small and vulnerable-looking, huddled together in bamboo grass on Mount Rausu, Shiretoko, Hokkaido, Japan. Soft afternoon light. Heartbreaking somber atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Two very small Hokkaido brown bear cubs huddled together in bamboo grass on Mount Rausu, Hokkaido. Soft afternoon light. Camera slowly zooms in on the vulnerable cubs. Somber mood. 5 seconds.
```

ナレーター: 曽田さんは、母グマのすぐそばで発見されました。

【制作メモ】ASSET-037 [Lovart動画] 台本L269-L275
シーン: 捜索隊が現場で発見。24時間以上経過。全身の複数外傷（直接描写なし、捜索隊の反応で間接表現）
```
Photorealistic, shot on RED camera. Documentary drama style. Japanese search party members standing in a dense bamboo grass clearing on Mount Rausu, Shiretoko, Hokkaido, Japan. Some removing helmets in respect, others looking down with grave expressions. A police officer speaking into a radio. Afternoon light filtering through the canopy. Devastating solemn atmosphere. No injury or remains visible. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Japanese search party members in a bamboo grass clearing on Mount Rausu, Hokkaido. Police officers and rescue workers standing with heads bowed. One officer speaks into a radio. Afternoon light. Camera slowly pulls back. Solemn atmosphere. 5 seconds.
```

ナレーター: 曽田圭亮さん。26歳。

【制作メモ】ASSET-038 [キャラアニメーション] 台本L277-L279
シーン: 曽田さんの追悼。日本百名山を夢見た青年が帰らぬ人に
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, standing with a warm gentle smile, looking slightly upward. Peaceful hopeful expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Summit panorama of Mount Rausu, Shiretoko, Hokkaido, Japan. Golden hour sunset light casting warm glow over the mountain peaks. Clouds below the summit. Beautiful ethereal memorial atmosphere. Slightly desaturated warm tones. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんキャラを山頂の背景に配置。ゆっくりフェードアウト（5秒）。追悼の雰囲気

---

### 承（本編 — セクション8: DNA鑑定）

ナレーター: 後日、北海道立総合研究機構がDNA鑑定を実施。

【制作メモ】ASSET-039 [Lovart静止画 + 編集者] 台本L284-L290
シーン: DNA鑑定の結果。駆除された母グマのDNAと一致し、科学的に確定
```
Photorealistic, shot on RED camera. Documentary style. A modern laboratory interior in Hokkaido, Japan. A microscope, test tubes, DNA analysis equipment on a clean white bench. A printed report document on the desk. Clinical sterile lighting. Forensic scientific atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 画面下部に「DNA鑑定結果：駆除された母グマ＝襲撃個体 — 一致」のテキスト追加。ゆっくり近づく（5秒で1.0→1.15）

---

### 承（本編 — セクション9: 岩尾別の母さん）

ナレーター: このヒグマは、知床財団の個体識別番号「SH」と記録されることに。

【制作メモ】ASSET-040 [Lovart動画] 台本L295-L303
シーン: 母グマ「SH」の個体情報。11歳メス、体長140cm、体重117kg。回想の入口
```
Photorealistic, shot on RED camera. Documentary style. A profile view of a large female Hokkaido brown bear in Shiretoko National Park, Hokkaido, Japan. The bear stands on all fours, muscular 140cm body, dark brown fur, powerful shoulders. Natural forest setting. Factual informative atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A large female Hokkaido brown bear with dark brown fur and muscular 140cm body slowly turns her head toward the camera in a Shiretoko National Park forest. Intense watchful eyes. 5 seconds.
```
→ 編集者指示: 回想シーン開始。色味をやや彩度低く。画面端にビネット効果。テキスト追加：「個体識別番号 SH / 11歳メス / 体長140cm / 体重117kg」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: この母グマには、ある特徴がありました。

【制作メモ】ASSET-041 [キャラアニメーション] 台本L305-L313
シーン: 回想 — 人間を怖がらないクマ。「人を避けない。すぐに逃走しない」と記録されたSH
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear sitting calmly on haunches, completely relaxed despite facing forward. Unfazed unbothered expression. No fear of anything ahead. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A paved road near Iwaobetsu area, Shiretoko, Hokkaido, Japan. A parked car visible at the roadside. Forest and mountains in the background. Slightly desaturated warm tones for flashback mood. Vignette effect on edges. Eerie unsettling atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。色味をやや彩度低く。画面端にビネット効果。母グマキャラを道路中央に配置。車の前で堂々と座るアニメーション（5秒）

ナレーター: 通常、野生のヒグマは人間を避けます。

【制作メモ】ASSET-042 [キャラアニメーション] 台本L315-L325
シーン: 回想 — 通常のクマは逃げるが、SHは違う。車が停まっても、カメラを向けても動じない
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear walking slowly along a road, looking directly at the viewer with calm indifferent expression. Completely unbothered by human presence. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A roadside near Iwaobetsu, Shiretoko, Hokkaido, Japan. Several tourists visible in the distance taking photos from behind car doors. Slightly desaturated warm tones for flashback mood. Vignette edges. Unsettling atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。母グマキャラを道路上に配置。ゆっくり歩くアニメーション、カメラ方向を気にしない（5秒）

ナレーター: 知床財団は、ヒグマを追い返すために、花火やゴムによる威嚇を何度も行ったとのこと。

【制作メモ】ASSET-043 [Lovart動画] 台本L327-L335
シーン: 回想 — 花火やゴム弾で威嚇するも母グマは嫌がる様子すら見せない。追い払っても翌日戻る
```
Photorealistic, shot on RED camera. Documentary drama style. A forest clearing near Iwaobetsu, Shiretoko, Hokkaido, Japan. Wildlife officers in green uniforms launching firework deterrents toward a forested area. Bright flashes and sparks in the air. Slightly desaturated warm tones for flashback mood. Vignette edges. Frustrated futile atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Wildlife officers in green uniforms in a forest clearing near Iwaobetsu, Shiretoko, Hokkaido, launching firework deterrents. Bright flashes and sparks light up the clearing. Slightly desaturated flashback tones. Camera holds steady as sparks fly. 5 seconds.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット

ナレーター: 地元のキャンプ場管理人の西山修次さんは、HTB北海道ニュースの取材にこう語っています。

【制作メモ】ASSET-044 [Lovart動画] 台本L337-L339
シーン: 西山さんの証言テロップ。「とんでもないクマだと、その時話した」
```
Photorealistic, shot on RED camera. Documentary style. A rustic campground manager's office in Shiretoko, Hokkaido, Japan. Wooden desk with papers, a walkie-talkie, and a window showing forest outside. Warm interior lighting. Slightly desaturated for flashback. Vignette edges. Serious concerned atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Interior of a rustic campground office in Shiretoko, Hokkaido. Camera slowly moves across a wooden desk with papers and a walkie-talkie. Warm light from window. Slightly desaturated flashback tones. 5 seconds.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。テロップ追加：「とんでもないクマだと、その時話した — 西山修次さん（キャンプ場管理人）」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: そして、2025年5月頃には、この母グマに子グマ2頭が生まれたことが確認されています。

【制作メモ】ASSET-045 [キャラアニメーション] 台本L341-L349
シーン: 回想 — 子連れになった母グマ。子を守るため攻撃的に。授乳期で常に空腹。目撃情報30件以上
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear walking with two very small cubs following closely behind. Protective alert expression, scanning surroundings. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Spring forest in Shiretoko National Park, Hokkaido, Japan. Fresh green leaves, wildflowers on the forest floor. Soft spring light. Slightly desaturated warm tones for flashback. Vignette edges. Deceptively peaceful atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。母グマと子グマ2頭を森の中に配置。歩くアニメーション（5秒）

ナレーター: 通常、野生のヒグマが人目につく場所に頻繁に出没する場合、専門家の間では「問題個体」として対処が検討されます。

【制作メモ】ASSET-046 [Lovart動画] 台本L351-L361
シーン: 世界自然遺産・国立公園・観光地としての制約。簡単に閉鎖・駆除できない知床の事情
```
Photorealistic, shot on RED camera. Documentary style. UNESCO World Heritage inscription plaque at Shiretoko National Park entrance, Hokkaido, Japan. Stone monument surrounded by green forest. Official serious atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Camera slowly approaches a UNESCO World Heritage stone monument at Shiretoko National Park entrance, Hokkaido, Japan, surrounded by lush green forest. Official somber atmosphere. 5 seconds.
```
→ 編集者指示: テキスト追加：「世界自然遺産 / 国立公園 / 観光地 → 簡単に閉鎖・駆除できない」

---

### 承（本編 — セクション10: 餌付けという火種）

ナレーター: さらに、知床財団によるヒグマの記録を追っていくと、ある事実が浮かび上がります。

【制作メモ】ASSET-047 [キャラアニメーション] 台本L366-L370
シーン: 回想 — 7月29日、観光客が車の窓からヒグマにスナック菓子を投げ与える
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [New character] Full body. A Japanese male tourist in casual summer clothes — polo shirt, shorts, sandals — leaning out of a car window, tossing a snack bag with a careless amused smile. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear approaching from a few meters away, curious interested expression. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A paved road through Iwaobetsu area, Shiretoko, Hokkaido, Japan, in summer. A parked sedan with open window. Forest on both sides. Slightly desaturated warm tones for flashback. Vignette edges. Irresponsible careless atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。観光客キャラを車の窓際に、母グマを道路上に配置。菓子を投げる→クマが近づくアニメーション（5秒）

ナレーター: 知床では、クマへの餌付けは条例で禁止されています。

【制作メモ】ASSET-048 [Lovart静止画 + 編集者] 台本L372-L376
シーン: 餌付け禁止の条例表示。罰則があるのに後を絶たない行為
```
Photorealistic, shot on RED camera. Documentary style. A large warning sign at a parking area in Shiretoko, Hokkaido, Japan, with bear silhouette pictogram. No readable written content on the sign. Forest background. Official stern atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。看板に「ヒグマへの餌付け 条例で禁止 / 罰則あり」のテキスト追加。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: なぜ餌付けが危険なのか。

【制作メモ】ASSET-049 [キャラアニメーション] 台本L378-L390
シーン: 回想 — 餌付けの危険性の説明。一度味を覚えたら消えない。人間に近づく→苛立ち→襲撃の連鎖
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear approaching aggressively, ears flattened, mouth slightly open showing irritation. Frustrated angry expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A road and parking area in Iwaobetsu, Shiretoko, Hokkaido, Japan. Empty parked cars, no snacks offered this time. Slightly desaturated warm tones for flashback. Vignette edges. Dangerous escalating atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。母グマが車に近づく→食べ物がない→苛立つ表情に変化するアニメーション（5秒）

ナレーター: 北米でもオーストラリアでも、野生動物への餌付けが重大事故につながった事例は数多く報告されています。

【制作メモ】ASSET-050 [Lovart動画] 台本L392-L398
シーン: 世界各地で餌付けが事故に発展した事例の象徴的映像。知床でも同じ構図
```
Photorealistic, shot on RED camera. Documentary style. Split composition: foreground shows a tourist's hand offering food toward camera, background shows a large wild bear in Shiretoko National Park, Hokkaido, Japan, approaching. The gap between human and wild animal dangerously small. Warning ominous atmosphere. Slightly desaturated. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A tourist's hand in the foreground slowly extends offering food, while in the background a large Hokkaido brown bear in Shiretoko approaches closer. The dangerous gap narrows. Desaturated tones. Camera holds steady. 5 seconds.
```

ナレーター: 毎日新聞は、この母グマをこう表現しています。

【制作メモ】ASSET-051 [Lovart静止画 + 編集者] 台本L400-L404
シーン: 「観光客に人気のあるヒグマだった」。写真を撮り、菓子を投げ、「かわいい」と声をかけていた
```
Photorealistic, shot on RED camera. Documentary style. Multiple Japanese tourists crowding near a roadside in Shiretoko, Hokkaido, Japan, holding up smartphones and cameras, leaning forward excitedly. Dense forest behind them. Bright summer day. Ironic tragically naive atmosphere. Slightly desaturated flashback tones. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。テロップ追加：「"観光客に人気のあるヒグマだった" — 毎日新聞」。ゆっくり近づく（5秒で1.0→1.15）

---

### 承（本編 — セクション11: 8月10日、最初の接近）

ナレーター: さらに事件発生から4日前の8月10日。

【制作メモ】ASSET-052 [Google Earth] 台本L409-L411
シーン: 回想 — 8月10日の遭遇場所。標高1,040m〜1,120mの区間
座標: 44°05'10"N, 145°06'00"E（標高1,040m付近）
カメラ: 高度2kmから岩尾別ルートの該当区間を表示。登山道上の遭遇ポイントを示す（6秒）

ナレーター: 子グマ2頭を連れた母グマが、登山道の上に姿を表したと報告されています。

【制作メモ】ASSET-053 [キャラアニメーション] 台本L413-L423
シーン: 回想 — 登山道に母子グマ。ガイドがスプレーを構えるが、母グマはすぐに逃げない。異常行動
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-03 reference | 再利用] Full body. A large female Hokkaido brown bear sitting on a trail with two cubs beside her, staring ahead calmly. No fear, no urgency to leave. Defiant calm expression. [New character] Full body. A Japanese mountain guide in his 40s, wearing a green outdoor vest and hiking boots, holding a bear spray canister at the ready with cautious tense expression. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Subalpine hiking trail at 1,040m elevation on Mount Rausu, Shiretoko, Hokkaido, Japan. Low scrubby vegetation, exposed rocky terrain. Slightly desaturated warm tones for flashback. Vignette edges. Tense standoff atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。母グマと子グマを登山道中央に、ガイドを手前端にスプレーを構えて配置。にらみ合いの静止→母グマがゆっくり去るアニメーション（5秒）

ナレーター: この時、居合わせた登山者の中には、恐怖を感じてその日のうちに下山した者もいました。

【制作メモ】ASSET-054 [キャラアニメーション] 台本L425-L431
シーン: 回想 — 恐怖で下山する登山者。しかし登山道は閉鎖されず。もし閉鎖されていれば...
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [Generic group] Full body. Two Japanese hikers in outdoor gear — one male, one female — hurrying down a mountain trail with frightened anxious expressions, looking back over their shoulders. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Descending trail on Mount Rausu, Shiretoko, Hokkaido, Japan. Open registration-free trailhead visible in the distance. Slightly desaturated warm flashback tones. Vignette edges. Foreboding regretful atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。登山者2人が急いで下山するアニメーション（4秒）

---

### 承（本編 — セクション12: 8月12日、5分間の追跡）

ナレーター: 8月12日。事件2日前。

【制作メモ】ASSET-055 [Lovart静止画 + 編集者] 台本L436-L442
シーン: 回想 — 日付と場所の提示。弥三吉水〜銀冷水間、午前8時30分
```
Photorealistic, shot on RED camera. Documentary style. Morning mountain trail between Yasayoshi-mizu and Ginreisui on Mount Rausu, Shiretoko, Hokkaido, Japan. Misty morning light through trees. Slightly desaturated flashback tones. Vignette edges. Ominous foreboding atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。テロップ追加：「8月12日 午前8時30分 — 事件2日前」。ゆっくり右から左に動かす（5秒）

ナレーター: 1人の登山者が、大人のヒグマと至近距離で遭遇。すかさずクマスプレーを噴射。

【制作メモ】ASSET-056 [キャラアニメーション] 台本L444-L448
シーン: 回想 — 登山者がスプレーを噴射。クマは一度離れるが、すぐに戻ってくる
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [New character] Full body. A Japanese male hiker in his 30s wearing a dark green rain jacket, brown hiking pants, gray backpack, holding a bear spray canister forward with determined frightened expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Mountain trail between Yasayoshi-mizu and Ginreisui on Mount Rausu, Shiretoko, Hokkaido, Japan, at approximately 900 meters elevation. Dense mixed forest. Slightly desaturated flashback tones. Vignette edges. Terrifying confrontation atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。登山者キャラがスプレーを噴射するアニメーション→一瞬の安堵→再びクマが迫る恐怖の表情変化（5秒）

ナレーター: クマはスプレーを浴びながら、接近と後退を繰り返し、登山者のあとを5分間、つけまわしたと報告されています。

【制作メモ】ASSET-057 [Lovart動画] 台本L450-L458
シーン: 回想 — 5分間の追跡。100キロ超のヒグマがすぐそこにいる恐怖。時速50km、握力500kg
```
Photorealistic, shot on RED camera. Documentary drama style. A mountain trail on Mount Rausu, Shiretoko, Hokkaido, Japan. First-person perspective of a narrow forest path. A large dark shape of a Hokkaido brown bear visible 10 meters behind, partially obscured by vegetation, following. Slightly desaturated flashback tones. Vignette edges. Primal terror atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
First-person perspective on a narrow forest trail on Mount Rausu, Hokkaido. Camera moves forward urgently while a dark massive bear shape follows 10 meters behind through vegetation. Desaturated flashback tones. Terrifying pursuit atmosphere. 5 seconds.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット

ナレーター: 羅臼町猟友会の桜井憲二さんは、HTB北海道ニュースの取材に

【制作メモ】ASSET-058 [Lovart動画] 台本L460-L464
シーン: 桜井さんの証言テロップ。「スプレー噴射しても付きまとう時点で十分に危険。もっと周知すればよかった」
```
Photorealistic, shot on RED camera. Documentary style. Interior of a local hunting association office in Rausu, Hokkaido, Japan. A wooden desk with hunting permits, maps, and an old rifle case on the wall. Warm interior lighting. Slightly desaturated flashback tones. Regretful somber atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Interior of a hunting association office in Rausu, Hokkaido. Camera slowly moves across a desk with hunting permits and maps. An old rifle case hangs on the wall. Warm desaturated lighting. 5 seconds.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット。テロップ追加：「"スプレーを噴射しても付きまとう時点で十分に危険。もっと周知すればよかった" — 桜井憲二さん（羅臼町猟友会）」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: この情報は、知床財団に正式に報告されています。

【制作メモ】ASSET-059 [Lovart動画] 台本L466-L470
シーン: 回想 — 報告されたのに閉鎖されず、注意喚起の看板が設置されただけ
```
Photorealistic, shot on RED camera. Documentary style. A simple handwritten warning notice pinned to a wooden post at a trailhead on Mount Rausu, Shiretoko, Hokkaido, Japan. The notice is small and easily overlooked. Forest and trail visible behind. Slightly desaturated flashback tones. Vignette edges. Inadequate futile atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Camera slowly pulls back from a small warning notice pinned to a wooden post at a trailhead on Mount Rausu, Hokkaido. The notice becomes smaller and more insignificant as the vast forest trail is revealed. Desaturated tones. 5 seconds.
```
→ 編集者指示: 回想シーン。彩度低め＋ビネット

---

<!-- PART: TEN-KETSU -->

### 転結 — セクション13: なぜ閉鎖されなかったのか

ナレーター: なぜか？

【制作メモ】ASSET-060 [Lovart動画] 台本L475-L481
シーン: 斜里町担当者の証言。「どういう場面でどういう対応をとるか決まっていなかった」
```
Photorealistic, shot on RED camera. Documentary style. A Japanese municipal government office interior in Shari town, Hokkaido, Japan. Cluttered desk with documents, a telephone ringing. Fluorescent office lighting. Bureaucratic overwhelmed atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Interior of a Japanese municipal government office in Shari town, Hokkaido. Camera slowly moves across a cluttered desk with stacked documents and a telephone. Fluorescent lighting. Bureaucratic atmosphere. 5 seconds.
```
→ 編集者指示: テロップ追加：「"どういう場面で、どういう対応をとるか、あらかじめ決まっていなかった" — 斜里町担当者」

ナレーター: クマがスプレーを浴びても人間を追い続ける。この異常事態が報告されても、登山道を閉じるという決まりはありませんでした。

【制作メモ】ASSET-061 [Lovart動画] 台本L483-L491
シーン: 観光ガイド綾野さんの証言。「とりあえず2、3日閉鎖して様子を見る」が判断の仕組みがなかった
```
Photorealistic, shot on RED camera. Documentary style. A nature guide's small office in Shiretoko, Hokkaido, Japan. Maps and hiking trail posters on the wall. Outdoor gear hanging. Warm but worried atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Interior of a nature guide's small office in Shiretoko, Hokkaido. Camera slowly moves past maps and hiking trail posters on the wall. Outdoor gear visible. Warm worried atmosphere. 5 seconds.
```
→ 編集者指示: テロップ追加：「"危ないクマがいたら、とりあえず2、3日閉鎖して様子を見る" — 綾野雄次さん（観光ガイド）/ しかし、その判断の仕組みが存在しなかった」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 知床の登山道は環境省の管轄です。しかし、入山規制の判断は地元自治体に委ねられていました。

【制作メモ】ASSET-062 [Lovart動画] 台本L493-L501
シーン: 複数組織の管轄の複雑さ。環境省・北海道・斜里町・羅臼町・知床財団。誰が閉じるのか決まっていない
```
Photorealistic, shot on RED camera. Documentary style. An empty conference room table in a Japanese government building in Hokkaido, Japan. Multiple nameplates for different organizations visible but no one seated. Overhead fluorescent lighting. Bureaucratic vacuum atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Camera slowly moves along an empty conference room table in a Japanese government building, Hokkaido. Multiple nameplates visible but no one seated. Fluorescent overhead lighting. Empty bureaucratic atmosphere. 5 seconds.
```
→ 編集者指示: テーブルの名札に「環境省 / 北海道 / 斜里町 / 羅臼町 / 知床財団」を追加。中央に「誰が閉じるのか？→ 取り決めなし」のテキスト。ゆっくり近づく（5秒で1.0→1.15）

---

### 転結 — セクション14: 見過ごされた前兆

ナレーター: 7月29日。観光客がヒグマに餌を与える。

【制作メモ】ASSET-063 [Lovart静止画 + 編集者] 台本L506-L514
シーン: エスカレーションのタイムライン。7/29餌付け→8/10登山道出没→8/12スプレー無効→8/14襲撃
```
Photorealistic, shot on RED camera. Documentary style. A dark moody background of Mount Rausu, Shiretoko, Hokkaido, Japan, at dusk. Mountain silhouette against deep orange and purple sky. Ominous escalating atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: タイムライン表示：「7/29 餌付け → 8/10 登山道出没（逃げない）→ 8/12 スプレー無効（5分追跡）→ 8/14 襲撃」の4段階を左から右に追加。ゆっくり右から左に動かす（5秒）

ナレーター: 2週間の間に、段階的にエスカレートしていたのです。

【制作メモ】ASSET-064 [Lovart動画] 台本L514-L516
シーン: お盆の登山者が多い時期に、スプレーが効かないヒグマがいる山が野放し状態
```
Photorealistic, shot on RED camera. Documentary drama style. Busy trailhead at Iwaobetsu, Mount Rausu, Shiretoko, Hokkaido, Japan, during August Obon holiday. Many Japanese hikers in colorful gear happily preparing to climb. A small faded warning notice on a post that nobody is reading. Bright cheerful summer day contrasting with hidden danger. Ironic tragic atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Busy trailhead scene at Iwaobetsu, Mount Rausu, Hokkaido, during Obon. Many Japanese hikers in colorful gear walk past a small faded warning notice that nobody notices. Bright summer day. Camera slowly zooms in on the unread notice. 5 seconds.
```

ナレーター: HTB北海道ニュースは、この状況について、

【制作メモ】ASSET-065 [Lovart静止画 + 編集者] 台本L518-L528
シーン: 情報が届かなかった問題。登山者の証言「クマの出没情報は一切知らなかった」
```
Photorealistic, shot on RED camera. Documentary style. A Japanese hiker looking at a trailhead information board at Iwaobetsu, Mount Rausu, Shiretoko, Hokkaido, Japan. The board has general trail information but the bear warning is a small note in the corner. The hiker does not notice it. Summer morning. Tragic oversight atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: テロップ追加：「"クマの出没情報は一切知らなかった。登山口の張り紙にも気付かなかった" — 登山者の証言」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 知床で人がヒグマに襲われて命を落としたのは、2005年の世界自然遺産登録以来、これが初めてのことでした。

【制作メモ】ASSET-066 [Lovart動画] 台本L530-L532
シーン: 2005年の世界遺産登録以来初の死亡事故。前例がなかったからこそ対処できなかった
```
Photorealistic, shot on RED camera. Documentary style. The official Shiretoko UNESCO World Heritage Site entrance monument in Hokkaido, Japan. Stone marker surrounded by pristine forest. Afternoon light casting long shadows. A single flower offering placed at the base. Somber reflective atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Camera slowly approaches the Shiretoko UNESCO World Heritage monument in Hokkaido surrounded by forest. A single flower offering at its base. Long afternoon shadows. Reflective somber atmosphere. 5 seconds.
```

---

### 転結 — セクション15: 駆除をめぐる批判

ナレーター: 事件の後、全国から斜里町に様々なクレームが殺到。

【制作メモ】ASSET-067 [Lovart動画] 台本L539-L553
シーン: 全国からのクレーム殺到。「なぜ射殺したのか」「子グマまで」。北海道庁160件、斜里町130件
```
Photorealistic, shot on RED camera. Documentary drama style. A Japanese municipal government office in Shari town, Hokkaido, Japan. Multiple desk phones ringing simultaneously. Office workers looking stressed and overwhelmed. Stacks of printed complaint letters on desks. Harsh fluorescent lighting. Chaotic burdened atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A Japanese municipal office in Shari, Hokkaido. Multiple desk phones ring. Office workers in suits look overwhelmed, one holding a phone at arm's length. Papers piled on desks. Camera slowly sweeps across the frantic office. 5 seconds.
```

ナレーター: これに対して、斜里町の山内浩彰町長は、

【制作メモ】ASSET-068 [Lovart静止画 + 編集者] 台本L555-L559
シーン: 山内町長の発言テロップ。「非常に衝撃を受けた」
```
Photorealistic, shot on RED camera. Documentary style. A Japanese town mayor's office in Shari, Hokkaido, Japan. An official desk with a nameplate, a Japanese flag in the corner. Formal serious atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: テロップ追加：「"大変なことになったと、非常に衝撃を受けた" — 山内浩彰 斜里町長」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 増田泰副町長は、

【制作メモ】ASSET-069 [Lovart静止画 + 編集者] 台本L561-L569
シーン: 増田副町長の発言テロップ。「今後の検証が必要」「知床のクマは人を襲わないということはない」
```
Photorealistic, shot on RED camera. Documentary style. A Japanese government press conference podium in Hokkaido, Japan. Two microphones on the podium, official backdrop. Formal grave atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: テロップ追加：「"注意喚起がどこまで伝わっていたのか。今後の検証が必要" / "知床のクマは人を襲わないということはない" — 増田泰 副町長」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 知床では、過去にもヒグマと人間の距離が近すぎることが問題視されてきました。

【制作メモ】ASSET-070 [Lovart動画] 台本L571-L577
シーン: 知床五湖でクマが遊歩道に座り込む。至近距離で撮影する観光客。SNS投稿
```
Photorealistic, shot on RED camera. Documentary style. Elevated wooden boardwalk at Shiretoko Five Lakes, Hokkaido, Japan. Japanese tourists crowded together, some holding smartphones up to photograph something ahead on the boardwalk. Excited curious expressions. Bright summer day. Dangerously naive atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Japanese tourists on a wooden boardwalk at Shiretoko Five Lakes, Hokkaido, crowding together and holding up smartphones. They lean forward excitedly. Bright summer day. Camera slowly reveals their proximity to wild nature ahead. 5 seconds.
```

ナレーター: 専門家は最後に、

【制作メモ】ASSET-071 [Lovart動画] 台本L579-L585
シーン: 「良くも悪くも、知床のクマは人を怖がらない」。起こるべくして起きた事件
```
Photorealistic, shot on RED camera. Documentary style. A Hokkaido brown bear calmly walking along a paved road in Shiretoko, Hokkaido, Japan, with tourists' cars visible in the background. The bear shows no reaction to the vehicles. Natural light. Chillingly normal atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
A large Hokkaido brown bear with dark brown fur calmly walks along a paved road in Shiretoko, Hokkaido, Japan. Tourist cars visible in background. The bear ignores the vehicles completely. Natural daylight. 5 seconds.
```
→ 編集者指示: テロップ追加：「"良くも悪くも、知床のクマは人を怖がらない" — 専門家」

ナレーター: 羅臼町猟友会の桜井さんも、駆除について

【制作メモ】ASSET-072 [Lovart静止画 + 編集者] 台本L587-L591
シーン: 桜井さんの証言テロップ。「怖がって出てこないクマはそのまま。でもそうでないクマは取るべき」
```
Photorealistic, shot on RED camera. Documentary style. A mature Japanese hunter's face partially visible, looking out of a window at Shiretoko mountains, Hokkaido, Japan. Weathered hands resting on the window frame. Thoughtful resolute atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: テロップ追加：「"怖がって出てこないようなヒグマは、そのままでいい。でもそうでないクマは、取るべきだと思っています" — 桜井憲二さん」。ゆっくり近づく（5秒で1.0→1.15）

---

### 転結 — セクション16: 教訓

ナレーター: この事件を通して、クマスプレーの事前の準備の大切さが浮き彫りとなりました。

【制作メモ】ASSET-073 [Lovart動画] 台本L596-L606
シーン: クマスプレーの教訓。ヒグマ対応正規品・新品・使用期限確認・すぐ手が届く場所に装着
```
Photorealistic, shot on RED camera. Documentary style. Close-up of a proper Hokkaido bear spray canister with safety clip, attached to a hiking backpack chest strap at easy-reach position. Mountain forest background in Hokkaido, Japan. Clear instructional atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Close-up of a bear spray canister with safety clip attached to a hiking backpack chest strap. Camera slowly moves to show the easy-reach position. Mountain forest background in Hokkaido, Japan. 5 seconds.
```
→ 編集者指示: テキスト追加：「✅ ヒグマ対応 正規品 / ✅ 新品（使用期限確認）/ ✅ すぐ手が届く場所に装着」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 遭遇は一瞬で起きます。

【制作メモ】ASSET-074 [キャラアニメーション] 台本L608-L618
シーン: 走って下山の危険性。足音で気配に気づけない。鈴・声・手拍子でゆっくり歩くことの重要性
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [Generic group] Full body. Two Japanese hikers in outdoor gear walking slowly on a trail, one clapping hands, the other ringing a bear bell attached to their backpack. Alert cautious but calm expressions. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A hiking trail through dense bamboo grass on Mount Rausu, Shiretoko, Hokkaido, Japan. Sound waves rippling out from the trail (implied through atmosphere). Good visibility ahead. Cautious safe atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 登山者キャラを配置。手を叩く・鈴を鳴らすアニメーション。ゆっくり歩く動き（5秒）

ナレーター: 最新の目撃情報の確認も欠かせません。

【制作メモ】ASSET-075 [Lovart静止画 + 編集者] 台本L620-L634
シーン: 事前の情報確認の重要性。掲示板・ウェブサイト・SNS。数分で命を守る
```
Photorealistic, shot on RED camera. Documentary style. Close-up of a hiker's hands holding a smartphone showing a wildlife alert webpage, with a trailhead information board visible in the blurred background, Shiretoko, Hokkaido, Japan. Morning light. Proactive prepared atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: テキスト追加：「✅ 登山口の掲示板 / ✅ 管理団体のウェブサイト / ✅ SNSの最新情報 → 数分で終わる = 命を守る」。ゆっくり近づく（5秒で1.0→1.15）

---

### 転結 — セクション17: エンディング

ナレーター: 事件後、知床財団はウェブサイトでのクマ目撃情報の発信を強化しました。

【制作メモ】ASSET-076 [Lovart動画] 台本L639-L645
シーン: 情報発信の強化。しかし最後に判断するのは登山者自身。知床はヒグマの生息地
```
Photorealistic, shot on RED camera. Documentary style. Shiretoko National Park visitor center, Hokkaido, Japan. A large updated digital display showing bear sighting information. Staff members adding new warning posters. Natural light from large windows. Improved but still sobering atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Shiretoko National Park visitor center in Hokkaido. A large digital display updates with bear sighting information. Staff in uniform add new warning posters to a board. Camera pans from the display to the window showing Mount Rausu in the distance. 5 seconds.
```

ナレーター: もしあの日、登山道が閉鎖されていたら、、

【制作メモ】ASSET-077 [キャラアニメーション] 台本L647-L651
シーン: もしもの仮定。登山道閉鎖なら。正規スプレーなら。結果は違ったかもしれない
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, standing at a closed trail gate, looking slightly disappointed but safe. Alive and unharmed. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. A closed trailhead gate at Iwaobetsu, Mount Rausu, Shiretoko, Hokkaido, Japan, with a large official closure sign. Forest behind the gate. Morning light. Bittersweet what-if atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんキャラを閉鎖ゲート前に配置。安全な姿。ゆっくりフェードアウト（5秒）

ナレーター: 事件のあと、知床ヒグマ対策連絡会議は入山規制の基準を新たに策定しました。

【制作メモ】ASSET-078 [Lovart動画] 台本L653-L657
シーン: 新たな入山規制基準の策定。ようやく作られた判断基準
```
Photorealistic, shot on RED camera. Documentary style. A Japanese conference room with officials seated around a large table in Hokkaido, Japan. Documents and laptops open. Large projected screen showing a new protocol document. Formal determined atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Japanese officials seated around a conference table in Hokkaido, Japan, with documents and laptops open. A large projected screen displays a new protocol document. Camera slowly moves from the screen toward the officials. Formal determined atmosphere. 5 seconds.
```
→ 編集者指示: テロップ追加：「知床ヒグマ対策連絡会議 — 入山規制の基準を新たに策定 / 接近時の対応 / スプレー無効時の閉鎖基準 / 情報共有の手順」。ゆっくり近づく（5秒で1.0→1.15）

ナレーター: 同じ悲劇を繰り返さないために。

【制作メモ】ASSET-079 [Lovart動画] 台本L659-L665
シーン: 2025年8月の知床。世界遺産の山で1人の青年が命を落とした。クマの歴史を振り返る
```
Photorealistic, shot on RED camera. Documentary drama style. Mount Rausu, Shiretoko, Hokkaido, Japan, at golden hour sunset. The mountain in full silhouette against an orange and purple sky. The Sea of Okhotsk glistening below. A single memorial flower wreath at a trail marker in the foreground. Somber respectful atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Mount Rausu in Shiretoko, Hokkaido, silhouetted against a golden sunset sky. The Sea of Okhotsk glistens below. A memorial flower wreath at a trail marker in the foreground. Camera slowly pulls back, revealing the vast lonely mountain. 5 seconds.
```

ナレーター: その情報は全て、関係機関に届いていました。

【制作メモ】ASSET-080 [Lovart動画] 台本L667-L669
シーン: 全ての情報が届いていたのに、登山道は開いたままだった
```
Photorealistic, shot on RED camera. Documentary drama style. An open, unmanned trailhead gate at Iwaobetsu, Mount Rausu, Shiretoko, Hokkaido, Japan. The gate stands wide open with no barrier. Twilight light. Empty path stretching into dark forest. Haunting accusatory atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
An open trailhead gate at Iwaobetsu, Mount Rausu, Hokkaido. The gate stands wide open. Twilight fading. Camera slowly zooms in on the unguarded entrance leading into dark forest. Haunting atmosphere. 5 seconds.
```

ナレーター: 曽田圭亮さん。享年26歳でした。

【制作メモ】ASSET-081 [キャラアニメーション] 台本L671-L673
シーン: 最後の追悼。曽田さんの笑顔とご冥福。最後までご視聴ありがとうございましたのメッセージ
キャラプロンプト（1:1）:
```
Cute cartoon illustration style, thick black outlines, flat cel-shaded colors, large expressive eyes. [CHAR-01 reference | 再利用] Full body. A 26-year-old Japanese man in blue hiking jacket, gray pants, green daypack, standing with a bright warm smile, one hand raised in a gentle wave. Peaceful happy expression. Generate 5 separate images, each showing only this one character.
```
背景プロンプト（16:9）:
```
Photorealistic, shot on RED camera. Documentary style. Mount Rausu summit at sunrise, Shiretoko, Hokkaido, Japan. Golden morning light flooding the peak. Clouds below, blue sky above. The Shiretoko Peninsula stretching into the distance. Beautiful memorial hopeful atmosphere. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 曽田さんキャラを山頂の朝日背景に配置。静かにフェードアウト（5秒）。最後にテロップ：「ご冥福をお祈りいたします」

---

## Google Earth 座標・カメラ設定まとめ

| 素材ID | 座標 | カメラ指示 |
|--------|------|-----------|
| ASSET-004 | 44°04'30"N, 145°07'30"E（羅臼岳山頂） | 高度15kmから知床半島全景→羅臼岳にズームイン（15km→3km、10秒） |
| ASSET-007 | 44°04'30"N, 145°07'30"E（羅臼岳山頂） | 高度5kmから岩尾別ルート俯瞰。登山口→山頂をなぞる（10秒） |
| ASSET-017 | 44°05'50"N, 145°04'50"E（オホーツク展望台付近） | 高度1kmから現場付近を表示。カーブと笹藪を示す（8秒） |
| ASSET-029 | 44°05'50"N, 145°04'50"E（事件現場付近） | 登山口→現場ルート表示。距離と険しさ（8秒） |
| ASSET-052 | 44°05'10"N, 145°06'00"E（標高1,040m付近） | 高度2kmから8/10遭遇地点を表示（6秒） |

---

## 動画予算サマリー

| 項目 | 数 |
|:--|--:|
| Lovart動画（Google Flow使用） | 19本 |
| Veo Fastクレジット消費 | 19 × 20 = 380cr |
| 月間予算（4本/月） | 380 × 4 = 1,520cr |
| AIプロ月間枠 | ~2,500cr |
| 判定 | ✅ 予算内 |

---

## 素材カテゴリ別サマリー

| カテゴリ | 件数 | 自分の作業 | 編集者の作業 |
|----------|------|-----------|------------|
| Lovart生成（静止画＋編集者） | 17件 | コピペ→選ぶ | テキスト追加 |
| Lovart生成（動画→Flow） | 19本 | コピペ→選ぶ→Flow | なし |
| キャラアニメーション | 35件 | コピペ→選ぶ | CapCutアニメーション |
| Google Earth | 5箇所 | なし | 座標見て録画 |
| 実写画像 | 0件 | — | — |
| キャラ基準画像 | 3体 | コピペ→選ぶ | なし |
| **合計** | **81件（ASSET-001〜081）** | **Lovart 74回** | **図解17件 + GE 5箇所** |
| **動画/アニメ比率** | **67%（54/81）** | **目標: 50%以上 ✅** | — |

> ⚠️ **5秒ルール確認**: キャラアニメーション（35件）は各30-60秒カバー。Lovart動画（19件）は各5-10秒。静止画＋編集者（17件）は各5秒以内。静止画2連続箇所はセクション13-14の証言テロップ部（ASSET-060〜062）のみだが、各5秒以内かつ間にテロップ変化あり。

---

## ナレーション全行カバー検証

| セクション | 台本行範囲 | ナレーション行数 | ASSET | カバー状況 |
|:--|:--|:--|:--|:--|
| 1. フック | L11-L23 | 7行 | 001-004 | ✅ |
| 2. 人物と舞台 | L28-L56 | 15行 | 005-010 | ✅ |
| 3. 登頂と下山 | L63-L101 | 20行 | 011-015 | ✅ |
| 4. 遭遇 | L106-L142 | 19行 | 016-021 | ✅ |
| 5. 友人の闘い | L147-L195 | 25行 | 022-027 | ✅ |
| 6. 通報と捜索 | L200-L238 | 20行 | 028-032 | ✅ |
| 7. 翌日の発見 | L243-L279 | 19行 | 033-038 | ✅ |
| 8. DNA鑑定 | L284-L290 | 4行 | 039 | ✅ |
| 9. 岩尾別の母さん | L295-L361 | 34行 | 040-046 | ✅ |
| 10. 餌付け | L366-L404 | 20行 | 047-051 | ✅ |
| 11. 8/10最初の接近 | L409-L431 | 12行 | 052-054 | ✅ |
| 12. 8/12五分間の追跡 | L436-L470 | 18行 | 055-059 | ✅ |
| 13. なぜ閉鎖されなかったか | L475-L501 | 14行 | 060-062 | ✅ |
| 14. 見過ごされた前兆 | L506-L532 | 14行 | 063-066 | ✅ |
| 15. 駆除をめぐる批判 | L539-L591 | 27行 | 067-072 | ✅ |
| 16. 教訓 | L596-L634 | 20行 | 073-075 | ✅ |
| 17. エンディング | L639-L673 | 18行 | 076-081 | ✅ |
| **合計** | | **306行** | **81件** | **漏れ: 0行 ✅** |
