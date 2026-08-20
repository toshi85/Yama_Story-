# 2025年東成瀬村クマ襲撃事件 素材プロンプト — PART: KI（起）＋キャラ基準画像

> Lovartにコピペするだけの流れ作業用。生成順＝台本の登場順。
> 対象台本: `Master.md`（2026-08-20 v2確定・9,077字/286行）
> ASSET-001〜015 / 台本L155〜L187（§1フック〜§2 山林93%の村）
> ⚠️ 報道映像（ANN/ABS/カンテレ/防犯カメラ）を[実写]で使う箇所は各局の著作物＝切り抜き使用は `/revenue-guard` の判定対象。迷ったらLovartフォールバックを使う。
> 🎬 **冒頭フック（§1）は全カット実写風AI動画**（カートゥン禁止・2026-08-20ユーザー裁定）。これによりAI動画は計20本＝上限12本を超過するが、冒頭優先のユーザー決定として許容。

---

## 0. キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**: キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> Lovartでは1プロンプトにつき**1枚生成**（2026-08-20 ユーザー指定・全プロンプト共通）。気に入らなければ同じプロンプトで再生成。
> 服装は全ASSETで固定（一貫性の生命線）。変更禁止。

### CHAR-01: 佐々木喜行さん（38）— 東成瀬村の男性・母親を逃がして襲われた

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 38-year-old Japanese man, sturdy medium build, short black hair, kind gentle face, medium skin tone. Wearing a dark navy fleece jacket, black work pants, gray sneakers. Calm reliable expression. Generate 1 image, showing only this one character.
```

### CHAR-02: 父親（65）— 大工・佐々木さんの父

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 65-year-old Japanese man, lean strong build of a carpenter, short gray-streaked hair, weathered tanned face. Wearing an olive-gray work jacket, beige carpenter work pants, dark work boots. Earnest determined expression. Generate 1 image, showing only this one character.
```

### CHAR-03: 母親（60代）— 佐々木さんの母

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A Japanese woman in her early 60s, small slender build, short graying hair, soft round face. Wearing a dusty-pink cardigan over a cream blouse, gray pants, beige slip-on shoes. Gentle worried expression. Generate 1 image, showing only this one character.
```

### CHAR-04: 夫（76）— 横手市から畑仕事に来ていた男性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 76-year-old Japanese man, thin wiry build, deeply weathered face, white stubble. Wearing a light gray farm work jacket, dark green work pants, black rubber boots, and a dark flat cap. Mild friendly expression. Generate 1 image, showing only this one character.
```

### CHAR-05: 妻（72）— 夫とともに畑仕事に来ていた女性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 72-year-old Japanese woman, small round build, gray hair tied back, kind wrinkled face. Wearing a lavender farm work smock, dark monpe-style work pants, white sun hat hanging on her back, light rubber boots. Cheerful warm expression. Generate 1 image, showing only this one character.
```

### CHAR-06: ベテランハンター（76）— 猟歴50年超・東成瀬村猟友会

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 76-year-old Japanese hunter, lean tough build, deeply weathered face, short white hair. Wearing an olive-brown hunting vest over a checkered shirt, dark brown field pants, rubber boots, blaze-orange cap, hunting rifle slung over his shoulder. Sharp calm eyes of 50 years of experience. Generate 1 image, showing only this one character.
```

### CHAR-07: ツキノワグマ（東成瀬・メス成獣）— 体長1.2m・体重約80kg

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An adult female Asian black bear (Ursus thibetanus), 120cm body length, compact but powerful build weighing about 80kg, glossy black fur, a clear white crescent-moon patch on the chest, round ears, long curved claws. Standing on all fours. Intense unafraid eyes. Generate 1 image, showing only this one character.
```

### CHAR-08: 軽トラックの男性（70代）— 最初にクマに遭遇した農作業中の男性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A Japanese man in his 70s, medium sturdy farmer build, sun-tanned wrinkled face. Wearing a navy farm work jacket, khaki work pants, dark rubber boots, and a gray work cap. Honest straightforward expression. Generate 1 image, showing only this one character.
```

### CHAR-09: 犬の散歩の男性（57）— 湯沢市・左腕を噛まれた被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 57-year-old Japanese man, average build, short black hair with gray at the temples. Wearing a dark green windbreaker, blue jeans, gray walking shoes, holding a red dog leash in one hand. Mild everyday expression. Generate 1 image, showing only this one character.
```

### CHAR-10: 自宅にいた男性（65）— 湯沢市表町・クマを家に閉じ込めた被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 65-year-old Japanese man, medium build, thinning gray hair, calm quiet face. Wearing a brown cardigan over a gray shirt, dark gray trousers, indoor sandals. Composed steady expression. Generate 1 image, showing only this one character.
```

