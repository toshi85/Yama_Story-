# 画像生成の自動化（imagegen）

Asset_Prompts.md からキューを作り、ChatGPTのページ上で連続生成して、作品の `images/` へ回収する。

```
python3 extract_prompts.py <Asset_Prompts.md> <作品>/image_queue.json
python3 collect.py <作品フォルダ> --watch      # ~/Downloads → images/ を30秒おきに回収
```

`driver.js` は chatgpt.com のページに入れて動かす。開始 `__yamaRun()` ／ 状況 `__yamaGen.status()` ／ 停止 `__yamaGen.stop = true`。

## 受講生への配布（macOS／Windows）

受講生にはこの `imagegen` フォルダ一式を配布し、`start_imagegen.command` を1回実行してもらう。

```text
macOS:  start_imagegen.command をダブルクリック
Windows: start_imagegen_windows.bat をダブルクリック
→ 作品フォルダを選ぶ → 専用Chromeで初回ログイン
```

インストーラーは実行した場所から絶対パスを組み立てるため、受講生のユーザー名や配置場所に依存しない。macOSでは `~/Library/LaunchAgents/com.yama.imagegen.plist`、Windowsではタスクスケジューラの `Yama Imagegen` を生成し、ログイン後の再開、異常終了時の再起動、ログ保存、二重起動防止まで設定する。

専用Chromeの設定では `automatic_downloads=1` と `prompt_for_download=false` を自動設定し、CDPでも保存を許可する。受講生がChromeの「複数ファイルを常に許可」やCodexの「常に許可」を選ぶ必要はない。

初回のChatGPTログイン、Google Chrome、画像生成を使えるChatGPTアカウントは必要。アカウント認証やプランの利用上限は配布物では省略・変更できない。

詳しい受講生向け手順は `SETUP_FOR_STUDENTS.md`。

## 開発者向けの動かし方は2通りある

**A. `run.py`（推奨・受講生に配るのはこちら）**
```
python3 run.py <作品フォルダ>
```
自動化専用のChromeを開き、ログインを待ち、キューを作り、ループを入れ、
上限を待ち、回収し、全部そろうまで見張る。**AIエージェントの常駐も拡張機能も要らない。**
手順書は `SETUP_FOR_STUDENTS.md`。

**B. ブラウザ拡張から手で流し込む**
開発中に中を覗きたいときだけ。`driver.js` をページに入れて `__yamaRun()`。

## Chromeへの繋ぎ方（実測でここに落ち着いた）

`chrome_bridge.py` が、Chrome自身のデバッグ用の口（CDP）を通してJSを流し込む。

🚨**普段使っているプロファイルではデバッグポートが開かない**（Chrome 136以降の
乗っ取り対策。実測：151で `DevToolsActivePort` が作られない）。
だから `--user-data-dir` で**自動化専用のプロファイル**を作る。
新品なのでChatGPTに未ログイン＝**初回だけ人がサインインする**。ここは設計で消せない。

`chrome_bridge.py` は通常のChromeを終了せず、Chrome本体を別プロセスとして起動する。専用プロファイルはmacOSでは `~/.yama_imagegen_chrome`、Windowsでは `%LOCALAPPDATA%\YamaImagegen\Chrome` に置く。

❌ **osascript（Apple Events）は使わない。** ログイン済みプロファイルのまま使えて
魅力的だが、`browser.allow_javascript_apple_events` の設定が要るうえ、
**エージェントのサンドボックスがApple Events用のXPCを塞ぐ**（実測でXPCエラー）。

⚠️ **`codex sandbox` の結果を信じない。** あれは設定を読まない素のサンドボックスで、
実際の `codex exec` とは通る/通らないが逆に出る（localhostが前者では塞がれ後者では通った）。
検証は必ず本番の経路でやること。

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
