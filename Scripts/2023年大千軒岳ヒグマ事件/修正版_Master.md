# 大千軒岳ヒグマ事件（2023年10月）制作メモ付き Master

> **生成日**: 2026-05-14
> **ベース台本**: `修正版.txt`（8,705字 / 推定25:22 / 343字/分基準）
> **重要ルール**:
> - ナレーション本文は1字も改変禁止（フリガナ・補足・ユーザー要望のカッコ表記も全保持）
> - ASSET-001 から連番（飛び番なし）、台本登場順
> - 制作メモは【】内に配置、ナレーションの間に挿入

---

## キャラ基準画像（最初に生成→一貫性キャラ機能の参照画像にする）

> **スタイル方針**:
> - キャラ画像 = カートゥン調イラスト（太い輪郭線、フラットカラー、大きな瞳、子供向けアニメ風）
> - 背景・シーン画像/動画 = フォトリアル（RED camera風、ドキュメンタリー調）
> - Lovartは1プロンプトにつき5枚同時生成、ベスト1枚を一貫性キャラの参照画像に採用

### CHAR-01: 屋名池奏人さん（22歳）— 被害者・北大水産学部4年生

[実写参照: なし — 遺族配慮のため実写不使用、テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 22-year-old Japanese male university student, slim athletic build (former boat club, current canoe club member), short black hair, medium skin tone. Wearing a navy blue hiking jacket, dark gray hiking pants, brown hiking boots, and a medium-sized green daypack. Calm gentle expression, slight smile. Generate 3 separate images, each showing only this one character.
```

### CHAR-02: 大原巧海さん（41歳）— 福島消防署・反撃者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 41-year-old Japanese male firefighter, muscular tough build, short black hair, tan skin tone. Wearing a dark olive green hiking jacket, sturdy gray cargo pants, heavy hiking boots, and a tactical-style backpack. Strong determined expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-03: 阿部達也さん（36歳）— 福島消防署・滑落者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 36-year-old Japanese male firefighter, average athletic build, short black hair, medium skin tone. Wearing a dark red hiking jacket, dark gray pants, hiking boots, and a black daypack. Composed serious expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-04: 船板克志さん（41歳）— 知内消防署・最初の被害者

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 41-year-old Japanese male firefighter, broad-shouldered tough build, short black hair with slight gray at temples, tan skin tone. Wearing a dark navy blue hiking jacket, brown cargo pants, hiking boots, and a green daypack. Steady experienced expression. Generate 3 separate images, each showing only this one character.
```

### CHAR-05: 加害個体ヒグマ — 若いオス・体長1.25m・栄養良好

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A young male Hokkaido brown bear (Ursus arctos yesoensis), 125cm body length, muscular build with good nutritional condition, dark brown fur with slightly lighter muzzle, small rounded ears, intense unafraid watchful eyes showing hunger learned for humans. Standing on all fours. Generate 3 separate images, each showing only this one character.
```

### CHAR-06: ティモシー・トレッドウェルさん（46歳）— 海外事例参考

[実写参照: 報道写真使用可能（Wikipedia等のCC画像 / グリズリーマン映画スチール）]

```
（実写画像を優先使用。AI生成する場合のみ以下使用）
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. A 46-year-old American man, lean build, shoulder-length sandy blonde hair, light skin tone. Wearing a black hoodie with bear imagery, camouflage cargo pants, and a video camera in hand. Passionate naturalist expression. Generate 3 separate images.
```

### CHAR-07: エイミー・ヒューゲナードさん（37歳）— 海外事例参考

[実写参照: 報道写真使用可能（公開されている範囲で）]

### CHAR-08: 山口洋一さん（71歳）— 2024年10月鉢合わせ被害者・愛知県岡崎市

[実写参照: なし — テキスト情報のみ]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A 71-year-old Japanese male hiker, white hair, gentle determined expression, wearing a beige hiking jacket and brown pants, with a small daypack and hiking poles. Front-facing. White background. 1:1 aspect ratio. Generate 3 separate images, each showing only this one character.
```

### CHAR-09: 2024年10月遭遇個体ヒグマ（CHAR-05とは別個体）

[実写参照: なし — CHAR-05との混同を避けるため明確に区別]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, white background. Single character only, front-facing view. A different brown bear from CHAR-05: 150cm body length (slightly larger than CHAR-05), brown fur with a reddish tint to distinguish from CHAR-05, alert posture. Front-facing. White background. 1:1 aspect ratio. Generate 3 separate images, each showing only this one character.
```

### CHAR-10: 2025年5月遭遇個体・親子ヒグマ（母グマと子グマ）

[実写参照: なし — CHAR-05/CHAR-09 とは別個体]

```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Two brown bears: a larger mother bear (about 160cm body length, brown fur) and a smaller cub (about 60cm body length, lighter brown fur), standing close together on a forest trail. Both alert, looking at an unseen direction. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```

---

## グローバル背景プリセット

### BG-A: 笹薮の登山道（事件現場）
```
Narrow mountain hiking trail on Daisengen-dake, Hokkaido, Japan. Dense Sasa bamboo grass walls on both sides reaching above eye level, dwarf bamboo and short conifers crowding the path. Visibility limited to 3 meters. Overcast late-autumn sky filtering dim light. Damp leaf litter on the ground. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 3 separate images.
```

### BG-B: 沢沿いの薄暗い現場
```
A steep ravine on Daisengen-dake at 550m elevation, narrow gully with damp earth and scattered branches, surrounded by dense bamboo grass and shadowed conifers. Overcast autumn afternoon light filtering through canopy. Wet leaves and dark soil. Photorealistic, RED camera, documentary style, eerie quiet atmosphere. 16:9 aspect ratio. No people, no figures visible. Empty landscape only. Generate 3 separate images.
```

### BG-C: 函館市港町の住宅街
```
Quiet residential street in Minato-cho, Hakodate city, Hokkaido, early autumn morning. Low-rise houses, narrow side streets, distant view of the harbor through gaps. Soft golden sunrise light, mist near the ground. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures visible. Empty street only. Generate 3 separate images.
```

### BG-D: 福島町の山々
```
Forested mountains of Matsumae Peninsula in southwestern Hokkaido, autumn foliage transitioning from green to yellow, dense conifer-broadleaf mixed forest. Overcast sky, low clouds clinging to the ridges. Photorealistic, RED camera, aerial documentary style. 16:9 aspect ratio. No people, no figures visible. Empty landscape only. Generate 3 separate images.
```

---

## 1. フック部分（修正版.txt L1-L11）— ASSET-001〜006

---

太ももに、爪が食い込んでくる。

【制作メモ】ASSET-001 [AI動画 / Lovart or Google Flow]
シーン: 森の中で人間の太ももに伸びる、毛むくじゃらの巨大なヒグマの前足のクローズアップ。爪が衣服を引き裂きながら太ももに食い込む瞬間
静止画プロンプト（16:9・フォトリアル）:
```
Extreme close-up cinematic shot of a massive Hokkaido brown bear's front paw — thick curved black claws fully extended, each sharp talon catching the dim forest light, digging into a dark olive green hiking pant leg that is being torn and pierced inward. The claws sink into the thick fabric, fibers visibly fraying and stretching around each claw tip. Dense dark brown shaggy bear fur surrounds the paw with individual hairs catching the light. Strands of dirt and dried bamboo grass debris cling to the claws. The texture of the rough leathery paw pad pressed hard against the pant leg, the underlying thigh muscle compressing under the weight. Damp dirt and trampled bamboo grass on the forest floor beneath. Dim cold afternoon light filtering through dense vegetation overhead, deep shadows under the conifer canopy. Shallow depth of field with razor focus locked on the claws sinking in. Visceral and raw documentary intensity. No blood visible, no graphic injuries shown. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 3 separate images.
```
→ **Google Flow動画プロンプト:**
```
A 5-second slow-motion documentary video footage on Daisengen-dake at the moment a massive Hokkaido brown bear's front paw drives down into a male hiker's right thigh. Camera holds steady in extreme close-up on the paw. Thick curved black claws extend forward and sink into the dark olive green hiking pant leg, fabric fibers tear and stretch frame by frame, dirt fragments and bamboo grass debris scatter from the impact. Dense dark brown shaggy fur ripples with the downward pressure. The paw pad presses hard against the leg, the thigh muscle compresses beneath. Damp forest floor visible just below. Dim cold afternoon light, deep shadows under the conifer canopy. No blood visible, no graphic injuries shown. Photorealistic, RED camera, slow-motion documentary cinematography.
```
SE: 「ザッ」という鈍い衣服が裂ける音、低い唸り声を遠くに重ねる
編集者指示: 5秒以内、クローズアップ→そのまま暗転。冒頭の引き込みカットなので即座のインパクト最優先。テロップなし。

---

押し返しても、押し返しても、ヒグマの首は一向に下がらない。

【制作メモ】ASSET-002 [AI動画 / Lovart or Google Flow]
シーン: 仰向けに倒された登山者の視点から見上げる、覆いかぶさるヒグマの黒い影。両手で必死に押し返す手のひらが画面手前に映る
プロンプト（16:9・フォトリアル・POV）:
```
First-person POV shot lying on the forest floor looking up at a massive dark silhouette of a brown bear looming overhead, with two human hands in dark hiking gloves pushing up against the bear's neck and chest. Dim canopy light behind the bear creating dramatic backlighting. Sense of weight and inescapable pressure. Photorealistic, shot on RED camera. Documentary style. 5-second motion. 16:9 aspect ratio. Generate 3 separate images.
```
SE: 喘ぐ息遣い、ヒグマの低い唸り声、手が触れ合う鈍い音
編集者指示: 5秒、徐々にヒグマの顔が近づく動き。視聴者を主観に置く演出。テロップなし。

---

残った武器は、刃渡りわずか5センチの山菜採り用ナイフ、ただ一本。

【制作メモ】ASSET-003 [背景静止画 / Lovart]
シーン: 小型の山菜採り用フォールディングナイフを定規と並べて撮影したマクロ写真。刃渡り5cmが視覚的に分かる
プロンプト（16:9・フォトリアル・マクロ）:
```
Extreme macro photography of a small folding pocket knife with a 5cm blade open, used for harvesting wild mountain vegetables. Beside it, a metric ruler clearly showing the 5cm measurement. Polished steel blade reflecting dim light, wooden handle, traditional Japanese style. Dark mossy forest floor background, slight blur. Photorealistic, shot on RED camera with macro lens. Documentary still. 16:9 aspect ratio. Generate 3 separate images.
```
SE: 静寂、わずかな金属音
編集者指示: 「刃渡り5cm」の白文字テロップを画面下にゆっくりフェードイン。次のフックへのつなぎ。

---

なぜ、このヒグマは人間に襲いかかってきたのか。

【制作メモ】ASSET-004 [背景静止画 / Lovart]
シーン: 薄暗い針葉樹林の登山道、霧がかった奥行きのある画。何かが潜んでいそうな不穏な雰囲気
プロンプト（16:9・フォトリアル）:
```
Dim, fog-shrouded narrow hiking trail through a dense Hokkaido coniferous forest. Tall trees lining both sides, mist hanging low between trunks, leaf litter on the path. Late autumn, overcast sky, low visibility about 10 meters ahead. Ominous quiet atmosphere, sense of unseen presence. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures visible. Empty trail only. Generate 3 separate images.
```
SE: 風がそよぐ音、遠くで枝が折れる音
編集者指示: 「なぜ、このヒグマは人間に襲いかかってきたのか。」のテロップを白文字で重ね、ナレーション同期で表示。

---

そして、なぜ、22歳の若者は土と木の枝に覆われた姿で見つかることになったのか。

【制作メモ】ASSET-005 [背景静止画 / Lovart]
シーン: 沢沿いに土砂と木の枝が散乱する地面、不穏なライティング。遺体は映さない（遺族配慮）
プロンプト（16:9・フォトリアル）:
```
A small ravine floor on Daisengen-dake covered with scattered fallen branches and disturbed earth and leaves. Suggestion of something hidden beneath but nothing graphic visible — only earth, twigs, dry leaves, and shadow. Damp, cold autumn light, eerie atmosphere. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No bodies, no figures, no people visible. Empty disturbed ground only. Generate 3 separate images.
```
SE: 静寂、わずかに沢の水音
編集者指示: 「22歳」「土と木の枝に覆われた姿」の2行テロップをゆっくりフェードイン。重い余韻を残す間（2秒程度）を空ける。

---

地形図とともに解説します。

【制作メモ】ASSET-006 [Google Earth]
シーン: Google Earthで北海道全域を上空から映し、渡島半島南端の大千軒岳にズームイン
GE座標（メインカメラ・Wikipedia確定値）: `41°34'46"N, 140°09'39"E`（大千軒岳山頂・標高1,071.87m）
カメラ高度: 開始時 50,000m（北海道全域） → ズームイン後 5,000m
カメラ角度: 開始時 真上 → ズームイン後 斜め45°、3D地形ON
ピン・ラベル:
- 大千軒岳 山頂: `41°34'46"N, 140°09'39"E`（標高1,072m）
- 奥二股登山口（東側・福島町・知内川コース）: 約 `41°33'00"N, 140°15'00"E`（概算・要GE実測）
- 旧道登山口（西側・上ノ国町方面・松前町石崎経由）: 約 `41°35'30"N, 140°07'30"E`（概算）
- 新道登山口（西側・松前町上川ルート）: 約 `41°36'00"N, 140°07'00"E`（概算）
→ 編集者指示: 北海道全域から渡島半島南端へ約4秒かけてズームイン。「大千軒岳 標高1,072m」のテロップを山頂ピンの横にフェードイン。テンポ重視で6秒以内に完結させる。

---

## 2. 屋名池さん入山（修正版.txt L13-L29）— ASSET-007〜015

---

2023年10月29日。

【制作メモ】ASSET-007 [画面エフェクト+SE]
シーン: 「2023年10月29日（日）」の日付テロップ。秋の落葉カレンダーが背景にうっすら
編集者指示: 白文字大きめの日付テロップを画面中央にフェードイン→数秒キープ→フェードアウト。
SE: カレンダーをめくる紙の音、続いて遠くで鳥の鳴き声

---

函館市港町に住む、屋名池奏人（やないけ かなと）さんは、朝早く登山へ出かけました。

【制作メモ】ASSET-008 [キャラアニメーション + 背景BG-C]
シーン: 函館市港町の住宅街の朝。CHAR-01（屋名池さん）が玄関を出て、登山ザックを背負い、車に向かう
キャラプロンプト（1:1）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. CHAR-01: A 22-year-old Japanese male university student carrying a green daypack, walking with calm determined expression toward a small car parked in front of a residential house. Wearing a navy blue hiking jacket. White background. 1:1 aspect ratio. Generate 3 separate images.
```
背景プロンプト（16:9・BG-C 再利用）:
```
Quiet residential street in Minato-cho, Hakodate city, Hokkaido, early autumn morning. Low-rise houses, narrow side streets, distant view of the harbor through gaps. Soft golden sunrise light, mist near the ground. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures visible. Generate 3 separate images.
```
編集者指示: 「函館市港町」のテロップを画面左下にフェードイン。CHAR-01が車に乗り込む動きを5秒程度。

---

22歳。北海道大学水産学部、海洋生物学科の4年生です。

【制作メモ】ASSET-009 [画面エフェクト + 背景静止画]
シーン: 「屋名池奏人さん 22歳 / 北海道大学水産学部 海洋生物学科4年」プロフィールテロップ。背景は北海道大学水産学部の校舎外観（函館キャンパス）
背景プロンプト（16:9）:
```
Exterior of Hokkaido University Faculty of Fisheries main building in Hakodate, autumn morning. Modern academic architecture, beige brick walls, large windows. Maple trees with red and yellow autumn leaves in front of the building. Clear blue sky. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures visible. Generate 3 separate images.
```
編集者指示: プロフィールテロップを画面右側に縦書きでフェードイン。校舎の外観に「北海道大学 水産学部 函館キャンパス」のロケーション説明を画面下に小さく重ねる。

---

大学の友人には、「大千軒岳に登ってくる」と伝えて出発したと報じられています。

【制作メモ】ASSET-010 [AI動画 / Lovart]
シーン: CHAR-01が友人と短く言葉を交わして玄関を出る後ろ姿。短いセリフ吹き出し「大千軒岳に登ってくる」が浮かぶ
キャラプロンプト（1:1）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes. CHAR-01 (22yo Japanese male student in navy blue hiking jacket with green daypack) viewed from behind, waving to a male friend in the doorway, walking away into morning light. Speech bubble above with text "大千軒岳に登ってくる". White background. 1:1 aspect ratio. Generate 3 separate images.
```
編集者指示: 5秒の動きアニメ。吹き出しのテキストをタイピングアニメで表示。BGMは穏やかな朝のトーン。

---

北海道新聞によると、この日の朝は穏やかな秋晴れで、絶好の登山日和。

【制作メモ】ASSET-011 [背景静止画 / Lovart]
シーン: 晴天の樹林帯、木漏れ日が差し込む登山道
プロンプト（16:9・フォトリアル）:
```
A peaceful sunlit hiking trail through a mixed broadleaf-coniferous forest in southern Hokkaido in late October. Clear autumn morning, warm golden sunlight filtering through colorful red and yellow autumn foliage. Empty trail winding ahead. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures visible. Empty trail only. Generate 3 separate images.
```
編集者指示: 「絶好の登山日和」のテロップを白文字でゆっくりフェードイン。穏やかなBGMで「これから始まる悲劇」との対比を意識。

---

屋名池さんの自宅から大千軒岳までは、車で片道3時間ほど。近くはないですが、日帰り可能な距離感です。

【制作メモ】ASSET-012 [Google Earth]
シーン: Google Earthで函館市から大千軒岳までのルートをライン表示
GE座標:
- 函館市港町（出発地）: 約 `41°47'00"N, 140°43'00"E`
- 大千軒岳 山頂（目的地）: `41°34'46"N, 140°09'39"E`
カメラ高度: 30,000m
カメラ角度: 斜め30°、3D地形ON
編集者指示: 函館市から大千軒岳まで赤いラインで結ぶ。「車で片道3時間」「距離 約100km」のテロップを画面に重ねる。ラインが流れるアニメーションで距離感を演出。

---

屋名池さんは登山口に車を停め、ひとり登山道に向かうことに。しかし、屋名池さんはその後、生きて帰ることはありませんでした。

【制作メモ】ASSET-013 [AI動画 / Lovart]
シーン: 登山ザックを背負ったCHAR-01の後ろ姿、樹林に消えていく
キャラプロンプト（1:1）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors. CHAR-01 (22yo male student with green daypack, navy blue jacket) viewed from behind, walking alone into a forest trail entrance, disappearing into the trees. Calm peaceful posture. White background. 1:1 aspect ratio. Generate 3 separate images.
```
背景プロンプト（16:9・BG-A 流用ベース）:
```
Wide shot of a forest trail entrance at Daisengen-dake parking area in autumn morning. A small car parked in the foreground gravel lot. Dense Sasa bamboo grass and coniferous trees beyond. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures visible. Empty entrance only. Generate 3 separate images.
```
編集者指示: 後ろ姿で森に消えていく動きを5秒。「生きて帰ることはありませんでした」のセリフ部分でBGMを一気に低音ダークに切り替え、画面をフェードブラックで暗転させる。重い余韻を3秒キープ。

---

屋名池さんと連絡がつかず、異変を感じる家族。すぐに松前警察署に通報することに。

【制作メモ】ASSET-014 [AI動画 / Lovart]
シーン: 夜の家庭の電話前、不安げな家族のシルエット。受話器を取り、松前警察署に電話
プロンプト（16:9・フォトリアル）:
```
A dimly lit family living room at night, a silhouetted figure of a parent holding a landline phone near their ear with worried posture. Faint warm interior lighting from a single lamp, the rest of the room in shadow. Empty dinner plate on the table untouched. Tense atmosphere. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No identifiable faces, silhouettes only. Generate 3 separate images.
```
編集者指示: 「松前警察署」のテロップ。電話の発信音→警察への通報音声をうっすら重ねる。5秒。

---

既に夜だったこともあり、捜索は明日となりました。

【制作メモ】ASSET-015 [背景静止画]
シーン: 夜の松前警察署、無線機の前で待機する警察官のシルエット
プロンプト（16:9・フォトリアル）:
```
Exterior or interior shot of Matsumae Police Station at night. Dim blue-tinted lighting, a silhouetted police officer near a radio communication console, looking out into the dark night through a window. Quiet tense waiting atmosphere. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No identifiable faces, silhouette only. Generate 3 separate images.
```
編集者指示: 「捜索開始は翌朝」のテロップ。BGMを静かなまま、低音で不安感を持続。

---

## 3. 10月30日 捜索開始（修正版.txt L31-L53）— ASSET-016〜026

---

10月30日（翌日）

【制作メモ】ASSET-016 [画面エフェクト + SE]
シーン: 「10月30日（翌日）」の日付テロップ。秋の朝陽
編集者指示: 日付テロップを画面中央に大きく表示→数秒キープ。
SE: 朝の鳥の鳴き声、カレンダーをめくる音

---

警察は朝から聞き取り調査や屋名池さんの登山届の確認を実施。

【制作メモ】ASSET-017 [AI動画]
シーン: 警察官が家族から事情を聞く取材場面（自宅にて）
プロンプト（16:9・フォトリアル）:
```
A police officer in uniform sitting at a kitchen table interviewing a family member, taking notes on a clipboard. Soft morning sunlight through the curtains. Serious concerned atmosphere. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. Faces obscured or shown from behind, no identifiable individuals. Generate 3 separate images.
```
編集者指示: 5秒。穏やかながら緊張感あるトーン。

---

ところが、屋名池さんは登山届を提出してないことが判明します。これでは、どのルートで入山したのか本人しかわかりません。

【制作メモ】ASSET-018 [画面エフェクト + 背景静止画]
シーン: 「登山届 → 未提出」の赤字テロップ。背景は空欄の登山届の用紙とペン
背景プロンプト（16:9・フォトリアル）:
```
Close-up of a blank Japanese mountain climbing notification form (登山届) on a wooden desk, a pen resting on the empty form, soft natural light from a window. Crisp document photography. 16:9 aspect ratio. Photorealistic, no people. Generate 3 separate images.
```
編集者指示: 「登山届 → 未提出」を赤字で画面中央に大きくフェードイン。ドキッとする効果音（短いノイズ音）。

---

屋名池さんが向かった大千軒岳は届出義務のない山です。

【制作メモ】ASSET-019 [背景静止画 + テキストオーバーレイ]
シーン: 大千軒岳の遠景（紅葉の山）＋「大千軒岳：登山届 義務なし」のテロップ
背景プロンプト（16:9・BG-D 流用ベース）:
```
Forested autumn mountains of southwestern Hokkaido viewed from a distance, Daisengen-dake silhouetted in the center under cloudy sky. Red and yellow autumn foliage on the slopes. Photorealistic, RED camera, aerial documentary style. 16:9 aspect ratio. No people. Generate 3 separate images.
```
編集者指示: 「大千軒岳：登山届 義務なし」のテロップを白文字でゆっくりフェードイン。

---

また北海道では現状、登山届の提出は義務ではなく、ただの推奨にとどまっています。罰則もありません。

【制作メモ】ASSET-020 [画面エフェクト / テキストオーバーレイ]
シーン: 「北海道：登山届 推奨のみ・罰則なし」のテキスト＋北海道全体図
背景: 北海道地図のシンプルなイラスト・グラフィック
編集者指示: 北海道の地図シルエットを画面右に、テキストを左に表示。「罰則なし」を赤太字で強調。

---

ちなみに、岐阜県や富山県の一部の指定山域では、登山届を提出しないと、最大5万円の過料が科せられます。

【制作メモ】ASSET-021 [画面エフェクト / 日本地図+テキスト]
シーン: 日本地図の岐阜県・富山県をハイライト。「過料 最大5万円」のテロップ
編集者指示: 日本地図上で岐阜・富山を赤くハイライト。「岐阜県 5万円以下の過料」「富山県 剱岳周辺（冬季）」のテキストを順に表示。BGMはニュース調。

---

警察は少しでも手がかりがないかと聞き込み調査を開始。しかし、なかなか有力な情報は得られません。

【制作メモ】ASSET-022 [AI動画]
シーン: 警察官が複数の住民・店主・釣り人に次々と聞き込みを続けるが、皆首を振る。日が傾き、警察官の表情に疲労が滲む時間経過モンタージュ
静止画プロンプト（16:9・フォトリアル）:
```
A police officer in dark uniform walking through a quiet rural town in southwestern Hokkaido in late autumn, approaching different local residents one after another — an elderly farmer in front of a small house, a shop owner outside a general store, a fisherman at a small harbor. Each resident shaking their head with apologetic gestures. Multiple sequential moments shown across the frame as a documentary photo essay. Long shadows of late afternoon, low warm sunlight, overcast sky with patches of pale blue. Officer's face shown from behind or in profile only, no identifiable individuals. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. Generate 3 separate images.
```
→ **Google Flow動画プロンプト:**
```
A 5-second documentary-style montage following a police officer in dark uniform walking through a rural Hokkaido town in late autumn. Quick sequential cuts: the officer questioning an elderly farmer (head shake), then a shop owner (apologetic gesture), then a fisherman at a small harbor (shrug). Each cut lasts about 1 second. Lighting subtly shifts from afternoon to dusk to show time passing. The officer's shoulders gradually sink with fatigue. Camera mostly handheld, slight motion. Officer always seen from behind or in profile, no identifiable faces. Photorealistic, RED camera, documentary style.
```
編集者指示: 5秒。3カット程度のモンタージュで時間経過を表現。BGMはゆっくりとした寂寥感のあるピアノ。最後のカットで警察官の手帳に「？」マークだけが増えていくインサートを編集で追加。「有力な情報なし」のテロップを最後にフェードイン。

---

一見、登った山は分かっているので、登山ルートが不明でも簡単に捜索できるのでは？と思われるかもしれません。しかし、実際はそうではありません。

【制作メモ】ASSET-023 [Google Earth / 概観]
シーン: 大千軒岳を真上から見下ろし、3つの登山ルートが伸びる様子を概観表示
GE座標（メインカメラ）: `41°34'46"N, 140°09'39"E`（大千軒岳山頂）
カメラ高度: 8,000m
カメラ角度: 真上→徐々に斜め45°へ
編集者指示: 真上カメラから徐々に斜めに傾ける動き。「ルートは3つ」のテロップをフェードイン。次のASSET-024へつなぐための導入カット。

---

大千軒岳の登山ルートは全部で3つあり、 東の福島町と西の上ノ国町の登山口は、30km以上離れています。

【制作メモ】ASSET-024 [Google Earth / 3ルート明示]
シーン: 3つの登山口を全てピンで表示し、ルートを色分け
GE座標:
- 大千軒岳 山頂: `41°34'46"N, 140°09'39"E`
- 奥二股登山口（東・福島町・知内川コース）: 約 `41°33'00"N, 140°15'00"E`
- 旧道登山口（西・松前町石崎経由）: 約 `41°35'30"N, 140°07'30"E`
- 新道登山口（西・松前町上川ルート）: 約 `41°36'00"N, 140°07'00"E`
カメラ高度: 10,000m
カメラ角度: 斜め30°、3D地形ON
編集者指示: 各登山口を異なる色のピン（東=赤、西新道=青、西旧道=緑）でマーク。各ルートを点線で山頂までつなぐ。「東の福島町」と「西の上ノ国町」の登山口の間に「直線距離 約30km」のテロップを表示。

---

車で移動しても1時間以上かかるうえ、どのルートで登ったとしても往復6、7時間はかかる道のりです。

【制作メモ】ASSET-025 [Google Earth + テキストオーバーレイ]
シーン: 前カットのGE映像に「車1時間以上 / 往復6-7時間」のテロップ重ね
編集者指示: 前ASSET-024のGE映像を継続させ、テロップで時間情報を順に表示。時計のアイコンと組み合わせて視覚的に。

---

運良く屋名池さんが入山したルートから捜索できればいいのですが、もし違った場合は大幅な時間ロス。

【制作メモ】ASSET-026 [Google Earth + アニメーション]
シーン: 3つのルートに「？」マークが点滅し、捜索の困難を視覚化
編集者指示: GE上で3つのルートに順番に「？」マークを点滅表示。「ルート絞り込み困難」のテロップ。BGMで緊迫感を強調。
※（ユーザー要望L73「捜索予定のルートが分かっていれば、そこの座標を表示」については、屋名池さんは奥二股登山口から入山したことが後で判明するため、本カットでは「未確定」状態として演出。確定後（ASSET-029）で奥二股ピンを強調する形に繋ぐ。

---

結局、初日は丸一日以上、屋名池さんの登山ルートの絞り込みの時間に費やされることとなりました。

【制作メモ】ASSET-027 [画面エフェクト + 背景]
シーン: 時計の針が早回しで進む。書類が山積みの机
背景プロンプト（16:9・フォトリアル）:
```
A desk piled with documents, maps, and a phone in a police station office. A wall clock in the background showing time passing rapidly (or motion blur on the hands). Late afternoon to evening lighting transition. Photorealistic, documentary style. 16:9 aspect ratio. No people. Generate 3 separate images.
```
編集者指示: 時計の早回しエフェクト。「丸一日以上」のテロップ。徒労感のあるBGM。

---

## 4. 車発見・夜の断念（修正版.txt L55-L64）— ASSET-028〜032

---

翌日（10月31日）午後7時ごろ、事態が進展します。

【制作メモ】ASSET-028 [画面エフェクト + SE]
シーン: 「10月31日 午後7時」の時刻テロップ。夜の闇
編集者指示: 時刻テロップを画面中央に表示。SE: 静寂から無線機のノイズ音が入る。

---

東の福島町、奥二股登山口あたりで無人の車を発見。

【制作メモ】ASSET-029 [AI動画 / Lovart + Google Flow]
シーン: 夜の奥二股登山口駐車場、警察車両のヘッドライトが無人の小型乗用車を照らし出す発見の瞬間（人物は映さず、車と光のみで緊張感を出す）
GE参考座標: 奥二股登山口 約 `41°33'00"N, 140°15'00"E`
静止画プロンプト（16:9・フォトリアル）:
```
A remote gravel parking area at the Okufutamata trailhead in rural southwestern Hokkaido at night, deep in late autumn. A police patrol vehicle's headlights cutting through the darkness, illuminating an abandoned small civilian car parked alone in the lot. Handheld flashlight beams scanning the empty car from off-frame. Cold autumn night, breath-like vapor faintly visible in the cold air, frost on the ground. Dense black silhouettes of cedar and birch forest surrounding the lot. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty scene only. Generate 3 separate images.
```
→ **Google Flow動画プロンプト:**
```
A 5-second documentary night scene at a remote mountain trailhead parking area in Hokkaido. The camera starts in near darkness, then a police patrol vehicle's headlights slowly sweep across the gravel lot, gradually revealing an abandoned small civilian car. Off-frame flashlight beams scan the empty driver's seat through the windshield. Breath-like vapor faintly visible in the cold night air. Slow, tense pacing. No people visible in frame, only the car and the moving lights. Photorealistic, RED camera, documentary style.
```
編集者指示: 5秒。冒頭1秒は暗闇、ヘッドライトが車を照らし出す瞬間に「無人の車を発見」のテロップを衝撃音とともにフェードイン。BGMは緊張感のある低音ドローン。最後に懐中電灯の光が車内（空席）を映すアップで締める。次ASSET-030（実写写真）への引き。

---

それはまさしく、屋名池さん本人の車でした。
（実際の画像を使用）

【制作メモ】ASSET-030 [実写画像 / 報道スクショ]
シーン: 屋名池さんの車（ユーザー要望に基づき、報道写真の実写を使用）
編集者指示: 公開されている報道写真または車種が分かる実写画像を使用。プライバシー配慮でナンバープレートはモザイク必須。出典クレジット（HBC・北海道新聞等）を画面下に小さく表示。
※ユーザー要望（L60「実際の画像を使用」）に従う。

---

車が数日間、登山口に残され音信不通。全員の頭に、最悪の事態がよぎりました。

【制作メモ】ASSET-031 [AI動画 / Lovart]
シーン: 警察官・家族のシルエットが顔を見合わせる、悲痛な表情
プロンプト（16:9・フォトリアル）:
```
Silhouettes of police officers and family members standing near the abandoned car at night, exchanging concerned glances. Headlights creating dramatic backlight. Heavy quiet atmosphere. Photorealistic, documentary style. 16:9 aspect ratio. Faces not visible, silhouettes only. Generate 3 separate images.
```
編集者指示: 「最悪の事態」のテロップを赤字でゆっくりフェードイン。BGMを一段ダークに。

---

既に日が暮れていることもあり、この日の捜索はここで断念することに。

【制作メモ】ASSET-032 [背景静止画]
シーン: 夜の登山口、奥二股駐車場の風景。月光と懐中電灯
プロンプト（16:9・フォトリアル）:
```
Wide nighttime shot of Okufutamata trailhead parking area surrounded by dark forest. Faint moonlight breaking through clouds. A single police vehicle's tail lights leaving the scene. Cold, isolated atmosphere. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. No people. Generate 3 separate images.
```
編集者指示: 「この日の捜索は断念」のテロップを下部に表示。フェードアウトで翌日へ繋ぐ。

---

## 5. 10月31日 消防士襲撃日（修正版.txt L66-L191）— ASSET-033〜075

---

10月31日、火曜日（行方不明から2日目）

【制作メモ】ASSET-033 [画面エフェクト]
シーン: 「10月31日 火曜日 / 行方不明から2日目」の日付＋日数テロップ
編集者指示: 日付＋経過日数を画面中央にフェードイン。BGMは緊迫感を保つ。

---

実はこの日、屋名池さん捜索とは別に、大千軒岳では地元の消防士にも、ある任務が組まれていました。

【制作メモ】ASSET-034 [AI動画]
シーン: 消防署で出発準備をする消防士3人のシルエット
プロンプト（16:9・フォトリアル）:
```
Interior of a small rural fire station early in the morning. Three firefighter silhouettes preparing hiking gear, checking backpacks. Warm interior fluorescent lighting. Tense routine atmosphere. Photorealistic, RED camera, documentary style. 16:9 aspect ratio. Faces not yet shown clearly. Generate 3 separate images.
```
編集者指示: 「消防士に組まれた、ある任務」のテロップ。視聴者の好奇心を引く演出。

---

それは、登山道の点検です。

【制作メモ】ASSET-035 [画面エフェクト + 背景BG-A]
シーン: 「登山道の点検」のテロップ＋笹薮の登山道（BG-A 流用）
背景プロンプト（16:9・BG-A 再利用）:
```
Narrow mountain hiking trail on Daisengen-dake, dense Sasa bamboo grass walls on both sides. Empty trail. Photorealistic, RED camera. 16:9. Generate 3 separate images.
```
編集者指示: テロップ「登山道の点検」を大きく表示。

---

大千軒岳は山岳遭難が多発するルートがあるので、事前に問題がないかチェックをしていたのです。
（捜索予定のルートが分かっていれば、そこの座標を表示）

【制作メモ】ASSET-036 [Google Earth]
シーン: 消防士3人が点検した登山道ルート（おそらく奥二股ルート）を地形図で表示
GE座標:
- 奥二股登山口: 約 `41°33'00"N, 140°15'00"E`
- 7合目襲撃地点（標高約550m）: 概算 `41°33'30"N, 140°13'30"E`（実測要・概算）
- 大千軒岳 山頂: `41°34'46"N, 140°09'39"E`
カメラ高度: 3,000-5,000m
カメラ角度: 斜め40°、3D地形ON
編集者指示: 奥二股登山口から山頂までのルートを赤いラインで結ぶ。7合目（標高550m）地点を黄色ピンで強調。「点検ルート 約6km」「往復約7時間」のテロップ。
※（ユーザー要望L73）について: 消防士3人の点検ルートは奥二股からの知内川コースが報道で確認可能。

---

担当は、福島消防署勤務の大原巧海（おおはら たくみ）さん、41歳。

【制作メモ】ASSET-037 [キャラアニメーション]
シーン: CHAR-02（大原さん）の登場。プロフィールテロップ「大原巧海さん 41歳 / 福島消防署」
キャラプロンプト（1:1・CHAR-02 初登場）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes. CHAR-02: A 41-year-old Japanese male firefighter, muscular tough build, short black hair, wearing dark olive green hiking jacket and a tactical backpack, holding a small folding knife visible at his belt. Standing front-facing with strong determined expression. White background. 1:1 aspect ratio. Generate 3 separate images.
```
編集者指示: プロフィールテロップを画面下に表示。CHAR-02のキャラ画像を画面右側に大きめに配置。

---

同じく福島消防署の阿部達也（あべ たつや）さん、36歳。

【制作メモ】ASSET-038 [キャラアニメーション]
シーン: CHAR-03（阿部さん）の登場。プロフィールテロップ
キャラプロンプト（1:1・CHAR-03 初登場）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors. CHAR-03: A 36-year-old Japanese male firefighter, average athletic build, short black hair, wearing dark red hiking jacket and black daypack. Composed serious expression. Front-facing. White background. 1:1 aspect ratio. Generate 3 separate images.
```
編集者指示: プロフィールテロップを画面下に表示。

---

そして、知内消防署勤務の船板克志（ふないた かつし）さん、41歳の計3名。

【制作メモ】ASSET-039 [キャラアニメーション]
シーン: CHAR-04（船板さん）の登場 + 3人並びの構図
キャラプロンプト（1:1・CHAR-04 初登場）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors. CHAR-04: A 41-year-old Japanese male firefighter, broad-shouldered tough build, short black hair with slight gray, wearing dark navy blue hiking jacket and green daypack. Steady experienced expression. Front-facing. White background. 1:1 aspect ratio. Generate 3 separate images.
```
3人並び構図:
```
Three Japanese firefighters CHAR-02, CHAR-03, CHAR-04 standing side by side in their respective hiking gear, white background, cartoon style consistent with previous CHARs. Generate 3 separate images, each showing these 3 characters together.
```
編集者指示: 3人並びの集合カットを最後に表示。「計3名」のテロップ。

---

3人とも、登山経験のある現役の消防士です。ただ、登山経験は、全員それほど多くはありませんでした。

【制作メモ】ASSET-040 [画面エフェクト + キャラ流用]
シーン: 3人並びの構図に「登山経験：多くない」のテキストを重ねる
編集者指示: 「現役消防士」「ただし登山経験は浅め」の対比テロップ。3人並びのキャラアニメ画像（ASSET-039 再利用）を流用。

---

実は、この登山計画は1年前から、進めていましたが、

【制作メモ】ASSET-041 [背景静止画 + 画面エフェクト]
シーン: カレンダーに「1年前」とテロップ。机の上の登山計画書
背景プロンプト（16:9・フォトリアル）:
```
A planning desk with a hiking map of Daisengen-dake, a calendar marked with circled dates, and a notebook with handwritten plans. Soft warm interior lighting. Documentary still. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「1年前から計画」のテロップ。

---

なかなか3人の予定が合わず、実現できなかったのです。

【制作メモ】ASSET-042 [画面エフェクト]
シーン: 3人のスケジュール表が交錯し、空きがない様子をアニメ表現
編集者指示: 「予定が合わず」のテロップ。スケジュール表が×印で埋まるアニメ。

---

そこから月日は流れ、3人の予定が空いたことで、今回の登山が実現しました。

【制作メモ】ASSET-043 [画面エフェクト]
シーン: カレンダーがめくれて、10月31日に丸印が付く
編集者指示: 「ついに実現」のテロップ。日付に赤丸でハイライト。

---

3人は出発2週間前から、ヤマップというアプリで、大千軒岳の最新情報をチェック。

【制作メモ】ASSET-044 [AI動画 / スマホ画面]
シーン: スマートフォンの画面に登山アプリが表示され、大千軒岳の最新情報をスクロール
プロンプト（16:9・フォトリアル）:
```
Close-up of a smartphone screen displaying a hiking app interface with a map of Daisengen-dake mountain, recent activity logs, and bear sighting alerts in Japanese text. Hands holding the phone. Soft indoor lighting. Photorealistic, documentary style. 16:9 aspect ratio. Generate 3 separate images.
```
編集者指示: アプリ画面はモザイク不要（一般的なUI想定）。「最新情報チェック」のテロップ。

---

クマのフンの跡があったという目撃情報も、しっかりと把握。

【制作メモ】ASSET-045 [画面エフェクト + 背景静止画]
シーン: アプリの目撃情報投稿画面に「クマのフンの跡」の文字。背景に実際のフン痕跡のイメージ
背景プロンプト（16:9・フォトリアル）:
```
Bear scat (droppings) discovered on a forest trail in autumn, scientific documentary photography style, soft natural light. Photorealistic, RED camera. 16:9 aspect ratio. No people. Generate 3 separate images.
```
編集者指示: 「クマのフンの跡 目撃情報あり」の赤字テロップ。視聴者に「危険を認識しつつ登った」点を強調。

---

しかし、3人ともクマスプレーは1つも準備していませんでした。

【制作メモ】ASSET-046 [画面エフェクト + 商品写真]
シーン: 「クマスプレー：所持なし」の×マークテロップ。背景にクマスプレー製品の参考画像
背景プロンプト（16:9・フォトリアル）:
```
Bear spray canister product photography on a neutral background, with a large red X mark or "NONE" overlay. Sharp product shot. 16:9. Generate 3 separate images.
```
編集者指示: 「クマスプレー 0本」の赤字を画面中央に大きく表示。視聴者に決定的な準備不足を伝える。ドキッとする効果音。

---

というのも、急遽登山が決まり、買いに行く時間がありませんでした。

【制作メモ】ASSET-047 [AI動画]
シーン: ホームセンターのクマスプレー陳列棚（空き状態）、または時計が早く進む
プロンプト（16:9・フォトリアル）:
```
A retail shelf display with empty space where bear spray products would be, store interior. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「時間なし」「準備不足」のテロップ。やや残念感のある演出。

---

代わりに、大原さんが持っていたのは、刃渡り5センチの山菜採り用ナイフ。

【制作メモ】ASSET-048 [背景静止画 / ASSET-003 流用検討]
シーン: ASSET-003（5cmナイフのマクロ写真）を再利用 or 別アングルで再撮
編集者指示: ASSET-003と同じナイフ画像を再利用可能。新規撮影する場合は手に持って構えるアングルで違いを出す。「刃渡り 5cm」のテロップ。
※（再利用メモ）ASSET-003と同じナイフのため、素材コスト削減のため流用推奨。

---

実はこのナイフ、今年の山菜採りで、大原さんが50メートル先のクマを目撃した経験から、念の為ホームセンターで購入したものでした。

【制作メモ】ASSET-049 [回想シーン / AI動画]
シーン: 春の山菜採り中、50m先の藪からクマがチラッと姿を見せる回想。大原さんが驚いて固まる
キャラプロンプト（1:1）:
```
Cute cartoon character design. CHAR-02 (Ohara, 41yo firefighter in casual outdoor clothes, not in firefighter gear) crouching in a bamboo grass area picking wild edible plants, suddenly looking up with shocked expression toward a distant bear silhouette in the background. White background. 1:1. Generate 3 separate images.
```
背景プロンプト（16:9・回想・色調セピア）:
```
A spring mountain bamboo grass field with wild edible plants growing. A distant brown bear silhouette barely visible 50 meters away through the bamboo. Sepia-toned warm vintage tinted lighting (flashback effect). Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「回想・今年春」のテロップ。色調をセピアに（回想エフェクト）。「50m先にクマ」のテロップ。3秒で次のカット（ホームセンターでナイフ購入）に切り替える小演出。

---

3人のルートとしては、12時に頂上、夕方には下山して帰宅という登山計画で進めることに。

【制作メモ】ASSET-050 [Google Earth + テキスト計画表]
シーン: GE上に登山予定タイムテーブルを重ねる
GE座標: 奥二股登山口→7合目→山頂のルート（ASSET-036 流用ベース）
編集者指示: 画面右に計画表テロップ「8:30 登山開始」「10:30 7合目通過」「12:00 山頂到着」「16:00 下山完了」を順に表示。
※（再利用メモ）ASSET-036のGEルートマップを流用してテキストオーバーレイで対応可能。

---

午前10時半ごろ。

【制作メモ】ASSET-051 [画面エフェクト + SE]
シーン: 「午前10時半」の時刻テロップ
編集者指示: 時刻テロップを画面中央。SE: 鳥の鳴き声、登山靴で笹薮を踏む音。

---

3人は7合目付近、標高およそ550メートルの登山道に到着。

【制作メモ】ASSET-052 [キャラアニメーション + 背景BG-A]
シーン: CHAR-02・03・04の3人が笹に囲まれた登山道で立ち止まる
キャラプロンプト（1:1）:
```
Three Japanese firefighters CHAR-02, CHAR-03, CHAR-04 in hiking gear standing on a narrow trail, taking a brief break. CHAR-02 in front, CHAR-03 in middle, CHAR-04 (Funaiita) slightly behind. Cartoon style consistent. White background. 1:1. Generate 3 separate images, each showing these 3 characters together.
```
背景プロンプト（16:9・BG-A 再利用）:
```
Narrow mountain trail on Daisengen-dake at 7th station, 550m elevation, dense bamboo grass walls. Photorealistic. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「7合目 標高550m」のテロップを画面下に表示。
※（再利用メモ）BG-Aの登山道背景は今後の襲撃シーン（ASSET-053以降）まで継続使用するため、複数バリエーション生成推奨。

---

大千軒岳の登山道は、身長よりも高い笹に覆われた、見通しの悪い道です。

【制作メモ】ASSET-053 [背景静止画 / BG-A 強調版]
シーン: 笹が背丈を超え、3m先が見えない登山道。視点ローアングル
プロンプト（16:9・フォトリアル）:
```
Eye-level POV of a narrow hiking trail completely walled by tall dense Sasa bamboo grass exceeding human height on both sides. Visibility limited to about 3 meters ahead. Damp dim autumn light filtering through. Claustrophobic atmosphere. Photorealistic, RED camera. 16:9. No people, no figures. Generate 3 separate images.
```
編集者指示: 「視界3m」のテロップ。視聴者に「何が潜んでいるか分からない」感覚を伝える。

---

3人は一旦休憩のため、その場で立ち止まることに、

【制作メモ】ASSET-054 [キャラアニメーション]
シーン: 3人が休憩する。CHAR-04（船板さん）はやや後方
キャラプロンプト（1:1）:
```
Three Japanese firefighters CHAR-02, CHAR-03 in front taking a short break, drinking water. CHAR-04 slightly behind them, also resting. Slight casual posture. Cartoon style. White background. 1:1. Generate 3 separate images, each showing these 3 characters together.
```
編集者指示: 「休憩」のテロップ。穏やかなBGMを保ちつつ、視聴者には次の急展開への伏線として静けさを演出。

---

そのときです。

【制作メモ】ASSET-055 [画面エフェクト + SE]
シーン: 暗転＋緊張感の効果音
編集者指示: 一瞬の暗転（黒画面 0.3秒）→「そのときです。」のテキストを白文字で大きく表示。SE: ドンと低い心拍音。

---

少し下の登山道、距離およそ20メートル先。

【制作メモ】ASSET-056 [背景BG-A + 距離マーカー]
シーン: 登山道の下方にカメラが向く。20mのスケール感を強調
編集者指示: 「20m先」のテロップ＋赤い矢印で下方を指す。視点をゆっくりパンダウン。

---

笹の中から、のっそりと、毛むくじゃらの大きなヒグマが姿を現したのです。

【制作メモ】ASSET-057 [キャラアニメーション / CHAR-05 初登場]
シーン: 笹薮からヒグマ（CHAR-05）がのっそりと現れる
キャラプロンプト（1:1・CHAR-05 初登場）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors. CHAR-05: A young male Hokkaido brown bear, 125cm body length, muscular build, dark brown fur, intense unafraid eyes, emerging from dense bamboo grass, standing on all fours. Front-facing slightly. White background. 1:1. Generate 3 separate images.
```
背景プロンプト（16:9・BG-A 再利用）:
```
Bamboo grass area on Daisengen-dake trail, viewed from above looking down at a section of the path. Photorealistic. 16:9. No people. Generate 3 separate images.
```
編集者指示: ヒグマが笹から姿を現す動きを5秒のアニメで。BGMを一気にダークに切り替え。

---

体長およそ1.7メートル。若いオスのヒグマ。

【制作メモ】ASSET-058 [画面エフェクト + キャラ流用]
シーン: ヒグマのスケール表示（1.7m）。CHAR-05の画像に身長スケールを重ねる
編集者指示: ヒグマの横に1.7mのスケールバーをグラフィック表示。「若いオス」のテロップ。
※CHAR-05画像（ASSET-057）流用可能。

---

通常、野生のヒグマは、人間の集団の存在を察知すると一目散に逃げ去ります。

【制作メモ】ASSET-059 [AI動画 / 一般的なクマの行動]
シーン: 一般的なヒグマが人の気配で逃げていく様子（参考映像）
プロンプト（16:9・フォトリアル）:
```
A typical wild brown bear in a Hokkaido forest, looking up alert, then turning and quickly running away into the deep forest. Natural daylight, documentary style. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「通常は逃げる」のテロップ。「→ しかし」と次のカットへ繋ぐ伏線。

---

ところが、目の前のヒグマは一切逃げる様子はありませんでした。

【制作メモ】ASSET-060 [キャラ流用 + 強調]
シーン: CHAR-05が逃げず、3人を見つめる
編集者指示: CHAR-05画像（ASSET-057流用）に「逃げない」の赤字テロップ。BGMでさらに緊張を高める。

---

船板さんは、この時の状況について、「実は、私は2人からちょっとだけ遅れて登っていました」「ホイッスルも、その時は鳴らしていなかった」

【制作メモ】ASSET-061 [証言テロップ + キャラ]
シーン: CHAR-04（船板さん）の顔アップ＋証言テロップ
キャラプロンプト（1:1・CHAR-04 アップ）:
```
Close-up portrait of CHAR-04 (Funaiita) in serious reflective expression, head-and-shoulders framing. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「船板さん 証言」のキャプション。証言は引用符付きで画面下に2行ずつ表示。テロップタイピング演出。

---

「ふと振り返ったときに、カーブのところから、クマが四つ足でのそのそ歩いているのが見えた」「音もせず、私には猫が忍び寄ってくるように感じられました」と語っています。

【制作メモ】ASSET-062 [回想視点 / POV]
シーン: 船板さんの視点で振り返るPOV。カーブの先からヒグマがゆっくり歩いてくる
プロンプト（16:9・フォトリアル・POV）:
```
First-person POV looking back over the shoulder along a curved trail, seeing a brown bear walking on all fours, slowly approaching from around a bend, partially obscured by bamboo grass. Eerily silent approach. Photorealistic, RED camera, documentary style. 16:9. No human figures visible from this POV. Generate 3 separate images.
```
編集者指示: 「猫のように忍び寄る」のテロップ。BGMに微かな足音SEを重ねる。

---

船板さんがヒグマの存在に気づいた時、5メートルほどの距離だったといいます。

【制作メモ】ASSET-063 [画面エフェクト / スケール表示]
シーン: 「距離 5m」の表示。緊迫を伝える視覚化
編集者指示: 「5m」の大きな赤字テロップを画面中央に。視聴者に「もう逃げられない距離」感を伝える。

---

一方の大原さんもこの時の状況について、「クマが近づいていることには、全く気がつかなかった」「いつから、つけられていたのだろう、という感じだった」と振り返ります。

【制作メモ】ASSET-064 [証言テロップ + キャラ]
シーン: CHAR-02（大原さん）の顔アップ＋証言テロップ
キャラプロンプト（1:1・CHAR-02 アップ）:
```
Close-up portrait of CHAR-02 (Ohara) in serious reflective expression, head-and-shoulders framing. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「大原さん 証言」のキャプション。証言テロップを2行ずつ。

---

ヒグマと遭遇してしまった3人は慌てて、「おい！！！」と大声で威嚇。

【制作メモ】ASSET-065 [キャラアニメーション]
シーン: 3人が口を開けて大声を出す。ヒグマは怯まず
キャラプロンプト（1:1）:
```
Three firefighters CHAR-02, CHAR-03, CHAR-04 shouting loudly with hands raised, facing toward CHAR-05 (the bear) in the foreground. Tense action pose. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「おい！！！」を吹き出しで大きく表示。SE: 男性の叫び声。

---

その後、救助要請のために使われる火薬式の発射器である信号ピストルを3発、発砲。

【制作メモ】ASSET-066 [画面エフェクト + 商品+効果]
シーン: 信号ピストルの説明＋発砲シーン
プロンプト（16:9・フォトリアル）:
```
Close-up of a signal flare pistol (used for emergency rescue calls in mountains) being fired into the air, producing a bright red flare and loud crack. Daylight forest background. Photorealistic, RED camera. 16:9. Hand visible holding the pistol, no full body. Generate 3 separate images.
```
編集者指示: 「信号ピストル / 火薬式」の説明テロップ。発砲音SE（3回）と赤い閃光エフェクト。

---

強い破裂音や赤い閃光を発するにもかかわらず、ヒグマは全く逃げなかったのです。

【制作メモ】ASSET-067 [キャラ流用 + 強調]
シーン: CHAR-05が閃光と音にも動じず、3人を見続ける
編集者指示: 「ピストルも無効」のテロップ。視聴者に「装備が通用しない」事実を強調。ドキッとするBGM変化。

---

それどころか、ヒグマは猛スピードで襲ってきました。

【制作メモ】ASSET-068 [キャラアニメーション]
シーン: CHAR-05が3人に向かって突進する
キャラプロンプト（1:1）:
```
CHAR-05 (young male bear) charging forward at high speed, four legs running, mouth slightly open showing teeth, intense aggressive expression. Motion blur effect. White background. Cartoon style. 1:1. Generate 3 separate images.
```
編集者指示: 突進シーンを5秒のアニメで。SE: 重い足音、唸り声。BGMでパニック感を最大化。

---

真っ先に襲われたのは船板さん。

【制作メモ】ASSET-069 [キャラアニメーション]
シーン: CHAR-04（船板さん）が突き飛ばされ、仰向けに転倒
キャラプロンプト（1:1）:
```
CHAR-04 (Funaiita) being slammed backward by CHAR-05 (bear), falling on his back on the trail. CHAR-05 mounting him with paws pressing down on his shoulders. Cartoon style, intense action pose, no blood shown. White background. 1:1. Generate 3 separate images.
```
編集者指示: 衝撃シーン。「真っ先に襲われたのは船板さん」のテロップ。

---

突き飛ばされ、仰向けに転倒。100キロを超えるヒグマが、馬乗りとなり、首元を噛みつかれそうになります。

【制作メモ】ASSET-070 [キャラ + 視点切替]
シーン: 仰向け視点（ASSET-002と類似）。馬乗りのCHAR-05
編集者指示: 「100kg超」「馬乗り」のテロップ。ASSET-002のPOV映像が再利用可能（フックで使用）。
※（再利用メモ）ASSET-002（仰向け視点）の素材を流用可能。視点POVが完全一致するため。

---

船板さんは、「クマの左手の爪で、右太ももを引っかかれるように引きずり倒された」

【制作メモ】ASSET-071 [AI動画 / Lovart + Google Flow]
シーン: ヒグマの左前足の爪が船板さんの右太ももを引っかき、横方向に引きずり倒す瞬間。船板さんの証言を実写ドキュメンタリー風に映像化。流血表現は避け、ズボンの破れと土埃で表現
静止画プロンプト（16:9・フォトリアル）:
```
A young male Hokkaido brown bear (Ursus arctos yesoensis), 125cm body length, muscular well-fed build weighing over 100kg, dark brown shaggy fur with a slightly lighter muzzle, uses its left front paw with extended sharp dark claws to hook into the right thigh of a fallen Japanese male firefighter (41-year-old, broad-shouldered tough build, short black hair with slight gray at temples, tan skin tone, dark navy blue hiking jacket, brown cargo pants with the right thigh visibly torn at the hook point), dragging him sideways along the damp dirt trail. The firefighter twists on the ground, hands clawing desperately at the dirt, face contorted in extreme pain, mouth open in a silent gasp. Dense tall Sasa bamboo grass walls flanking both sides of the narrow trail at Daisengen-dake. Cold overcast late autumn afternoon light, deep shadows under the conifer canopy. Dirt and fallen leaves scattering from the dragging motion. No blood visible, no graphic injuries shown — only the bear's claws hooking the torn pants and the man being pulled. Photorealistic, shot on RED camera. Documentary wildlife style, raw unfiltered tension. 16:9 aspect ratio. Generate 3 separate images.
```
→ **Google Flow動画プロンプト:**
```
A 5-second slow-motion documentary video footage from a first-person POV at Daisengen-dake in late autumn. The camera is positioned at the eye level of a Japanese male firefighter lying flat on his back on a damp dirt mountain trail. Opening frame: the firefighter's own legs in brown cargo pants visible in the lower frame, his hands visible in the foreground palms-down on the dirt. A large young male Hokkaido brown bear with dark brown shaggy fur enters from the upper edge of the frame, head lowered. Action sequence unfolds in continuous motion: the bear advances directly toward the camera with deliberate predatory steps, head pushed forward, mouth wide open exposing massive sharp white fangs and bared gums in a ferocious snarl. The bear's intense eyes lock directly on the viewer, drawing closer and closer until its open jaws fill the upper portion of the frame, just inches away from the camera as if about to bite down. The camera shakes slightly from the firefighter's heavy breathing. Dense bamboo grass walls visible flanking the trail, cold overcast afternoon light, faint swirling mist. No blood visible, no graphic injuries shown — the threat suggested only by proximity, bared fangs, and the bear's predatory intent. Photorealistic, shot on RED camera, slow-motion documentary cinematography.
```
編集者指示: 5秒。1秒目: 仰向けPOV視点、ヒグマがフレーム上部に登場 → 2〜4秒目: ヒグマがゆっくりと正面に迫り、口を大きく開けて牙を見せる → 5秒目: 牙がフレーム上部いっぱいに広がり噛みつき直前で止まる。証言テロップを画面下に1行タイピング演出で表示:
- 「私には猫が忍び寄ってくるように感じられた」（前ASSET-062の証言と連動）
キャプション「船板克志さん 証言」を画面右上に固定表示。SE: ヒグマの低い唸り声が次第に大きくなる、船板さんの荒い息遣い、心拍音、噛みつき直前で全音カット（無音の衝撃）。BGMは前ASSETの心拍音を継続しつつ、最後の瞬間に低音ヒット。

---

「両足を使って、足を突っ張り、クマの顎を蹴り上げた」と当時を振り返っています。

【制作メモ】ASSET-072 [キャラアニメーション]
シーン: CHAR-04が両足でCHAR-05の顎を蹴り上げる
キャラプロンプト（1:1）:
```
CHAR-04 (Funaiita) on his back using both legs to kick upward at CHAR-05 (bear)'s jaw, struggling defensively. Action pose. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 蹴り上げの動きを5秒。「両足で顎を蹴り上げ」のテロップ。

---

それでも、右太ももをヒグマに噛まれ、首も噛まれます。

【制作メモ】ASSET-073 [画面エフェクト + 黒シルエット]
シーン: 噛まれる瞬間（直接描写は避けて、シルエット化）
プロンプト（16:9）:
```
Stylized silhouette dark shadow scene of a bear figure biting at a fallen human figure, shown only in pure black silhouettes against a deep red dramatic background. Symbolic representation, not graphic. 16:9. Generate 3 separate images.
```
編集者指示: 直接的な描写を避け、シルエットで象徴的に。「右太もも噛まれ / 首噛まれ」のテロップ。BGMで衝撃を補完。

---

揉み合っている間、ヒグマは低く唸り声を上げ続けていたといいます。

【制作メモ】ASSET-074 [SE強調 + 背景]
シーン: 笹薮の中、唸り声がこだまする音響演出メイン
編集者指示: 視覚は控えめ（BG-A流用）、SE: 低く長いヒグマの唸り声をループ。「低い唸り声」のテロップ。

---

さらに、揉み合いの最中、所持していた信号ピストルが破壊され絶体絶命のピンチ。

【制作メモ】ASSET-075 [背景静止画 + 緊迫演出]
シーン: 破壊された信号ピストルが地面に転がる
プロンプト（16:9・フォトリアル）:
```
Close-up of a broken signal flare pistol lying on the damp forest floor. The orange plastic frame is cracked and split along the side, the barrel bent at an unnatural angle, the trigger guard snapped off. Deep scratch marks and dirt smears across the surface suggest a violent struggle. Scattered fallen leaves, broken twigs, and trampled bamboo grass around it. Disturbed earth visible. Dim afternoon light filtering through dense vegetation overhead. Shallow depth of field with the broken pistol in sharp focus. Tense, ominous atmosphere of aftermath. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 3 separate images.
```
編集者指示: 「武器破壊」「絶体絶命」の赤字テロップ。視聴者に最大の絶望を伝える演出。

---

## 6. 大原さんの反撃〜ヒグマ退散（修正版.txt L153-L191）— ASSET-076〜092

---

即座に動いたのは、大原さん。

【制作メモ】ASSET-076 [キャラアニメーション]
シーン: CHAR-02（大原さん）が即座に動く決意の表情
キャラプロンプト（1:1）:
```
CHAR-02 (Ohara) with determined intense expression, hand reaching into his backpack pocket, ready to act. Action pose. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「即座に動いた」のテロップ。BGMで一気にヒーロー的テンションへ。

---

大原さんは先日購入した小型ナイフを取り出し、ヒグマの右目を狙います。

【制作メモ】ASSET-077 [キャラアニメーション + ナイフ素材流用]
シーン: CHAR-02がナイフを取り出し、CHAR-05の右目に向かって振りかぶる極限の瞬間
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical backpack) gripping a small folding knife with both hands, knuckles white, body coiled forward in a violent lunge — face contorted with desperate fury, teeth clenched hard, eyes blazing with life-or-death focus, sweat and dirt streaked across his face, jaw locked, every muscle taut. The knife tip stops just short of CHAR-05's right eye, about to strike. CHAR-05 (young male Hokkaido brown bear, 125cm, dark brown fur) reacting with raw aggression — mouth wide open in a snarling roar, sharp teeth bared, lips curled back, eyes blazing with primal rage, nostrils flared, head jerking violently sideways. Extreme tension at the breaking point. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: 動きは3秒のアニメ。「右目を狙う」のテロップ。

