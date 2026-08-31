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
