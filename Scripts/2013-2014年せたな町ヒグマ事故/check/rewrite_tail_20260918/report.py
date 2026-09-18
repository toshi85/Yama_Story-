from pathlib import Path
import re, json, hashlib

a=Path(__file__).resolve().parent
p=a.parent.parent
before=(a/'Master.md.before').read_text(encoding='utf-8')
after=(p/'Master.md').read_text(encoding='utf-8')
marker='<!-- src: 素材#72 #77 #78 #60。以下は本人未チェック。 -->'
old=before[before.index(marker):]
tail=(a/'tail.txt').read_text(encoding='utf-8')
def count(s):
    return sum(len(re.sub('[ 　\r]','',l.split(': ',1)[1])) for l in s.splitlines() if l.startswith('ナレーター: '))
start,end=count(before),count(after)
fixed=(a/'Master.md.before').read_bytes().split(marker.encode())[0]
assert (p/'Master.md').read_bytes().startswith(fixed)
checks={
'2014年3月の捕獲許可・早い雪解け':'§12',
'4月4日太田の事故・ギョウジャニンニク・男性の後ろを下山・背後・肩と腕・ナタで顔・手負い':'§13',
'旧校舎付近の通行止め・翌日の看板・血痕採取・現地調査・聞き取り・前年の毛とのDNA一致':'§14',
'4月7日の捜索とヘリ要請・8日夜の通行止め・9日の大捜索・足跡・日没まで未発見':'§15',
'5月19日の箱わな・駆除・肉片送付・DNA不一致':'§16',
'12月18日の議会・対策本部・捕獲活動・免許補助の利用・農協の支援・職員採用等の提案・町長の未捕獲発言・翌春の方針・入山規制':'§17',
'2015年春の異例の捜索・足跡とナタ傷の手がかり・ビラ・住民と旅行者への入山自粛':'§18',
'4月上旬の鑑定依頼と照合':'§19',
'4月22日夜の一致・2014年8月4日の今金町での捕獲と駆除・場所・推定年齢・体格・現場からの隔たり':'§20',
'4月23日の発表・捜索打ち切り方針・町長、住民、ハンターの反応・移動についての町の見解・継続する注意喚起':'§21',
'いま山に入る人への呼びかけ':'§22',
}
full='\n'.join(l for l in tail.splitlines() if not l.startswith('<!--'))
full=re.sub(r'\n{3,}','\n\n',full).strip()

# All removed original narrator lines are listed, including rewrites. This makes
# wording deletion auditable without pretending retained facts were discarded.
newlines=set(after.splitlines())
mapping={'11':'§11','12':'§17','13':'削除','14':'§12','15':'§13','16':'§13','17':'§13','18':'§13',
 '18a':'§14','19':'§14','20':'§14','21':'§13・§14','21a':'§15','21b':'§16','22':'§17',
 '23':'§17・§18','23a':'§18','24':'§13・§14・§22','25':'§11・§17','26':'§20','27':'§19・§20',
 '27a':'§21','28':'§11・§22'}
def classify(ch,t):
    if ch=='11': return '削除：助成の対象条件・回数・上限額とその説明','YCP-058・061（ユーザー指定の断り書きを含む）'
    if ch=='13': return '削除：地域統計とその留保、既出の会議に戻る周辺説明','YCP-058・061・065'
    if any(x in t for x in ['わけではありません','わけではない','ではありません','とは特定できません','確認できなかった','証拠にはなりません','とまでは述べていません','とみなすことはできません','約束にはできません','条件にはなりません','番号はないのです']):
        return '削除：断り書き・不明事項の説明','YCP-053／ユーザー指定「書かないもの」'
    if any(x in t for x in ['現場写真','舗装面','写真が載って','写真の説明']):
        return '削除：資料の見た目・本筋を進めない写真説明','YCP-051・058・061'
    if (ch=='22' and any(x in t for x in ['広報には','農業者','農作物','窓口','対応事例'])):
        return '削除：本件の捜索と直接結びつかない相談窓口の紹介','YCP-058・061'
    if t in ['看板を立てたのは、2カ所でした。','規制された区間は、9.2キロでした。','従事していたのは25人です。','年度の途中までに捕まえたクマは、20頭です。','この数は、せたな町のその年度の捕獲実績でした。','配ったのは、200枚。','4月4日までに、目撃や負傷の情報は5件になっています。','前年の同じ時期より、3件多い数です。']:
        return '削除：人数・箇所数・集計値などの周辺細部','YCP-061'
    if ch=='23a' and ('多くのクマは' in t or '人が減り' in t or '新たな被害者を' in t):
        return '削除：同一場面の証言を町の発言1つへ整理','ユーザー指定「1場面1つまで」・YCP-061'
    if ch=='21a' and 'きょうこそ' in t:
        return '削除：同じ捜索場面の証言を雪解けの期限に絞る','ユーザー指定「1場面1つまで」'
    dest=mapping[ch]
    if any(x in t for x in ['記事','報告','一覧','広報','記されています','記して','報じられ','報道','資料','説明でした','という答弁','答弁です']):
        return f'出典説明を外して改稿・統合（事実は{dest}）','YCP-058・062'
    if any(x in t for x in ['ことになります','つながっていました','このあと','そのあとの出来事','迎えます','なったのです']):
        return f'予告・総括を削り、出来事へ統合（{dest}）','YCP-055・059'
    if re.search(r'\d+年.*月|月\d+日|午後\d+時',t):
        return f'日付行と動作へ再配置・統合（{dest}）','YCP-054・055・065'
    return f'同じ事実を場面内の動作へ改稿・統合（{dest}）','YCP-055・062・063（固有名詞は066、不要な数値は061）'

