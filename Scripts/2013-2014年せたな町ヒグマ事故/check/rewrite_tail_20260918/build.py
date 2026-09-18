from pathlib import Path
import re

a = Path(__file__).resolve().parent
p = a.parent.parent
b = (a / 'Master.md.before').read_bytes()
marker = '<!-- src: 素材#72 #77 #78 #60。以下は本人未チェック。 -->'.encode()
prefix = b[:b.index(marker)]
tail = (a / 'tail.txt').read_text(encoding='utf-8')
(p / 'Master.md').write_bytes(prefix + tail.replace('\n', '\r\n').encode('utf-8'))
s = (p / 'Master.md').read_text(encoding='utf-8')
chap = []
for m in re.finditer(r'^## (\d+)\. (.+)\n([\s\S]*?)(?=^## \d+\.|\Z)', s, re.M):
    n, title, body = m.groups()
    ids = sorted(set(map(int, re.findall(r'#(\d+)', body))))
    count = sum(len(l.split(':', 1)[1].strip()) for l in body.splitlines() if l.startswith('ナレーター:'))
    chap.append((n, title, ids, count))
plot = '''# プロット表: 2013・2014年せたな町ヒグマ人身事故

- 2026-09-18: 本人指定の§11後半以降を改稿。§1〜§11前半はコメント・空行を含めバイト単位で保持。
- 12月18日の議会を§17へ集約。§20は鑑定判明後に前年8月の捕獲を振り返る。
- 設計・実測字数は今回の再構成に合わせて更新。旧稿と旧表はcheck/rewrite_tail_20260918に保存。
- 字数下限8,100字は未達。検査通過と原稿の完成を同一視しない。

| 章 | タイトル | PART | 種別 | 設計字数 | 実測字数 | 素材# |
|--:|:--|:--|:--|--:|--:|:--|
'''
for n, title, ids, count in chap:
    part = 'KI' if int(n) < 4 else 'SHO' if int(n) < 20 else 'TEN-KETSU'
    kind = '実用' if n == '22' else '動き'
    plot += f'| {n} | {title} | {part} | {kind} | {count} | {count} | ' + ','.join(map(str, ids)) + ' |\n'
plot += '''
## 事実の扱い

- 2014年の毛・血痕の一致と、2015年の捕獲個体の一致を区別する。
- 2014年12月の「未捕獲」は当時の町の認識。町や捜索隊に前年夏の駆除を先回りして知らせない。
- 町職員の採用・資格取得は議員の提案、翌春の2月下旬の対応は町長の方針として保持。
- クマの移動は町担当者の見解。実際の移動経路や鑑定に時間を要した理由を補わない。
- 入山時刻、当事者の心理、鈴の鳴り方、ナタの回数・刃か峰か、搬送手段を補わない。
- 固定範囲以前の制作メモには旧章数・旧字数の記載があるが、固定範囲保全のため変更しない。
'''
(p / 'Plot_Sheet_せたな町.md').write_text(plot, encoding='utf-8')
f = (a / 'Fact_Sheet_せたな町.md.before').read_text(encoding='utf-8')
def update(m):
    line = m[0]
    sid = int(re.match(r'\| (\d+)', line)[1])
    fields = line.split('|')
    fields[-2] = ' ' + (', '.join('§' + n for n, title, ids, count in chap if sid in ids) or '不使用（2026-09-18後半改稿）') + ' '
    return '|'.join(fields)
f = re.sub(r'^\| \d+ \|.*$', update, f, flags=re.M)
(p / 'Fact_Sheet_せたな町.md').write_text(f, encoding='utf-8')
assert (p / 'Master.md').read_bytes().startswith(prefix)
print('固定範囲バイト一致: PASS')
