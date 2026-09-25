# せたな町 本人確認後の作り直し（2026-09-25・030〜050）

# 何度も出る人物の固定（このファイル以降は必ず再利用）

### CHAR-05｜地元のハンター（60代・捜索・わな設置・足跡の確認で毎回同じ人）

```text
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. One full-body Japanese local hunter in his 60s with short grey hair and a grey stubble, an orange cap, a dark green field jacket under a blaze-orange safety vest, khaki trousers and brown boots, a small backpack. No lettering, no badge, no logo. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw him with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```

### CHAR-06｜町の職員（40代・役場の対応で毎回同じ人）

```text
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. One full-body Japanese male town official in his 40s with short black hair, a navy work jacket, a light blue shirt, grey trousers and black shoes. No lettering, no badge, no logo, no name tag. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw him with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```

### CHAR-07｜研究者（40代女性・道総研の調査で毎回同じ人）

```text
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. One full-body Japanese female researcher in her 40s with shoulder-length dark brown hair tied back, a plain white lab coat over a navy top, grey trousers and black shoes. No lettering, no badge, no logo, no name tag. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw her with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```

---

ナレーター: また、現場から南へおよそ200メートルには、38世帯が暮らす新成地区の集落があり、かなり民家から近い地点でのクマ事件だったと言えるでしょう。

【制作メモ】ASSET-030 [Google Earth] 台本L50
シーン: Google Earthで現場付近と、その南約200mの新成の集落を1画面に入れ、2点を赤いラインで結ぶ。
- 検索座標: `42.3605, 139.8030`
- カメラ高度: 約800m
- カメラ角度: 斜め45°、3D地形ON
- 向き: 北→南（現場付近の丘の山林が手前、新成の集落が奥）
- 現場付近（道新「集落から北へ約200m・高さ約30mの丘の山林」から推定）: 約 `42.3645, 139.8060`（標高 約36m）
- 新成の集落（OSM建物の集まりの中心）: `42.3565, 139.7998`（標高 約66m）
- 演出: 現場付近に赤ピン＋「現場付近」ラベル／集落に白ラベル「新成の集落（38世帯）」／2点を赤いラインで結び「約200m」／集落の屋根と畑が見分けられる高さで止める
→ 編集者指示: 中央に「民家から約200m」を白字で表示し、「200m」だけ赤字。Google Earthと画像提供元のクレジットを表示中ずっと残す。

---

ナレーター: 地元の方によると、亡くなった奥さんは、次の日に夫とともに札幌に住む一人娘を訪ねる予定だったとのこと。

【制作メモ】ASSET-031 [キャラアニメーション] 台本L52
シーン: 新成の集落の家の前で、地元の高齢女性が涙ぐみながら、亡くなった女性の翌日の予定を悲しそうに語る。
キャラプロンプト（1:1）:
```
Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese local woman in her late 70s with short white permed hair, a slightly bent back, a mauve cardigan over a cream blouse, dark grey slacks and simple slip-on shoes, standing square to the viewer with her shoulder line parallel to the picture plane, her face clearly visible. She holds a folded handkerchief to her chest with both hands, tears running down both cheeks, eyebrows slanted steeply upward in the middle, mouth bent into a trembling downturned frown, grieving and heartbroken, NOT calm, NOT smiling. Only this one woman, no other people. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw her with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```
背景プロンプト（16:9）:
```
The front of an old wooden two-storey rural house in the small farming settlement of Shinsei near Setana, southwestern Hokkaido, in mid-April early spring: a small front yard, a vegetable plot, forested hills behind with bare and budding trees, No snow anywhere, no frost, no ice, no winter. No readable text, no nameplate, no sign. Framed from adult eye height about four metres back, the middle of the frame left as clear open space. Quiet, mournful, soft overcast light, muted natural tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 1 image.
```
→女性セリフ「娘さんに／会いに行くはずだったのに、、」
→ 編集者指示: 背景・キャラとも新規。女性を中央に置き、うつむくように小さく上下させる（動画は作らない）。左上に「翌日、娘に会う予定だった」を白字で置き、「娘」だけ赤字。

