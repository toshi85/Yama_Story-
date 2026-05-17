# Generic Person Prompts — 名無し人物プロンプトテンプレ集

> Yama_Story Master.md の Phase 2 アセット割り振りで、CHAR-XX を持たない**名無し人物**（家族・警察官・住民・隊員等）のプロンプトに使用する標準テンプレ。
> **目的**: Lovart / Google Flow がデフォルトで欧米人を生成する問題を防ぎ、全人物を日本人として確実に出力させる。
> **強制**: `.claude/hooks/validate-asset-prompts.sh` チェック7が Edit/Write 後に自動検査。違反は exit 2。

---

## 1. 使用ルール

| 状況 | 使い方 |
|:--|:--|
| 名前のある主要人物 | CHAR-XX を Asset_Prompts.md に定義 → 制作メモで `[CHAR-XX reference]` 参照 |
| 名前のない人物（Generic group） | 本ファイルのテンプレを Master.md の 制作メモにコピペ |
| 群衆・複数名・通行人 | 本ファイルの「群衆系」テンプレを使用 |

**禁止**: 「青年が…」「警察官が…」だけで Japanese を省略すること。

---

## 2. 個人テンプレ（単独人物）

### 2-1. 一般登山者・ハイカー
```
A Japanese hiker in mid-to-late 30s, wearing outdoor hiking gear (jacket, technical pants, hiking boots), carrying a daypack. Realistic documentary style.
```

### 2-2. 高齢の登山者
```
An elderly Japanese hiker, 60s-70s, weathered face with kind expression, wearing traditional mountain wear with a daypack. Realistic documentary style.
```

### 2-3. 高齢男性（被害者・住民役など）
```
An elderly Japanese man in his 70s-80s, weathered face, wearing simple farming or casual clothes. Realistic documentary style.
```

### 2-4. 高齢女性（被害者・住民役など）
```
An elderly Japanese woman in her 70s-80s, gray hair, weathered face, wearing simple casual clothes or work apron. Realistic documentary style.
```

### 2-5. 若い男性（友人・大学生役など）
```
A young Japanese man in his early 20s, university student, casual modern clothes, short black hair. Realistic documentary style.
```

### 2-6. 若い女性（友人役など）
```
A young Japanese woman in her early 20s, casual modern clothes, long black hair. Realistic documentary style.
```

### 2-7. 中年男性（家族・関係者役など）
```
A Japanese man in his 40s-50s, casual or business casual clothes, short black hair with slight graying. Realistic documentary style.
```

### 2-8. 中年女性（家族・関係者役など）
```
A Japanese woman in her 40s-50s, casual clothes, shoulder-length black hair. Realistic documentary style.
```

---

## 3. 職業別テンプレ（単独）

### 3-1. 警察官（制服）
```
A Japanese police officer in dark blue uniform with peaked cap, badge, and equipment belt. Standing posture, professional expression. Realistic documentary style.
```

### 3-2. 警察官（私服・捜査員）
```
A Japanese plain-clothes detective in dark suit, short black hair, serious expression. Realistic documentary style.
```

### 3-3. 消防士（出動服）
```
A Japanese firefighter in orange-red rescue uniform with helmet and equipment, sturdy build. Realistic documentary style.
```

### 3-4. 消防士（山岳救助・出動前）
```
A Japanese firefighter in mountain rescue gear — softshell jacket, cargo pants, hiking boots, carrying a daypack and rope. Determined expression. Realistic documentary style.
```

### 3-5. 山岳救助隊員
```
A Japanese mountain rescue worker in technical outdoor gear, helmet, harness, carrying ropes and rescue equipment. Realistic documentary style.
```

### 3-6. 自衛隊員
```
A Japanese Self-Defense Force member in olive-green field uniform, cap, rugged outdoor gear. Realistic documentary style.
```

### 3-7. ハンター（猟友会）
```
A Japanese hunter in olive-brown hunting jacket, cap, carrying a hunting rifle slung over shoulder. Weathered face, alert expression. Realistic documentary style.
```

### 3-8. 役所職員・行政担当
```
A Japanese local government official in business casual attire (blazer, tie), holding documents or pointing at a map. Realistic documentary style.
```

### 3-9. 報道記者
```
A Japanese news reporter holding a microphone, wearing business casual jacket, professional posture. Realistic documentary style.
```

### 3-10. 医師・救急隊員
```
A Japanese paramedic in orange emergency uniform with medical equipment, urgent professional expression. Realistic documentary style.
```

---

## 4. 群衆系テンプレ（複数人）

### 4-1. 家族（深刻な状況・通報など）
```
A Japanese family group (2-3 people, mixed ages), worried expressions, casual modern clothes, in an indoor or street setting. Realistic documentary style.
```

### 4-2. 警察官たち（捜索本部・打ち合わせ）
```
A group of Japanese police officers in dark blue uniforms gathered around a table or map, serious discussion postures. Realistic documentary style.
```

### 4-3. 消防士たち（出動準備・作戦会議）
```
A group of Japanese firefighters in mountain rescue gear, gathered for briefing, holding maps or radios, determined expressions. Realistic documentary style.
```

### 4-4. 捜索隊（複数人・登山道）
```
A group of Japanese search-and-rescue team members in outdoor gear walking along a mountain trail, carrying rescue equipment. Realistic documentary style.
```

### 4-5. 集落住民（取材場面）
```
Local Japanese village residents (mid-aged to elderly), wearing casual rural clothes, gathered for interview or conversation outdoors. Realistic documentary style.
```

### 4-6. 報道陣（取材現場）
```
A group of Japanese reporters with microphones and cameras, professional attire, attending a press conference or incident scene. Realistic documentary style.
```

### 4-7. 通行人・一般市民
```
Generic Japanese pedestrians in casual modern clothes, mixed ages and genders, walking in an urban or village setting. Realistic documentary style.
```

---

## 5. 視点系テンプレ（主観・後ろ姿等）

### 5-1. 登山者の後ろ姿（誰でも可）
```
Back view of a Japanese hiker walking along a mountain trail, wearing outdoor gear with a daypack. Cinematic documentary framing.
```

### 5-2. 倒れる登山者（被害シーン）
```
A Japanese hiker in outdoor gear falling backward onto the ground, slow-motion impact, shock expression. Realistic documentary style.
```

### 5-3. 主観視点（手・足など部分）
```
First-person POV of Japanese hands gripping a hiking pole / radio / equipment, with Japanese skin tone. Realistic documentary style.
```

---

## 6. 使用例（Master.md内）

### Before（NG）
```markdown
ナレーター: 夜の警察署に家族が駆け込みました。

【制作メモ】
- 【AI動画】夜の警察署、受付に駆け込む家族（5秒）
```

### After（OK）
```markdown
ナレーター: 夜の警察署に家族が駆け込みました。

【制作メモ】
- 【AI動画】夜の警察署、受付に駆け込む Japanese family、worried expressions（5秒）
```

または、Asset_Prompts.md側にフルプロンプトを書く場合:
```
A Japanese family group (2-3 people, mixed ages), worried expressions, running into a Japanese police station reception desk at night, fluorescent lighting. Realistic documentary style. 5 seconds.
```

---

## 7. 注意事項

- **動物（ヒグマ・鹿等）・風景・物のみのプロンプトには適用不要**
- **CHAR-XX参照画像がある人物には適用不要**（基準画像で Japanese 確定済み）
- **テンプレは出発点**: シーン固有の動作・服装・表情はテンプレに追記する
- **新しいパターンが出てきたら本ファイルに追加**して、次の台本以降で再利用する