### CHAR-11: ツキノワグマ（湯沢・オス成獣）— 体長1.3m・東成瀬の個体とは別

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An adult male Asian black bear (Ursus thibetanus), 130cm body length, slightly larger and shaggier than average, dull brownish-black fur, a wide white crescent-moon patch on the chest, a small notch on the right ear as an identifying mark. Standing on all fours. Bold fearless eyes. Generate 1 image, showing only this one character.
```

---

## 1. 全素材リスト（台本順）

> **⚠️ 1ASSETの記述順序（厳守）**: ①ナレーター行 → ②【制作メモ】ASSET-XXX [カテゴリ] 台本L○○ → ③シーン: → ④プロンプト → ⑤編集者指示

---

<!-- PART: KI -->

### 起（§1 フック 〜 §2 山林93%の村）

---

ナレーター: 2025年10月24日。秋田県の東成瀬村（ひがしなるせむら）。

【制作メモ】ASSET-001 [Lovart動画] 台本L155 ★冒頭は必ず動画（恒久ルール）
シーン: 夜明け直後の東成瀬村を進む不穏な空撮。この動画の上に日付・地名テロップを重ねる（朱鞠内湖型の開始）
```
High aerial still view at first light over a small mountain village in Akita, Japan: dark forested ridges pressing in on a thin line of houses along one road, cold mist lying in the valley floor, muted pre-dawn blue tones. Ominous quiet before something begins. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
Slow forward aerial drone movement at first light over a narrow Japanese mountain valley in Akita: dark forested ridges, a thin line of village houses below, cold mist drifting between the trees, muted blue pre-dawn tones, steady ominous glide. No people visible. 5 seconds. Photorealistic, shot on RED camera. Documentary style.
```
→ 編集者指示: 動画の上に「2025年10月24日」を白テキストでフェードイン（1秒）、続けて下段に「秋田県 東成瀬村」。低いドローン音のBGMを開始。

---

ナレーター: 午前10時10分ごろ、農作業中の70代男性の目の前に

【制作メモ】ASSET-002 [Lovart動画] 台本L157 ★冒頭フックは実写風動画（恒久ルール）
シーン: 秋の畑で農作業する70代男性が、ふと手を止めて顔を上げる（実写風）
```
A Japanese farmer in his 70s wearing a navy work jacket and gray cap, kneeling among crop rows in a small vegetable field in a mountain village in Akita on a late October morning, head lifted and eyes fixed on something off-frame, hands frozen mid-weeding, golden autumn foliage on the low mountains behind. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
A Japanese farmer in his 70s in a navy work jacket and gray cap kneels weeding a vegetable field in an autumn Japanese mountain village, then slowly stops moving and raises his head, turning toward something off-frame, morning light, subtle tension entering a peaceful scene. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「午前10時10分ごろ」テロップを左上に。環境音のみ。
---

ナレーター: 突如ツキノワグマが出没。

【制作メモ】ASSET-003 [Lovart動画] 台本L159 ★冒頭フックは実写風動画
シーン: 藪の際からツキノワグマが姿を現す衝撃（実写風）
```
An adult Asian black bear with a white crescent chest patch frozen mid-stride as it emerges from tall dry grass at the edge of a village field in Akita, on all fours, head low, front paw raised, dry stalks bent around its shoulders, late October morning light. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
An adult Asian black bear, glossy black fur with a white crescent chest patch, bursts on all fours out of tall dry grass at the edge of a Japanese village field and takes two fast strides toward the camera, dust and leaves kicked up, sudden and violent motion, autumn morning light. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 衝撃SE一発。1〜2秒の短カット。
---

ナレーター: さらに1時間後、空き地にいた70代夫婦がクマに襲われ、

【制作メモ】ASSET-004 [Lovart動画] 台本L161 ★冒頭フックは実写風動画
シーン: 空き地の70代夫婦が振り返り、身を寄せ合う。迫る影で襲撃を暗示（直接描写なし・実写風）
```
An elderly Japanese couple in farm work clothes — a thin man in his 70s in a light gray jacket and flat cap, a small woman in her 70s in a lavender work smock — turned around in alarm in a vacant lot behind village houses in Akita, clinging to each other, a large dark four-legged animal shadow stretched across the grass toward their feet, cold late-morning light. No injuries shown. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
An elderly Japanese couple in farm work clothes — a thin man in his 70s in a light gray jacket and flat cap, a small woman in a lavender work smock — spin around in a village vacant lot in Akita and clutch each other as a huge four-legged animal shadow sweeps across the grass toward them, camera pushing in slightly, no contact or injuries shown, ending just before the shadow reaches them. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「1時間後」テロップ。影が届く直前でカット。
---