---

しかし、頑丈なヒグマの頭蓋骨にはじかれてしまいました。

【制作メモ】ASSET-078 [キャラアニメーション + ナイフ素材分離]
シーン: 大原のナイフがヒグマの頭蓋骨にはじかれ、絶望の表情。ヒグマは無傷で臨戦態勢継続
キャラプロンプト（1:1 / 大原ナイフ無し + ヒグマ）:
```
(CHAR-02、CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical backpack) recoiling backward from the impact, both hands empty and open with fingers splayed in shock — face frozen in absolute despair, eyes wide and hollow, mouth half-open in a silent gasp, all color drained from his face, shoulders sagging with the realization that his weapon was knocked away. He is unarmed. CHAR-05 (young male Hokkaido brown bear, 125cm, dark brown fur) standing firm in full battle stance completely unharmed — head lowered, mouth open in a low menacing growl, sharp teeth visible, lips curled back, eyes fixed coldly on CHAR-02 with predatory focus, ears flattened, massive shoulders tensed and coiled for the next strike. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
ナイフ単体プロップ画像（1:1 / 編集者のナイフ飛ばし演出用素材）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. A small folding knife shown as an isolated prop object — 5cm silver blade fully extended, black molded handle with grip texture, clean cartoon line art. No characters, no hands, no people. The knife floats centered on the canvas. White background, no shadow. 1:1 aspect ratio. Generate 3 separate images.
```
編集者指示: ヒグマの頭蓋骨にナイフがはじかれる「カキン！」の衝撃音SE。ナイフ素材をキャラ画像に重ね、ヒグマの頭付近から斜め上方向へ高速回転しながら飛んでいくモーションを付与（モーションブラー＋スピンアニメ）。「はじかれた」「武器ロスト」テロップを赤字で強調。BGM一瞬カットして絶望感を作る。
シーン: ナイフが弾かれる効果音と視覚演出
編集者指示: 「カキン！」の効果音＋ナイフが弾かれる動きを示すモーションライン。「頭蓋骨にはじかれた」のテロップ。

