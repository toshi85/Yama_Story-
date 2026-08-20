# 2025年東成瀬村クマ襲撃事件 素材プロンプト — PART: KI（起）＋キャラ基準画像

> Lovartにコピペするだけの流れ作業用。生成順＝台本の登場順。
> 対象台本: `Master.md`（2026-08-20 v2確定・9,077字/286行）
> ASSET-001〜015 / 台本L155〜L187（§1フック〜§2 山林93%の村）
> ⚠️ 報道映像（ANN/ABS/カンテレ/防犯カメラ）を[実写]で使う箇所は各局の著作物＝切り抜き使用は `/revenue-guard` の判定対象。迷ったらLovartフォールバックを使う。

---

## 0. キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**: キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> Lovartでは1プロンプトにつき5枚同時生成。ベスト1枚を一貫性キャラの参照画像として採用。
> 服装は全ASSETで固定（一貫性の生命線）。変更禁止。

### CHAR-01: 佐々木喜行さん（38）— 東成瀬村の男性・母親を逃がして襲われた

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 38-year-old Japanese man, sturdy medium build, short black hair, kind gentle face, medium skin tone. Wearing a dark navy fleece jacket, black work pants, gray sneakers. Calm reliable expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-02: 父親（65）— 大工・佐々木さんの父

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 65-year-old Japanese man, lean strong build of a carpenter, short gray-streaked hair, weathered tanned face. Wearing an olive-gray work jacket, beige carpenter work pants, dark work boots. Earnest determined expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-03: 母親（60代）— 佐々木さんの母

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A Japanese woman in her early 60s, small slender build, short graying hair, soft round face. Wearing a dusty-pink cardigan over a cream blouse, gray pants, beige slip-on shoes. Gentle worried expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-04: 夫（76）— 横手市から畑仕事に来ていた男性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 76-year-old Japanese man, thin wiry build, deeply weathered face, white stubble. Wearing a light gray farm work jacket, dark green work pants, black rubber boots, and a dark flat cap. Mild friendly expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-05: 妻（72）— 夫とともに畑仕事に来ていた女性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 72-year-old Japanese woman, small round build, gray hair tied back, kind wrinkled face. Wearing a lavender farm work smock, dark monpe-style work pants, white sun hat hanging on her back, light rubber boots. Cheerful warm expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-06: ベテランハンター（76）— 猟歴50年超・東成瀬村猟友会

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 76-year-old Japanese hunter, lean tough build, deeply weathered face, short white hair. Wearing an olive-brown hunting vest over a checkered shirt, dark brown field pants, rubber boots, blaze-orange cap, hunting rifle slung over his shoulder. Sharp calm eyes of 50 years of experience. Generate 5 separate images, each showing only this one character.
```

### CHAR-07: ツキノワグマ（東成瀬・メス成獣）— 体長1.2m・体重約80kg

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An adult female Asian black bear (Ursus thibetanus), 120cm body length, compact but powerful build weighing about 80kg, glossy black fur, a clear white crescent-moon patch on the chest, round ears, long curved claws. Standing on all fours. Intense unafraid eyes. Generate 5 separate images, each showing only this one character.
```

### CHAR-08: 軽トラックの男性（70代）— 最初にクマに遭遇した農作業中の男性

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A Japanese man in his 70s, medium sturdy farmer build, sun-tanned wrinkled face. Wearing a navy farm work jacket, khaki work pants, dark rubber boots, and a gray work cap. Honest straightforward expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-09: 犬の散歩の男性（57）— 湯沢市・左腕を噛まれた被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 57-year-old Japanese man, average build, short black hair with gray at the temples. Wearing a dark green windbreaker, blue jeans, gray walking shoes, holding a red dog leash in one hand. Mild everyday expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-10: 自宅にいた男性（65）— 湯沢市表町・クマを家に閉じ込めた被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 65-year-old Japanese man, medium build, thinning gray hair, calm quiet face. Wearing a brown cardigan over a gray shirt, dark gray trousers, indoor sandals. Composed steady expression. Generate 5 separate images, each showing only this one character.
```

### CHAR-11: ツキノワグマ（湯沢・オス成獣）— 体長1.3m・東成瀬の個体とは別

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. An adult male Asian black bear (Ursus thibetanus), 130cm body length, slightly larger and shaggier than average, dull brownish-black fur, a wide white crescent-moon patch on the chest, a small notch on the right ear as an identifying mark. Standing on all fours. Bold fearless eyes. Generate 5 separate images, each showing only this one character.
```

---

## 1. 全素材リスト（台本順）

> **⚠️ 1ASSETの記述順序（厳守）**: ①ナレーター行 → ②【制作メモ】ASSET-XXX [カテゴリ] 台本L○○ → ③シーン: → ④プロンプト → ⑤編集者指示

---

<!-- PART: KI -->

### 起（§1 フック 〜 §2 山林93%の村）

---

ナレーター: 2025年10月24日。秋田県の東成瀬村（ひがしなるせむら）。