ナレーター: 悲鳴を聞いて駆けつけた男性と

【制作メモ】ASSET-005 [Lovart動画] 台本L163 ★冒頭フックは実写風動画
シーン: 悲鳴を聞いて路地を全力で走る38歳男性（実写風）
```
A sturdy Japanese man in his late 30s wearing a dark navy fleece jacket and black work pants captured frozen mid-sprint in a narrow lane between single-story houses in a Japanese mountain village in Akita, arms pumping, urgent expression, slight motion blur at the frame edges, autumn morning light. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
A sturdy Japanese man in his late 30s in a dark navy fleece jacket and black work pants sprints toward the camera down a narrow village lane in Akita, arms pumping, breath visible, houses and utility poles rushing past, handheld urgency. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 足音と息づかいのSE。1.5〜2秒使用。
---

ナレーター: その父親もクマに襲われ重傷。

【制作メモ】ASSET-006 [Lovart動画] 台本L165 ★冒頭フックは実写風動画
シーン: 駆けつけた65歳の父親が立ちすくみ、画面が短く暗転（襲撃の直接描写なし・実写風）
```
A lean weathered Japanese carpenter in his 60s wearing an olive-gray work jacket, frozen mid-step in shock at the edge of a village vacant lot in Akita, one hand raised defensively, cold overcast light, ominous atmosphere. No injuries shown. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
A lean weathered Japanese carpenter in his 60s in an olive-gray work jacket runs into frame at the edge of a village vacant lot in Akita, stops dead, raises one hand defensively as something unseen rushes him from off-frame, quick camera shake, cut to black at the moment of impact, nothing graphic shown. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「重傷」赤テロップを一瞬→暗転0.5秒。
---

ナレーター: 警察が到着したころには、

【制作メモ】ASSET-007 [Lovart動画] 台本L167 ★冒頭フックは実写風動画
シーン: 赤色灯を回したパトカーが村道を走ってくる（実写風）
```
A Japanese police patrol car with red lights flashing, captured head-on on a narrow rural road in a small mountain village in Akita, a faint dust cloud hanging behind it, autumn morning, golden foliage on the mountains behind. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
A Japanese police patrol car with red lights flashing speeds along a narrow rural road toward the camera in an autumn Japanese mountain village, slight low-angle, dust trailing, siren urgency, mountains with golden foliage behind. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: サイレンSE。
---

ナレーター: 倒れている4人と、走り去っていくクマの姿。

【制作メモ】ASSET-008 [Lovart動画] 台本L169 ★フック最大の画（HOOK-IMAGE）
シーン: 空き地に4人が倒れており、その奥をクマが山へ走り去っていく。引きの構図で直接的な描写は避ける
```
Wide high-angle still of an open lot in a Japanese mountain village: four Japanese adults lying motionless on the ground at a distance, seen small and far away so no injuries are visible, and a black bear frozen mid-run away from the scene toward the forested mountain in the background, dust and leaves suspended behind it. Late October morning, muted colors, documentary realism, tragic and quiet. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
Static wide high-angle shot of an open lot in a rural Japanese village in autumn: four Japanese adults in farm work clothes lying motionless far from the camera, no injuries visible, while one black bear with a white chest crescent runs on all fours away from the scene toward the dark forested mountain. The bear moves fast, dust and fallen leaves kicked up. Camera holds still. 5 seconds. Photorealistic, shot on RED camera. Documentary style.
```
→ 編集者指示: 音を一瞬すべて消してこのカットを見せる（3〜4秒）。直後に心拍音。

---

ナレーター: なぜ、このような事件が発生したのか？

【制作メモ】ASSET-009 [Lovart動画] 台本L172 ★冒頭フックは実写風動画
シーン: 現場の空き地をゆっくり寄っていくドローン俯瞰。問い①のテキストは編集者が重ねる（実写風）
```
High drone still view over an empty vacant lot in a Japanese mountain village in Akita, bare soil and flattened grass, a single small shed, cold overcast light, somber aftermath mood with calm space at the center of the frame. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
A slow steady drone descent over an empty vacant lot in an autumn Japanese mountain village, flattened grass and a small shed below, cold overcast light, the camera easing downward and forward with funeral calm. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「なぜ、このような事件が発生したのか？」を白文字でゆっくりフェードイン。
---

ナレーター: そして、なぜハンターは、すぐに引き金を引けなかったのか。