deleted=[]; ch='11'
for line in old.splitlines():
    m=re.match(r'## (\d+[a-z]?)\.',line)
    if m: ch=m[1]
    if not line.startswith('ナレーター: ') or line in newlines: continue
    text=line.split(': ',1)[1]
    how,kind=classify(ch,text)
    deleted.append((ch,text,how,kind))

report=f'''# §11後半以降の改稿報告

**字数条件は未達のため、完成稿としての要件は満たしていません。**

| 時点 | ナレーション字数 | 323字／分 |
|:--|--:|--:|
| 開始時 | {start:,}字 | {start/323:.2f}分 |
| 終了時 | {end:,}字 | {end/323:.2f}分 |
| 指定下限との差 | {8100-end:,}字不足 | {(8100-end)/323:.2f}分不足 |

指定のgrep・awk式をGit Bashで開始時と終了時に実行。空白・全角空白・CRを除外し、ナレーター行だけを計数しました。

§1〜§11前半は見出し・コメント・空行を含めバイト単位で一致。固定範囲は1,381字です。gitコミットはしていません。

## 検査結果

指定の5本を実行し、改稿対象の§11後半以降のWARN／FAILは0件です。

| 検査 | 修正対象 | 全体の結果 |
|:--|:--|:--|
| validate_yama_narrative.py | WARN 0／FAIL 0 | 固定範囲に既存WARN 3件（§4の奥尻町、§5の振興局の初出・道南地区） |
| validate_yama_safety.py | 0件 | PASS |
| validate_yama_facts.py | 0件 | PASS |
| audit_numeric_facts.py | 未検証0件 | PASS |
| validate_yama_consistency.py | 0件 | PASS |

ナラティブ検査の補足出力には「一年後」「数百メートル」の漢数字案内があります。前者は固定範囲、後者は素材の概数を保持した表現です。WARN／FAILとは別の情報出力です。

Plot_Sheetの章題・素材番号・字数を本文に合わせ、Fact_Sheetは「使う章」欄のみ更新しました。検査コードと素材の事実本文は変更していません。

## 主要な出来事の照合

'''
for fact,dest in checks.items(): report+=f'- {fact}：{dest}\n'
report+='''
削除した文は下記です。出典文から事実を移したもの、短文を統合したものも含め、元の文面が消えた箇所を全件示します。「削除」と「改稿・統合」を分け、出来事自体を残した箇所は移動先を記しました。

既存の出来事を戻す再点検後も、8,100字には達していません。削除した条件・統計・留保や同じ事実の反復を戻して字数を満たすことはしていません。ただし、これは字数条件を満たしたという報告ではありません。

## §11後半以降の全文（src省略）

### 11. 捕獲を担う町民への助成（固定範囲より後）

'''+full+'\n\n## 削った元の文面と、当てた型\n\n'
for i,(ch,t,how,kind) in enumerate(deleted,1):
    report+=f'{i}. 旧§{ch}「{t}」\n   - {how}。{kind}。\n\n'
(a/'改稿報告.md').write_text(report,encoding='utf-8')
(a/'後半全文_src省略.md').write_text('# 11. 捕獲を担う町民への助成（後半）\n\n'+full+'\n',encoding='utf-8')
(a/'verification.json').write_text(json.dumps({'before_chars':start,'after_chars':end,'before_minutes':start/323,'after_minutes':end/323,'minimum_met':end>=8100,'fixed_prefix_sha256':hashlib.sha256(fixed).hexdigest(),'fixed_prefix_identical':True,'removed_or_rewritten_lines':len(deleted)},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{start} -> {end}; removed/rewritten {len(deleted)} lines; report saved')