---

とはいえ、攻撃されたことに気づいたヒグマは、標的を大原さんに変更。

【制作メモ】ASSET-079 [キャラアニメーション]
シーン: ヒグマが標的を船板さんから大原さんに変更。汗を流し勇気を振り絞る大原と、四つ足で牙を剥くヒグマの対峙構図
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical backpack) bracing himself upright with feet planted wide and firm, fists clenched tight at his sides, shoulders squared — face streaming with sweat that runs down his temples and drips from his chin, eyes burning with fierce courage rising through the fear, teeth gritted hard, brow furrowed in absolute resolve as he steels himself for what comes next. He stands unarmed but unbroken. CHAR-05 (young male Hokkaido brown bear, 125cm, dark brown fur) lowered into a full four-legged predator stance, all four paws on the ground, body pressed close to the earth, head pushed forward and aimed directly at CHAR-02 — mouth wide open exposing sharp white fangs in a vicious snarl, lips curled back, eyes locked onto Ohara with murderous intent, ears flattened, massive shoulders bunched and trembling with coiled aggression, ready to lunge. The two stand face to face across a short distance. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: ヒグマの視線が船板さんから大原さんへ流れるカットを前置（カメラパン）してから本カットへ。「標的変更」の赤字テロップ。BGMを一気に緊張感MAXへ。汗が落ちる滴のSEを大原のクローズアップに重ねて勇気の溜めを演出。

