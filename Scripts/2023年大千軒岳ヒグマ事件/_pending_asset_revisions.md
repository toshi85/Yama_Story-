# 2023年大千軒岳ヒグマ事件 — 別PC継続用 残作業プロンプト

> **作成日**: 2026-05-18
> **目的**: 別PCで作業継続するときに、ここに貼ってある改訂プロンプトをMaster.mdの該当ASSETに上書きする
> **完了済み**: ASSET-001 / 075 / 077 / 078 / 079 / 081 / 082(再利用設計に戻し、現状維持) / 083 / 086 / 091 / 092 / 095
> **残作業**: 以下のASSET-101 / 102 / 105 / 108 / 109 を Master.md に反映

---

## 重要ルール（別PC作業時に必ず確認）

1. **再利用マーカー最先頭**: `(CHAR-XX 再利用)` はプロンプトの**1文字目から**書く。固定スタイルヘッダー6要素より前に置く。
2. **AI動画は2ブロック構成**: 静止画(16:9フォトリアル) + Google Flow動画プロンプト
3. **流血禁止**: `No blood visible, no graphic injuries shown.` 明記
4. **暴力描写は寸前止め**: `about to bite down` 等
5. **複数キャラ同居末尾**: `Generate N separate images, each showing these N characters together.`
6. **完了前**: `python3 Yama_Story/System_Tools/validate_yama_prompts.py 修正版_Master.md` 実行、違反0件確認

---

## ASSET-101 [キャラアニメーション + プロップ + 追跡クマ + 実写背景]

**シーン**: 3人が石を投げて追い払いながら必死に下山、横向きで追ってくるナイフ刺さったヒグマ

### ① キャラプロンプト（1:1 / 3人投擲モーション・手は空・視線一致）
```
(CHAR-02、CHAR-03、CHAR-04 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. Three battered firefighters retreating backward down a slope while continuously throwing stones toward the same unseen threat behind them. CHAR-03 (Abe, dark red hiking jacket torn at the shoulder, dark gray pants scratched and dirty) on the left, CHAR-02 (Ohara, dark olive green hiking jacket, tactical hiking pants torn at the right thigh, tactical backpack) in the center, CHAR-04 (Funaita, dark navy blue hiking jacket torn at the shoulder, brown cargo pants torn at the right thigh) on the right. Each of them: stepping backward awkwardly with weight shifted to the back foot, one arm cocked back high in a mid-throw motion with the hand empty and fingers spread open (the stones to be composited separately), the other arm extended forward for balance, torso twisted in the same direction toward the threat behind, head turned and looking back over the same shoulder, all three pairs of eyes locked on the exact same point behind them with identical fearful intense focus, brows tightly furrowed, teeth gritted in desperate determination, sweat dripping down their faces, every muscle braced and trembling. The three share one unified gaze fixed on the same threat. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 3 characters together.
```