---

ナレーター: ちなみにこの年は、今回の事件が起きるまで、町にはクマの目撃情報が寄せられていませんでした。

【制作メモ】ASSET-032 [Lovart動画] 台本L54
シーン: せたな町の集落の上を、ドローン視点でゆっくり進む。静かで、クマの気配のない春の町。
```
A high aerial drone view over a small quiet farming settlement near Setana, southwestern Hokkaido, in mid-April early spring: low houses with dark roofs scattered along a country road, small brown fields, forested hills around it with bare and budding trees, the Sea of Japan faintly visible in the distance, No snow anywhere, no frost, no ice, no winter. The camera looks forward and slightly down from about 120 metres above the settlement. No people visible, no readable signs, no real institution name, no crest, no emblem, no logo. Calm, peaceful, soft overcast morning light, muted natural tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. Generate 1 image.
```
→ **Google Flow動画プロンプト:**
```
One single continuous aerial drone shot: the camera glides slowly forward over the small quiet farming settlement near Setana in early spring, over the low houses and brown fields toward the forested hills. No cuts, no scene change, smooth steady movement. No people visible. 8 seconds. Photorealistic, shot on RED camera. Documentary style.
```
→ 編集者指示: 動画をナレーションの尺に合わせて使う。中央に「目撃情報ゼロ」を白字で表示し、「ゼロ」だけ赤字。

---

ナレーター: しかし、クマは一向に見つかりません。

【制作メモ】ASSET-034 [キャラアニメーション] 台本L58
シーン: 誰もいない春の山道で、クマが見つからず困り果てるハンター（CHAR-05）。
キャラプロンプト（1:1）:
```
(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese local hunter in his 60s with short grey hair and a grey stubble, an orange cap, a dark green field jacket under a blaze-orange safety vest, khaki trousers and brown boots, a small backpack, standing square to the viewer with his shoulder line parallel to the picture plane, his face clearly visible. He scratches the back of his head with one hand, eyebrows pulled together and slanted upward, eyes wide and darting, mouth bent into a worried frown, a bead of sweat on his temple, baffled and troubled, NOT calm, NOT smiling. No lettering, no badge, no logo. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw him with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```
背景プロンプト（16:9）:
```
An empty mountain trail winding into a quiet forest near Setana, southwestern Hokkaido, in mid-April early spring: bare and budding deciduous trees, dense bamboo grass along the trail, brown leaf litter, No snow anywhere, no frost, no ice, no winter. No animal visible, no footprints. Framed from adult eye height about four metres back, the middle of the frame left as clear open space. Quiet, empty, frustrating stillness, soft overcast light, muted natural tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 1 image.
```
→ハンターセリフ「まるで／見つからない、、」
→ 編集者指示: 背景・キャラとも新規。ハンターを中央に置き、頭をかく腕を小さく動かす。中央に「見つからない」を白字で表示し、「見つからない」だけ赤字。

---

ナレーター: 北海道の行政も、念のためせたな町周囲の5つの町にも、事故を知らせる緊急文書を送りました。

【制作メモ】ASSET-036 [キャラアニメーション] 台本L62
シーン: 役場の廊下を、緊急文書の束を抱えて急ぐ職員。キャラは既存の ASSET-036_char.png（書類を運ぶ職員）を使い、背景だけ廊下に作り直す。
→ キャラは既存の ASSET-036_char.png を再利用。
背景プロンプト（16:9）:
```
A plain corridor inside a small rural government office building in southwestern Hokkaido, in mid-April: a long linoleum floor, white walls, a row of closed office doors, a window at the far end with bare and budding trees outside, No snow anywhere, no frost, no ice, no winter. No readable text, no signs, no real institution name, no crest, no emblem, no logo. Framed from adult eye height about four metres back looking down the corridor, the middle of the frame left as clear open space. Urgent, tense mood, cool fluorescent light, NOT pure black, the corridor clearly readable, muted tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 1 image.
```
→ 編集者指示: 背景は新規、キャラは既存の ASSET-036_char.png。職員を右から左へ急ぐように移動させる（動画は作らない）。中央に「周囲5町へ緊急文書」を白字で表示し、「緊急文書」だけ赤字。

