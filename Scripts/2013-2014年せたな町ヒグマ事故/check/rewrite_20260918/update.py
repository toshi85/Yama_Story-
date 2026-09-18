from pathlib import Path
import re
import json

d = Path(__file__).resolve().parents[2]
work = Path(__file__).resolve().parent
original = (work / 'Master.md.before').read_bytes()
prefix = original.split('## 5.'.encode('utf-8'))[0]
replacement = (work / 'replacement.md').read_text(encoding='utf-8')
newline = '\r\n' if b'\r\n' in original else '\n'
(d / 'Master.md').write_bytes(prefix + replacement.replace('\n', newline).encode('utf-8'))

text = (d / 'Master.md').read_text(encoding='utf-8')
chapters = []
part = 'KI'
for line in text.splitlines():
    marker = re.match(r'<!-- PART: (.*?) -->', line)
    if marker:
        part = marker[1]
    heading = re.match(r'## (\d+)\. (.*)', line)
    if heading:
        chapters.append(dict(no=int(heading[1]), title=heading[2], part=part, chars=0, src=set()))
    elif chapters:
        if line.startswith('ナレーター:'):
            chapters[-1]['chars'] += len(line.split(':', 1)[1].strip())
        if line.startswith('<!-- src:'):
            chapters[-1]['src'].update(map(int, re.findall(r'#(\d+)', line)))

# 固定章のsrcは原本どおり。そこで文章で示されている追加出典も改変しない。

kinds = {1:'フック', 2:'動き', 3:'動き', 4:'動き', 5:'動き', 6:'動き', 7:'動き', 8:'動き', 9:'動き', 10:'動き', 11:'動き', 12:'動き', 13:'動き', 14:'動き', 15:'証言', 16:'証言', 17:'証言', 18:'動き', 19:'動き', 20:'動き', 21:'実用'}
plot = '''# プロット表: 2013・2014年せたな町ヒグマ人身事故

- 設計変更: 2026-09-18 本人指定の全面改稿。旧28章の制度・統計・出典説明・留保を整理し、追加された事故の具体と捕獲個体の照合を中心に21章へ再構成。旧設計はcheck/rewrite_20260918/Plot_Sheet_せたな町.md.before、改稿前の配分案は同design.mdに保存。
- 目標尺: 最大30分（9,700字）。未使用素材の上限見積もり8,000字を字数ノルマにしない。内容の重複・創作による引き延ばしは禁止。
- 前半ピーク: 5
- 後半ピーク: 20
- ボトム: 17
- 字数欄: 今回は本人が本文に合わせた再構成を指示したため、確定した章の内容を今回の設計として登録。以後の検査調整では実測欄のみ更新する。旧配分との変更は保存済み。

| 章 | タイトル | PART | 種別 | 設計字数 | 実測字数 | 素材# |
|--:|:--|:--|:--|--:|--:|:--|
'''
design_path = work / 'final_design.json'
if design_path.exists():
    design = json.loads(design_path.read_text(encoding='utf-8'))
else:
    design = {str(c['no']): c['chars'] for c in chapters}
    design_path.write_text(json.dumps(design, ensure_ascii=False, indent=2), encoding='utf-8')
for c in chapters:
    src = ','.join(map(str, sorted(c['src'])))
    plot += f"| {c['no']} | {c['title']} | {c['part']} | {kinds[c['no']]} | {design[str(c['no'])]} | {c['chars']} | {src} |\n"
plot += '''
## 事実と場面の制約

- §1〜§4は本人確定の見出し・本文・コメント・空行を含め原本からバイト単位で保持。プロットの旧章題と実測のみ整合させた。§5冒頭2行も保持。
- 固定章の素材番号は既存srcに合わせて保持。§2〜§4のNHK・研究所の追加出典は原本に番号ではなく文章で記載され、内容は#84・#86・#87に対応する。番号の付け直しも固定範囲を変えるため行わない。
- §5は4月17日の調査から、前日の発見時刻、沢の近く、傷と足跡だけを補足。§4の食害・所持品描写は重ねない。
- §6は同日早朝の猟友会へ視点を移す。振興局から周辺町への連絡は前日と明記。調査団の派遣日・作業完了日は補わない。
- §7のオス・前足幅は当時の会議で判明していた特徴。わな5カ所は捕獲成績へ置き換えない。
- §8の助成は開始年度の制度として短く扱い、本件を制度創設の理由にしない。条件・上限額は使わない。
- §9の照合は2013年に付近で捕獲された個体の範囲。翌年3月の許可取得へ日付を明示して進める。
- §10〜§12は#93〜#97の当時記事全文引用を中心に、並び順・距離・負傷部位・反撃・搬送を描く。看板を見たか、鈴が鳴っていたか、恐怖や判断、ナタの回数・刃か峰か、搬送方法は創作しない。
- §13〜§14の調査・聞き取り・血痕照合は、2014年の二事故間の同定。2015年の捕獲個体との鑑定を混ぜない。8キロは現場間の隔たり。
- §15〜§17は12月18日の議会の場面。対策本部の設置がどちらの事故直後かは限定せず、防災ヘリの出動日も補わない。20頭は2014年度途中の捕獲数。議員案は提案として、町長の未捕獲発言は当時の認識として扱う。
- §18で捕獲個体の鑑定依頼、§19で対象個体の前年夏の捕獲経緯を置く。加害個体との一致は§20まで語らない。
- §19の16キロは太田の事故現場と捕獲地点の隔たり。推定7歳を保持。捕獲時の負傷確認の限界を完治や無傷へ言い換えない。
- §20が結末の山。2014年8月の捕獲と、12月の認識、2015年4月22日夜の結果を区別する。鑑定の遅れの理由・住民の反応は足さない。
- §21は本件の同行者・鈴・看板・入山規制に即した短い注意。ナタでの反撃を一般向けの対処法にしない。
- 〔外部〕#45〜#47を使用しない。写真の#29・#30、個体を同定できない#64も実景描写の根拠へ転用しない。
'''
(d / 'Plot_Sheet_せたな町.md').write_text(plot, encoding='utf-8', newline=newline)

# 素材本文は変えず、章再編に必要な「使う章」列だけ更新する。
fact_path = d / 'Fact_Sheet_せたな町.md'
fact = (work / 'Fact_Sheet_せたな町.md.before').read_text(encoding='utf-8')
uses = {}
for c in chapters:
    for sid in c['src']:
        uses.setdefault(sid, []).append(c['no'])
lines = []
for line in fact.splitlines():
    m = re.match(r'^\|\s*(\d+)\s*\|', line)
    if m:
        cells = line.split('|')
        cells[-2] = ' ' + (', '.join(f'§{n}' for n in uses.get(int(m[1]), [])) or '不使用（2026-09-18改稿）') + ' '
        line = '|'.join(cells)
    lines.append(line)
fact_path.write_text('\n'.join(lines)+'\n', encoding='utf-8', newline=newline)
assert (d / 'Master.md').read_bytes().split('## 5.'.encode('utf-8'))[0] == prefix
print('fixed_prefix_bytes_match=True')
print('total_chars=', sum(c['chars'] for c in chapters))
print('minutes=', sum(c['chars'] for c in chapters)/323)
