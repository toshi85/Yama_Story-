#!/usr/bin/env python3
"""上限が解けるころに、生成の常駐を安全に入れ直す。

ChatGPTの画像生成上限は「20時間後に解除」で毎日ずれていく。解除直後に
run.py を入れ直すと、ページのドライバが新しい状態で投げ直すので取りこぼしがない。

ただし生成中に入れ直すと、その1枚を捨てることになる。だから
「前回見たときから1枚も増えていない＝待ちで止まっている」ときだけ入れ直す。
"""
import json
import pathlib
import subprocess
import sys
import time

LABEL = 'com.yama.imagegen'


def main(work: pathlib.Path) -> None:
    queue = json.loads((work / 'image_queue.json').read_text(encoding='utf-8'))
    have = {p.stem for p in (work / 'images').glob('*.png')}
    done = sum(1 for q in queue if q['id'] in have)
    stamp = time.strftime('%H:%M:%S')

    if done >= len(queue):
        print(f'{stamp} kick: 全{len(queue)}枚そろっています。何もしません', flush=True)
        return

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

    uid = subprocess.run(['id', '-u'], capture_output=True, text=True).stdout.strip()
    result = subprocess.run(
        ['launchctl', 'kickstart', '-k', f'gui/{uid}/{LABEL}'],
        capture_output=True, text=True)
    ok = '入れ直しました' if result.returncode == 0 else \
         f'入れ直しに失敗（{(result.stderr or result.stdout).strip()}）'
    print(f'{stamp} kick: {done}/{len(queue)}枚で止まっていたので {ok}', flush=True)


if __name__ == '__main__':
    main(pathlib.Path(sys.argv[1]).expanduser().resolve())
