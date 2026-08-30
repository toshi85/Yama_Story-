# 画像生成の自動化（imagegen）

Asset_Prompts.md からキューを作り、ChatGPTのページ上で連続生成して、作品の `images/` へ回収する。

```
python3 extract_prompts.py <Asset_Prompts.md> <作品>/image_queue.json
python3 collect.py <作品フォルダ> --watch      # ~/Downloads → images/ を30秒おきに回収
```

`driver.js` は chatgpt.com のページに入れて動かす。開始 `__yamaRun()` ／ 状況 `__yamaGen.status()` ／ 停止 `__yamaGen.stop = true`。

## 動かす前に必ず読む（実測でつまずいた順）

**1. Chromeは起動オプション付きで開く。** これが無いと、ウィンドウが他の窓に隠れた時点で
タブのタイマーが**凍結**する。間引きではなく完全停止で、触ると数秒だけ動いてまた止まるため
「動いているのに進まない」という一番気づきにくい壊れ方をする。

```
open -a "Google Chrome" --args --disable-backgrounding-occluded-windows \
  --disable-background-timer-throttling --disable-renderer-backgrounding
```

Chromeを普通に再起動すると**黙って元に戻る**。長時間回す前に、5分放置して枚数が増えるかを見ること。

**2. 完成の判定は「停止ボタンが消えたか」だけ。** 生成中も画像要素はページに出る（途中経過の
プレビュー）。これを掴むと絵柄の崩れた半端な絵が保存される。

**3. 画像の選別に `naturalWidth` を使わない。** 裏のタブではデコードされず 0 のままになる。
落とした blob の大きさで判定する。

**4. 上限の判定は `main`（会話部分）だけを見る。** `document.body` だと、上限のたびに履歴へ
溜まる「Image Generation Limit」という**チャット名**に反応し、解除後も永久に上限中と誤診する。

## 上限について（2026-08-29 実測）

ChatGPT Plus は **24時間で約90枚**。枠の時計は「その日の1枚目」から回り始める。
解除までの残り時間は、画像を頼んだときの**返答の中にしか出ない**（設定画面には無い）。
driver.js は残り時間に応じて2〜20分間隔で投げ直し、空いた瞬間に再開する。

## 復旧のしかた

進捗は `images/` のファイルがすべて。キューは「全体 − 保存済み」で作り直せる。

```python
q = json.load(open('image_queue.json'))
have = {p.stem for p in pathlib.Path('images').glob('*.png')}
todo = [{'id': x['id'], 'prompt': x['prompt']} for x in q if x['id'] not in have]
```

ページへの流し込みは file_upload（`<input type=file>` を作って渡す）。CSPのため
localhost への fetch もクリップボードもページ内 eval も通らない。
