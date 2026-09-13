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

## 上限について（2026-08-29 実測 / 2026-09-04 追記）

ChatGPT Plus は **24時間で約90枚**。枠の時計は「その日の1枚目」から回り始める。
解除までの残り時間は、画像を頼んだときの**返答の中にしか出ない**（設定画面には無い）。

### 🚨 断り文句は何通りもある。全部拾う

2026-09-04、下の文面を取りこぼして**20分おきに17時間投げ直し続け、77/311枚で一晩止まっていた**。
`limitLeftMin()` が読める形（node で総当たり済み）:

| 文面 | 読み取り |
|:---|:---|
| 明日の 14:33にもう一度お試しください | 翌日14:33 |
| 今日の 21:49 に／21:49までお待ちください | 当日21:49 |
| 上限は 17 時間後にリセットされ | +17時間 |
| resets in 3 hours and 20 minutes | +200分 |
| Try again tomorrow at 2:33 PM | 翌日14:33 |

**明示の時刻を、相対表現より先に見る**（「17時間後」は丸めた値、「14:33」は正確）。
どれも読めなければ `null` を返し、driver.js は**誤判定を疑って2回目まで待つ**。

### 解除時刻に合わせて自動で再開する

1. driver.js が解除予定を読み、`__yamaGen.limitUntil` に置く
2. run.py がそれを `.imagegen/limit_until.json` へ書き出し、ログに「解除は 09/05 14:33 ごろ」と出す
3. `kick.py`（launchd `com.yama.imagegen.kick` が**10分おき**に呼ぶ）がその時刻を見て、
   **過ぎるまで触らない／過ぎたら入れ直す**

⚠️ 以前は決め打ちの6時刻（14:35/15:35/…）で起こしていたが、**解除時刻は毎日ずれる**ので外れる。
判断だけ確かめたいときは `python3 kick.py <作品フォルダ> --dry-run`（常駐は触らない）。

🚨 **解除がまだ遠いうちは1時間おきにしか投げ直さない。** 20分おきに17時間投げ続けると
「画像生成上限通知」の断りチャットが50本以上溜まり、`document.body` 判定だと誤診の元になる。

🚨 **driver.js を直したら、ページを読み込み直してから入れ直す。**
古いコピーがページに残ったまま動き続け、直したはずのエラーが出続ける（実測）。

## 復旧のしかた

進捗は `images/` のファイルがすべて。キューは「全体 − 保存済み」で作り直せる。

```python
q = json.load(open('image_queue.json'))
have = {p.stem for p in pathlib.Path('images').glob('*.png')}
todo = [{'id': x['id'], 'prompt': x['prompt']} for x in q if x['id'] not in have]
```

ページへの流し込みは file_upload（`<input type=file>` を作って渡す）。CSPのため
localhost への fetch もクリップボードもページ内 eval も通らない。

## 修正カットだけ作り直す（最短手順）

Pillow が利用できる Python 環境で実行する。この作業環境ではルートの
`.venv-edit/bin/activate` を有効にしてから、以下の `python3` を使う。

1. `Asset_Prompts_Full.md` のプロンプトを直してコミットする。
2. 修正前のコミットと比較して、変更・追加された画像だけを生成する。
   `python3 Yama_Story/System_Tools/imagegen/regen.py <作品> --since <直す前のコミット> --run`
3. 終わったら `python3 Yama_Story/System_Tools/imagegen/regen.py <作品> --verify`。
   `.imagegen/regen_<YYYYMMDD>/sheet.jpg` をClaudeが目視確認する。
4. 目視確認後に `python3 Yama_Story/System_Tools/imagegen/regen.py <作品> --export`。
   表示されたデスクトップの `<作品の短い名前>_差し替え画像_<YYYYMMDD>/` を本人がDriveへアップする。
   `--apply [--drive-dir <同期フォルダ>]` は「画像/」を差し替えたいときだけ使う。

作業フォルダには対象だけの `image_queue.json`、`run.log`、`run.pid` が残る。
`--run` は既存の専用Chrome・`run.py` をnohupで背景起動してすぐ戻る。
未ログインなら専用Chromeに表示される案内に従って本人がログインし、同じコマンドで再開する。
生成の完了は `run.log` の「完成しました」と対象PNGがすべてそろったことを確認する。
検査結果は `verify.json`。未生成・透過不足・描き込まれた市松模様があれば適用できない。

