# 2025年東成瀬村クマ襲撃事件 サムネイル設計

## タイトル
村役場から350メートルで4人が次々と…2025年10月 秋田・東成瀬村クマ襲撃事件の結末

## サムネ構成（2026-09-05 策定・主役を佐々木さんに変更）

### 共通要素
- **メイン画像（右1/3）:** 38歳の男性（CHAR-01 佐々木喜行さん相当・母親の悲鳴を聞いて駆けつけた）。濃紺フリース、口を大きく開けて笑いカメラ目線
- **背景:** 晩秋の里山の集落（木造家屋＋収穫後の畑、黄金〜茶）、すぐ後ろに暗い森の丘、空は重い曇天
- **フッター:** 黒帯に白文字「地形図・アニメーションで解説」
- **文字は2段＋フッター**（Channel_Master §7 の3層は旧仕様。SKILL.md 2026-02改訂＝中間廃止に従う）
- サムネに実名は載せない（本文も匿名運用）

### A/Bテスト（3案・人物画像は共通、テキストと左右のみ変える）

| 枠 | 上部セリフ | 下部オチ | 人物の位置 | 狙う感情 |
|---|---|---|---|---|
| A（本命） | 「ちょっと見てくるわ」 | 母を逃がして | 右1/3 | 共感（軽い一言 × 重い行為） |
| B | 「役場のすぐそこだから」 | 全員が"赤" | 右1/3 | 驚き（安全な場所 × 救命の色） |
| C | 「クマなんて来ないって」 | 顔だけを狙う | **左1/3（反転）** | 恐怖（襲い方の異常さ） |

- 変数はテキストのみ（人物画像は3枠同一）。Cだけ左右反転で反復回避（§7 Anti-Demonetization）
- 下部は**タイトルと重複させない**。タイトルが「350m／4人」なので、サムネは「母」「赤」「顔」で別の情報を出す
- 「全員が"赤"」＝消防のトリアージ。意味が分からないから開く（数字の"規模"ではなく"意外性"）

## Lovart画像プロンプト（人物のみ・テキストなし）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome and charismatic with clean-cut refined features. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones with sculpted hollows beneath, very high straight strong nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes and a warm confident gaze, thick well-defined dark eyebrows, well-shaped full lips, smooth clear handsome skin with a healthy light tan and mature masculine appeal, thick glossy perfectly styled short black hair with a natural side sweep gently blown by the wind. Tall lean broad-shouldered model build with elegant 8-head body proportions, straight confident posture. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket with the collar slightly open over a light gray shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

### 必須7要素チェック

| # | 要素 | 該当箇所 |
|---|---|---|
| 1 | 職業ベース容姿（2職業） | `fashion model` + `prime-time drama leading-man actor` |
| 2 | 顔骨格 | V字小顔・高頬骨・高鼻筋・二重アーモンド目・8頭身 |
| 3 | 肌（年代別） | `smooth clear handsome skin with a healthy light tan and mature masculine appeal` |
| 4 | カメラ目線 | `facing the camera, looking directly at the viewer` |
| 5 | 口大開け笑い | `mouth wide open laughing heartily showing perfect white teeth` |
| 6 | 自然な動き（1〜2要素） | 髪＋襟の風のみ（落ち葉・霧渦巻きは併用しない） |
| 7 | 暗い背景＋不穏な空 | 集落＋暗い森の丘＋`heavy and overcast with rolling grey clouds` |

- 背景のクマシルエットは**入れない**（デフォルト方針。指示があれば追加）
- 季節の冬化対策として `Late October, autumn` を文頭、`No snow, no ice, no winter scenery` を末尾に配置
- イケメン度は強調語でなく具体パーツで出す（頬骨の陰・太い眉・rim light を追加。三重強調・3職業重ねは不使用）
- 服装は CHAR-01（dark navy fleece jacket）準拠。小物なし＝手の破綻リスクなし


## 別パターン（人物画像の候補・2026-09-05追加）

> 上の「基本パターン」と合わせて3種から選ぶ。選んだ1枚を3枠共通で使う（A/Bの変数はテキストのみ）。
> パターン2・3は服装が CHAR-01（濃紺フリース）から離れる。本編キャラとの一致は必須ではない（立山・風不死岳も一致させていない）

### パターン2: ワイルド系（軽トラ・夕方の斜光）

