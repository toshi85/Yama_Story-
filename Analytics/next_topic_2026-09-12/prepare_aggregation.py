"""Prepare reproducible aggregation; do not overwrite report with unresolved wording."""
import csv
import hashlib
import json
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path

BASE = Path(__file__).resolve().parent
OWN = BASE.parents[1] / 'Video_Performance_Log.md'
REFERENCE = date(2026, 9, 12)

def save(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

manual_exclusions = {
    '8LrxqRuAjhc': '至仏山・苗場山・達磨山・富士山・御在所岳の複数事例',
    'DlVypKuttzY': '八方尾根2024年と白馬乗鞍岳2023年の複数事例',
    'DuC_C5NVr8E': '岳沢2024年と上高地2020年の複数事例',
    'NFWF3YOv7mY': '概要欄・章立てが谷川岳の宙づり事故、雪崩、男女の遭難など複数事例',
    'V022WlFGahU': '鞍掛山2024年9月ほかのハチ被害事例',
    'WjQ2ScCdy-g': 'マダニ感染事例・予防情報で単独事件ではない',
    'XpTJ9Wby8X0': '尾瀬2022〜2025年の複数事例・クマ対応',
    'xRzetHX4Q8A': '阿蘇山1953年・1958年・1979年の複数噴火',
    'yNVfFqLp7rA': '2010年奥秩父の9日間に起きた複数の遭難事故',
    'cfymOpcR4JM': '2010年奥秩父4重遭難の複数事故',
    'pdc2280wFxw': 'エマ・ゲイトウッドの踏破・人物史で事件ではない',
}
# Explicit correspondence, with table row numbers preserved for verification.
matches = {
    'eqaUKWlI4z8': (1, '1970年福岡大学ヒグマ事件'),
    'QuAPqsepDLk': (5, '2022年弥山、道標で道を誤った女性2名。自作Scripts/2022年弥山遭難事故.mdも参照'),
    'TEpjBVNJUoE': (5, '概要欄2022年弥山・新設道標・登山者2名'),
    'FeQNAJXfF7g': (6, '2018年新潟親子遭難'),
    'ds2_U1LkuX0': (6, '6歳児を連れた新潟親子遭難'),
    'oT2GLkV_K2Q': (7, '国見岳で夫が行方不明となる事故'),
    'Z8RBTyphbCo': (9, '1915年三毛別ヒグマ事件'),
    '4V61Mabp3kI': (10, '2025年羅臼岳クマ襲撃事件'),
    'W-DHZU_uAtI': (13, '2023年大千軒岳ヒグマ事件'),
    '8vXbAjBHI6A': (16, '2009年乗鞍岳クマ襲撃、観光客1000人'),
    'p3FR8lqoP2M': (18, '2009年トムラウシ山遭難'),
    'q7GguQB8N1M': (19, '概要欄1996年8月写真家事故、章立てに星野道夫'),
    '6RRPDM1QiU4': (20, '1989年立山、10人中8人死亡'),
    'e5sgqeqDp7E': (20, '立山中高年大量遭難事故'),
    'fG900Hqj2oU': (21, '1972年富士山。snapshot_2026-09-07.jsonの同一自作タイトルで欠落末尾を確認'),
    'nK8mwMpgHM0': (21, '1972年富士山。snapshot_2026-09-07.jsonの同一自作タイトルで欠落末尾を確認'),
    'qyKzxwqfhrg': (22, '2017年那須雪崩。snapshot_2026-09-07.jsonの同一自作タイトルで欠落末尾を確認'),
    '1EYlSWlr100': (23, '岩木山の高校山岳部5人遭難'),
    'AUzINa24Ys0': (24, '2006年六甲山遭難'),
    'dKV0I-yM77o': (24, '2006年六甲山遭難、24日後発見'),
    'j-IlplmC-WM': (25, '2013年12月富士山滑落事故'),
    'e0L4ji2pVPc': (27, '172人のランナーの低体温遭難に対応する2021年黄河石林トレイルランニング事故'),
}

own_text = OWN.read_text()
own_rows = {}
for line in own_text.splitlines():
    cells = [c.strip() for c in line.split('|')]
    if len(cells) > 3 and cells[1].isdigit():
        own_rows[int(cells[1])] = cells[2]
assert len(own_rows) == 28

raw = []
invalid = []
for f in sorted(BASE.glob('video_full_default_*.json')):
    try:
        v = json.loads(f.read_text())
        assert isinstance(v, dict) and v.get('title')
    except (ValueError, AssertionError):
        invalid.append(f.name.removeprefix('video_full_default_').removesuffix('.json'))
        continue
    raw.append((f, v))
channel_map = defaultdict(set)
for _, v in raw:
    if v.get('channel_id') and v.get('channel'):
        channel_map[v['channel_id']].add(v['channel'])

rows = []
repairs = []
for f, v in raw:
    vid = v['id']
    title = v['title']
    reasons = []
    if v.get('availability') in ('subscriber_only', 'premium_only'):
        reasons.append('メンバーシップ限定')
    for pattern, label in [ ('総集編', '総集編'), ('朗読', '朗読'), ('怪談', '怪談'),
                           (r'[0-9０-９一二三四五六七八九十百〇◯○]+選', '複数選'), ('ノーカット', 'ノーカット') ]:
        if re.search(pattern, title):
            reasons.append(label)
    if vid in manual_exclusions:
        reasons.append(manual_exclusions[vid])
    channel = v.get('channel')
    if not channel:
        candidates = channel_map[v.get('channel_id')]
        assert len(candidates) == 1, (vid, candidates)
        channel = next(iter(candidates))
        repairs.append({'id': vid, 'field': 'channel', 'channel_id': v['channel_id'], 'value': channel,
                        'basis': '同一channel_idを持つ取得済みJSONのchannel値は1種類'})
    elapsed = max(1, (REFERENCE - datetime.strptime(v['upload_date'], '%Y%m%d').date()).days)
    views = v.get('view_count')
    if not reasons:
        assert isinstance(views, (int, float)) and views >= 0, vid
    match = matches.get(vid)
    rows.append({'id': vid, 'title': title, 'view_count': views, 'upload_date': v.get('upload_date'),
                 'duration': v.get('duration'), 'channel': channel, 'elapsed_days': elapsed,
                 'views_per_day': views / elapsed if views is not None else None,
                 'included': not reasons, 'exclusion_reasons': reasons,
                 'published_mark': '既出' if match and not reasons else '',
                 'own_row': match[0] if match else None,
                 'own_title': own_rows[match[0]] if match else None,
                 'match_basis': match[1] if match else None,
                 'source_file': f.name, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest()})

included = sorted((r for r in rows if r['included']), key=lambda r: (-r['view_count'], r['id']))
excluded = [r for r in rows if not r['included']]
by_channel = []
for channel in sorted({r['channel'] for r in rows}):
    all_c = [r for r in rows if r['channel'] == channel]
    kept = [r for r in included if r['channel'] == channel]
    by_channel.append({'channel': channel, 'acquired': len(all_c), 'single_incident': len(kept),
                       'excluded': len(all_c)-len(kept),
                       'median_views_single_incident': statistics.median(r['view_count'] for r in kept) if kept else None})
failed = (BASE / 'failed_ids.txt').read_text().splitlines()
conflicts = [{'id':r['id'], 'title':r['title'], 'matched_words':re.findall('推奨|評価|有望|おすすめ|おススメ|オススメ',r['title'])}
             for r in included if re.search('推奨|評価|有望|おすすめ|おススメ|オススメ',r['title'])]
summary = {'reference_date': str(REFERENCE), 'acquisition_date': '2026-09-12',
           'yt_dlp_version': '2025.10.14', 'player_client': 'android',
           'acquired': len(rows), 'failed': len(failed), 'failed_ids': failed,
           'invalid_json_or_title_count':len(invalid), 'invalid_ids':invalid,
           'single_incident_count':len(included), 'excluded_count':len(excluded),
           'median_views':statistics.median(r['view_count'] for r in included),
           'median_views_per_day':statistics.median(r['views_per_day'] for r in included),
           'published_mark_count':sum(bool(r['published_mark']) for r in included),
           'channels':by_channel, 'channel_repairs':repairs,
           'missing_view_count':sum(r['view_count'] is None for r in rows),
           'own_source':str(OWN), 'own_source_sha256':hashlib.sha256(OWN.read_bytes()).hexdigest(),
           'literal_title_conflicts':conflicts,
           'report_status':'blocked_on_original_title_wording',
           'classification_basis':'取得済みのタイトル・availability・概要欄・章立て。動画映像の内容確認は未実施。',
           'count_unit':'動画単位。同一事件でもチャンネル間の動画は統合しない。単一災害を扱う動画は含め、複数事故を並べた動画は除外。'}
save('aggregation_summary.json', summary)
save('aggregation_classification.json', {'rows':rows,'own_table_rows':own_rows})
for name, data in [('single_incidents.csv',included), ('excluded_videos.csv',excluded)]:
    with (BASE / name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0])); writer.writeheader();writer.writerows(data)
checks = {'json_valid':len(invalid)==0, 'count_conservation':len(included)+len(excluded)==len(rows),
          'sorted_descending':all(a['view_count']>=b['view_count'] for a,b in zip(included,included[1:])),
          'published_marks_exist':any(r['published_mark'] for r in included),
          'matched_rows_in_source':all(r['own_row'] in own_rows and r['own_title']==own_rows[r['own_row']] for r in included if r['published_mark']),
          'header_data_complete':all(summary.get(k) is not None for k in ['player_client','failed_ids','median_views','median_views_per_day','channels']),
          'literal_title_word_conflicts':len(conflicts), 'report_overwritten':False}
save('aggregation_checks.json',checks)
print(json.dumps({k:summary[k] for k in ['acquired','single_incident_count','excluded_count','median_views','median_views_per_day','published_mark_count','literal_title_conflicts']},ensure_ascii=False))