---

ナレーター: 北海道の行政職員と研究者ら合わせて3人が派遣され、町と警察から聞き取りを行いました。

【制作メモ】ASSET-039 [キャラアニメーション] 台本L66
シーン: せたな町の町なかで、派遣された3人（研究者CHAR-07と道の職員2人）が、町の職員（CHAR-06）と警察官から話を聞く。聞く側と聞かれる側の両方を描く。
キャラプロンプト（1:1）:
```
[Generic group] Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. Five full-body Japanese figures in two groups facing each other, all faces clearly visible. On the left, the three visitors facing right: 1) (CHAR-07 再利用) a female researcher in her 40s in a plain white lab coat over a navy top, dark brown hair tied back, holding a clipboard and writing; 2) a male prefectural official in his 50s in a grey suit, listening with a deeply worried frown and furrowed eyebrows; 3) a male prefectural official in his 30s in a navy suit, holding a folder, eyes wide and serious. On the right, the two being interviewed facing left: 4) (CHAR-06 再利用) a male town official in his 40s in a navy work jacket, explaining with one hand raised, eyebrows pulled together, mouth open, anxious; 5) a male police officer in his 40s in a plain dark navy uniform and cap with no lettering and no badge, speaking with a grave frown. No lettering, no badge, no logo, no emblem anywhere. Each figure has a very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw them with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```
背景プロンプト（16:9）:
```
A quiet main street in the small town of Setana, southwestern Hokkaido, in mid-April early spring: low two-storey shops and houses, a wide empty road, power poles, forested hills behind with bare and budding trees, No snow anywhere, no frost, no ice, no winter. No readable text, no signs, no real institution name, no crest, no emblem, no logo. Framed from adult eye height about six metres back, the middle of the frame left as clear open space. Serious, tense mood, soft overcast light, muted natural tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 1 image.
```
→職員セリフ「現場は／集落のすぐそばです」
→ 編集者指示: 背景・キャラとも新規。左の3人と右の2人を向かい合わせで中央に置き、話す職員の腕を小さく動かす（動画は作らない）。左上に「道から3人派遣」を白字で置き、「3人」だけ赤字。

---

ナレーター: ハンターもクマの捜索に入っていました。

【制作メモ】ASSET-043 [キャラアニメーション] 台本L74
シーン: 夜明け前の春の林道に、ヘッドランプを付けて捜索に入るハンター（CHAR-05）。雪は描かない。
キャラプロンプト（1:1）:
```
(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese local hunter in his 60s with short grey hair and a grey stubble, an orange cap with a small headlamp, a dark green field jacket under a blaze-orange safety vest, khaki trousers and brown boots, a small backpack, a rifle slung on his back pointing upward, walking toward the viewer at a slight three-quarter angle, facing the viewer, his face clearly visible. Eyebrows pulled down hard, eyes narrowed and alert, mouth pressed into a tight grim line, a bead of sweat on his temple, tense and determined, NOT calm, NOT smiling. No lettering, no badge, no logo. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw him with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```
背景プロンプト（16:9）:
```
A forest track at dawn near Setana, southwestern Hokkaido, in mid-April early spring: bare and budding deciduous trees, brown leaf litter, dry brown grass along the track, a faint blue pre-dawn light over the hills, No snow anywhere, no snow patches, no frost, no ice, no winter. Dim but NOT pure black, the track and trees clearly readable. Framed from adult eye height about four metres back, the middle of the frame left as clear open space. Tense, quiet, cold blue dawn light, muted tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Empty landscape only. Generate 1 image.
```
→ハンターセリフ「必ず／見つけ出す」
→ 編集者指示: 背景・キャラとも新規。ハンターを左から中央へ歩くように移動させる。左上に「ハンターも捜索」を白字で置き、「ハンター」だけ赤字。

