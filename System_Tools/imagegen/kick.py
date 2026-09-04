#!/usr/bin/env python3
"""上限が解けたら、生成の常駐を入れ直す。

ChatGPTの画像生成上限は解除時刻が毎日ずれる（「明日の14:33に」「17時間後に
リセット」など）。決め打ちの時刻で起こすと外れるので、**run.py がページから
読み取って書き出した解除予定時刻**（.imagegen/limit_until.json）を見て、
その時刻を過ぎてから入れ直す。10分おきに呼ばれる前提。

  python3 kick.py <作品フォルダ>            # 本番
  python3 kick.py <作品フォルダ> --dry-run  # 判断だけ見る（常駐は触らない）

触らない条件は3つ。
  ・全部そろっている
  ・解除予定の時刻がまだ来ていない（＝待っているだけで、壊れてはいない）
  ・前回見たときから1枚でも増えている（＝生成中。入れ直すとその1枚を捨てる）
"""
import json
import pathlib
import subprocess
import sys
import time

LABEL = 'com.yama.imagegen'


def main(work: pathlib.Path, dry_run: bool = False) -> None:
    queue = json.loads((work / 'image_queue.json').read_text(encoding='utf-8'))
    have = {p.stem for p in (work / 'images').glob('*.png')}
    done = sum(1 for q in queue if q['id'] in have)
    stamp = time.strftime('%H:%M:%S')

    if done >= len(queue):
        print(f'{stamp} kick: 全{len(queue)}枚そろっています。何もしません', flush=True)
        return

    # 上限待ちの最中は触らない。run.py がページから読んだ解除予定を信じる。
    limit_path = work / '.imagegen' / 'limit_until.json'
    if limit_path.exists():
        try:
            until = json.loads(limit_path.read_text(encoding='utf-8'))['until']
        except Exception:
            until = 0
        if until > time.time():
            at = time.strftime('%m/%d %H:%M', time.localtime(until))
            left = int((until - time.time()) / 60)
            print(f'{stamp} kick: 上限待ち。解除は {at} ごろ（あと{left}分）', flush=True)
            return
        if until:
            limit_path.unlink(missing_ok=True)
            print(f'{stamp} kick: 上限が解けたので入れ直します', flush=True)

    state_path = work / '.imagegen' / 'kick_state.json'
    before = None
    if state_path.exists():
        try:
            before = json.loads(state_path.read_text(encoding='utf-8')).get('done')
        except Exception:
            before = None
    state_path.parent.mkdir(exist_ok=True)
    state_path.write_text(json.dumps({'done': done, 'at': time.time()}), encoding='utf-8')

    if before is not None and done > before:
        print(f'{stamp} kick: {before}→{done}枚と進んでいるので触りません', flush=True)
        return

    if dry_run:
        print(f'{stamp} kick: （試し）{done}/{len(queue)}枚で止まっているので入れ直すところ', flush=True)
        return

    uid = subprocess.run(['id', '-u'], capture_output=True, text=True).stdout.strip()
    result = subprocess.run(
        ['launchctl', 'kickstart', '-k', f'gui/{uid}/{LABEL}'],
        capture_output=True, text=True)
    ok = '入れ直しました' if result.returncode == 0 else \
         f'入れ直しに失敗（{(result.stderr or result.stdout).strip()}）'
    print(f'{stamp} kick: {done}/{len(queue)}枚で止まっていたので {ok}', flush=True)


if __name__ == '__main__':
    main(pathlib.Path(sys.argv[1]).expanduser().resolve(), '--dry-run' in sys.argv)
