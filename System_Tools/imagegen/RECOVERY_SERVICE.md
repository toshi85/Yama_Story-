# 戸沢村の画像回収サービス

`com.yama.imagegen.recovery` が `recovery_service.py` を管理する。手動で別の回収プロセスを重ねて起動しない。

- ワーカーの回収記録が4分更新されなければ終了させ、30〜300秒の間隔で再開する。
- 通信タイムアウト時は専用タブを作り直す。正常に処理が進んだ場合は連続失敗回数をリセットする。
- サービス自体の異常終了は launchd の `KeepAlive: SuccessfulExit=false` で再起動する。
- サービス用ロックと生成・回収共通ロックで二重起動を防ぐ。
- 利用制限やログイン待ちは15分待つ。ログインが必要なときはMacへ通知する。
- 回収終了、異常からの復旧待ちをMacへ通知する。通知が届かなくてもログと進捗画面で確認できる。
- 回収終了は全素材完成と同義ではない。未回収画像や目視確認が残る場合を区別して通知する。

進捗画面：<http://127.0.0.1:8794>（このMac内のみ）。`com.yama.imagegen.progress` が管理する。
回収記録は作品の `.imagegen/recovery.json`、稼働状態は `.imagegen/service.json`、ログは `/tmp/yama-image-recovery.log`。
既存の生成サービス `com.yama.imagegen` と `com.yama.imagegen.kick` は回収中は解除しておく。
画像の新規発注や動画APIへの切り替えは、このサービスでは行わない。

設定の正本は `~/Library/LaunchAgents/com.yama.imagegen.recovery.plist`。
`ProgramArguments` は仮想環境のPython、`recovery_service.py`、作品パス、`--history`、回収用履歴コピー。
`WorkingDirectory` は `/tmp`、`RunAtLoad` は true、`ThrottleInterval` は30。
Macのスリープ・電源断中は動かない。次回ログイン時に再開する。

検証済み：無応答ワーカーの終了、後続処理の実行、サービス終了後のlaunchd再起動、保存済み位置からの回収増加、共通ロックによる競合防止、画像・プロンプトの照合。

## 待ち時間の削減

- 完全一致する要求の全対応枠が回収済みなら、画像ロードを待たず次の履歴へ進む。
- タブ作り直し時は空ページを使い、ChatGPTトップページの余分な読み込みを避ける。
- 初期ポーリングを0.5秒、件間の待ちを0.25秒に短縮。未完了ページの待機上限36秒は維持する。
- `--retry-unmatched` は初回に未照合だった履歴だけを一度再確認する。途中再起動で最初からやり直さない。
- `.imagegen/recovery_timings.jsonl` にページ待ち・ダウンロード・合計時間を記録する。会話URLや署名付き画像URLは計測ログへ出さない。
