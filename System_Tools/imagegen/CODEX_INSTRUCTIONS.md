# Codexへの指示書 — 画像生成

受講生は原則としてCodexへ指示する必要はありません。macOSでは `start_imagegen.command`、Windowsでは `start_imagegen_windows.bat` をダブルクリックし、作品フォルダを選ぶだけです。

Codexから開始する場合は、次の一文で十分です。

```
System_Tools/imagegen/install_for_student.py を、画像を作る作品フォルダを指定して1回実行してください。
```

インストーラーが、キュー作成、Chromeの自動ダウンロード許可、自動起動登録、ログ保存、二重起動防止をまとめて設定します。受講生のホームディレクトリや作品名を指示文へ直書きしないでください。

状態確認では以下を見ます。

- macOSのジョブ: `launchctl print gui/$(id -u)/com.yama.imagegen`
- Windowsのジョブ: `schtasks /Query /TN "Yama Imagegen" /V /FO LIST`
- ログ: `<作品フォルダ>/.imagegen/imagegen.log`
- 進捗: `<作品フォルダ>/images/*.png` の枚数

生成上限待ちは正常動作です。停止、別方式への切り替え、二重起動は行いません。

## 本人の Yama 素材を作るとき（2026-09-25 追加・受講生には適用されません）

生成スクリプト（imagegen・System_Tools/edit/fal_*.py）の中で `System_Tools/generation_gate.py` が必ず走ります。止められたら、回避せず次の順で進めます。

1. `python System_Tools/check_prompts_all.py <プロンプト.md>` を失敗0・警告0で通す（合格票が出る）
2. キューはその .md から作り、**一字一句変えない**（1文でも足す・削ると全文一致せず止まる）
3. 本人の承認前は **種類ごとに3件まで**。見本3件を作ったら本人に見せ、本人が自分のターミナルで
   `python System_Tools/generation_gate.py approve <プロンプト.md> --kind image` を打つのを待つ（AI は打てない）
4. 発注の中身は `<作品>/発注記録/` に自動で残る。作業の締めに git へ入れる
- Codex 内蔵の画像生成は設定で切ってある。使うのは `codex exec --enable image_generation` に合格票のキュー（image_queue*.json）を渡すときだけ
- 合格票・見本承認・見本枠のファイルを書き換える、生成APIを直接叩くコードを書く、はフックで止まる
