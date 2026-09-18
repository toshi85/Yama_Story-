cd /d/0/Yama_Story-/Scripts/2013-2014年せたな町ヒグマ事故
grep '^ナレーター: ' Master.md | LC_ALL=C.UTF-8 awk '{sub(/^ナレーター: /,""); gsub(/[ 　\r]/,""); n+=length($0)} END{print n}'
