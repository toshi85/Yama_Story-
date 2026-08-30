#!/bin/zsh
set -eu

script_dir="${0:A:h}"

if (( $# > 0 )); then
  work_dir="$1"
else
  work_dir="$(osascript -e 'POSIX path of (choose folder with prompt "画像を作る作品フォルダを選んでください")')"
fi

python_bin=""
for candidate in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3; do
  if [[ -x "$candidate" ]]; then
    python_bin="$candidate"
    break
  fi
done

if [[ -z "$python_bin" ]]; then
  osascript -e 'display alert "Python 3が見つかりません" message "Codexをインストールした状態で、もう一度実行してください。" as critical'
  exit 1
fi

if ! "$python_bin" "$script_dir/install_for_student.py" "$work_dir"; then
  printf '\n準備に失敗しました。上のメッセージを講師へ送ってください。\n'
  read -k 1 '?何かキーを押すと閉じます。'
  exit 1
fi
printf '\nこの画面は閉じて構いません。画像生成はバックグラウンドで続きます。\n'
read -k 1 '?何かキーを押すと閉じます。'