```
Photorealistic cinematic close-up portrait shot, framed from chest up, body angled slightly to the side with the face turned straight to the camera. Late October, autumn, late afternoon. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with rugged refined features. Sharp strong defined V-shaped jawline tapering to a firm pointed chin, high prominent cheekbones with sculpted hollows beneath, very high straight strong nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes and an intense confident gaze, thick well-defined dark eyebrows, well-shaped full lips, neatly trimmed short dark stubble along the jaw, smooth handsome tan skin with mature masculine appeal, thick glossy black hair cut short on the sides and swept up on top, gently blown by the wind. Tall broad-shouldered muscular model build with elegant 8-head body proportions, straight confident posture. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the turned-up collar of his jacket. He is wearing a black canvas work jacket with the collar turned up over a plain white T-shirt, one hand resting on the side of a small white Japanese kei truck beside him. Behind him, a narrow farm road through a small mountain village in Akita in late autumn, harvested rice fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Low warm late-afternoon light raking across his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

### パターン3: 爽やか系（実家の庭先・柿の木・朝の光）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. Late October, autumn, early morning. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese drama heart-throb lead actor, strikingly handsome with clean-cut refined features and a fresh youthful energy. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes and a bright warm gaze, thick well-defined dark eyebrows, well-shaped full lips, porcelain-smooth clear skin without a single blemish, thick glossy perfectly styled black hair with a soft natural fringe gently blown by the wind. Tall lean model build with elegant 8-head body proportions, relaxed upright posture. Mouth wide open laughing joyfully showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the open collar of his shirt. He is wearing an olive-green lightweight shirt jacket with the sleeves rolled to the forearms over a plain white T-shirt. Behind him, the front yard of an old wooden farmhouse in a small mountain village in Akita in late autumn, a persimmon tree heavy with bright orange fruit and a few bare branches, harvested fields beyond, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Soft warm morning light on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```


### パターン1-B: 誠実・清潔／別の顔（センターパート・切れ長の目）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, gently blown by the wind. Tall lean model build with elegant 8-head body proportions, straight quiet posture. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

### パターン1-C: 誠実・清潔／別の顔（七三・細縁メガネ・カーディガン）

```
Photorealistic cinematic close-up portrait shot, framed from chest up. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with an intelligent, gentle, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid almond-shaped eyes with long thick eyelashes and a warm kind gaze behind thin silver-rimmed glasses, neat well-defined dark eyebrows, well-shaped full lips, smooth clear handsome skin with a healthy light tan, thick glossy black hair in a neat side part swept off the forehead, gently blown by the wind. Tall lean model build with elegant 8-head body proportions, straight composed posture. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his shirt. He is wearing a navy knit cardigan over a crisp white button-up shirt with the collar open. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```


### パターン1-B 動きあり（同じ顔で構図を変える・2026-09-05追加）

> 5枚とも正面バストアップで揃ってしまったため、顔ブロックは1-Bのまま固定し、体の向き・手・カメラ位置だけ変える。
> 動きは1枚につき1〜2要素（風＋ポーズ）。ジャンプ・走りは人物が浮く／ブレるので使わない。

#### 1-B-1: 肩越しの振り返り＋軽く手を挙げる

```
Photorealistic cinematic portrait shot, framed from the waist up, the camera slightly behind and to the side of him. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is caught mid-turn, body angled three-quarters away from the camera, looking back over his shoulder with one hand raised in a casual wave, feet planted on the ground. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, his face turned straight to the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-2: 農道を歩きながら手を振る（ローアングル）

```
Photorealistic cinematic portrait shot, framed from the waist up, low camera angle looking slightly up at him. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is walking toward the camera along a narrow farm road, caught sharp and frozen in a relaxed mid-stride, one hand raised waving to the viewer, the other hand in his jacket pocket. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, his face turned straight to the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-3: 軽トラの窓から肘を出して

```
Photorealistic cinematic portrait shot, framed from chest up, camera at window height just outside the vehicle. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is sitting in the driver's seat of a small white Japanese kei truck parked on a village road, the window fully rolled down, his left elbow resting on the open window frame and his upper body leaning slightly out toward the camera. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, his face turned straight to the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-4: 柿の木の枝に手を伸ばして（実家の庭先）

```
Photorealistic cinematic portrait shot, framed from the waist up, camera at eye level slightly off to the side. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is standing under a persimmon tree in the front yard of an old wooden farmhouse, one arm raised reaching up to a low branch heavy with bright orange fruit, the other hand holding a single persimmon, feet planted on the ground. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, his face turned straight to the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Dramatic warm lighting on his face like a fashion magazine cover, a crisp rim light outlining his hair and shoulders to separate him from the dark background, autumn earth tones glowing warmly, dark cold shadows behind. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