【制作メモ】ASSET-010 [Lovart動画] 台本L174 ★冒頭フックは実写風動画
シーン: ライフルを構えたまま引き金を引けない高齢ハンターの横顔（実写風）
```
A 76-year-old Japanese hunter in an olive-brown hunting vest and blaze-orange cap, aiming a rifle up a grassy slope in a Japanese mountain village in Akita but holding fire, jaw clenched, finger resting outside the trigger guard, houses visible close behind him, tense overcast light. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
Side profile of a 76-year-old Japanese hunter in an olive-brown vest and blaze-orange cap aiming a rifle upward and holding completely still, only his breathing moving his shoulders, a bead of sweat on his temple, village rooftops soft behind him, the barrel trembling almost imperceptibly. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「なぜ、すぐに引き金を引けなかったのか」を下段に白テロップ。呼吸音のみ。
---

ナレーター: 地形図とともに解説します。

【制作メモ】ASSET-011 [Google Earth] 台本L176
シーン: 日本列島→秋田県→東成瀬村へズームインして「地形図で解説する」宣言に応える導入カット
座標: `39.1792, 140.6489`（東成瀬村役場）
カメラ: 高度300km（東北全体）から高度10kmまでズームイン、3D地形ON、真上→斜め45°へ
→ 編集者指示: ズーム終点で「東成瀬村」ラベルと赤ピンを役場位置に表示。「地形図とともに解説します」のナレーションに合わせて2段階ズーム。

---

ナレーター: 事件が発生した東成瀬村は、秋田県のいちばん端に位置します。

【制作メモ】ASSET-012 [Google Earth] 台本L181
シーン: 秋田県全体を俯瞰し、県の南東端にある東成瀬村の位置を示す。県境（岩手・宮城側）が見える角度
座標: `39.1792, 140.6489`（東成瀬村役場）を画面右下に置き、秋田県全体が入る構図
カメラ: 高度120〜150km、斜め30°、3D地形ON、北西から南東を見下ろす
→ 編集者指示: 秋田県の輪郭を白線でなぞり、東成瀬村に赤ピン＋「東成瀬村」ラベル。「秋田県のいちばん端」に合わせて県境ラインを一瞬光らせる。

---

ナレーター: 面積のおよそ93パーセントが山林と原野で占められた、人口2,100人ほどの村。

【制作メモ】ASSET-013 [Lovart動画] 台本L183 ※GE3連続を回避（GEは連続2回まで・2026-08-20ルール化）
シーン: 見渡す限りの山林の中に、細長い集落がぽつんと沈む村の空撮（実写風）
```
High aerial still view over a tiny Japanese mountain village in Akita: a thin line of dark-roofed houses and small fields along a single road in a narrow valley, surrounded on all sides by endless forested mountains in autumn colors, morning mist lying in the side valleys. The village looks small and isolated in a sea of forest. Photorealistic, shot on RED camera. Documentary drama style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
Slow forward aerial drone movement over a narrow Japanese mountain valley in autumn: a small village of dark-roofed houses and tiny fields along one road below, endless forested ridges in gold and red on every side, thin morning mist drifting through the side valleys. No people visible. 5 seconds. Photorealistic, shot on RED camera. Documentary drama style.
```
→ 編集者指示: 「山林・原野 93%」「人口 約2,100人」の2行テロップを左下に順番にフェードイン。

---

ナレーター: 家の勝手口を出て、数十歩あるけば、もう山の入り口。

【制作メモ】ASSET-014 [Lovart静止画] 台本L185
シーン: 民家の勝手口と、そのすぐ裏に迫る山の斜面。家と山の距離の近さが一目で分かる構図
```
The back door of an old Japanese country house in Akita, a few stepping stones across a tiny yard, and immediately behind it a steep forested mountain slope rising over the roof, autumn foliage. The forest edge is only a few steps from the door. Quiet rural realism. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 1 image.
```
→ 編集者指示: 勝手口から山へ、ゆっくり左から右に動かす（4秒）。

---

ナレーター: それほど自然との距離が近い環境でした。

【制作メモ】ASSET-015 [Lovart静止画] 台本L187
シーン: 庭先のすぐ向こうの茂みに野生動物（ニホンカモシカ）の気配。人の暮らしと自然の近さ
```
View from a Japanese village garden in Akita: laundry pole and a small vegetable patch in the foreground, and just beyond a low hedge, a wild Japanese serow standing quietly at the edge of the forest, autumn morning light. The wild and the everyday in one frame. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 1 image.
```
→ 編集者指示: ゆっくり近づく（4秒で1.0→1.1）。※静止画はここで2連続のため、次のカット（SHO冒頭）はテキスト演出に切り替わる。

---

