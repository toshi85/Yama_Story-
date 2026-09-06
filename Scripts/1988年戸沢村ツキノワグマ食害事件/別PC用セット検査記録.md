# 別PC用セットの検査記録

2026年9月7日、GitHubへの画像・編集セットの保存を確認。

- 編集用ZIPは素材用約1.2GBと確認用約417MB。GitHub側のサイズとSHA-256が保存記録に一致。
- 両ZIPを別フォルダへ展開し、起動前に2,368ファイルのSHA-256を照合。全298カットの参照素材に欠落なし。
- 元の制作フォルダと異なる場所から専用編集サーバーを起動し、298カットのシート表示と動画のRange配信を確認。
- Macでの展開・起動を検査。Windows用の起動ファイルも同梱したが、Windows実機での実行は未検査。
- 転送後、検査に使った一時ZIPを整理。元素材と編集動画は保持。GitHubから同じZIPを取得できる。

GitHubに本人のアカウントでログインし、[Releases一覧](https://github.com/toshi85/Yama_Story-/releases)の「戸沢村：画像311枠・全編編集確認セット」を開く。Tozawa_Edit_Materials.zip と Tozawa_Edit_Review.zip を両方取得し、Tozawa_Editフォルダを同じ場所へ展開・統合。Macは編集を開く.command、Windowsは編集を開く.bat。Python 3が必要。

仮の機械音声を使った本人確認版。本人の最終確認・本番音声の差し替えは未実施。残る演出の確認箇所は編集確認メモ.mdを参照。