| 枝 | 動き | 構図 | 人物が入る側 |
|---|---|---|---|
| 1-B-1 | 振り返り＋手を挙げる | 斜め後ろから・腰上 | 右（反転で左も可） |
| 1-B-2 | 歩きながら手を振る | ローアングル・腰上 | 右 |
| 1-B-3 | 軽トラの窓から身を乗り出す | 窓の高さ・胸上 | 右（軽トラの車体が左に伸びるので文字は上下に） |
| 1-B-4 | 柿の枝に手を伸ばす | 横寄り・腰上 | 右 |

- 顔ブロックは1-Bと完全一致（同じ人に見える）。変わるのは体の向き・手・カメラ位置だけ
- 「顔は正面」を `his face turned straight to the camera` で維持。振り返り・車内でも目線ルールは崩さない
- 1-B-3は車体が画面に入るぶん、文字を上端・下端に置いても人物と重ならないことを確認する


### パターン1-B 自然なスナップ（ポーズなし・撮られた瞬間の感じ・2026-09-05追加）

> 「ポーズは入れない」。カメラを構えた人の前で自然に笑った瞬間を、手持ちの35mmで撮ったスナップ写真の質感にする。
> 変えるのは撮り方（レンズ・距離・傾き・光の柔らかさ・その場の状況）だけ。手は下ろすかポケット。雑誌の照明語は外し、自然光に置き換える。

#### 1-B-5: 手持ちスナップ（35mm・少し斜め・笑い出した瞬間）

```
Candid documentary-style photograph, shot handheld on a 35mm lens, framed from chest up, the frame slightly off-center and a touch tilted as if taken quickly. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, slightly tousled and gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He has just burst out laughing at something said off-camera, shoulders relaxed, arms hanging naturally at his sides, standing on a narrow village road. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Soft warm natural light on his face, dark cold shadows behind, a faint natural rim of light on his hair and shoulders separating him from the dark background. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-6: 会話の途中でカメラに気づいた瞬間

```
Candid documentary-style photograph, shot on a 50mm lens from a few steps away, framed from chest up, natural unposed framing. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, slightly tousled and gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is in the middle of a relaxed conversation and has just noticed the camera, turning his head toward it with a slight natural tilt and laughing, hands loosely in his jacket pockets, standing at the edge of a harvested field by a wooden house. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Soft warm natural light on his face, dark cold shadows behind, a faint natural rim of light on his hair and shoulders separating him from the dark background. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-7: 軒先での一息（望遠・遠くから抜いた感じ）

