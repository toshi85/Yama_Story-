"""Render and verify the approved aggregation, preserving quoted original titles."""
import hashlib
import html
import json
import re
import statistics
from datetime import date, datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
REPORT = BASE.parent / 'Next_Topic_Candidates_2026-09-12.md'

def read(name):
    return json.loads((BASE / name).read_text())

def save(name, data):
    (BASE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def cell(text):
    return html.escape(text, quote=False).replace('|', '&#124;').replace('\n', ' ')

summary = read('aggregation_summary.json')
classification = read('aggregation_classification.json')
rows = classification['rows']
kept = sorted((r for r in rows if r['included']), key=lambda r: (-r['view_count'], r['id']))
invalid = []
raw = {}
for path in sorted(BASE.glob('video_full_default_*.json')):
    try:
        value = json.loads(path.read_text())
        assert isinstance(value, dict) and value.get('title')
        raw[value['id']] = value
    except (ValueError, AssertionError):
        invalid.append(path.name)
assert not invalid, invalid
assert len(raw) == len(rows) == 195
assert digest(Path(summary['own_source'])) == summary['own_source_sha256']
for row in rows:
    assert digest(BASE / row['source_file']) == row['sha256'], row['id']
for row in kept:
    source = raw[row['id']]
    days = max(1, (date(2026, 9, 12) - datetime.strptime(source['upload_date'], '%Y%m%d').date()).days)
    assert row['title'] == source['title'] and row['view_count'] == source['view_count']
    assert row['elapsed_days'] == days and row['views_per_day'] == source['view_count'] / days
failed = (BASE / 'failed_ids.txt').read_text().splitlines()
assert failed == summary['failed_ids'] == ['3f68dRLjiPQ']
assert len(kept) == 142 and len(rows)-len(kept) == 53
assert sum(r['published_mark'] == '既出' for r in kept) == 22
median_views = statistics.median(r['view_count'] for r in kept)
median_daily = statistics.median(r['views_per_day'] for r in kept)
assert median_views == 689942 and round(median_daily, 2) == 1235.58

lines = [
    '# 競合動画・単独事件の実測一覧（2026-09-12）', '',
    '禁止語検査はタイトル列を除外。原題の引用は保持。', '',
    '- 取得日：2026-09-12。計算基準日：2026-09-12。',
    '- yt-dlp：2025.10.14。追加取得に使用した player_client：android（既存の取得済みJSONは保持）。',
    '- 取得：195件。未取得：1件。failed_ids.txt：`3f68dRLjiPQ`。',
    '- 単独事件：142本。除外：53本。合計：195本。',
    f'- 単独事件の中央値：総再生 {median_views:,.0f}回／再生数per日 {median_daily:,.2f}回。',
    '- 再生数per日＝総再生÷経過日数。経過日数は基準日と公開日の差で、下限は1日。日次の表示は小数第2位まで。中央値は丸め前の値から計算。',
    '- 集計単位は動画。同一事件を扱う別動画は統合せず、既出の動画も残す。',
    '- 除外対象：総集編・朗読・怪談・複数選・対策／準備系・メンバーシップ限定・ノーカット・複数事故を扱う動画・事件ではない人物史。',
    '- 分類は取得済みのタイトル・公開範囲・概要欄・章立てによる。映像内容の確認は未実施。',
    '- 再生数が欠けた25件はすべてメンバーシップ限定で、除外53本に含む。チャンネル名欠落1件は、同一channel_idの取得済みデータから補完。',
    '- 既出印：22行。照合元：`../Video_Performance_Log.md`（28本の表）。', '',
    'チャンネル別小計（中央値は単独事件の総再生）：', '',
]
for channel in summary['channels']:
    lines.append(f"- {channel['channel']}：取得{channel['acquired']}本／単独事件{channel['single_incident']}本／除外{channel['excluded']}本／中央値 {channel['median_views_single_incident']:,.0f}回。")
lines += ['', '| 総再生 | 経過日 | 再生数per日 | チャンネル | 既出印 | タイトル |',
          '| --: | --: | --: | :-- | :-- | :-- |']
for row in kept:
    lines.append(f"| {row['view_count']:,} | {row['elapsed_days']} | {row['views_per_day']:,.2f} | {cell(row['channel'])} | {row['published_mark']} | {cell(row['title'])} |")
lines += ['', '集計・分類・既出照合の記録：`next_topic_2026-09-12/aggregation_classification.json`。',
          '検査記録：`next_topic_2026-09-12/aggregation_checks.json`。', '']
REPORT.write_text('\n'.join(lines))

# Verify the saved Markdown, not merely the renderer input.
text = REPORT.read_text()
data_lines = [line for line in text.splitlines() if re.match(r'^\| [\d,]+ \|', line)]
parsed = [[html.unescape(c.strip()) for c in line.strip('|').split('|')] for line in data_lines]
assert len(parsed) == 142 and all(len(c) == 6 for c in parsed)
for cells, source in zip(parsed, kept):
    assert cells == [f"{source['view_count']:,}", str(source['elapsed_days']), f"{source['views_per_day']:,.2f}",
                     source['channel'], source['published_mark'], source['title']]
non_title = '\n'.join('|'.join(line.split('|')[:6]) if line in data_lines else line for line in text.splitlines())
words = re.findall(r'おすすめ|おススメ|オススメ|有望|狙い目|本命|推奨|推薦|評価|ランキング上位', non_title)
assert not words, words
own_lines = Path(summary['own_source']).read_text().splitlines()
for row in kept:
    if row['published_mark']:
        assert any(re.match(r'^\|\s*' + str(row['own_row']) + r'\s*\|', line) and row['own_title'] in line for line in own_lines)
assert len([c for c in parsed if c[4]=='既出']) == 22
checks = {
    'json_valid': True, 'json_count': len(raw), 'invalid_json_or_title_count': 0,
    'invalid_ids': invalid, 'report_rows': len(parsed), 'single_incident_count': len(kept),
    'excluded_count': 53, 'count_conservation': len(parsed)+53==len(raw),
    'sorted_descending': all(int(a[0].replace(',','')) >= int(b[0].replace(',','')) for a,b in zip(parsed,parsed[1:])),
    'median_views': median_views, 'median_views_per_day': median_daily,
    'published_mark_count':22, 'matched_rows_in_source':True,
    'header_data_complete':all(token in text.split('| 総再生 |')[0] for token in ['android','3f68dRLjiPQ','689,942','1,235.58','477,267','694,446']),
    'channels':summary['channels'], 'forbidden_words_outside_title_count':len(words),
    'title_column_excluded_from_word_check':True, 'original_titles_preserved':True,
    'report_overwritten':True, 'report_sha256':digest(REPORT), 'all_pass':True,
}
assert checks['sorted_descending'] and checks['header_data_complete']
save('aggregation_checks.json', checks)
summary['report_status']='complete'
summary['title_quote_policy']='ユーザー承認：原題を保持し、禁止語検査はタイトル列を除外。'
save('aggregation_summary.json', summary)
ledger = read('active_work2.json')
for task in ledger['tasks']:
    if task['id']=='aggregate2':
        task['status']='complete'
        task['next_action']='Claudeによる結果の確認'
        task.pop('blocker_evidence', None)
        task['evidence']=[{'path':str(path),'sha256':digest(path)} for path in [REPORT, BASE/'aggregation_checks.json', BASE/'aggregation_classification.json']]
save('active_work2.json', ledger)
print(json.dumps(checks, ensure_ascii=False))