`--assets CHAR-15,ASSET-020_char,...` を付けると差分検出を指定IDで上書きする。
動画プロンプト、フェンスのない再利用・文字だけのカットは対象外。
CHAR基準画像を先に、その後はASSET番号順に生成する。

納品名は固定で、`CHAR-XX` は `画像/キャライラスト/CHAR-XX.png`、
`ASSET-NNN_char` と `_still` は `画像/ASSET-NNN.png`、
`_bg` は `画像/ASSET-NNN-1.png`、`_overlay` は `画像/ASSET-NNN_overlay.png`。
shots.jsonとの差異は `mapping_notes.json` に参考情報として残す。shots.jsonは変更しない。
標準名の既存ファイルは `画像/_旧_<YYYYMMDD>/` の同じ相対パスへ退避し、なければ新規に置く。
派生ファイル（`_実写`、`_キャラ`、`_raw`、`_v2` 等）は変更しない。
`--drive-dir` は「画像/」に相当する同期フォルダを指定し、その直下にも同じ相対パスでコピーする。
同日の退避先が既にある場合は停止し、前の原本を上書きしない。

`--since`・`--assets` を省いた検査・適用は、最新日付の既存キューを使うため、
生成が日付をまたいでも同じコマンドで続けられる。
同日に別の対象・変更版で既存キューを上書きする操作も停止する。

## 並べて同時に作る

```sh
python3 run.py <作業フォルダ> --parallel 2
python3 run.py <作業フォルダ> --parallel 3
```

専用プロファイルのChromeに、会話を**それぞれ別のウィンドウ**で開く。
同じウィンドウの裏タブではタイマーが凍るため、タブへまとめない。
`run.py` が未保存のIDを1件ずつ割り振り、保存とreceiptsの確認が済んだ
ウィンドウへ次を渡す。失敗した項目は中央キューへ戻し、1回再投入する。
同じ項目が再び失敗したら停止する。停止ボタンによる完成判定、保存名、
`collect.py` の回収、receiptsの照合方法は従来と同じ。

画像生成の上限は**アカウント全体で共有**する。どれかで上限が出たら
全ウィンドウへの投入とページ内の再試行を止め、解除予定を
`.imagegen/limit_until.json` へ保存して終了コード75で終了する。
既存の `kick.py` はこの時刻を参照する。時刻表示が読めない場合は
従来の20分間隔を使う。実測は上限検出時に打ち切り、勝手に再開しない。

割当て・失敗数・再投入数・画面の返答文は
`.imagegen/parallel_state.json` に残る。中断後は記録された同じウィンドウで
結果を引き継ぐ。処理中のウィンドウが消えた場合は重複再送せず停止する。
`regen.py` の作業フォルダを引数に取る呼出し方も引き続き使える。

**既定値は2。** 引数を省略した `python3 run.py <作業フォルダ>` も
2つの別ウィンドウで生成する。従来の1会話で動かす場合は `--parallel 1` を指定する。

2026-09-13の実測（出力は `.parallel_bench/` 内のみ）:

| N | 枚数 | 全件保存まで | 1枚あたり秒 | 失敗／再投入 | 上限表示 |
|---|---:|---:|---:|---|---|
| 1（既存参考値） | — | — | 約105 | 未記録 | 未記録 |
| 2（修正後） | 2 | 89.5秒 | 44.8 | 0／0 | なし |

N=2は失敗0件で参考値105秒/枚より速かったため、既定値2を採用した。
N=3は未計測で、追加の実測は行わない。

**判定C（保存先の不一致）:** 初回は画像・receiptが `~/Downloads` に保存されて実測側で回収できなかったため、並列時のダウンロード設定用CDP接続を全件回収まで維持するよう修正した。

修正後の実測記録は `.parallel_bench/diagnosis_n2/summary.json`、
各ウィンドウの開始直後・60秒後・120秒後の画面6枚は同フォルダの `screenshots/`。
生成画像はコミットしない。

ブラウザ無しの検査（Yama_Storyリポジトリのルートから）:

```sh
python3 -B -m unittest discover -s System_Tools/imagegen -p test_parallel.py
```