---

大原さんも、船板さん同様に登山道に押し倒され馬乗り状態に。

【制作メモ】ASSET-080 [キャラアニメーション]
シーン: CHAR-02がCHAR-05に押し倒される。馬乗り状態
キャラプロンプト（1:1）:
```
CHAR-02 (Ohara) being knocked onto his back by CHAR-05 (bear), the bear mounting him from above, paws on his chest. CHAR-02 raising both arms defensively. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「馬乗り状態」のテロップ。同じ展開が繰り返される絶望感を演出。

---

噛みつかれないよう必死に抵抗しますが、ヒグマは強靭な力でグイグイと顔を近づけます。

【制作メモ】ASSET-081 [キャラアニメーション]
シーン: 馬乗り状態で顔を近づけるヒグマと必死に押し返す大原。焦った表情と牙剥き出し噛みつき寸前
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical backpack) lying on his back with CHAR-05 mounted on top of him — both hands shoved hard against the bear's lower jaw and throat with arms shaking from the strain, elbows trembling, every muscle straining at the limit. Face contorted with panicked desperation, eyes wide and darting, brow furrowed sharply, sweat pouring down his face and dripping onto the ground, teeth clenched in a grimace, veins on his neck and arms bulging from the effort. CHAR-05 (young male Hokkaido brown bear, 125cm, dark brown fur) crushing down from above with overwhelming weight, head pushed forward toward Ohara's face just inches away — mouth wide open exposing massive sharp white fangs in a full bare, lips fully curled back, tongue and gums visible, jaws snapping forward about to bite down on Ohara's face, eyes blazing with raw predatory hunger, ears flattened, massive paws planted on either side of Ohara, shoulders driving forward with brute strength. The bear's face closes the distance inch by inch despite Ohara's resistance. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: ヒグマの顔と大原の顔の距離が縮まっていく1秒の寄りカットを重ね、距離マーカー（10cm→5cm→3cm）を小さく表示。「噛みつき寸前」の赤字テロップ。BGMを心拍音に切り替え緊迫MAX。

---

さらに、ヒグマの鋭い爪が、大原さんの太ももに食い込んでいきました。

【制作メモ】ASSET-082 [キャラ流用 + ASSET-001 関連]
シーン: 爪が太ももに食い込む（フックASSET-001と同じシチュエーション）
編集者指示: ASSET-001のフックカット（爪が太ももに食い込むクローズアップ）が、ここで「ああ、冒頭のシーンはここのことだったのか」と視聴者に気づきを与える瞬間。
※（再利用メモ）ASSET-001を**意図的に再利用**することで、視聴者の冒頭フックの伏線回収となる。最重要再利用ポイント。

---

この時の感覚を大原さんは、「ぐーっと（太ももが）熱くなっていった」と語っています。

【制作メモ】ASSET-083 [キャラアニメーション]
シーン: ヒグマの爪が右太ももに刺さり、絶叫する大原と食らいつこうとするヒグマ
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical hiking pants, tactical backpack) lying on his back on the ground pinned beneath the bear, head thrown back and mouth wrenched wide open to the absolute maximum in a full-throated agonized scream — jaw stretched as wide as it can go, teeth fully visible, tongue and throat exposed, neck veins bulging hard, sweat flying from his face, brow knotted tight, eyes squeezed shut, body arched and twisting in extreme agony. CHAR-05 (young male Hokkaido brown bear, 125cm, dark brown fur) crushing down from above with overwhelming weight, head lowered and driven forward toward Ohara's chest and face — jaws stretched wide open to the absolute maximum exposing huge sharp white fangs, upper and lower jaw spread far apart, gums and tongue visible, mouth lunging forward as if about to bite down on Ohara, eyes blazing with raw predatory hunger, ears flattened, massive shoulders bearing down. The bear's front right paw with thick black claws fully extended is sunk deep into Ohara's right thigh — each claw embedded into and piercing the dark olive green pant fabric over the right thigh, the fabric stretched and torn around each claw tip, the paw pressing the leg into the ground. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: 「ぐーっと（太ももが）熱くなっていった」の証言テロップを大きめに重ねる。BGMを一瞬カットして証言を際立たせ、心拍音SEで痛みの感覚を演出。爪が刺さる右太ももに赤いゆらぎエフェクト（熱の感覚を可視化）。

---

「このままではやられる」そう判断した大原さんは、小型ナイフをヒグマの喉元めがけて、力の限り突き刺したのです。

【制作メモ】ASSET-084 [キャラアニメーション / クライマックス]
シーン: CHAR-02が決死の表情でCHAR-05の喉元にナイフを突き刺す
キャラプロンプト（1:1）:
```
CHAR-02 (Ohara) with desperate fierce expression, plunging the small knife with all his strength into CHAR-05 (bear)'s throat from below. Decisive moment of life or death. Cartoon style, stylized impact (no graphic blood). White background. 1:1. Generate 3 separate images.
```
編集者指示: ハイライト・クライマックスシーン。スローモーション風に3秒で見せる。SE: 突き刺す決定的な瞬間の効果音。BGMで盛り上げる。「決死の一撃」のテロップ。

---

すると、ヒグマは大きな唸り声をあげ、ナイフが刺さったまま逃げ去りました。

【制作メモ】ASSET-085 [キャラアニメーション + SE]
シーン: CHAR-05が大きな唸り声を上げ、首にナイフが刺さったまま後退
キャラプロンプト（1:1）:
```
CHAR-05 (bear) with knife embedded in throat, head raised with painful roar, backing away from CHAR-02. Cartoon style, stylized injury. White background. 1:1. Generate 3 separate images.
```
編集者指示: SE: ヒグマの長い苦痛の唸り声。「ナイフが刺さったまま逃走」のテロップ。BGMを一瞬軽くして視聴者にカタルシスを与える。

---

二人はこれで一安心だと思いましたが、実は、これで終わりではありませんでした。

【制作メモ】ASSET-086 [キャラアニメーション]
シーン: ヒグマが逃げ去った直後、登山道に座り込み「もう大丈夫」と安堵する負傷した大原と船板
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-04 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket, tactical hiking pants visibly torn and scratched across the right thigh, tactical backpack) sitting heavily on the ground with knees bent, one hand braced behind him on the ground, the other hand resting lightly on his right thigh — shoulders sagging in deep relief, head tilted slightly back, eyes half-closed from exhaustion, mouth open in a long heavy exhale, sweat soaking his face and hair, dirt smudges across his cheeks and jacket, a faint exhausted smile starting to form. CHAR-04 (Funaita, 41-year-old firefighter, broad-shouldered build with short black hair and slight gray at temples, dark navy blue hiking jacket torn at the shoulder, brown cargo pants torn and scratched at the right thigh) crouched down on one knee beside Ohara, leaning forward with both hands resting on his bent knee, head hanging low, eyes half-shut, chest heaving with deep ragged breaths, sweat dripping from his chin, dirt and torn fabric across his clothes, a quiet exhausted relief washing over his face. Both men look battered and spent but quietly relieved, as if the worst is finally over. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: 二人のホッとした表情から数秒の間を作り、その後「しかし、終わりではなかった」の赤字テロップをフェードイン。BGMを穏やかなトーンから一気にダークに反転させ、視聴者の油断を裏切る演出。

---

なんと、ヒグマは完全には逃げずに、4、5メートル離れたところで止まり睨んでいたのです。その間、1分弱。

【制作メモ】ASSET-087 [キャラアニメーション]
シーン: CHAR-05が4-5m先で止まり、睨み続ける。CHAR-02・04も警戒
キャラプロンプト（1:1）:
```
CHAR-05 (bear) standing 4-5 meters away from CHAR-02 and CHAR-04, staring at them with knife still in throat, blood-stained but standing firm. CHAR-02 and CHAR-04 in defensive postures, breathing hard. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「4-5m先 / 睨み合い 1分弱」のテロップ。BGMで持続的な緊張を演出。

---

そのとき、ヒグマがもう一度、2人に向かって走り出してきたのです。

【制作メモ】ASSET-088 [キャラアニメーション]
シーン: CHAR-05が再び突進する
キャラプロンプト（1:1）:
```
CHAR-05 (bear) charging forward again, still wounded with knife in throat, intense aggressive expression. Motion blur. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「再突進」のテロップ。視聴者に最後の山場を感じさせる。

---

大原さんと、起き上がった船板さんは、ヒグマを足で蹴り続けました。そして、ヒグマはじわじわと後ろへ下がっていき、

【制作メモ】ASSET-089 [キャラアニメーション]
シーン: CHAR-02とCHAR-04が立ち上がり、CHAR-05を蹴り続ける
キャラプロンプト（1:1）:
```
CHAR-02 (Ohara) and CHAR-04 (Funaiita) both standing now, kicking repeatedly at CHAR-05 (bear), driving it back. CHAR-05 retreating slowly, still wounded. Cartoon style, intense action. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「蹴り続ける / 後退」のテロップ。BGMでカタルシスへ向けて盛り上げる。

---

ついに登山道を下って消えていったのです。