### ② 石プロップ画像（1:1）
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Several small to medium rough mountain stones shown as isolated prop objects — gray and brown granite-like surface texture, irregular jagged shapes, varying sizes from fist-size down to pebble. Clean cartoon line art, no characters, no hands, no background details. The stones float spread across the canvas at different angles. White background, no shadow. 1:1 aspect ratio. Generate 3 separate images.
```

### ③ CHAR-05（横向き / ナイフ刺さり追跡）プロンプト（1:1）
```
(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body, side view profile facing right. CHAR-05 (young male Hokkaido brown bear, 125cm body length, muscular build, dark brown fur) standing in side-view silhouette — head lowered slightly with eyes glaring sideways with cold predatory focus, ears flattened, mouth open in a low menacing growl with sharp teeth visible. A small folding knife (5cm silver blade, black molded handle) is embedded in the side of his throat with the handle sticking out at an angle. Body still tense and dangerous despite the wound, weight balanced on all four paws, dark thick fur ruffled along the back. The bear remains an active threat. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images.
```

### ④ 背景プロンプト（16:9・フォトリアル / 下山中の登山道）
```
A descending mountain hiking trail on Daisengen-dake in late autumn, viewed from a slightly elevated angle looking down the path. Damp dirt path winding sharply downward, dense tall sasa bamboo grass walls on both sides over two meters high, scattered fallen leaves on the path, occasional broken twigs and disturbed earth from recent hurried passage. Cold overcast late autumn afternoon light filtering through dense conifer canopy overhead, deep shadows along the trail. Tense oppressive atmosphere of desperate escape, the trail stretching ahead into uncertain forest gloom. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 3 separate images.
```

### 編集者指示
- 背景④を下地に敷く
- 3人キャラ①を画面手前に配置（後ろ向きに下る構図）
- CHAR-05③を画面奥に配置（横向き、追ってくる構図）
- 石プロップ②を3人の手から後方へ高速飛行するモーションで合成（複数の石が円弧軌道を描く）
- 「石を投げ追い払い」のテロップ
- BGMで緊張を保ちつつ「必死の下山」感を演出
- 石が地面やヒグマ近くに着弾する「コツン」「カチン」SEを散らす
- ヒグマは石を浴びてもじりじり追ってくる威圧感を演出

---

## ASSET-102 [キャラアニメーション + 実写背景 + ロゴ展開]

**シーン**: 下山直後、登山口の駐車場で警察・消防・北海道庁に緊急電話する3人

### ① キャラプロンプト（1:1 / 3人緊急通報）
```
(CHAR-02、CHAR-03、CHAR-04 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. Three battered firefighters standing close together making urgent phone calls immediately after descending from the mountain. CHAR-03 (Abe, dark red hiking jacket torn at the shoulder, dark gray pants scratched and dirty) on the left, CHAR-02 (Ohara, dark olive green hiking jacket, tactical hiking pants torn at the right thigh, tactical backpack) in the center, CHAR-04 (Funaita, dark navy blue hiking jacket torn at the shoulder, brown cargo pants torn at the right thigh) on the right. Each of them: holding a smartphone tightly pressed to one ear with one hand, the other hand gesturing emphatically while speaking, mouths open and speaking rapidly with urgent serious expressions, brows tightly furrowed in focused intensity, eyes sharp and locked forward, sweat and dirt still on their faces from the descent, posture upright but visibly exhausted, bodies still trembling slightly from the recent ordeal. The urgency of the report etched on every face. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 3 characters together.
```

### ② 背景プロンプト（16:9・フォトリアル / 登山口駐車場）
```
A small mountain trailhead parking lot at the base of Daisengen-dake in late autumn afternoon. A modest gravel-and-dirt clearing with a single old SUV parked off to one side, a wooden trail information signpost near the entry path, dense forest of conifers and bare deciduous trees surrounding the lot. Fallen leaves scattered across the gravel, distant mountain peaks visible through the trees on the horizon. Cold overcast late autumn afternoon light, deep shadows under the tree canopy. Quiet remote atmosphere of a rural mountain access point, far from the nearest town. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 3 separate images.
```

### 編集者指示
- 背景②（登山口駐車場）を下地に、3人キャラ①を中央〜手前に配置
- 通話している3人の画面右側に、警察・消防・北海道庁のロゴを順次フェードイン（各2秒）
- 「ただちに通報」のテロップを下部に表示
- 電話の呼び出し音SE → 受話SE → 緊迫した会話の遠い背景音をフェード
- BGMは緊張感あるサスペンス調、ロゴ表示時に決断系の重い一音

---

## ASSET-105 [キャラアニメーション + 実写背景]

**シーン**: 病院で治療を受けて包帯を巻かれたが、その日のうちに回復に向かう元気な3人

### ① キャラプロンプト（1:1 / 3人包帯+元気）
```
(CHAR-02、CHAR-03、CHAR-04 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, slightly chibi proportions, children's animation style. Full body. Three firefighters freshly treated at the hospital, visibly recovering with relieved cheerful energy. CHAR-03 (Abe, dark red hiking jacket, dark gray pants, a white bandage wrapped around his right elbow and a small square bandage on his left cheek) on the left, CHAR-02 (Ohara, dark olive green hiking jacket, tactical hiking pants, a thick white gauze bandage wrapped around his right thigh visible over the pants, smaller bandages on the back of his hands) in the center, CHAR-04 (Funaita, dark navy blue hiking jacket, brown cargo pants, a wide white bandage wrapped around his neck and another bandage around his right thigh) on the right. Each of them: standing upright on their own feet with surprisingly good posture, a relieved tired smile on their face, color returned to their cheeks, eyes warm and slightly tearful from sheer relief, faces now clean and washed of dirt, one hand giving a small thumbs-up or held lightly at the side, the other relaxed. Bandages are clean white and freshly applied. The three look battered but undeniably alive and on the mend. No blood visible, no graphic injuries shown. White background. 1:1 aspect ratio. Generate 3 separate images, each showing these 3 characters together.
```

### ② 背景プロンプト（16:9・フォトリアル / 病院の処置室）
```
A clean modern Japanese regional hospital treatment room in the late afternoon. Pale beige walls, a treatment bed with crisp white sheets in the center of the room, an examination chair to one side, a small wheeled medical cart with bandages, gauze rolls, and antiseptic bottles arranged neatly, a wall-mounted blood pressure monitor, a curtain partition partially drawn to the side. Bright clinical fluorescent lighting from overhead with soft warm window light from one side, polished vinyl floor reflecting the light. Quiet sterile atmosphere of a small rural hospital, calm and orderly. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty interior only. Generate 3 separate images.
```

### 編集者指示
- 背景②（処置室）を下地に、3人キャラ①を中央に配置
- 「入院なし / その日のうちに回復」のテロップを上部に表示
- BGMを安堵のトーン（暖かい弦楽器系）に切り替え、視聴者にカタルシスを与える
- 「驚くことに」のテロップを軽く強調エフェクト付きで表示
- 3人の包帯を順にハイライト→ズームでケガの軽さを視覚化

---

## ASSET-108 [AI動画 / Lovart or Google Flow]

**シーン**: 行方不明となった屋名池さんを捜索する警察・山岳救助隊の実写映像

### ① 静止画プロンプト（16:9・フォトリアル）
```
A search team of Japanese police officers and mountain rescue personnel in fluorescent orange and white uniforms with helmets methodically searching through dense forest understory on Daisengen-dake in late autumn. Multiple searchers spread out in a line, walking slowly forward with long search sticks probing through dense tall sasa bamboo grass and fallen leaves on the forest floor. One officer holds a portable radio to his mouth speaking into it, another scans the terrain ahead with binoculars, another crouches to examine the ground for tracks. Search dogs on leashes alongside the handlers. Cold overcast late autumn afternoon light filtering through the dense conifer canopy overhead, deep shadows along the forest floor. Their breath faintly visible in the cold air. Tense somber atmosphere of a serious missing-person operation. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 3 separate images.
```

### ② Google Flow動画プロンプト
```
A 5-second slow-motion documentary video footage on Daisengen-dake in late autumn at a missing-person search operation. Camera films a line of search team officers in fluorescent orange uniforms with helmets walking slowly forward through dense sasa bamboo grass and forest understory, their long search sticks probing the ground in synchronized rhythm, their breath visible faintly in the cold autumn air. One officer raises a portable radio to his mouth and speaks into it, another scans the slope with binoculars, a search dog handler advances along the flank. The camera holds steady tracking the line as they advance carefully through the dense undergrowth. Cold overcast afternoon light, deep shadows under the conifer canopy. Photorealistic, RED camera, slow-motion documentary cinematography.
```

### 編集者指示
- ①の静止画 → ②の動画クリップへ繋ぐ
- 「屋名池さんの捜索は続く」のテロップを画面下に表示
- 画面右上に CHAR-01（屋名池さん）の小さなキャラ画像を回想カットとしてフェードイン（ASSET-008 流用可）
- BGMを再びシリアスなトーンへ切り替え、緊張感と悲壮感を両立
- 無線の交信音SE・足音SE・笹葉のざわめきSEを背景に重ねる

---

## ASSET-109 [AI動画 / Lovart or Google Flow]

**シーン**: 笹薮の奥深くに潜む消防士を襲ったヒグマのシルエット

### ① 静止画プロンプト（16:9・フォトリアル）
```
A dense tall sasa bamboo grass forest deep on Daisengen-dake in late autumn afternoon, viewed at trail level. Deep within the bamboo wall, the vague half-hidden silhouette of a massive Hokkaido brown bear is partially visible — dark shaggy fur blending into the shadows, only a portion of the head and shoulder discernible through the dense vertical grass blades, two faint glints of predatory eyes catching the dim filtered light. The bamboo grass blades hang motionless around it. Cold overcast afternoon light filtering weakly through the dense conifer canopy overhead, deep shadows pooling throughout the understory. Oppressive eerie silence and tension, the threat lurking unseen by hikers. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 3 separate images.
```

### ② Google Flow動画プロンプト
```
A 5-second slow-motion documentary video footage on Daisengen-dake in late autumn, deep within a dense tall sasa bamboo grass forest. Camera holds steady at trail level looking into the depths of the bamboo wall. The bamboo blades stand motionless in the cold still air. Slowly, almost imperceptibly, a dark massive shape shifts in the shadows behind the bamboo — the half-hidden silhouette of a brown bear's head and shoulder rotates slightly toward the camera, two faint predatory eyes catch the dim filtered light and lock onto the viewer. The bamboo barely sways from the bear's movement. Cold overcast afternoon light, deep shadows pooling under the conifer canopy. Oppressive eerie atmosphere of an unseen threat watching from the dark. Photorealistic, RED camera, slow-motion documentary cinematography.
```

### 編集者指示
- ①の静止画→②の動画クリップへ繋ぐ（静止からの微細な動きで観る人を不安にさせる）
- 「ヒグマはまだ潜んでいる」のテロップを画面下部に赤字で表示
- BGMで不安を持続、低音のドローン音を底に敷く
- 笹葉のかすかなざわめきSE+遠くのカラスの鳴き声SEで森の不気味さを演出
- 数秒の沈黙からヒグマの目が光るカットで視聴者の緊張をMAXに

---

## 別PCでの作業手順

1. `git pull origin main` で最新を取得
2. `修正版_Master.md` を開き、ASSET-101 / 102 / 105 / 108 / 109 の各ブロックを上記プロンプトで上書き
3. 上書き後、ファイル末尾の参照用 `_pending_asset_revisions.md` は削除（または `done_` プレフィックスを付けて残す）
4. `python3 Yama_Story/System_Tools/validate_yama_prompts.py 修正版_Master.md` で検証、違反0件確認
5. `git add` → `git commit` → `git push`