【制作メモ】ASSET-001 [テキストのみ] 台本L155
シーン: 黒背景に日付と地名の全画面テロップ（朱鞠内湖で維持率貢献が実証された開始型）
→ 編集者指示: 黒背景に「2025年10月24日」を白テキストでフェードイン（1秒）、続けて下段に「秋田県 東成瀬村」を表示。低いドローン音のBGMを開始。

---

ナレーター: 午前10時10分ごろ、農作業中の70代男性の目の前に

【制作メモ】ASSET-002 [キャラアニメーション] 台本L157
シーン: 秋の畑で農作業をするCHAR-08（70代男性）。ふと手を止めて顔を上げた瞬間
キャラプロンプト（1:1）:
```
(CHAR-08 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-08: Japanese man in his 70s, navy farm work jacket, khaki work pants, gray work cap, kneeling with a small hand hoe, then looking up with a puzzled expression. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
A small vegetable field on the edge of a mountain village in Akita, northern Japan, late October morning. Rows of autumn vegetables, a rural road nearby, golden larch and red maple foliage on the surrounding low mountains. Soft morning light. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: 「午前10時10分ごろ」の時刻テロップを左上に表示。CHAR-08が顔を上げる動きをキーフレームで作る（2〜3秒）。

---

ナレーター: 突如ツキノワグマが出没。

【制作メモ】ASSET-003 [キャラアニメーション] 台本L159
シーン: 畑のすぐそば、CHAR-07（ツキノワグマ）が四足歩行で姿を現す衝撃の瞬間
キャラプロンプト（1:1）:
```
(CHAR-07 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-07: adult female Asian black bear, 120cm, glossy black fur, white crescent chest patch, standing on all fours, head low, staring straight ahead with intense unafraid eyes. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
The grassy edge of a rural field in Akita, Japan, where farmland meets a dark cedar forest. Tall dry autumn grass, fallen leaves, shadows under the trees. Late October morning light with an uneasy mood. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: 衝撃音（ドン）とともにクマを画面外から素早くスライドイン。1〜2秒の短カット。

---

ナレーター: さらに1時間後、空き地にいた70代夫婦がクマに襲われ、

【制作メモ】ASSET-004 [キャラアニメーション] 台本L161
シーン: 空き地でCHAR-04（夫）とCHAR-05（妻）が振り返り、恐怖で身を寄せ合う。クマ本体は映さず影で暗示
キャラプロンプト（1:1）:
```
(CHAR-04 再利用)(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-04: 76-year-old Japanese man, light gray farm jacket, dark green work pants, dark flat cap. CHAR-05: 72-year-old Japanese woman, lavender farm smock, dark monpe pants. Both turning around in alarm, clinging to each other, faces frozen in fear. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
An open vacant lot behind rural Japanese houses in Akita, patchy grass and bare soil, a small weathered wooden shed at the edge, low mountains with autumn colors behind. A long dark animal shadow stretching across the ground from the shed. Tense atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: 「1時間後」テロップを右上に。夫婦のカットは1.5秒、影がゆっくり伸びる動きを付ける。

---

ナレーター: 悲鳴を聞いて駆けつけた男性と

【制作メモ】ASSET-005 [キャラアニメーション] 台本L163
シーン: CHAR-01（佐々木さん）が家から飛び出し、全力で走る横向きの姿
キャラプロンプト（1:1）:
```
(CHAR-01 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-01: 38-year-old Japanese man, dark navy fleece jacket, black work pants, running at full sprint, side view, arms pumping, urgent worried expression. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
A narrow residential lane in a small Japanese mountain village, single-story houses with dark roofs, utility poles, autumn mountains close behind the rooftops. Morning light, long shadows. Sense of urgency. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: CHAR-01を左→右へ素早くスライド（1.5秒）。足音と息づかいのSE。

---

ナレーター: その父親もクマに襲われ重傷。

【制作メモ】ASSET-006 [キャラアニメーション] 台本L165
シーン: CHAR-02（父親）が現場に駆けつけた直後、画面が赤みを帯びて衝撃を暗示（直接の暴力描写はしない）
キャラプロンプト（1:1）:
```
(CHAR-02 再利用)(CHAR-07 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-02: 65-year-old Japanese carpenter, olive-gray work jacket, beige work pants, frozen mid-step in shock, eyes wide, one hand raised defensively. CHAR-07: adult female Asian black bear, 120cm, glossy black fur, white crescent chest patch, lunging toward him on all fours, mouth open. Family-friendly depiction, no injuries shown. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
An open vacant lot in a Japanese mountain village, trampled autumn grass, a small light truck parked at the edge, overcast late-morning light turning cold. Ominous heavy atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: 「重傷」の赤テロップを一瞬だけ表示し、画面を短くホワイトアウト→次カットへ。

---

ナレーター: 警察が到着したころには、

【制作メモ】ASSET-007 [Lovart静止画] 台本L167
シーン: 村道を走ってくるパトカー。赤色灯が回っている
```
A Japanese police patrol car with red lights flashing, arriving on a narrow rural road in a small mountain village in Akita, autumn morning, mountains with golden foliage in the background. Urgent documentary mood. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: ゆっくり近づく（3秒で1.0→1.1）。サイレンSE。

---

ナレーター: 倒れている4人と、走り去っていくクマの姿。

【制作メモ】ASSET-008 [Lovart動画] 台本L169 ★フック最大の画（HOOK-IMAGE）
シーン: 空き地に4人が倒れており、その奥をクマが山へ走り去っていく。引きの構図で直接的な描写は避ける
```
Wide high-angle shot of an open lot in a Japanese mountain village: four Japanese adults lying motionless on the ground at a distance, seen small and far away so no injuries are visible, while a black bear runs away from the scene toward the forested mountain in the background. Late October morning, muted colors, documentary realism, tragic and quiet. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Static wide high-angle shot of an open lot in a rural Japanese village in autumn: four Japanese adults in farm work clothes lying motionless far from the camera, no injuries visible, while one black bear with a white chest crescent runs on all fours away from the scene toward the dark forested mountain. The bear moves fast, dust and fallen leaves kicked up. Camera holds still. 5 seconds. Photorealistic, shot on RED camera. Documentary style.
```
→ 編集者指示: 音を一瞬すべて消してこのカットを見せる（3〜4秒）。直後に心拍音。

---

ナレーター: なぜ、このような事件が発生したのか？

【制作メモ】ASSET-009 [Lovart静止画 + 編集者] 台本L172
シーン: 現場の空き地を見下ろす静かな俯瞰カットをベースに、問い①のテキストを編集者が重ねる（起パートの図解・テロップ演出枠）
```
Somber overhead view of an empty vacant lot in a Japanese mountain village at autumn, bare soil and flattened grass, a single small shed, cold overcast light. Quiet aftermath mood, calm empty space in the center of the frame. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 画面中央に「なぜ、このような事件が発生したのか？」を白文字で1行表示（ゆっくりフェードイン）。ベース画はゆっくり近づく（4秒で1.0→1.08）。

---

ナレーター: そして、なぜハンターは、すぐに引き金を引けなかったのか。

【制作メモ】ASSET-010 [キャラアニメーション] 台本L174
シーン: CHAR-06（ベテランハンター）がライフルを構えたまま動けない。引き金に指がかからない緊張
キャラプロンプト（1:1）:
```
(CHAR-06 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-06: 76-year-old Japanese hunter, olive-brown hunting vest, blaze-orange cap, aiming a hunting rifle but holding fire, jaw clenched, sweat drop on temple, conflicted tense expression. Full body. White background. 1:1 aspect ratio. Generate 5 separate images.
```
背景プロンプト（16:9）:
```
Looking up a grassy embankment toward a small wooded hilltop on the edge of a Japanese mountain village, autumn afternoon, houses visible close behind the camera position. Tense standoff atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 5 separate images.
```
→ 編集者指示: 「なぜ、すぐに引き金を引けなかったのか」を下段に白テロップ。銃口の先をわずかに揺らすキーフレーム（2〜3秒）。

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

【制作メモ】ASSET-013 [Lovart動画] 台本L183
シーン: 山あいに小さな集落がぽつんと沈む村の空撮。見渡す限りの山林の中の細長い集落
```
Aerial drone shot slowly gliding over a tiny Japanese mountain village in Akita: a thin line of houses and small fields along a single road in a narrow valley, surrounded on all sides by endless forested mountains in autumn colors, morning mist in the valleys. The village looks small and isolated in a sea of forest. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ **Google Flow動画プロンプト:**
```
Slow forward aerial drone movement over a narrow Japanese mountain valley in autumn: a small village of dark-roofed houses and tiny fields along one road, surrounded by endless forested ridges in gold and red, thin morning mist drifting through the valleys. No people visible. Camera glides forward smoothly. 5 seconds. Photorealistic, shot on RED camera. Documentary style.
```
→ 編集者指示: 「山林・原野 93%」「人口 約2,100人」の2行テロップを左下に順番にフェードイン。

---

ナレーター: 家の勝手口を出て、数十歩あるけば、もう山の入り口。

【制作メモ】ASSET-014 [Lovart静止画] 台本L185
シーン: 民家の勝手口と、そのすぐ裏に迫る山の斜面。家と山の距離の近さが一目で分かる構図
```
The back door of an old Japanese country house in Akita, a few stepping stones across a tiny yard, and immediately behind it a steep forested mountain slope rising over the roof, autumn foliage. The forest edge is only a few steps from the door. Quiet rural realism. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: 勝手口から山へ、ゆっくり左から右に動かす（4秒）。

---

ナレーター: それほど自然との距離が近い環境でした。

【制作メモ】ASSET-015 [Lovart静止画] 台本L187
シーン: 庭先のすぐ向こうの茂みに野生動物（ニホンカモシカ）の気配。人の暮らしと自然の近さ
```
View from a Japanese village garden in Akita: laundry pole and a small vegetable patch in the foreground, and just beyond a low hedge, a wild Japanese serow standing quietly at the edge of the forest, autumn morning light. The wild and the everyday in one frame. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 5 separate images.
```
→ 編集者指示: ゆっくり近づく（4秒で1.0→1.1）。※静止画はここで2連続のため、次のカット（SHO冒頭）はテキスト演出に切り替わる。

---