```
Candid documentary-style photograph, shot from a distance on an 85mm lens with natural compression, framed from chest up, unposed. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, slightly tousled and gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is standing under the eaves of an old wooden farmhouse taking a short break, one hand holding a small cup of tea near his chest, caught in a natural unguarded laugh toward the camera. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Soft warm natural light on his face, dark cold shadows behind, a faint natural rim of light on his hair and shoulders separating him from the dark background. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

#### 1-B-8: 歩いている途中を横から（ポーズなし・歩きの延長）

```
Candid documentary-style photograph, shot handheld on a 35mm lens while walking alongside him, framed from chest up, natural unposed framing. Late October, autumn. A Japanese male fashion model in his late 30s (38 years old) with the looks of a Japanese prime-time drama leading-man actor, strikingly handsome with a calm, sincere, clean-cut presence. Small V-shaped face, sharp slim defined jawline tapering to a pointed chin, high prominent cheekbones, very high straight nose bridge, deep-set double-eyelid long narrow almond-shaped eyes with long thick eyelashes and a gentle steady gaze, straight well-defined dark eyebrows, well-shaped full lips, smooth clear fair skin without a single blemish, thick glossy black hair parted in the center and falling softly to the brow, slightly tousled and gently blown by the wind. Tall lean model build with elegant 8-head body proportions. He is simply walking along a farm road at an easy pace, arms swinging naturally, and glances toward the camera beside him with a natural laugh. Mouth wide open laughing heartily showing perfect white teeth, ecstatic exhilarated expression, facing the camera, looking directly at the viewer, completely unaware of danger. Wind gently blowing his hair and the collar of his fleece jacket. He is wearing a dark navy fleece jacket zipped halfway over a crisp white crew-neck shirt. Behind him, a small mountain village in Akita in late autumn, wooden houses and harvested terraced fields in golden and brown tones, dark forested hills rising close behind, the sky above heavy and overcast with rolling grey clouds hinting at approaching danger. Soft warm natural light on his face, dark cold shadows behind, a faint natural rim of light on his hair and shoulders separating him from the dark background. Shallow depth of field, background slightly blurred. No snow, no ice, no winter scenery. No text, no words, no letters. 16:9 aspect ratio. Generate 5 images.
```

| 枝 | 状況 | レンズ・距離 | 手 |
|---|---|---|---|
| 1-B-5 | 笑い出した瞬間 | 35mm手持ち・少し斜め | 下ろす |
| 1-B-6 | 会話中にカメラに気づく | 50mm・数歩の距離 | ポケット |
| 1-B-7 | 軒先で一息 | 85mm・遠くから | 湯のみを胸元に |
| 1-B-8 | 歩きながら横から | 35mm・並走 | 自然に振る |

- 顔ブロックは1-Bと同じ（髪だけ `slightly tousled` を足して撮られた感を出す）
- 照明は `Dramatic warm lighting ... like a fashion magazine cover` を外し、`Soft warm natural light on his face` に置換。暗い背景と輪郭光は維持
- 1-B-7の湯のみで手が崩れたら `one hand holding a small cup of tea near his chest` を削る

| 枝 | 顔の違い | 髪 | 服 |
|---|---|---|---|
| 1（基本） | 彫りの深い・頬骨の陰 | 横流しショート | 濃紺フリース＋薄灰シャツ |
| 1-B | 切れ長の目・色白・静か | センターパート | 濃紺フリース半開き＋白クルーネック |
| 1-C | 知的・優しい・メガネ | 七三 | 紺カーディガン＋白シャツ |

- 1-Cのメガネは笑いで目が隠れやすい。目が見えない生成が続いたら `behind thin silver-rimmed glasses` を削る

| パターン | 印象 | 服装 | 背景 | 光 |
|---|---|---|---|---|
| 1（基本） | 誠実・清潔 | 濃紺フリース（CHAR-01準拠） | 集落＋畑 | 正面の暖色 |
| 2 | ワイルド・頼れる | 黒ワークジャケット襟立て＋白T・無精ひげ | 農道＋軽トラ | 夕方の斜光 |
| 3 | 爽やか・若々しい | オリーブのシャツジャケット袖まくり＋白T | 実家の庭先＋柿の木 | 朝の柔らかい光 |

- 3パターンとも必須7要素・冬化対策・背景クマなし・2職業まで・三重強調なしを満たす
- パターン2の軽トラは手を添えるだけ（乗り込む・運転席は姿勢が崩れるので不使用）
- パターン3の柿は事件の誘因（人里の果樹）の記号。実が目立ちすぎて人物を食う場合は `a persimmon tree` の一文を削る

## Photopea配置ガイド（1280×720px）

### A案・B案（人物右）
```
┌──────────────────────────────────┐
│「ちょっと見てくるわ」              │ ← 上端
│                                   │
│                            [顔]   │
│                            [顔]   │
│  母を逃がして                     │ ← 下端
│■■ 地形図・アニメーションで解説 ■■│ ← 黒帯
└──────────────────────────────────┘
```

### C案（人物左・反復回避枠）
```
┌──────────────────────────────────┐
│            「クマなんて来ないって」│ ← 上端
│                                   │
│   [顔]                            │
│   [顔]                            │
│                      顔だけを狙う │ ← 下端
│■■ 地形図・アニメーションで解説 ■■│ ← 黒帯
└──────────────────────────────────┘
```

## フォント・テキスト設定

### 上部（慢心セリフ）
- Font: LightNovelPOPv2
- Color: #FFFFFF
- Stroke: #000000, 5px, Outside
- カギカッコ「」あり／1行・改行禁止

### 下部（衝撃オチ）
- Font: Source Han Sans JP Heavy
- Color: 黄→橙グラデ #FFD700 → #FFA500
- Stroke: #000000, 5px, Outside
- Shadow: #000000, Opacity 75%, Angle 135°, Distance 5px, Size 8px
- 右上がり3〜5度の傾き／カギカッコなし／1行・改行禁止
- B案の `"赤"` はダブルクォート込みで1行。`赤` の一字だけ特大にする

### フッター
- Font: Source Han Sans JP Medium
- 黒帯に白文字「地形図・アニメーションで解説」

## NGワードチェック
✅ 問題なし（死／死亡／遺体／殺す を使用していない。「母を逃がして」は行為のみで結末は語らない）

## 設計意図
- 画像＝村の日常の笑顔（安全） / テキスト＝母を逃がした行為と救命の色（死の結末）。情報を重複させずギャップを最大化
- 主役を「駆けつけた息子」にすることで、上部の軽い一言（ちょっと見てくるわ）がそのまま最後の言葉に聞こえる構造
- 競合Top3（ABS・カンテレ・日テレ）は全て報道フォーマットで**人物の表情が主役になっていない**。笑顔の当事者を主役に据えるだけで棚の中で浮く

## AI開示ラベル
- YouTube Studio: 「改変または合成コンテンツ」→「はい」を選択