---

ナレーター: 町は道路沿いの3カ所に注意看板を立て、新成地区の周辺には鉄製の箱わなを2つ設置。

【制作メモ】ASSET-045 [キャラアニメーション] 台本L78
シーン: 見つからないクマに困りながら、道路沿いの注意看板の横で箱わなを据えるハンター（CHAR-05＝043と同じ人）。
キャラプロンプト（1:1）:
```
(CHAR-05 再利用) Cute cartoon character design, thick black outlines, flat cel-shaded colors, large expressive eyes, children's animation style. A full-body Japanese local hunter in his 60s with short grey hair and a grey stubble, an orange cap, a dark green field jacket under a blaze-orange safety vest, khaki trousers and brown boots, standing square to the viewer with his shoulder line parallel to the picture plane, his face clearly visible. He rests one hand on top of a small steel box trap beside him and wipes his forehead with the other, eyebrows pulled together and slanted upward, eyes wide and uneasy, mouth bent into a worried frown, sweat on his temple, troubled and anxious, NOT calm, NOT smiling. No lettering, no badge, no logo. A very large head about one third of the total height, a short compact torso and short stubby arms and legs, roughly three heads tall. Do NOT draw him with realistic adult proportions — not four, five, six or seven heads tall. Full body. Transparent background, real alpha transparency. 1:1 aspect ratio. Generate 1 image.
```
背景プロンプト（16:9）:
```
A country roadside near the forest edge near Setana, southwestern Hokkaido, in mid-April early spring: a plain bear warning sign with only a bear pictogram and no words, bare and budding trees, dry brown grass, No snow anywhere, no frost, no ice, no winter. No readable text, no real institution name, no crest, no emblem, no logo. Framed from adult eye height about four metres back, the left half of the frame left as clear open space. Uneasy, quiet overcast light, muted tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 1 image.
```
→ 背景は既存の ASSET-045_still.png（道路脇のクマ注意看板・人物なし）をそのまま使う。新しく作るのはキャラだけ。
→ハンターセリフ「わなに／かかってくれ、、」
→ 編集者指示: 背景は既存の ASSET-045_still.png、キャラは新規の ASSET-045_char.png。ハンターを左に置く（動画は作らない）。中央に「看板3カ所・わな2つ」を白字で表示し、「わな2つ」だけ赤字。

---

ナレーター: クマの情報を集めるため、住民からの目撃通報を集めるよう、それぞれの町へ要請します。

【制作メモ】ASSET-050 [キャラアニメーション] 台本L88
シーン: 047から続く対策会議の会議室で、職員が各町へ電話で要請する。キャラは既存の ASSET-050_char.png（電話でメモを取る職員）を使い、背景だけ会議室に作り直す。
→ キャラは既存の ASSET-050_char.png を再利用。
背景プロンプト（16:9）:
```
A meeting room in a small rural town office in southwestern Hokkaido, in mid-April: long tables pushed together, empty folding chairs, a large blank map board on the wall, a desk telephone and scattered documents on the table, a window with bare and budding trees outside, No snow anywhere, no frost, no ice, no winter. No readable text, no real institution name, no crest, no emblem, no logo. Framed from adult eye height about four metres back, the middle of the frame left as clear open space. Tense, busy mood, cool daylight, muted tones. Photorealistic, shot on RED camera. Documentary style. 16:9 aspect ratio. No people, no figures, no humans visible. Generate 1 image.
```
→ 編集者指示: 背景は新規、キャラは既存の ASSET-050_char.png。職員を中央に置く。中央に「目撃通報を集める」を白字で表示し、「目撃通報」だけ赤字。