【制作メモ】ASSET-090 [背景BG-A + キャラ流用]
シーン: CHAR-05が登山道を下って笹薮に消える後ろ姿
キャラプロンプト（1:1）:
```
CHAR-05 (bear) walking away down the trail, viewed from behind, disappearing into the bamboo grass. Knife still in throat, weakened movement. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「ついに消えていった」のテロップ。BGMを安堵のトーンに切り替える。3秒の余韻。

---

大原さんはこの一連の事件について、「ただじゃすまないと思った。助かったのは、運がよかっただけ」と振り返っています。

【制作メモ】ASSET-091 [キャラアニメーション + 実写背景]
シーン: 事件後、頭を抱えて恐怖と疲労に打ちのめされる大原さんが自宅で振り返る
キャラプロンプト（1:1）:
```
(CHAR-02 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-02 (Ohara, 41-year-old firefighter, muscular build, dark olive green hiking jacket torn at the shoulder, tactical hiking pants visibly torn and scratched across the right thigh) sitting hunched forward with both hands clutching the sides of his head, fingers gripping his hair tight, elbows resting on his bent knees, body trembling — face contorted with raw lingering fear and disbelief, eyes wide open and staring vacantly at nothing, pupils dilated, mouth slightly open as if frozen in a silent gasp, sweat beading on his forehead, all color drained from his face. The realization of how close he came to dying etched into every line of his expression. White background. 1:1 aspect ratio. Generate 3 separate images.
```
背景プロンプト（16:9・フォトリアル / 家の中）:
```
A dimly lit Japanese living room in the early evening, simple modest interior — tatami flooring, low wooden table, an old television set in the corner, a single floor lamp casting warm but somber light, sliding paper doors slightly ajar showing darkness beyond. Quiet still atmosphere of solitude and contemplation, the room feels heavy and silent. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty interior only. Generate 3 separate images.
```
編集者指示: 「ただじゃすまないと思った」「助かったのは、運がよかっただけ」の証言テロップを順にフェードイン。BGMを重い独白トーンに切り替え。大原さんの震える肩に微細なシェイクエフェクト。証言と恐怖の表情で「あの瞬間が今も離れない」深いトラウマを表現。

---

ちなみに、3人目の阿部さんは、ヒグマから逃げようとしたはずみで、およそ3.5メートル下の崖下へと転落したとのことです。負傷はしましたが、命に別状はありませんでした。

【制作メモ】ASSET-092 [キャラアニメーション + 実写背景]
シーン: 阿部さんがヒグマから逃げようとして3.5m下の崖下へ転落する瞬間
キャラプロンプト（1:1 / 滑落の瞬間）:
```
(CHAR-03 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. CHAR-03 (Abe, 36-year-old firefighter, average athletic build, short black hair, dark red hiking jacket, dark gray pants, hiking boots, black daypack) caught mid-fall tumbling down a steep slope — body tilted sharply backward off balance, both arms flailing wildly in the air desperately trying to grab onto anything, legs splayed and skidding, one boot kicking up dirt and small stones. Face frozen in absolute panic — mouth wrenched wide open in a sudden terrified shout, eyes bulging wide with raw fear, eyebrows shot up high, sweat flying from his face, all color drained, every muscle tensed in the instinctive terror of falling. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images.
```
背景プロンプト（16:9・フォトリアル / 崖下と落下痕）:
```
A steep narrow cliff edge along a mountain hiking trail on Daisengen-dake in late autumn. The trail abruptly drops off into a 3.5-meter rocky drop below — exposed dark soil, broken rocks, scattered fallen leaves and dried bamboo grass at the bottom. Fresh signs of a recent fall — disturbed earth on the slope face, scuff marks dragged down the dirt wall, a few broken twigs and torn leaves marking the path of descent. Dense tall sasa bamboo grass framing the upper edge of the trail. Cold overcast late autumn afternoon light, deep shadows under the conifer canopy overhead. Tense quiet atmosphere of immediate aftermath. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 3 separate images.
```
編集者指示: 背景を実写崖カットに切り替えてから阿部さんの滑落アニメをモーションブラー付きで合成（上から下へ斜め落下、約1秒）。「3.5m転落」のテロップを高さインフォグラフィック（矢印＋距離マーカー）と共に表示。「負傷あり・命に別状なし」のサブテロップを安堵BGMと共に重ねる。

---

## 7. 全員生還〜下山再遭遇（修正版.txt L189-L218）— ASSET-093〜103

---

この一件は、人がヒグマに襲われたにもかかわらず、全員無事という、かなり稀なケースです。

【制作メモ】ASSET-093 [画面エフェクト + 3人並び]
シーン: 3人が立ち上がって寄り添う構図
編集者指示: 「全員無事 / 稀なケース」のテロップ。3人並び画像（ASSET-039 流用）。

---

日頃から鍛えている消防士だったからこその生還事例とも言えるでしょう。

【制作メモ】ASSET-094 [画面エフェクト + キャラ流用]
シーン: 3人並び画像にナレーション・テロップを重ねる
編集者指示: 「消防士だったからこそ」のテロップ。3人並び画像（ASSET-039 再利用）。

---

その後、3人はその場で10分ほど様子を見て、ヒグマが戻ってこないことを確認。

【制作メモ】ASSET-095 [キャラアニメーション + 背景BG-A流用]
シーン: ヒグマが戻らないか10分間警戒し続ける、傷ついて怯える3人
キャラプロンプト（1:1）:
```
(CHAR-02、CHAR-03、CHAR-04 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. Three battered firefighters huddled close together on the ground, supporting one another. CHAR-03 (Abe, dark red hiking jacket torn at the shoulder, dark gray pants scratched and dirty, dark dirt smudges on his face from his fall) on the left, CHAR-02 (Ohara, dark olive green hiking jacket, tactical hiking pants torn at the right thigh) in the center, CHAR-04 (Funaita, dark navy blue hiking jacket torn at the shoulder, brown cargo pants torn at the right thigh) on the right. Each of them: crouched low and pressed close to the others, heads up and eyes wide darting nervously in every direction scanning their surroundings for any sign of the bear, faces frozen with lingering fear and hyper-vigilance, mouths slightly open in shallow rapid breaths, sweat beading on their foreheads, bodies tense and trembling, hands gripping each other's arms or shoulders for support, every muscle braced ready to flee at the first sound. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 3 characters together.
```
編集者指示: 背景は既存BG-A（笹薮の登山道）に合成。3人のキャラ画像を中央に配置し、左下に時計アニメを置いて10分の経過を早回し表示（実時間2〜3秒）。「10分待機」のテロップを時計と並べて表示。BGMは緊張感のあるサスペンス調を維持し、最後の数秒で安堵のトーンへわずかに緩める。視線が周囲をキョロキョロ動くシェイクエフェクトでサスペンスを強化。

---

互いを支え合いながら、1時間ほどかかる登山道をおりていきました。

【制作メモ】ASSET-096 [キャラアニメーション]
シーン: 3人が互いを支え合いながらゆっくり下山
キャラプロンプト（1:1）:
```
Three firefighters CHAR-02, CHAR-03, CHAR-04 supporting each other while walking down the mountain trail, slow careful pace. Some visible bandages or torn clothing showing the aftermath. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「1時間かけて下山」のテロップ。BGMを希望のトーンに。

---

ちなみに、下山の途中でも、先ほどのヒグマにまた遭遇したといいます。

【制作メモ】ASSET-097 [画面エフェクト + 緊張再再]
シーン: 「再遭遇」のテロップ
編集者指示: 「再遭遇」のテロップを大きく赤字で表示。BGMを一瞬で再びダークに切り替え。

---

場所は、襲撃現場からおよそ500メートル下の登山道。

【制作メモ】ASSET-098 [Google Earth + マーカー]
シーン: 襲撃地点と再遭遇地点をGE上に表示
GE座標:
- 7合目襲撃地点: 概算 `41°33'30"N, 140°13'30"E`
- 再遭遇地点（500m下）: 概算 `41°33'25"N, 140°14'00"E`（実測要）
編集者指示: GE上で2地点を結び、「500m下」のテロップ。

---

ヒグマが襲ってくることはなかったですが、笹薮から、3人の姿をじっと見ていたといいます。

【制作メモ】ASSET-099 [キャラアニメーション]
シーン: 笹薮の隙間からCHAR-05が3人を見つめる視線
キャラプロンプト（1:1）:
```
CHAR-05 (bear) partially hidden in dense bamboo grass, only its head and eyes visible, watching three figures in the distance. Still wounded, knife visible. Cartoon style, eerie atmosphere. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「じっと見ていた」のテロップ。視点POVでヒグマの視線を強調。BGMで気味悪さを演出。

---

すでに首にナイフが刺さり、血を流していたヒグマが、なぜ再び現れたのか。
その理由として、獲物に執着し、諦めていなかった可能性が指摘されています。

【制作メモ】ASSET-100 [画面エフェクト + テキスト]
シーン: 「なぜ再び現れたのか？」の問いかけテロップ＋専門家見解
編集者指示: 「獲物への執着」のテロップを画面中央に。後段のキャッシング行動解説への伏線。

---

3人は石を投げて追い払いながら、必死に山を下りることに。

【制作メモ】ASSET-101 [キャラアニメーション]
シーン: 3人が石を投げ続けて下山
キャラプロンプト（1:1）:
```
Three firefighters CHAR-02, CHAR-03, CHAR-04 throwing stones backward as they continue descending the trail, glancing fearfully behind them. Tense survival mode. Cartoon style. White background. 1:1. Generate 3 separate images.
```
編集者指示: 石を投げるアニメ。「石を投げ追い払い」のテロップ。BGMで緊張を保つ。

---

下山後、ただちに警察、消防、北海道庁に連絡。

【制作メモ】ASSET-102 [画面エフェクト + 報告アニメ]
シーン: 警察・消防・北海道庁のロゴを画面に展開
編集者指示: 3つの機関ロゴを順に表示。「ただちに通報」のテロップ。

---

即座に緊急事態となり、大千軒岳の登山道は入山禁止に。

【制作メモ】ASSET-103 [画面エフェクト + 看板]
シーン: 登山口に「入山禁止」の赤い看板が立てられる
プロンプト（16:9・フォトリアル）:
```
A large red warning sign reading "入山禁止" (entry forbidden) and "Bear danger" being installed at the trailhead of Daisengen-dake. Workers in safety gear stepping back after placing the sign. Late autumn afternoon light. Photorealistic, RED camera. 16:9. No identifiable faces. Generate 3 separate images.
```
編集者指示: 「入山禁止」の赤字テロップを画面中央に大きく表示。

---

## 8. 住民・3人のその後（修正版.txt L210-L226）— ASSET-104〜110

---

付近の住民にも、外出禁止が呼びかけられました。

【制作メモ】ASSET-104 [AI動画]
シーン: 福島町の住宅街、無線スピーカーから外出禁止の呼びかけが流れる
プロンプト（16:9・フォトリアル）:
```
A quiet rural neighborhood in Fukushima Town with a public address speaker on a utility pole broadcasting a warning. Empty streets, doors closed. Late autumn afternoon. Photorealistic, RED camera, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「外出禁止」のテロップ。スピーカーの音声SE（注意喚起アナウンス）を重ねる。

---

病院に運ばれた3人ですが、驚くことに入院することもなく、その日のうちに回復に向かったとのこと。

【制作メモ】ASSET-105 [AI動画]
シーン: 病院の処置室、軽い処置を受ける3人
プロンプト（16:9・フォトリアル）:
```
A clean modern hospital treatment room with three patients being treated for minor wounds by medical staff. Faces obscured or shown from behind. Bright clinical lighting. Photorealistic, RED camera. 16:9. Generate 3 separate images.
```
編集者指示: 「入院なし / その日のうちに回復」のテロップ。安堵のBGM。

---

船板さんは首に噛み傷ができましたが、病院でホッチキスのようなもので止め、入院は不要でした。

【制作メモ】ASSET-106 [背景静止画 + 説明]
シーン: 医療用ステープラー（皮膚縫合器）の参考画像
プロンプト（16:9・フォトリアル）:
```
A medical skin stapler (used for closing wounds) on a sterile tray, close-up product shot, hospital setting. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「医療用ステープラー」のテロップで簡潔に説明。

---

翌日には、もう仕事に出ていたといいます。

【制作メモ】ASSET-107 [AI動画]
シーン: 翌朝の消防署、3人が出勤する後ろ姿
プロンプト（16:9・フォトリアル）:
```
A small rural fire station in the early morning, three firefighter figures arriving for work, viewed from behind. Normal routine restored. Soft morning light. Photorealistic, documentary style. 16:9. No identifiable faces. Generate 3 separate images.
```
編集者指示: 「翌日には仕事に復帰」のテロップ。視聴者に「消防士の鍛え抜かれた身体」を再認識させる演出。

---

一方、行方不明となった屋名池さんの捜索は続いていました。

【制作メモ】ASSET-108 [画面エフェクト + 屋名池さん回想]
シーン: CHAR-01の表情（ASSET-008流用）＋「捜索継続中」のテロップ
編集者指示: CHAR-01のキャラ画像を画面に表示しつつ、「屋名池さんの捜索は続く」のテロップ。BGMを再びシリアスに。

---

しかし、大千軒岳には消防士を襲ったヒグマがどこかに潜んでいます。

【制作メモ】ASSET-109 [背景BG-A + シルエット]
シーン: 笹薮の中に潜むヒグマのシルエット
プロンプト（16:9・フォトリアル）:
```
Eerie bamboo grass forest with a vague silhouette of a bear hidden deep within, only partially visible. Dim eerie light. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「ヒグマはまだ潜んでいる」のテロップ。BGMで不安を持続。

---

捜索隊が下手に動けば、さらなる被害になりかねない状況。そのため、安全に動けるよう警察、消防、ハンター、北海道警察航空隊の協力のもと捜索を進めることとなります。

【制作メモ】ASSET-110 [画面エフェクト + 各機関ロゴ]
シーン: 警察・消防・ハンター・防災ヘリの各部隊が集結
プロンプト（16:9・フォトリアル）:
```
Multiple emergency vehicles gathered at a rural staging area: police cars, fire trucks, hunter trucks with red license plates, and a rescue helicopter on the ground. Coordinating teams in uniforms (faces from behind). Late autumn day, low overcast. Photorealistic, RED camera, documentary style. 16:9. Generate 3 separate images.
```
編集者指示: 各機関名のテロップを順に表示。「大規模捜索体制」のテロップ。

---

## 9. 11月2日 遺体発見（修正版.txt L228-L274）— ASSET-111〜127

---

11月2日（捜索開始から4日目）

【制作メモ】ASSET-111 [画面エフェクト]
シーン: 「11月2日 / 捜索開始から4日目」の日付＋経過日数テロップ
編集者指示: 日付テロップを画面中央。BGMで緊迫を保つ。

---

午前6時50分、捜索開始。

【制作メモ】ASSET-112 [画面エフェクト + AI動画]
シーン: 「午前6時50分」の時刻テロップ＋早朝の捜索開始の風景
プロンプト（16:9・フォトリアル）:
```
Early morning at Daisengen-dake trailhead, breath visible in the cold air, search teams in tactical gear preparing equipment. Dawn light just beginning. Photorealistic, RED camera. 16:9. Faces from behind. Generate 3 separate images.
```
編集者指示: 「6:50 捜索開始」のテロップ。寒さを感じさせる青いトーン。

---

ハンター2人を伴い、合計18人態勢で山頂に向かう本格的な捜索でした。

【制作メモ】ASSET-113 [AI動画]
シーン: 18人の捜索隊が登山道を進む
プロンプト（16:9・フォトリアル）:
```
A team of 18 search personnel including hunters with rifles, police, and firefighters, climbing up a forest trail in single file. Backpacks, communication gear. Early morning light. Photorealistic, RED camera, documentary style. 16:9. Faces from behind. Generate 3 separate images.
```
編集者指示: 「18人態勢」のテロップ。歩く列の上空ショット推奨。

---

地上だけでなく、北海道警察の防災ヘリが、空中からも探します。

【制作メモ】ASSET-114 [AI動画]
シーン: 北海道警察の防災ヘリが山の上を旋回
プロンプト（16:9・フォトリアル）:
```
A police rescue helicopter (Hokkaido Police, white with blue stripes) flying low over a forested mountain ridge. Crew members visible through the side door scanning the terrain. Late autumn sky, overcast. Photorealistic, RED camera, documentary style. 16:9. Generate 3 separate images.
```
編集者指示: 「防災ヘリ 空中捜索」のテロップ。ヘリのローター音SE。

---

午後0時半ごろ。

【制作メモ】ASSET-115 [画面エフェクト]
シーン: 「12:30」の時刻テロップ
編集者指示: 時刻テロップを表示。視聴者に「何かが起きる予感」を持たせる。BGMをわずかに変化させる。

---

7合目付近の沢で、ヘリの隊員が、地面に倒れた人影を発見。

【制作メモ】ASSET-116 [AI動画 / ヘリ視点]
シーン: ヘリから見下ろす視点で、沢の地面に何かが横たわる
プロンプト（16:9・フォトリアル・ヘリ視点）:
```
Aerial view from a low-flying helicopter looking down at a steep narrow ravine on a mountain side. A vague human-shaped form partially covered with earth and branches barely visible from this height. Surrounding dense bamboo grass and conifers. Photorealistic, RED camera, documentary style. 16:9. No identifiable human features visible. Generate 3 separate images.
```
編集者指示: 「7合目の沢で発見」のテロップ。視聴者がショックを受けすぎないよう、上空視点で抑制的に。

---

それはまぎれもなく屋名池さんでしたが、とても奇妙な状態で見つかっています。
（黒塗り状態のイラスト）

【制作メモ】ASSET-117 [画面エフェクト + 黒塗りイラスト]
シーン: ユーザー要望L241通り「黒塗り状態のイラスト」で遺体を直接描写せず
プロンプト（16:9・抽象表現）:
```
Stylized symbolic illustration: a completely blacked-out human silhouette lying on the ground covered with scattered earth and branches. Pure black silhouette only, no details. Surrounding bamboo grass partially visible. Solemn respectful representation. Cartoon style adapted to silhouette only. 16:9. Generate 3 separate images.
```
編集者指示: 遺族配慮のため遺体は黒塗りシルエットで描写。「奇妙な状態で発見」のテロップ。BGMを重く沈める。
※（ユーザー要望L241「黒塗り状態のイラスト」を完全準拠）

---

なぜか、全身に土と木の枝がかけられていたのです。土と木の枝のかぶせ方は、表面に薄くまぶしたものではなく、屋名池さんの全身を覆い隠すように、丁寧に積み上げられていました。

【制作メモ】ASSET-118 [背景静止画 / BG-B 再利用]
シーン: ASSET-005（土と枝が散乱した地面）を発展させ、丁寧に積み上げられた様子
プロンプト（16:9・フォトリアル）:
```
A close-up view of a forest floor where earth, twigs, and dried branches have been deliberately piled up in a mound shape, as if to cover something underneath. No body visible — only the carefully arranged covering. Dim autumn light. Photorealistic, RED camera. 16:9. No bodies, no figures. Generate 3 separate images.
```
編集者指示: 「丁寧に積み上げられた」のテロップで意図性を強調。BGMを重い余韻に。
※（再利用メモ）ASSET-005の素材を発展形として再利用可能。BG-Bを継続使用。

---

専門家曰く、これは何者かが、意図的に屋名池さんの上にかぶせたものと断定。
（黒塗り状態のイラスト）

【制作メモ】ASSET-119 [画面エフェクト + 黒塗り]
シーン: ユーザー要望L246通り「黒塗り状態のイラスト」継続
編集者指示: ASSET-117の黒塗りシルエットを再利用＋「意図的にかぶせられた」の赤字テロップ。
※（ユーザー要望L246「黒塗り状態のイラスト」完全準拠）（再利用メモ：ASSET-117の素材流用）

---

発見場所は、7合目付近の登山道から外れた、急な沢沿い。

【制作メモ】ASSET-120 [Google Earth / 沢の地形]
シーン: 7合目の沢の位置をGEで表示
GE座標:
- 発見地点（7合目沢）: 概算 `41°33'30"N, 140°13'30"E`（実測要）
カメラ高度: 1,000m
カメラ角度: 斜め60°、3D地形ON
編集者指示: 急峻な沢の地形を強調。「7合目付近 / 登山道から外れた沢」のテロップ。

---

両側は高い笹に囲まれているので、空からヘリで探さないと発見しにくい場所でした。

【制作メモ】ASSET-121 [Google Earth + 補足]
シーン: GEで沢が笹に囲まれている様子を上空から表示
編集者指示: 「ヘリでないと発見困難」のテロップ。BGMで重さを持続。

---

そして、屋名池さんから数十メートル先にもう一つの体が、横たわっていました。
（黒塗り状態のイラスト）

【制作メモ】ASSET-122 [画面エフェクト + 黒塗り]
シーン: ユーザー要望L253通り「黒塗り状態のイラスト」継続
編集者指示: ASSET-117と類似の黒塗りシルエット（今度はヒグマの形）。「数十メートル先にもう一つの体」のテロップ。
※（ユーザー要望L253「黒塗り状態のイラスト」完全準拠）

---

それはなんとヒグマの、亡骸（なきがら）でした。

【制作メモ】ASSET-123 [画面エフェクト]
シーン: 黒塗りシルエットがヒグマの形であることを明示
編集者指示: 「ヒグマの亡骸」のテロップ。視聴者に「あのヒグマだ」と気づかせる演出。

---

首には、深い刺し傷があり、消防士を襲ったヒグマと一致。

【制作メモ】ASSET-124 [画面エフェクト + キャラ流用]
シーン: ヒグマの首の刺し傷を強調。消防士襲撃のヒグマ（CHAR-05）と一致
編集者指示: 「首の刺し傷 / 同一個体」のテロップ。CHAR-05画像（ASSET-085 流用）と並べて表示。
※（再利用メモ）ASSET-085（ナイフ刺さったCHAR-05）流用。

---

函館新聞デジタルは、「首の刺し傷が深く、大動脈まで到達しており、致命傷となったとみられている」と報道。

【制作メモ】ASSET-125 [画面エフェクト / 報道引用]
シーン: 函館新聞デジタルの記事スクショ風＋引用テロップ
編集者指示: 「函館新聞デジタル」のクレジット＋引用テキストを画面に表示。実際の記事スクショ使用可能なら使用。

---

さらに、北海道立総合研究機構の調査により、ヒグマの胃の内容物から、屋名池さんのDNAが検出され、このヒグマが屋名池さんを確実に「食べていた」と科学的に証明されました。

【制作メモ】ASSET-126 [画面エフェクト + 科学解説]
シーン: DNA鑑定のグラフィック表現
プロンプト（16:9・フォトリアル）:
```
Scientific laboratory setting with DNA analysis equipment, computer screens displaying DNA sequence graphs. Documentary style. Photorealistic, RED camera. 16:9. No identifiable faces. Generate 3 separate images.
```
編集者指示: 「北海道立総合研究機構」のクレジット。「胃の内容物からDNA検出」「食べていた」と段階的にテロップ。

---

胃の内容物の量から、屋名池さんを襲ったあと、繰り返し食事をするために、何回も現場に戻ってきた可能性が高い、と分析されています。

【制作メモ】ASSET-127 [画面エフェクト + テキスト]
シーン: 「繰り返し戻ってきた」の動線アニメ
編集者指示: 「複数回戻ってきた」のテロップ。BGMで戦慄感。

---

## 10. 栄養状態・キャッシング解説（修正版.txt L271-L315）— ASSET-128〜140

---

しかし、ヒグマの栄養状態は比較的、良好だったこともわかってます。

【制作メモ】ASSET-128 [画面エフェクト + 解剖イラスト]
シーン: ヒグマの体格を示すイラスト＋「栄養状態 比較的良好」のテロップ
編集者指示: 「栄養状態 良好」のテロップ。視聴者に「空腹のせいではない」事実を伝える伏線。

---

つまり、空腹で仕方なく人を襲ったわけではなく、単なる日常の餌として食事をしていたということです。

【制作メモ】ASSET-129 [画面エフェクト + 衝撃テロップ]
シーン: 「空腹ではなかった = 日常の餌」の衝撃事実
編集者指示: 「空腹ではない」「日常の餌として」の赤字テロップを画面に大きく表示。視聴者の戦慄ポイント。BGMで重い衝撃を演出。

---

ヒグマに襲われたにもかかわらず、全員が生還したこともあり、この事件は新聞やウェブメディアなど様々な媒体で報道されました。
（新聞の実写画像）

【制作メモ】ASSET-130 [実写画像 / 新聞スクショ]
シーン: ユーザー要望L276通り、新聞の実写画像を使用
編集者指示: 北海道新聞、函館新聞、HBC等の報道スクショを画面に重ねる。複数メディアのカバレッジを示す。出典クレジット必須。
※（ユーザー要望L276「新聞の実写画像」完全準拠）

---

また、文春オンラインでは、今回の屋名池さんの奇妙な状態ついて「保存食」と語っています。

【制作メモ】ASSET-131 [画面エフェクト / 文春引用]
シーン: 文春オンライン記事の「保存食」見出し
編集者指示: 「保存食」の言葉を画面中央に大きく赤字で表示。文春オンラインのクレジット。

---

ヒグマには、ある特殊な習性があります。

【制作メモ】ASSET-132 [画面エフェクト]
シーン: 「ヒグマの特殊な習性」の引きテロップ
編集者指示: 「ヒグマの特殊な習性とは？」のテロップで視聴者の興味を引く。

---

一度に食べきれない食物を、土や枝で覆い隠して、後から食べに戻る習性です。これを専門用語で「キャッシング行動」といいます。

【制作メモ】ASSET-133 [画面エフェクト + AI動画]
シーン: ヒグマが獲物に土と枝をかぶせる行動の説明アニメ
プロンプト（16:9・フォトリアル）:
```
A wild brown bear in a forest deliberately scraping earth and pulling branches with its paws to cover a prey item on the ground. Documentary nature footage style. Photorealistic, RED camera. 16:9. No human elements. Generate 3 separate images.
```
編集者指示: 「キャッシング行動」のテロップを大きく表示。動きをスローモーション風に。

---

北米のグリズリーやロシアのヒグマでも観察されている、クマの本能的な行動パターン。

【制作メモ】ASSET-134 [Google Earth / 世界地図]
シーン: 北米・ロシアのヒグマ生息地を世界地図でハイライト
GE座標:
- 北米アラスカ・カトマイ国立公園: `58°30'N, 155°00'W`
- ロシア・カムチャッカ: 概算 `56°N, 159°E`
- 日本・北海道: 概算 `43°N, 142°E`
カメラ高度: 全球視点
編集者指示: 世界地図で3地域をハイライト。「北米 / ロシア / 日本」のテロップ。BGMで普遍性を伝える。

---

アラスカやモンタナの国立公園でも、グリズリーや鹿の死骸を、土や草、枝で覆い隠す行動が、繰り返し観察されています。

【制作メモ】ASSET-135 [AI動画 / アラスカ風景]
シーン: アラスカ・モンタナの国立公園の風景＋グリズリーがキャッシング行動
プロンプト（16:9・フォトリアル）:
```
Vast wilderness of Katmai National Park (Alaska) or Glacier National Park (Montana), mountains and forests, with a distant grizzly bear silhouette burying something with earth and branches. Documentary nature photography. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「アラスカ / モンタナ」のテロップ。広大な大自然の中に行動を位置づける。

---

数日かけて戻ってきて、また食べる。

【制作メモ】ASSET-136 [画面エフェクト + 時間経過]
シーン: 「Day 1 → Day 2 → Day 3」のテロップでクマが何度も戻る様子
編集者指示: 時間経過テロップ。BGMで継続的な恐怖を表現。

---

クマは一度「自分の食べ物」と認識した獲物に対しては、非常に強く執着することが分かっています。

【制作メモ】ASSET-137 [画面エフェクト + 強調]
シーン: 「執着」のキーワードを大きく表示
編集者指示: 「強い執着」の赤字テロップ。BGMで重みを持たせる。

---

そのため、獲物に近づく動物には、容赦なく敵とみなし攻撃をします。それは近づく動物が人であっても同じです。

【制作メモ】ASSET-138 [画面エフェクト + 攻撃動作]
シーン: 獲物の周囲に近づくものを攻撃するヒグマのイメージ
プロンプト（16:9・フォトリアル）:
```
A brown bear standing protectively over a covered prey mound in a forest clearing, snarling at approaching shadows. Defensive posture. Photorealistic, RED camera. 16:9. No people visible. Generate 3 separate images.
```
編集者指示: 「人も例外なし」のテロップ。視聴者に「自分も対象になりうる」と認識させる。

---

偶然、クマに近づいてしまい悲惨な結果となった事例は世界中で山ほど報告されています。

【制作メモ】ASSET-139 [画面エフェクト / 世界地図 + 事件数]
シーン: 世界各地の熊事件をマッピング
編集者指示: 世界地図に複数のピンを点滅表示。「世界各地で多発」のテロップ。

---

13年間にわたりグリズリーと共存する暮らしを撮影し続けていた、自然映像作家のティモシー・トレッドウェルさん46歳と、
（実写を使用）

【制作メモ】ASSET-140 [実写画像]
シーン: ユーザー要望L297通り、ティモシー・トレッドウェルさんの実写を使用
編集者指示: ウィキペディア・グリズリー・マン映画の公開実写画像を使用。CHAR-06のキャラ画像は使用しない。
出典クレジット明示（CC画像または映画スチール）必須。
※（ユーザー要望L297「実写を使用」完全準拠）

---

## 11. トレッドウェル事件〜日本3事件（修正版.txt L299-L317）— ASSET-141〜148

---

恋人のエイミー・ヒューゲナードさん37歳の2人が、撮影中にテント近くでグリズリーに襲われ、命を落としています。
（実写を使用）

【制作メモ】ASSET-141 [実写画像]
シーン: ユーザー要望L300通り、エイミー・ヒューゲナードさんの実写を使用
編集者指示: 公開実写画像を使用。CHAR-07のキャラ画像は補助として使用可能だが、実写優先。
出典クレジット明示必須。
※（ユーザー要望L300「実写を使用」完全準拠）

---

その襲撃の様子は、トレッドウェルさんのビデオカメラのオーディオに、およそ6分間、記録されていました。

【制作メモ】ASSET-142 [画面エフェクト + 音響波形]
シーン: ビデオカメラと音声波形のイメージ
プロンプト（16:9・フォトリアル）:
```
A small handheld video camera on a forest floor with audio waveform visualization overlaid, suggesting recorded but unseen audio. Dark dramatic atmosphere. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「6分間の音声記録」のテロップ。波形アニメで時間経過を視覚化。

---

レンズキャップは閉じたままでしたので、映像は残っていませんが、生々しい叫び声は全て残されています。

【制作メモ】ASSET-143 [画面エフェクト + 黒画面]
シーン: 完全な黒画面に「音声のみ」のテロップ
編集者指示: 「映像なし・音声のみ」の白文字を黒背景に表示。「叫び声」のテロップ。BGMを切り、わずかなノイズ音だけにする音響演出。視聴者の想像力を刺激。

---

この一連の出来事は、ドキュメンタリー映画「グリズリー・マン」として2005年に公開され、世界中で大きな衝撃を呼びました。

【制作メモ】ASSET-144 [画面エフェクト / 映画ポスター]
シーン: 「グリズリー・マン」(2005) の映画ポスターまたはタイトルロゴ
編集者指示: 映画タイトル「Grizzly Man / グリズリー・マン (2005)」のテロップ。映画ポスターを使用可能ならば著作権配慮で使用。出典クレジット必須。

---

日本でも、1915年の三毛別羆事件、1970年の福岡大学ワンダーフォーゲル部ヒグマ事件、2016年の十和利山熊襲撃事件。
（動画内のシーンを切り取り使用）

【制作メモ】ASSET-145 [動画内シーン再利用 / 過去動画クリップ]
シーン: ユーザー要望L309通り「動画内のシーンを切り取り使用」
編集者指示: 当チャンネル過去動画から該当シーンを切り取って使用:
- **三毛別羆事件**（1915）→ 該当の過去動画クリップ（チャンネル内最古の支柱動画）
- **福岡大学ワンダーフォーゲル部ヒグマ事件**（1970, c_kkIsQlFe8）→ 該当動画のクリップ
- **十和利山熊襲撃事件**（2016, Ot4G3-EHj5Q）→ 該当動画のクリップ
各クリップを3秒ずつ繋ぎ、それぞれに事件名・年号テロップを重ねる。
※（ユーザー要望L309「動画内のシーンを切り取り使用」完全準拠）（再利用メモ：同チャンネル内動画の流用、H13クラスタ強化に効果大）

---

いずれも、同じ個体が多大な被害を出しています。

【制作メモ】ASSET-146 [画面エフェクト]
シーン: 「同一個体による複数被害」のテロップ
編集者指示: 「同一個体 / 多数の犠牲者」のテロップ。3事件の共通点を強調。

---

大千軒岳のヒグマも、消防士3人と屋名池さんの合計4人を襲っています。

【制作メモ】ASSET-147 [画面エフェクト + 数字]
シーン: 「4人」の数字を大きく表示
編集者指示: 「合計4人」のテロップを画面中央に大きく赤字で表示。3事件と並べて大千軒岳も同じ構造であることを示す。

---

ヒグマの記憶力は、犬の数倍とも言われており「人間は食べ物」と覚えてしまうと、その記憶はなかなか消えません。屋名池さんを襲い、本格的に人間の味を覚え、消防士3人の事件へと発展したのでしょう。

【制作メモ】ASSET-148 [画面エフェクト + 推論アニメ]
シーン: 時系列フロー（屋名池さん→消防士）のアニメ
編集者指示: 「10/29 屋名池さん襲撃」→「10/31 消防士襲撃」の矢印アニメ。「人間の味を覚えた」のテロップ。BGMで重い因果関係を伝える。

---

## 12. 11月4日 北大発表〜屋名池さん人物（修正版.txt L319-L347）— ASSET-149〜159

---

11月4日（遺体発見から二日後）

【制作メモ】ASSET-149 [画面エフェクト]
シーン: 「11月4日 / 遺体発見から二日後」の日付テロップ
編集者指示: 日付テロップを表示。

---

北海道大学水産学部は、今回のヒグマ事件について公式サイトで掲載。
（実際の画像を使用）

【制作メモ】ASSET-150 [実写画像 / 北大サイトスクショ]
シーン: ユーザー要望L322通り「実際の画像を使用」
編集者指示: 北大水産学部公式サイトの該当発表ページ（https://www2.fish.hokudai.ac.jp/infomation/25535/）のスクショを使用。
※（ユーザー要望L322「実際の画像を使用」完全準拠）

---

司法解剖の結果、屋名池さんが命を落とした原因はヒグマに襲われたことによる出血性ショックと発表されました。

【制作メモ】ASSET-151 [画面エフェクト + 医学用語]
シーン: 「出血性ショック」の医学解説テロップ
編集者指示: 「死因：出血性ショック」のテロップ。やや控えめに事実を伝える。

---

屋名池さんは、海洋生物学を専攻する学生でした。

【制作メモ】ASSET-152 [背景静止画]
シーン: 海洋生物学の研究風景（北大水産・海の生き物）
プロンプト（16:9・フォトリアル）:
```
A marine biology research setting: aquarium tanks with fish specimens, microscopes, marine charts on the wall, North University setting. Soft natural lighting through windows. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「海洋生物学を専攻」のテロップ。屋名池さんの学業への情熱を視覚化。

---

高校時代は、ボート部に入り、北大入学後は、カヌー部に所属。

【制作メモ】ASSET-153 [AI動画]
シーン: ボートとカヌーの活動風景
プロンプト（16:9・フォトリアル）:
```
A split or sequential shot: left side shows a high school rowing boat on calm water, right side shows a university canoe on a river, both empty boats representing past activities. Soft warm sunset light. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「ボート部→カヌー部」のテロップ。屋名池さんの活動的な人物像を伝える。

---

2023年4月の釧路川100キロカヌーマラソンでは、第8位に入賞しています。

【制作メモ】ASSET-154 [画面エフェクト + 実績テロップ]
シーン: 「釧路川100kmカヌーマラソン / 第8位入賞」のテロップ
プロンプト（16:9・フォトリアル）:
```
A river view of Kushiro River in Hokkaido with empty canoes lined up at a starting line, autumn morning light, mountain backdrop. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「第8位入賞」を赤字で強調。屋名池さんの実力を示す。

---

そして、すでに北海道大学大学院 国際食資源学院への進学が決まっていた人物です。

【制作メモ】ASSET-155 [画面エフェクト + 背景]
シーン: 「大学院進学決定 / 国際食資源学院」のテロップ＋大学院の校舎
背景プロンプト（16:9・フォトリアル）:
```
Exterior of Hokkaido University main campus building in Sapporo, autumn colors, academic atmosphere. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「大学院進学決定」のテロップ。視聴者に「失われた未来」を強く印象づける。BGMで重い余韻。

---

北大水産学部の都木靖彰学部長は、「志半ばの若い命が失われたことに対し、深い悲しみを感じる」「ご遺族の皆様のお気持ちをお察しすると、心が痛みます」とホームページでコメントを残してます。
（実際の画像を使用）
https://www.memoriaactiva.com/yanaikekanato-1/

【制作メモ】ASSET-156 [実写画像 + 引用テロップ]
シーン: ユーザー要望L337通り「実際の画像を使用」
編集者指示: 都木靖彰学部長の公開画像（北大公式サイト等）を使用。あわせてユーザー指定URL（https://www.memoriaactiva.com/yanaikekanato-1/）からも画像参照可能。
引用テロップを2行ずつ表示。
※（ユーザー要望L337「実際の画像を使用」完全準拠）（出典クレジット必須）

---

そして、屋名池さんと親しかった学生は、「友だちでした。何も言えない」「北大生はアウトドア好きが多いが、まさか、こんな身近な人が亡くなるなんて」「学生は皆、沈んだ様子」と回答しています。
（学校の背景にテキストを都度表示する表現）

【制作メモ】ASSET-157 [画面エフェクト / 背景+テキスト]
シーン: ユーザー要望L341通り「学校の背景にテキストを都度表示する表現」
背景プロンプト（16:9・フォトリアル）:
```
Exterior of Hokkaido University Faculty of Fisheries campus, soft autumn afternoon light, empty walkway with falling leaves. Quiet melancholic atmosphere. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 校舎の背景画像を固定し、3つの証言を順番にテロップ表示（1つずつフェードイン→アウト）。BGMを静かに、間をしっかり取る。
※（ユーザー要望L341「学校の背景にテキストを都度表示する表現」完全準拠）

---

北海道総合研究所は、今回のヒグマの印象について、「人を恐れず、積極的に攻撃する」と表現を残してますが、北海道のヒグマ調査において、ここまで強い表現が公的機関から出ることは滅多にありません。それほど異常な行動だったと言えます。

【制作メモ】ASSET-158 [画面エフェクト / 公的機関引用]
シーン: 「北海道総合研究所」の公的機関ロゴ＋引用テロップ
編集者指示: 「人を恐れず、積極的に攻撃する」の引用を画面中央に大きく赤字で表示。北海道総合研究所のクレジット。

---

ヒグマは人間の声を聞けば逃げていく。それが、何百年と続いてきた常識でした。

【制作メモ】ASSET-159 [画面エフェクト + 歴史]
シーン: 「何百年の常識」を伝える歴史的なヒグマと人のイラスト
プロンプト（16:9・フォトリアル）:
```
A historical illustration style depicting Ainu people coexisting with brown bears in old Hokkaido, traditional respect and distance between human and bear. Warm vintage tones. Photorealistic painterly style. 16:9. Generate 3 separate images.
```
編集者指示: 「何百年の常識」のテロップ。歴史的な距離感を視覚化。

---

## 13. ヒグマ人慣れの変化（修正版.txt L349-L395）— ASSET-160〜175

---

しかし、近年は人間を見ても逃げない。大声を聞いて、逆に距離を詰めてくる。そういった事例も増えています。
（回想シーンを使用）

【制作メモ】ASSET-160 [回想シーン / 過去動画再利用]
シーン: ユーザー要望L352通り「回想シーンを使用」
編集者指示: 当チャンネル過去動画から、ヒグマが人に向かってきたシーンを切り取って使用（福岡大・十和利山・羅臼岳など）。各クリップに「○○年 ○○事件」のテロップ。
※（ユーザー要望L352「回想シーンを使用」完全準拠）（再利用メモ：H13クラスタ強化）

---

なぜ、ヒグマが、ここまで「人慣れ」していたのか。事件の検証を進める中で、ある調査の存在が浮かび上がります。

【制作メモ】ASSET-161 [画面エフェクト + 引き]
シーン: 「ある調査の存在」の引きテロップ
編集者指示: 視聴者の興味を引くカット。「ある調査とは？」のテロップ。

---

ヘア・トラップ調査。
（黒背景にテキストのみ）

【制作メモ】ASSET-162 [画面エフェクト / 黒背景テキスト]
シーン: ユーザー要望L357通り「黒背景にテキストのみ」
編集者指示: 完全な黒画面に「ヘア・トラップ調査」のテキストを白文字大きめで表示。シンプル・印象的。
※（ユーザー要望L357「黒背景にテキストのみ」完全準拠）

---

これは、ヒグマの個体数や行動範囲を把握するための、科学調査のひとつです。

【制作メモ】ASSET-163 [画面エフェクト + 科学イメージ]
シーン: 科学調査のイメージ（地図にピンとデータ）
プロンプト（16:9・フォトリアル）:
```
A research office with a large map of Hokkaido on the wall, pins marking various locations, charts and data sheets. Scientific documentary atmosphere. Photorealistic, RED camera. 16:9. No identifiable people. Generate 3 separate images.
```
編集者指示: 「個体数・行動範囲 把握」のテロップ。

---

木の柱に、有刺鉄線（バラ線）を巻きつけ、その柱にクレオソートという液体をまんべんなく塗っていきます。

【制作メモ】ASSET-164 [背景静止画 / ヘア・トラップ装置]
シーン: ヘア・トラップ装置の構造図（木の柱に有刺鉄線、クレオソート塗布）
プロンプト（16:9・フォトリアル）:
```
A wooden post with barbed wire wrapped around it in a forest setting, a researcher's gloved hands applying a dark liquid (creosote) with a brush. Documentary detail shot. Photorealistic, RED camera. 16:9. Only hands visible. Generate 3 separate images.
```
編集者指示: 「ヘア・トラップ装置」のテロップ＋部品ラベル（木の柱／有刺鉄線／クレオソート）。

---

クレオソートは家屋の木材防腐剤としても使われる、強烈な匂いの液体です。

【制作メモ】ASSET-165 [背景静止画 + 商品]
シーン: クレオソート液体のクローズアップ
プロンプト（16:9・フォトリアル）:
```
A dark brown viscous creosote liquid in a glass container, close-up product photography, scientific lab setting. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「クレオソート / 木材防腐剤」のテロップ。「強烈な匂い」を伝える視覚化。

---

ヒグマは、この匂いに強く惹きつけられる性質があると分かっています。

【制作メモ】ASSET-166 [AI動画]
シーン: ヒグマがクレオソート臭に引き寄せられて近づく
プロンプト（16:9・フォトリアル）:
```
A brown bear in a forest, nose raised sniffing the air, then approaching a wooden post wrapped with barbed wire. Curious cautious posture. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「匂いに惹きつけられる」のテロップ。

---

引き寄せられたヒグマが、有刺鉄線に体を擦りつけることで、毛が抜け落ちるので、

【制作メモ】ASSET-167 [AI動画]
シーン: ヒグマが有刺鉄線に体を擦りつけ、毛が抜ける
プロンプト（16:9・フォトリアル）:
```
A brown bear rubbing its back against a barbed wire wrapped post in a forest, tufts of brown fur snagging on the wire. Documentary nature photography. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「毛が抜け落ちる」のテロップ。仕組みを視覚的に説明。

---

その毛をDNA分析することで、地域の生息頭数を把握するという仕組み。

【制作メモ】ASSET-168 [画面エフェクト + DNA図]
シーン: 採取された毛のDNA分析イメージ
プロンプト（16:9・フォトリアル）:
```
A scientific lab worker (hands only) collecting bear fur samples from barbed wire into sample bags, then placing them under a microscope. Modern lab equipment. Photorealistic, documentary style. 16:9. Only hands visible. Generate 3 separate images.
```
編集者指示: 「DNA分析→個体数推定」のフローテロップ。

---

どこを行動範囲にしているかも、すぐに判別可能です。

【制作メモ】ASSET-169 [Google Earth + データ表示]
シーン: GE上にヒグマの行動範囲マップ
編集者指示: 北海道のGE地図上に複数のヒグマ行動範囲をカラーゾーンで表示。

---

大千軒岳でも2008年頃から、このヘア・トラップ調査を実施。

【制作メモ】ASSET-170 [画面エフェクト + 年表]
シーン: 「2008年〜現在」のタイムライン＋大千軒岳の位置
編集者指示: 「大千軒岳 / 2008年〜実施」のテロップ。タイムライン視覚化。

---

しかしある団体が、このヘア・トラップ調査について問題点を指摘しています。

【制作メモ】ASSET-171 [画面エフェクト + 引き]
シーン: 「問題点指摘」の引きテロップ
編集者指示: 「ある団体が問題点を指摘」のテロップ。BGMで疑問を喚起。

---

というのも、人が仕掛けたクレオソートには、当然ですが人の匂いが付近に残ります。

【制作メモ】ASSET-172 [画面エフェクト + 説明]
シーン: 人の足跡や匂いを示すグラフィック
プロンプト（16:9・フォトリアル）:
```
Forest floor with visible human boot prints near a hair trap post, scattered leaves. Documentary detail. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「人の匂いが残る」のテロップ。

---

その状態でヒグマを呼ぶ好意は、「人間の匂いがするところには、何かいいものがある」と学習させてしまう可能性もあるのです。

【制作メモ】ASSET-173 [画面エフェクト + ヒグマ学習]
シーン: ヒグマが人の匂いと餌を関連付けて学習するイメージ
編集者指示: 「人の匂い ＝ 良いもの」と学習の図解テロップ。問題提起の核心。

---

同団体は、「ヒグマの餌付け行為と何ら変わらない」とも指摘しています。

【制作メモ】ASSET-174 [画面エフェクト / 引用]
シーン: 引用テロップ
編集者指示: 「ヒグマの餌付け行為と何ら変わらない」の引用を画面中央に赤字で表示。引用元（団体名は「流域の自然を考えるネットワーク」）クレジット。

---

現在、ヘア・トラップ調査は、渡島半島の鹿部周辺、富良野、知床、興部、札幌市、旭川など、全国的に行われています。そして、環境省からも予算が付くため、今後さらに広域・大規模化される見込みです。

【制作メモ】ASSET-175 [Google Earth / 全国マップ]
シーン: 北海道全域でヘア・トラップ調査実施地域をマッピング
GE座標:
- 渡島半島・鹿部: 約 `42°02'N, 140°45'E`
- 富良野: 約 `43°20'N, 142°23'E`
- 知床: 約 `44°09'N, 145°06'E`
- 興部: 約 `44°28'N, 143°09'E`
- 札幌市: 約 `43°03'N, 141°20'E`
- 旭川: 約 `43°46'N, 142°22'E`
編集者指示: 各地域に赤いピンを表示。「環境省予算 / 拡大予定」のテロップ。

---

## 14. するめ工場事件〜事件直前の状況（修正版.txt L387-L418）— ASSET-176〜189

---

クレオソートそのものは食物ではありません。

【制作メモ】ASSET-176 [画面エフェクト]
シーン: 「食物ではない」のテロップ
編集者指示: 「クレオソート ≠ 食物」のテロップ。次のテーマへの繋ぎ。

---

しかし、人間の足跡や体臭がそこに残っている以上、ヒグマが人間を覚えるきっかけにもなりえます。

【制作メモ】ASSET-177 [画面エフェクト + ヒグマ学習図]
シーン: ヒグマが学習する図解
編集者指示: 「人間 = 良いもの」のテロップ。シンプルな因果関係。

---

そして、この仮説が証明されるかのように、福島町とその周辺では、調査開始と共にヒグマ被害が相次いでいました。

【制作メモ】ASSET-178 [Google Earth + データ]
シーン: 福島町周辺のヒグマ被害マップ
GE座標: 福島町 `41°29'17"N, 140°16'00"E`（概算）
編集者指示: 福島町周辺に被害発生ピンを点滅表示。「調査開始＝被害増加」の対応関係を視覚化。

---

地元猟友会の関係者は、「これまで登山者がクマを見たことはあっても、人的被害はまずなかった」「それが、人が襲われる事故が出てきたのは、ここ数年のこと」と発言しています。
（テキストのみをタイミングごとに出す仕様）

【制作メモ】ASSET-179 [画面エフェクト / テキスト演出]
シーン: ユーザー要望L394通り「テキストのみをタイミングごとに出す仕様」
編集者指示: 黒背景or暗い背景に、証言テキストを1文ずつタイピングアニメで順に表示。
「これまで登山者がクマを見たことはあっても、人的被害はまずなかった」→ 数秒キープ→
「それが、人が襲われる事故が出てきたのは、ここ数年のこと」→ 数秒キープ。
「地元猟友会関係者」のクレジット。
※（ユーザー要望L394「テキストのみをタイミングごとに出す仕様」完全準拠）

---

また、大千軒岳事件の2ヶ月ほど前、麓に近いするめ工場で、ある事件が発生しています。

【制作メモ】ASSET-180 [背景静止画 + 引き]
シーン: 暗いするめ工場の外観
プロンプト（16:9・フォトリアル）:
```
A small rural dried squid (surume) processing factory in southern Hokkaido at night, exterior view. Wooden building with a metal shutter, single dim light over the entrance. Late summer atmosphere. Photorealistic, RED camera, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「事件の2ヶ月前」のテロップ。

---

何者かが、夜間、工場に侵入し、
（黒シルエット）

【制作メモ】ASSET-181 [画面エフェクト / 黒シルエット]
シーン: ユーザー要望L399通り「黒シルエット」
プロンプト（16:9・フォトリアル）:
```
A pure black silhouette of a large bear-shaped figure entering through a damaged metal shutter into a factory at night. Dark moody atmosphere. Photorealistic, RED camera. 16:9. Only the silhouette visible against the door. Generate 3 separate images.
```
編集者指示: 黒シルエットでヒグマを示唆。視聴者に「ヒグマだったのか？」と気づかせる演出。
※（ユーザー要望L399「黒シルエット」完全準拠）

---

干し終えたするめが、20万円分、食い荒らされてしまったのです。

【制作メモ】ASSET-182 [背景静止画 + 数字テロップ]
シーン: 散乱したするめと食い荒らされた様子
プロンプト（16:9・フォトリアル）:
```
Scattered dried squid (surume) products inside a damaged factory, torn packaging, signs of large animal disturbance. No animal visible. Photorealistic, RED camera, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「被害 20万円分」の赤字テロップ。

---

現場には大型獣の毛と足跡が残されており、工場の鉄製のシャッターは、外側から強引にこじ開けられ変形していました。

【制作メモ】ASSET-183 [背景静止画 + ディテール]
シーン: 大型獣の毛・足跡・歪んだシャッター
プロンプト（16:9・フォトリアル）:
```
Close-up details: bear fur stuck to a damaged metal shutter, large clawed footprints in the dust on the factory floor, the steel shutter twisted and bent outward from the inside. Documentary forensic photography. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「大型獣の毛 / 足跡 / 歪んだシャッター」のテロップを順に表示。

---

地元の住民は、「夜中に物音はしたが、まさかクマだとは思わなかった」「20年以上工場をやってきて、こんなことは初めて」と話しています。
（動画かイラストアニメ）

【制作メモ】ASSET-184 [動画かイラストアニメ]
シーン: ユーザー要望L406通り「動画かイラストアニメ」
プロンプト（16:9・フォトリアル）:
```
A worried local resident (face obscured or silhouette) standing near the damaged factory, looking at the broken shutter with concern. Documentary interview style. Photorealistic, RED camera. 16:9. No identifiable face. Generate 3 separate images.
```
編集者指示: 住民証言を引用テロップで2行ずつ表示。「20年以上で初めて」を強調。
※（ユーザー要望L406「動画かイラストアニメ」完全準拠）

---

そして2か月後、大千軒岳事件が発生。

【制作メモ】ASSET-185 [画面エフェクト + タイムライン]
シーン: 「8月 するめ工場」→「10月 大千軒岳事件」のタイムライン
編集者指示: 矢印アニメで時系列を視覚化。「2か月後」のテロップ。

---

するめ工場の一件は、ヒグマが人間の生活圏を「食料源」と認識し始めたサインだったとも言えます。

【制作メモ】ASSET-186 [画面エフェクト + 推論]
シーン: 「人間の生活圏 = 食料源」の認識アニメ
編集者指示: 「食料源と認識」の赤字テロップ。視聴者に「予兆だった」と気づかせる演出。

---

二つとも同じヒグマの仕業かはわかりませんが、まったく関係がないとも言えません。

【制作メモ】ASSET-187 [画面エフェクト]
シーン: 2つの事件を結ぶ点線アニメ
編集者指示: 「同個体？関連？」の疑問テロップ。視聴者に判断を委ねる演出。

---

実は、屋名池さんが大千軒岳に向かったとされる、10月29日。登山口には、ヒグマ注意の一般的な看板がありました。

【制作メモ】ASSET-188 [AI動画 + 看板]
シーン: 登山口の「ヒグマ注意」看板
プロンプト（16:9・フォトリアル）:
```
A weathered "Warning: Brown Bear" wooden sign at a remote mountain trailhead, generic content. Autumn forest background. Photorealistic, RED camera, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「ヒグマ注意」の一般的な看板を映す。

---

しかし、ヘア・トラップ調査が現在進行形で行われていることや2ヶ月前のするめ工場の事件についての看板はひとつもありませんでした。

【制作メモ】ASSET-189 [画面エフェクト + 強調]
シーン: 「情報なし」のテロップ。看板に取り消し線
編集者指示: 「ヘア・トラップ実施中：表示なし」「するめ工場事件：表示なし」の×印テロップ。情報共有の不全を強調。BGMで重さを出す。

---

---

## 15. 2024年5月再開放〜2024年10月3件鉢合わせ（修正版.txt L421-L448）— ASSET-190〜200

---

事件から半年後の2024年5月。事件直後にかけられていた入山禁止が解除され、車道は安全確認を終えて、一度シーズン開放されました。

【制作メモ】ASSET-190 [画面エフェクト + AI動画]
シーン: 「2024年5月」のテロップ＋林道のゲートが開く様子
プロンプト（16:9・フォトリアル）:
```
A metal gate at a forest road being opened by a worker, sunny spring morning. The road extends into a green forest beyond. Optimistic atmosphere. Photorealistic, RED camera, documentary style. 16:9. Worker from behind only. Generate 3 separate images.
```
編集者指示: 「2024年5月 / 入山禁止解除」のテロップ。穏やかなBGMで再開放を伝える。

---

しかし、その同じ年の10月。北海道新聞は、衝撃的な記事を掲載しました。

【制作メモ】ASSET-191 [画面エフェクト + 新聞]
シーン: 「2024年10月」のテロップ＋北海道新聞の見出し（実写）
編集者指示: 北海道新聞の該当記事スクショ（「10月にヒグマ鉢合わせ3件も町は把握できず」）を画面に。出典クレジット必須。

---

大千軒岳で、登山者がヒグマと至近距離で鉢合わせる事例が、10月だけで3件発生していたのです。

【制作メモ】ASSET-192 [画面エフェクト + 数字]
シーン: 「10月だけで3件」の数字を大きく表示
編集者指示: 「3件」を画面中央に大きく赤字で表示。視聴者の戦慄ポイント。

---

そのうちのひとつ。愛知県岡崎市から訪れた、71歳の登山者、山口洋一さん。

【制作メモ】ASSET-193 [キャラアニメーション + プロフィール]
シーン: 山口洋一さん（71歳・愛知県岡崎市）の新キャラ登場
キャラプロンプト（1:1・新規キャラCHAR-08）:
```
Cute cartoon character design, thick black outlines. CHAR-08: A 71-year-old Japanese male hiker, white hair, gentle determined expression, wearing a beige hiking jacket and brown pants, with a small daypack and hiking poles. Front-facing. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「山口洋一さん 71歳 / 愛知県岡崎市」のプロフィールテロップ。

---

5合目付近で、体長1.5メートルのヒグマと至近距離で遭遇。

【制作メモ】ASSET-194 [キャラアニメーション + 背景BG-A]
シーン: CHAR-08が5合目付近で別のヒグマ（CHAR-09・別個体）と遭遇
キャラプロンプト（1:1・CHAR-09 別ヒグマ）:
```
Cute cartoon character design. CHAR-09: A different brown bear, 150cm body length (slightly larger than CHAR-05), brown fur with reddish tint, alert expression. Front-facing. White background. 1:1. Generate 3 separate images.
```
編集者指示: 「5合目 / 別個体」のテロップ。CHAR-05とは別のヒグマであることを明示（混同を避ける）。

---

幸いなことに何事もなく下山することができましたが、取り返しのつかない事態になっていたかもしれませんでした。

【制作メモ】ASSET-195 [画面エフェクト]
シーン: 「無事下山」「しかし……」のテロップ
編集者指示: 「無事下山」の安堵カットから、「取り返しのつかない事態」への危機感へ転じる。

---

さらに驚くことに、福島町はこの事件を把握していませんでした。

【制作メモ】ASSET-196 [画面エフェクト + 強調]
シーン: 「福島町 / 把握せず」の赤字テロップ
編集者指示: 「自治体 把握せず」を画面中央に大きく赤字で表示。視聴者の戦慄ポイント。

---

担当者は、北海道新聞の取材に対し、「報告は、北海道新聞からの問い合わせで、初めて知った」と答えています。

【制作メモ】ASSET-197 [画面エフェクト / 引用テロップ]
シーン: 福島町担当者の証言引用
編集者指示: 「報告は、北海道新聞からの問い合わせで、初めて知った」の引用を画面中央に表示。北海道新聞のクレジット。

---

つい1年前に、大千軒岳で22歳の若者が亡くなったにもかかわらず、
（回想使用）

【制作メモ】ASSET-198 [回想 / 過去カット流用]
シーン: ユーザー要望L442通り「回想使用」
編集者指示: 屋名池さん関連の過去ASSET（ASSET-008、ASSET-013、ASSET-117など）から、CHAR-01の後ろ姿や暗転シーンを切り取って使用。色調をセピアに。
※（ユーザー要望L442「回想使用」完全準拠）（再利用メモ：チャンネル内ASSET流用）

---

人とヒグマの遭遇が3件発生し、
（回想使用）

【制作メモ】ASSET-199 [回想 / 過去カット流用]
シーン: ユーザー要望L445通り「回想使用」
編集者指示: 3件の鉢合わせシーンを、ASSET-194のような遭遇カットの色調セピア版で繋ぐ。
※（ユーザー要望L445「回想使用」完全準拠）（再利用メモ：ASSET-194流用）

---

地元自治体はその事実を知らないままだったのです。
（回想使用）

【制作メモ】ASSET-200 [回想 / 過去カット流用]
シーン: ユーザー要望L448通り「回想使用」
編集者指示: 福島町役場の風景（過去カットまたは新規生成）を色調セピアで表示。「知らないまま」のテロップ。BGMで重い余韻。
※（ユーザー要望L448「回想使用」完全準拠）

---

## 16. 北海道庁対応〜現在進行形（修正版.txt L450-L482）— ASSET-201〜215

---

北海道庁は、再びクマと人間が接近したということで、入山規制の判断基準づくりを進めることに。

【制作メモ】ASSET-201 [AI動画 + ロゴ]
シーン: 北海道庁の建物外観＋会議室での議論
プロンプト（16:9・フォトリアル）:
```
Hokkaido Prefectural Government office building in Sapporo, modern architecture, daytime. Photorealistic, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「北海道庁」のロゴ＋「入山規制の判断基準づくり」のテロップ。

---

未整備の車道の閉鎖、住民への自粛要請、ヒグマ目撃情報の共有体制、ヘア・トラップ調査の見直しを実施。

【制作メモ】ASSET-202 [画面エフェクト / 施策リスト]
シーン: 4つの施策を順に箇条書きで表示
編集者指示: 各施策を1つずつテロップで順に表示（フェードイン）:
1. 未整備の車道の閉鎖
2. 住民への自粛要請
3. ヒグマ目撃情報の共有体制
4. ヘア・トラップ調査の見直し

---

しかし、これだけでは根本的な解決とは至らなかったといいます。

【制作メモ】ASSET-203 [画面エフェクト + 引き]
シーン: 「根本的な解決ではない」のテロップ
編集者指示: BGMを再びダークに切り替え、「しかし……」のテロップで次のテーマへ繋ぐ。

---

というのも、車道が閉じられたとしても、登山道はゲートをくぐれば簡単に入れる状態でした。

【制作メモ】ASSET-204 [AI動画]
シーン: 林道のゲートを徒歩で迂回する人のシルエット
プロンプト（16:9・フォトリアル）:
```
A closed metal gate at a forest road with a "no entry" sign, but a clear path around the gate where people can simply walk past on foot. Sunny day. Photorealistic, RED camera. 16:9. No identifiable people. Generate 3 separate images.
```
編集者指示: 「ゲートをくぐれば入れる」のテロップ。物理的に閉ざせない問題を視覚化。

---

そのため、人とヒグマが接近する可能性は依然として残っていたのです。

【制作メモ】ASSET-205 [画面エフェクト + 強調]
シーン: 「人とヒグマの接近 / 依然として残る」のテロップ
編集者指示: 赤字テロップ。問題が解決していないことを強調。

---

また、いくら自粛するよう要請しても、強制力のないお願いに過ぎません。

【制作メモ】ASSET-206 [画面エフェクト + 説明]
シーン: 「自粛要請 ＝ 強制力なし」のテロップ
編集者指示: 「自粛要請：強制力なし」の赤字テロップ。法的限界を伝える。

---

結局、最後にゲートをくぐるのも、引き返すのも、本人次第と言えます。

【制作メモ】ASSET-207 [画面エフェクト + 引き]
シーン: 「最後は本人次第」のテロップ
編集者指示: 「最後は本人次第」のテロップを画面中央に。重い責任感を強調。

---

そして、その翌年。

【制作メモ】ASSET-208 [画面エフェクト]
シーン: 「2025年へ」のテロップ
編集者指示: 「2025年」の年テロップを大きく表示。

---

2025年5月30日、封鎖中の登山道に無理やり登山者が侵入してしまいます。

【制作メモ】ASSET-209 [AI動画]
シーン: 閉ざされた登山道のゲートを徒歩で越える登山者
プロンプト（16:9・フォトリアル）:
```
A hiker in spring outdoor clothing walking past a closed metal gate with "no entry" sign, deliberately ignoring the warning. Spring morning forest light. Photorealistic, RED camera, documentary style. 16:9. No identifiable face. Generate 3 separate images.
```
編集者指示: 「2025年5月30日 / 封鎖中の登山道に侵入」のテロップ。

---

そこで、親子と思われる2頭のヒグマと至近距離で遭遇する事例が発生しました。

【制作メモ】ASSET-210 [キャラアニメーション]
シーン: 親子と思われる2頭のヒグマと登山者が遭遇
キャラプロンプト（1:1）:
```
Cute cartoon character design. Two brown bears: a larger mother bear and a smaller cub, standing on a forest trail. Both alert, looking at an unseen hiker. White background. 1:1. Generate 3 separate images, each showing these 2 characters together.
```
編集者指示: 「親子ヒグマ / 至近距離遭遇」のテロップ。CHAR-05とは別個体であることを明示。

---

福島町、檜山森林管理署、松前警察署は協議の上、2025年シーズン中の登山道開通を見送ることに決定。

【制作メモ】ASSET-211 [画面エフェクト + ロゴ]
シーン: 3機関のロゴ＋「協議」のテロップ
編集者指示: 福島町・檜山森林管理署・松前警察署の3機関ロゴを順に表示。「協議」「2025年シーズン 開通見送り」のテロップ。

---

「安全確保ができるまでは、ゲートを開けない」

【制作メモ】ASSET-212 [画面エフェクト / 引用]
シーン: 福島町の決定的な引用を画面中央に
編集者指示: 「安全確保ができるまでは、ゲートを開けない」の引用を画面中央に大きく白字で表示。BGMで決意の重さを伝える。

---

これ以上の被害を出してはいけないと、福島町の決断は明確でした。

【制作メモ】ASSET-213 [画面エフェクト + 解説]
シーン: 「福島町の決断」のテロップ
編集者指示: 「これ以上の被害を出さない」の決意テロップ。BGMで余韻。

---

それから事件から2年が経過した、現在。

【制作メモ】ASSET-214 [画面エフェクト]
シーン: 「事件から2年 / 現在」の年経過テロップ
編集者指示: 「2023→2024→2025→現在」のタイムラインで時間経過を視覚化。

---

大千軒岳の車道のゲートは、今もなお閉ざされたままです。

【制作メモ】ASSET-215 [背景静止画 + 現状]
シーン: 閉ざされたままの林道ゲート（現在）
プロンプト（16:9・フォトリアル）:
```
A closed and rusted metal gate at the entrance of a forest road on Daisengen-dake, overgrown with weeds, a "no entry" sign weathered. Late autumn or current season. Long-term closure suggested. Photorealistic, RED camera, documentary style. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「今もなお閉ざされたまま」のテロップ。BGMで長期的な余韻。

---

## 17. エンディング（修正版.txt L480-L501）— ASSET-216〜225

---

登山道も入山自粛は呼びかけられてはいるものの、いつでも入ろうと思えば入れる状態。

【制作メモ】ASSET-216 [背景BG-A + テロップ]
シーン: 入山自粛の貼り紙とその先に伸びる登山道
プロンプト（16:9・フォトリアル）:
```
A "voluntary restraint requested" sign posted on a wooden post at the edge of an open hiking trail. The trail extends into the forest beyond. Quiet melancholic atmosphere. Photorealistic, RED camera. 16:9. No people. Generate 3 separate images.
```
編集者指示: 「入山自粛 呼びかけ / 入ろうと思えば入れる」のテロップ。

---

いまもなお、登山道の7合目付近には、土と枝で覆われた青年が発見された場所が存在しています。

【制作メモ】ASSET-217 [背景BG-B 流用 + エンディング]
シーン: BG-B（沢沿いの薄暗い現場）を発展形で再利用＋現在の風景
背景プロンプト（16:9・フォトリアル）:
```
The same ravine on Daisengen-dake at 550m elevation where the body was found, now overgrown with bamboo grass and time. Quiet still atmosphere, fall season. Empty, no human traces visible anymore. Photorealistic, RED camera, documentary style. 16:9. No people, no bodies. Empty natural scenery. Generate 3 separate images.
```
編集者指示: 「今は静かに笹に覆われています」のニュアンスを伝える。BGMで深い余韻。
※（再利用メモ）BG-Bの素材を「現在は静か」に発展させて再利用。エンディング案4の場所への着地を強化。

---

この事件を間近で体験した船板さんはこの事件について、

【制作メモ】ASSET-218 [キャラアニメーション + 証言導入]
シーン: CHAR-04（船板さん）のアップ
編集者指示: CHAR-04アップ画像（ASSET-061流用可）。「船板さんの証言」のテロップ。

---

「クマとの格闘のトラウマは、時間が解決すると思っています」

【制作メモ】ASSET-219 [証言テロップ]
シーン: 証言テキストを画面中央に
編集者指示: 証言テロップを白文字でゆっくり表示。タイピングアニメ可。

---

「でも、夜、寝ようとして目を閉じると、目撃した一連の光景がフラッシュバックするんです」

【制作メモ】ASSET-220 [証言テロップ + フラッシュバック]
シーン: フラッシュバック演出（過去のASSETを瞬間的に挿入）
編集者指示: 証言テキストを画面中央に表示しながら、ASSET-001、ASSET-068、ASSET-084などの過去ASSETの一部を一瞬の閃きで重ねる。
※（再利用メモ）複数の襲撃シーン流用でフラッシュバック演出。

---

「当分、登山はする気にならないと思います」

【制作メモ】ASSET-221 [証言テロップ + 静寂]
シーン: 静かな証言締めくくり
編集者指示: 証言テロップを最後にゆっくり表示。BGMを最小限にして、言葉の重みを残す。

---

と振り返っています。

【制作メモ】ASSET-222 [画面エフェクト]
シーン: 「船板さん 証言」のクレジット
編集者指示: 短い間。次のメッセージへの間を空ける。

---

これまでクマは、人間を恐れる動物でした。しかし、わずか数十年で、その常識は崩れつつあります。

【制作メモ】ASSET-223 [画面エフェクト + AI動画]
シーン: ヒグマと人間の距離が縮まっていく時代の変化アニメ
プロンプト（16:9・フォトリアル）:
```
A symbolic representation of time passing: a brown bear in old forest gradually appearing closer and closer to a modern town in the same frame, suggesting the loss of natural distance. Atmospheric, painterly. Photorealistic, RED camera. 16:9. No identifiable people. Generate 3 separate images.
```
編集者指示: 「常識の崩壊」のテロップ。BGMで時代変化を表現。

---

私たちがこれからクマとどう関わっていくのか。その問いに、まだ明確な答えは出ていません。

【制作メモ】ASSET-224 [画面エフェクト + 問いかけ]
シーン: 視聴者への問いかけテロップ
編集者指示: 「私たちがこれからクマとどう関わっていくのか」の問いかけを画面中央に大きく表示。BGMで余韻を持続。

---

屋名池奏人さんのご冥福を、心よりお祈り申し上げます。

【制作メモ】ASSET-225 [画面エフェクト + 鎮魂]
シーン: 静かな黒背景に屋名池さんの名前
プロンプト（16:9）:
```
A solemn black background with simple elegant Japanese text honoring the deceased, a single small candle flame or chrysanthemum flower in the corner. Respectful, minimal. 16:9. Generate 3 separate images.
```
編集者指示: 屋名池奏人さんの名前をテロップで静かに表示。「ご冥福をお祈り申し上げます」の文字を白文字で。BGMは静かに、間を取る。

---

最後までご視聴いただき、ありがとうございました。

【制作メモ】ASSET-226 [画面エフェクト + クロージング]
シーン: チャンネルロゴ＋関連動画への誘導
編集者指示: 「最後までご視聴いただき、ありがとうございました」のテロップ。終了画面用カット。次の動画への自然な流れ（福岡大→十和利山→羅臼岳 等、H13クラスタ動画3本連鎖を終了画面に表示）。BGMでフェードアウト。

---

## 全体まとめ

### ASSET番号最終確認
- ASSET-001 〜 ASSET-226 連番（飛び番なし）
- 各ASSETは台本のナレーション登場順に対応

### キャラ・背景プリセット使用一覧
- **CHAR-01（屋名池さん）**: ASSET-008, 010, 013, 108, 198
- **CHAR-02（大原さん）**: ASSET-037, 049, 052, 064, 076, 077, 079, 080, 081, 083, 084, 087, 088, 089, 091, 094, 096, 101
- **CHAR-03（阿部さん）**: ASSET-038, 052, 092, 094, 096, 101
- **CHAR-04（船板さん）**: ASSET-039, 052, 061, 069, 070, 071, 072, 087, 089, 094, 096, 101, 218
- **CHAR-05（加害ヒグマ）**: ASSET-057, 058, 060, 067, 068, 069, 071, 077, 079, 080, 081, 082, 084, 085, 087, 088, 089, 090, 099, 124
- **CHAR-06/07（トレッドウェル夫妻）**: 実写優先（ASSET-140, 141）
- **CHAR-08（山口洋一さん）**: ASSET-193
- **CHAR-09（2024年別ヒグマ）**: ASSET-194
- **CHAR-10（2025年親子ヒグマ）**: ASSET-210
- **BG-A（笹薮の登山道）**: ASSET-013, 035, 052, 053, 054, 056, 057, 060, 074, 090, 095, 109, 216
- **BG-B（沢沿いの現場）**: ASSET-005, 118, 217
- **BG-C（函館港町）**: ASSET-008
- **BG-D（福島町の山々）**: ASSET-019

### 再利用ASSET一覧（素材コスト節約）
- ASSET-001 → ASSET-082（爪が太ももに食い込むシーン、フック伏線回収）
- ASSET-002 → ASSET-070（仰向け視点）
- ASSET-003 → ASSET-048（5cmナイフ）
- ASSET-005 → ASSET-118（土と枝の地面）
- ASSET-036 → ASSET-050（GE登山ルート）
- ASSET-039 → ASSET-093, 094（3人並び）
- ASSET-061/064 → ASSET-083, 091, 218（船板さん・大原さんアップ）
- ASSET-085 → ASSET-124（ナイフ刺さったヒグマ）
- ASSET-117 → ASSET-119, 122（黒塗りシルエット）
- ASSET-194 → ASSET-199（鉢合わせシーン）
- ASSET-001/068/084 → ASSET-220（フラッシュバック演出）

### Google Earth座標一覧
- **大千軒岳 山頂**: `41°34'46"N, 140°09'39"E`（Wikipedia確定値・標高1,071.87m）
- **奥二股登山口（東・福島町）**: 約 `41°33'00"N, 140°15'00"E`（概算・要GE実測）
- **旧道登山口（西・松前町石崎経由）**: 約 `41°35'30"N, 140°07'30"E`（概算）
- **新道登山口（西・松前町上川）**: 約 `41°36'00"N, 140°07'00"E`（概算）
- **7合目襲撃地点**: 概算 `41°33'30"N, 140°13'30"E`（実測要）
- **再遭遇地点（500m下）**: 概算 `41°33'25"N, 140°14'00"E`（実測要）
- **函館市港町（出発地）**: 約 `41°47'00"N, 140°43'00"E`
- **福島町**: 約 `41°29'17"N, 140°16'00"E`
- **ヘア・トラップ調査地域**: 渡島半島・鹿部、富良野、知床、興部、札幌市、旭川（各座標は本文参照）

### ユーザー要望（カッコ表記）完全反映確認
- L60「実際の画像を使用」→ ASSET-030
- L73「捜索予定のルートの座標」→ ASSET-036
- L241/246/253「黒塗り状態のイラスト」→ ASSET-117, 119, 122
- L276「新聞の実写画像」→ ASSET-130
- L297/300「実写を使用」→ ASSET-140, 141
- L309「動画内のシーンを切り取り使用」→ ASSET-145
- L322/337「実際の画像を使用」→ ASSET-150, 156
- L341「学校の背景にテキストを都度表示する表現」→ ASSET-157
- L352「回想シーンを使用」→ ASSET-160
- L357「黒背景にテキストのみ」→ ASSET-162
- L394「テキストのみをタイミングごとに出す仕様」→ ASSET-179
- L399「黒シルエット」→ ASSET-181
- L406「動画かイラストアニメ」→ ASSET-184
- L442/445/448「回想使用」→ ASSET-198, 199, 200

### 注意事項
- 本ファイルはナレーション本文を1字も改変していない（修正版.txtから完全保持）
- ASSET番号は001〜226まで連番（飛び番なし）
- 座標の一部は概算のため、本番GE設定時に実測値で更新推奨
- 過去動画クリップ流用箇所はチャンネル内アーカイブから素材抽出が必要

---

