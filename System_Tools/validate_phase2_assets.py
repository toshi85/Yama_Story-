#!/usr/bin/env python3
"""
Yama Phase2 アセット割り振り 自動検証（羅臼岳標準）
使い方:
  python3 validate_phase2_assets.py <Master.md> <台本.txt>   # フル検証(1-13)+プロンプトlint(14-20)
  python3 validate_phase2_assets.py --prompts <任意の.md>    # プロンプトlint(14-20)のみ（修正版資料等の単体チェック用）

「ユーザーに見せる前」に必ず実行し、全項目GREENにしてから提示する。
2026-07-16の朱鞠内湖で4〜5回の作り直しが発生した反省から作成。
2026-07-24拡張: 生成失敗パターン(冬化/二足歩行/グラフ動画崩れ/黒画面/方向曖昧)と
ナレ行⇄プロンプト整合(クマ不在等)の機械検出を追加。根拠: memory/yama-lovart-failure-patterns.md
ルール根拠: memory/feedback_yama_one_asset_per_narration_line.md
"""
import re, sys

if hasattr(sys.stdout, 'reconfigure'):  # Windows cp932コンソール対策
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def prompt_lint(text, errors, warns, info):
    """rules 14-20: 生成失敗パターン+ナレ行整合のlint。Master.md/修正版どちらの書式にも対応"""
    # ナレ行→次のナレ行までを1セグメントとして走査
    marks = [(mo.start(), mo.group(1)) for mo in re.finditer(
        r'^(?:ナレーター:|\*\*ナレ行\*\*:\s*ナレーター:)\s*(.*)$', text, re.M)]
    segs = []
    for i, (pos, nar) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        seg = text[pos:end]
        if '【制作メモ】' in seg:
            segs.append((nar, seg))

    def asset_no(seg):
        mo = re.search(r'ASSET-\d+', seg)
        return mo.group(0) if mo else '?'

    # 14) 冬化トリガー: 地名/北海道 + cold/grey系の光 + 季節宣言なし（朱鞠内湖=氷上ワカサギ連想）
    #     ※意図的な冬シーン（winter/snow等を明示宣言）は正しいので対象外。検出するのは「季節未指定の事故的冬化」のみ
    winter = []
    SEASON_DECLARED = re.compile(r'\b(winter|snow\w*|frozen|icy|midwinter)\b|no snow|Fresh green|fresh leaf|lush green|\b(spring|summer|autumn|May|June|July|August|September|October|November)\b', re.I)
    PLACE_JP = re.compile(r'\bJapan\w*|Akita|Higashinaruse|Yuzawa|Yokote|Hokkaido|Shumarinai\b', re.I)
    COLD_LIGHT = re.compile(r'\b(cold|chilly|grey|gray|overcast|bleak|wintry|pre-dawn|first light|dim|pale)\b[^.]{0,60}\b(light|daylight|morning|sky|air|water|tones?)\b', re.I)
    # 2026-08-28 拡張: 地名を北海道限定から日本全域へ、光の語も overcast/pre-dawn 等へ広げた。
    # ASSET-176（秋田の路上・cold blue morning・季節宣言なし）が旧条件をすり抜けて雪景色になったため。
    for nar, seg in segs:
        blocks = re.findall(r'```\n?(.*?)\n?```', seg, re.S)
        for b in blocks:
            if 'white background' in b.lower():
                continue
            if PLACE_JP.search(b) and COLD_LIGHT.search(b) and not SEASON_DECLARED.search(b):
                winter.append(asset_no(seg))
                break
    if winter:
        warns.append(f'冬化トリガー {len(winter)}件（季節を一言も書かずに cold/grey/overcast/pre-dawn 系の光を書くと雪景色になる。屋外背景には必ず季節を1語入れ、秋なら No snow anywhere, no frost, no winter も添える）: {", ".join(dict.fromkeys(winter))}')

    # 15) ナレ行にクマ/ヒグマ→プロンプト側にクマ不在（象徴表現逃げの検出）
    bearless = []
    for nar, seg in segs:
        nar_clean = re.sub(r'クマスプレー|クマよけ|クマ鈴|クマ避け', '', nar)
        if re.search(r'ヒグマ|クマ', nar_clean):
            body = seg.split('\n', 1)[1] if '\n' in seg else ''
            if not re.search(r'\bbear\b|クマ|ヒグマ|CHAR-03', body, re.I):
                bearless.append(asset_no(seg))
    if bearless:
        warns.append(f'ナレ行はクマなのにプロンプトにクマ不在 {len(bearless)}件（象徴表現逃げ禁止。主語をそのまま描く）: {", ".join(bearless)}')

    # 16) カートゥーンのクマ走り: ON ALL FOURS必須（二足歩行化防止 ASSET-143実例）
    biped = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if 'cartoon' in b.lower() and re.search(r'\bbear\b', b, re.I) \
               and re.search(r'\b(runn?ing|sprint|charg\w*|chas\w*|gallop\w*)\b', b, re.I) \
               and not re.search(r'ALL FOURS|all fours|quadruped', b):
                biped.append(asset_no(seg))
    if biped:
        errors.append(f'カートゥーンのクマ走りにON ALL FOURSなし {len(biped)}件（二足歩行化する。四足ギャロップ定型文+NOT standing upright必須）: {", ".join(biped)}')

    # 17) グラフ系に動画プロンプト（グラフの動画化は崩れる ASSET-177実例→静止画のみ+編集Ken Burns）
    graphvid = []
    for nar, seg in segs:
        if re.search(r'\b(chart|graph|infographic)\b|グラフ', seg, re.I) and 'Google Flow動画プロンプト' in seg:
            graphvid.append(asset_no(seg))
    if graphvid:
        warns.append(f'グラフ系にFlow動画プロンプト {len(graphvid)}件（グラフの動画化は崩れる→静止画のみ+編集ズームを推奨）: {", ".join(graphvid)}')

    # 18) 暗背景の黒つぶれ: dark背景に明度・コントラスト指定なし（真っ黒画面 ASSET-174実例）
    dark = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if re.search(r'dark (charcoal|slate|background)', b, re.I) \
               and not re.search(r'bright|high-contrast|clearly visible|NOT pure black', b, re.I):
                dark.append(asset_no(seg))
    if dark:
        warns.append(f'暗背景に明度指定なし {len(dark)}件（黒一色に沈む→NOT pure black+要素をbright/high-contrast明示）: {", ".join(dark)}')

    # 19) 投げる系に着地点なし: 方向が水側に解釈される（ASSET-178実例）
    throw = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if re.search(r'\b(toss\w*|throw\w*|hurl\w*)\b', b, re.I) \
               and not re.search(r'land(s|ing)? (on|flopping)|onto the (dry|gravel|ground)|AWAY from|never in the water', b, re.I):
                throw.append(asset_no(seg))
    if throw:
        warns.append(f'投げる動作に着地点指定なし {len(throw)}件（方向が曖昧だと水中等に誤解釈→AWAY from+着地点+既存落下物アンカー）: {", ".join(throw)}')

    # 20) 【chatGPT推奨】ブロックが日本語本文（形式は英語本文+日本語は引用符内のみ ASSET-147実例）
    jp_body = []
    for mo in re.finditer(r'(-[^\n]*【chatGPT推奨】[^\n]*|[^\n]*【chatGPT推奨】[^\n]*)\n(?:[^\n`]*\n)*?```\n?(.*?)\n?```', text, re.S):
        b = mo.group(2)
        stripped = re.sub(r"'[^']*'|「[^」]*」|『[^』]*』", '', b)
        jp = len(re.findall(r'[一-龠ぁ-んァ-ヴー]', stripped))
        if jp > 30:
            no = re.search(r'ASSET-\d+', mo.group(0))
            jp_body.append(no.group(0) if no else '?')
    if jp_body:
        warns.append(f'chatGPT推奨プロンプトが日本語本文 {len(jp_body)}件（形式統一=英語本文+描かせる日本語のみ引用符内）: {", ".join(dict.fromkeys(jp_body))}')

    # 21) 人物プロンプトに日本人指定なし（外国人顔化 ASSET-093実例: 場所でなく人物側に日本を付与）
    PERSON = re.compile(r'\b(man|men|woman|women|angler|hiker|journalist|fisherman|person|people|father|child|guide|staff|worker|hunter)\b', re.I)
    nonjp = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if PERSON.search(b) and not re.search(r'Japanese|East Asian', b, re.I) \
               and not re.search(r'no people|no humans|No people visible', b, re.I):
                nonjp.append(asset_no(seg))
                break
    if nonjp:
        warns.append(f'人物に日本人指定なし {len(nonjp)}件（外国人顔になる→各人物にJapanese+必要ならall East Asian with black hair+No Western-looking people）: {", ".join(dict.fromkeys(nonjp))}')

    # 22) 複数人なのに書き分け指定なし（全員同じ見た目のクローン化 ASSET-025実例）
    MULTI = re.compile(r'\b(two|three|four|five|six|seven|ten|several|group of|crowd)\b[^.]*\b(men|people|anglers|hikers|passengers|persons)\b|\b(men|people|anglers|hikers)\b[^.]*\b(side by side|together)\b', re.I)
    clones = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if MULTI.search(b) and not re.search(r'distinct individual|no two (people |anglers )?(wear|dressed)|different build', b, re.I):
                clones.append(asset_no(seg))
                break
    if clones:
        warns.append(f'複数人に書き分け指定なし {len(clones)}件（全員クローン化する→Every person is a distinct individual+服装を一人ずつ列挙+no two dressed alike）: {", ".join(dict.fromkeys(clones))}')

    # ===== rules 23-31: 構成バランス・文字数整合・生成失敗の追加検出（2026-08-21 追加）=====
    # 根拠: 東成瀬村セッションで人手で数えていた項目を機械化。ルール本文は ASSET_CHECKLIST.md STEP2/STEP3

    def asset_type(seg):
        """制作メモの [タイプ] を5分類に正規化。判定順が重要（動画>Earth>キャラ>静止画>テキスト）"""
        mo = re.search(r'【制作メモ】\s*ASSET-\d+\s*\[([^\]]+)\]', seg)
        if not mo:
            return None
        t = mo.group(1)
        if '動画' in t:            return '動画'
        if 'Google Earth' in t:    return 'Earth'
        if 'キャラアニメーション' in t: return 'キャラ'
        if '静止画' in t or '実写' in t: return '静止画'
        if 'テキスト' in t:        return 'テキスト'
        return 'その他'

    PUNCT = re.compile(r'[、。，．！？!?「」『』（）()【】・…—\-\s]')

    def nar_len(nar):
        """ナレーション文字数。句読点・括弧・記号・空白は数えない（本プロジェクトの数え方）"""
        return len(PUNCT.sub('', nar))

    typed = [(nar, asset_type(seg), asset_no(seg)) for nar, seg in segs]

    def run_lengths(target):
        """同一タイプの連続区間を [(開始index, 長さ)] で返す"""
        out, i = [], 0
        while i < len(typed):
            if typed[i][1] == target:
                j = i
                while j < len(typed) and typed[j][1] == target:
                    j += 1
                out.append((i, j - i))
                i = j
            else:
                i += 1
        return out

    # 23) キャラアニメーションの連続（4回以上で単調化）
    long_char = [(s, n) for s, n in run_lengths('キャラ') if n >= 4]
    if long_char:
        detail = ' / '.join(f'{typed[s][2]}から{n}連続' for s, n in long_char)
        warns.append(f'キャラアニメーションが4回以上連続 {len(long_char)}箇所（画が単調になる→実写かGoogle Earthを挟む）: {detail}')

    # 24) 静止画の連続（ASSET_CHECKLIST STEP2「連続静止画は2枚まで」）
    long_still = [(s, n) for s, n in run_lengths('静止画') if n >= 3]
    if long_still:
        detail = ' / '.join(f'{typed[s][2]}から{n}連続' for s, n in long_still)
        errors.append(f'静止画が3枚以上連続 {len(long_still)}箇所（連続静止画は2枚まで。AI静止画+Ken Burnsが2分以上続く）: {detail}')

    # 25) Google Earthの連続（GEは連続2回まで・2026-08-20ルール化）
    long_ge = [(s, n) for s, n in run_lengths('Earth') if n >= 3]
    if long_ge:
        detail = ' / '.join(f'{typed[s][2]}から{n}連続' for s, n in long_ge)
        warns.append(f'Google Earthが3回以上連続 {len(long_ge)}箇所（GEは連続2回まで→間に実写/キャラを挟む）: {detail}')

    # 26) ナレーション文字数とタイプの整合（25字以下=全タイプ / 26-50字=静止画不可 / 51字以上=要分割）
    too_long, still_in_band = [], []
    for nar, t, no in typed:
        L = nar_len(nar)
        if L >= 51:
            too_long.append(f'{no}({L}字)')
        elif L >= 26 and t == '静止画':
            still_in_band.append(f'{no}({L}字)')
    if too_long:
        warns.append(f'ナレーション51字以上 {len(too_long)}件（タイプを決める前に分割する）: {", ".join(too_long)}')
    if still_in_band:
        warns.append(f'26〜50字なのに静止画 {len(still_in_band)}件（この帯はキャラアニメ/動画/Earthのみ。分割するか動画に変える）: {", ".join(still_in_band)}')

    # 27) Google Flow動画プロンプトの総数（上限60本・2026-08-21にユーザー指定で12→20→40へ変更）
    #     根拠は実測: 朱鞠内湖96本(242中40%)/星野道夫20本(227中9%)/羅臼岳16本(151中11%)
    flow_n = text.count('Google Flow動画プロンプト')
    if flow_n > 60:
        warns.append(f'Google Flow動画プロンプトが{flow_n}本（上限60本を超過。動きが核心のカットだけに絞る）')
    else:
        info.append(f'Google Flow動画 {flow_n}本 / 上限60本')

    # 28) 素材カテゴリの内訳（1本で4カテゴリ以上使う）
    from collections import Counter
    mix = Counter(t for _, t, _ in typed if t)
    if mix:
        info.append('タイプ内訳: ' + ' / '.join(f'{k}{v}' for k, v in mix.most_common()))
        if len(typed) >= 50 and len([k for k in mix if k != 'その他']) < 4:
            warns.append(f'素材カテゴリが{len(mix)}種類（1本で4カテゴリ以上使う＝mass-produced判定の回避）')

    # 29) 秋の指定があるのに no snow が無い（10月/late Octoberは雪化しやすい）
    nosnow = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if re.search(r'late October|October|autumn|late autumn', b, re.I) \
               and not re.search(r'no snow|not winter|no winter', b, re.I):
                nosnow.append(asset_no(seg))
                break
    if nosnow:
        warns.append(f'秋指定なのに no snow なし {len(nosnow)}件（10月+overcastは雪景色化する→No snow anywhere, no frost, no winter を明記）: {", ".join(dict.fromkeys(nosnow))}')

    # 30) 暗いシーン指定に明度の下限がない（黒つぶれ。rule18の拡張版）
    #     ※「dark brown fur」等の“色の形容詞”は対象外。暗い『場』を指す表現だけを拾う
    DARKSCENE = re.compile(
        r'pre-dawn|before dawn|before sunrise|at night|by night|darkness|unlit|'
        r'\bdim(ly)?\b|deep shadow|in shadow|shadowed but|'
        r'dark (room|interior|hallway|corridor|background|backdrop|sky|water|street|forest|thicket|gap|mouth|opening|charcoal|slate)',
        re.I)
    darkish = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if DARKSCENE.search(b) \
               and not re.search(r'NOT pure black|not pure black|clearly readable|clearly visible|high-contrast', b, re.I):
                darkish.append(asset_no(seg))
                break
    if darkish:
        warns.append(f'暗いシーンに明度の下限指定なし {len(darkish)}件（黒一色に沈む→NOT pure black＋主要素をclearly readableと明示）: {", ".join(dict.fromkeys(darkish))}')

    # 31) 実在機関を示す語があるのに打ち消し指定がない（実在施設の偽映像を作らないため）
    REALORG = re.compile(r'\b(university|hospital|ministry|city hall|municipal|government (office|building)|police station|fire (department|headquarters)|air-ambulance)\b', re.I)
    NEGORG  = re.compile(r'no (institution|university|hospital|building|ministry|organization|municipal) name|no logo|no crest|no emblem|no signage|matching no specific', re.I)
    org = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if REALORG.search(b) and not NEGORG.search(b):
                org.append(asset_no(seg))
                break
    if org:
        warns.append(f'実在機関を示す語に打ち消し指定なし {len(org)}件（実在施設の偽映像になる→no institution name/no crest/no signage を明記し、名称はテロップで出す）: {", ".join(dict.fromkeys(org))}')

    # 32) クマの攻撃・威嚇カットに凶暴さの描写がない（2026-08-26 ユーザー指定で恒久化）
    #     毎回「凶暴さが足りない」と差し戻されていたため、指摘される前に入れる定型を機械化した。
    #     採食・逃走・遠景・死骸など「凶暴であってはならないカット」は除外する（一律凶暴化は演出を壊す）。
    BEAR = re.compile(r'\b(bear|moon bear|ursus)\b', re.I)
    # 「no bear」「no animals」等の打ち消しだけの言及は対象外（2026-08-28 ASSET-141の誤検出で追加）
    AGGRO_CTX = re.compile(
        r'charg|attack|lunge|pounce|mid-run|rush|snarl|roar|menac|threat|'
        r'head-on|at the lens|confront|stare|glare|'
        r'emerg|bursts|fills most of the frame', re.I)
    CALM_CTX = re.compile(
        r'seen from directly behind|escap|away from the (lot|scene|camera)|'
        r'forag|feeding|eating|grazing|acorn|beech nut|'
        r'carcass|culled|sedated|tranquil|box trap|cage|'
        r'walking calmly|resting|asleep|silhouette|'
        r'cub|playful|thriving|tumbling|family|mother bear with|'
        r'far in the (back|distance)|small and distant', re.I)
    FEROCITY = [
        r'fang', r'bared', r'snarl', r'gums', r'saliva',
        r'bristl', r'hackle', r'ferocious', r'enraged', r'creased',
        r'ears (pinned|laid back|flat)', r'claws (spread|fully extended|extended)',
        r'teeth', r'jaws (wide open|wrenched|parted)',
    ]
    # カートゥン用の軽量セット（絵柄と衝突しない範囲。2026-08-28 追加）
    FEROCITY_CARTOON = [r'teeth', r'snarl', r'growl', r'ears (flattened|laid back|pinned|back)',
                        r'bristl|raised ridge|fur .{0,20}raised', r'head (dropped|lowered) low',
                        r'claws (spread|out)', r'furious|ferocious|enraged']
    tame = []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if not BEAR.search(re.sub(r'\bno\s+(bears?|animals?)\b', '', b, flags=re.I)):
                continue
            # カートゥン調のキャラプロンプトは対象外（2026-08-26 ユーザー指定）。
            # 凶暴さを盛るのは実写・フォトリアルのカットだけ。絵柄と衝突して顔が崩れるため。
            is_cartoon = 'Cute cartoon character design' in b
            # カートゥンは牙・歯茎・唾液までは求めないが、軽量セット（口を開けて歯／耳を伏せる／毛を逆立てる／頭を下げる）は必須
            if CALM_CTX.search(b):
                continue
            if not AGGRO_CTX.search(b) and not re.search(r'クマ|熊|ツキノワ', nar or ''):
                continue
            pool = FEROCITY_CARTOON if is_cartoon else FEROCITY
            hits = sum(1 for pat in pool if re.search(pat, b, re.I))
            if hits < 3:
                tame.append(asset_no(seg))
                break
    if tame:
        warns.append(f'クマのカットに凶暴さの描写が不足 {len(tame)}件（毎回差し戻される定番。実写=牙/歯茎/唾液/逆立った毛/伏せた耳/しわ寄せた鼻筋/爪 から3つ以上、カートゥン=口を開けて歯/唸り/耳を伏せる/毛を逆立てる/頭を下げる/爪を開く/furious から3つ以上）: {", ".join(dict.fromkeys(tame))}')

    # 33) クマのサイズ指定がない／種と体格が矛盾している（2026-08-26 ユーザー指定で恒久化）
    #     生成AIは指定がないとクマを一律グリズリー級に描く。台本に実個体のサイズがあればそれを、
    #     無ければ種の標準体格（下記）を必ず書く。ツキノワグマとヒグマでは標準が全く違う。
    #       ツキノワグマ Ursus thibetanus japonicus … 体長 約110〜130cm / 体重 オス約60〜120kg・メス約40〜80kg
    #       ヒグマ（エゾヒグマ）Ursus arctos yesoensis … 体長 約190〜230cm / 体重 オス約150〜400kg・メス約100〜200kg
    SIZE_LEN = re.compile(r'\b\d{2,3}\s?cm\b|\b\d(?:\.\d)?\s?met(?:re|er)s?\b', re.I)
    SIZE_KG  = re.compile(r'\b\d{2,3}\s?kg\b', re.I)
    SP_BLACK = re.compile(r'asian black bear|asiatic black bear|moon bear|thibetanus', re.I)
    SP_BROWN = re.compile(r'brown bear|grizzly|ursus arctos|yesoensis', re.I)
    nosize, mism = [], []
    for nar, seg in segs:
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if not BEAR.search(re.sub(r'\bno\s+(bears?|animals?)\b', '', b, flags=re.I)):
                continue
            no = asset_no(seg)
            if not (SIZE_LEN.search(b) or SIZE_KG.search(b)):
                nosize.append(no)
            # 種が黒（ツキノワ）なのにヒグマ級の数値を書いていないか
            if SP_BLACK.search(b) and not SP_BROWN.search(b):
                kgs = [int(x) for x in re.findall(r'\b(\d{2,3})\s?kg\b', b, re.I)]
                cms = [int(x) for x in re.findall(r'\b(\d{2,3})\s?cm\b', b, re.I)]
                mtr = [float(x) for x in re.findall(r'\b(\d(?:\.\d)?)\s?met(?:re|er)s?\b', b, re.I)]
                if any(k > 150 for k in kgs) or any(c > 160 for c in cms) or any(m > 1.6 for m in mtr):
                    mism.append(no)
            break
    if nosize:
        warns.append(f'クマにサイズ指定なし {len(nosize)}件（無指定だとグリズリー級に描かれる→体長と体重を必ず明記。台本に実個体の数値があればそれを、無ければ種の標準を使う。ツキノワグマ=体長約110〜130cm/メス約40〜80kg・オス約60〜120kg、ヒグマ=体長約190〜230cm/メス約100〜200kg・オス約150〜400kg）: {", ".join(dict.fromkeys(nosize))}')
    if mism:
        warns.append(f'ツキノワグマなのにヒグマ級の体格 {len(mism)}件（種と数値が矛盾。ツキノワグマは体長160cm・体重150kgを超えない）: {", ".join(dict.fromkeys(mism))}')

    # 34) クマが死ぬカットの表現を統一する（2026-08-28 ユーザー指定で恒久化）
    #     仰向け・腹を上・脚が宙に浮く は人間の寝姿勢で、四足動物として破綻する（実測）。
    #     うつ伏せ（PRONE）＋四肢を地面に伸ばす＋目はバツ印、が確定形。
    DEATH_NAR = re.compile(r'動かなくなり|動かなくなっ|息絶え|絶命|事切れ|仕留め')
    BEAR_NAR  = re.compile(r'クマ|熊|ツキノワ')
    dead = []
    for nar, seg in segs:
        n = nar or ''
        if not (DEATH_NAR.search(n) and BEAR_NAR.search(n)):
            continue
        for b in re.findall(r'```\n?(.*?)\n?```', seg, re.S):
            if not BEAR.search(re.sub(r'no\s+(bears?|animals?)', '', b, flags=re.I)):
                continue
            has_prone = re.search(r'\bprone\b|flat on (her|his|its) belly|lying face-down', b, re.I)
            has_x     = re.search(r'X MARKS?|X-mark|cross(ed)? (straight )?lines', b, re.I)
            if not (has_prone and has_x):
                dead.append(asset_no(seg))
            break
    if dead:
        warns.append(f'クマの死亡カットが確定形になっていない {len(dead)}件（仰向けは人間ポーズに化ける→うつ伏せPRONE＋四肢を地面に伸ばす＋目はバツ印。詳細はASSET_CHECKLIST「クマ専用ルール⑤」）: {", ".join(dict.fromkeys(dead))}')

    info.append(f'プロンプトlint(14-34): {len(segs)}セグメント走査')

def main(master_path, daihon_path):
    m = open(master_path, encoding='utf-8').read()
    src = [l.strip() for l in open(daihon_path, encoding='utf-8') if l.strip()]
    lines = m.split('\n')
    errors, warns, info = [], [], []

    # 1) 本文完全一致（順序・重複・改変）
    nar = [re.sub(r'^ナレーター:\s*', '', l).rstrip() for l in lines if l.startswith('ナレーター:')]
    if src != nar:
        errors.append(f'本文不一致: 台本{len(src)}行 vs Master{len(nar)}行')
        for i, (a, b) in enumerate(zip(src, nar)):
            if a != b:
                errors.append(f'  最初の不一致 行{i}: 台本「{a[:30]}」≠ Master「{b[:30]}」'); break
    else:
        info.append(f'本文完全一致 {len(nar)}行')

    # 2) 1ナレ行=1制作メモ
    memo = sum(1 for l in lines if l.startswith('【制作メモ】'))
    if memo != len(nar):
        errors.append(f'1ナレ行=1メモ違反: メモ{memo} vs ナレ{len(nar)}')
    else:
        info.append(f'1ナレ行=1メモ {memo}')

    # 3) アセットタイプ（3種+黒カード+実写のみ。背景静止画/図解の単独禁止）
    tag_counts = {}
    for t in ['キャラアニメーション', 'Lovart動画', 'Google Earth', '画面エフェクト', '実写', '背景静止画', '図解', 'AI動画']:
        tag_counts[t] = len(re.findall(r'-\s*【' + t, m))
    if tag_counts['背景静止画'] > 0:
        errors.append(f'背景静止画の単独アセット {tag_counts["背景静止画"]}件（禁止→Lovart動画かキャラに）')
    if tag_counts['図解'] > 0:
        errors.append(f'図解の単独アセット {tag_counts["図解"]}件（禁止→実景に編集者指示で重ねる）')
    info.append('タイプ内訳: ' + ' / '.join(f'{k}{v}' for k, v in tag_counts.items() if v))

    # 4) コードフェンス整合
    if m.count('```') % 2 != 0:
        errors.append('コードフェンス奇数（```の対応崩れ）')

    # 5) 生成枚数（1枚＝Generate N separate images を書かない）
    g = len(re.findall(r'Generate \d+ separate', m))
    if g > 0:
        errors.append(f'「Generate N separate images」が{g}件残存（1枚生成なら削除）')

    # 5b) 日本語文字ぼかしの逃げ（掲示/看板/書類は実文字を描き【chatGPT推奨】を付ける。免許証等の個人情報のみ例外）
    tb = re.findall(r'(文字はぼかす|Japanese text softly blurred|text columns softly blurred|blurred Japanese text|with blurred text)', m)
    if tb:
        warns.append(f'日本語文字ぼかし {len(tb)}件（掲示/書類は実文字を描く＋ラベルに【chatGPT推奨】。免許証等の個人情報のみ例外）')

    # 6) Google Earth 座標必須
    ge = re.findall(r'- 【Google Earth】.*?(?=\n\nナレーター|\n## |\Z)', m, re.S)
    no_coord = [b for b in ge if '座標' not in b]
    if no_coord:
        errors.append(f'Google Earth座標欠落 {len(no_coord)}件')
    else:
        info.append(f'Google Earth {len(ge)}件 全座標あり')

    # 7) キャラプロンプトに環境語（白背景・環境なし）
    cp = re.findall(r'キャラプロンプト（1:1）:\s*\n```\n(.*?)\n```', m, re.S)
    scene = ['window', 'lakeshore', ' shore', 'riverbank', ' boat ', 'boat,', 'forest', 'bushes', ' trail', 'tundra', ' river ', 'wading']
    badcp = [b[:60] for b in cp if any(w in b.lower() for w in scene)]
    if badcp:
        errors.append(f'キャラプロンプトに環境語混入 {len(badcp)}件（白背景・環境なしに）')

    # 8) 背景使い回し（BGプリセット参照＝新規固有背景の原則違反の疑い）
    reuse = len(re.findall(r'背景プロンプト（16:9）:\s*BG-[A-Z]', m))
    if reuse > 0:
        warns.append(f'BGプリセット参照 {reuse}件（羅臼岳標準は毎回固有。使い回し過多に注意）')

    # 9) 動画比率（羅臼岳=約26%。少なすぎ注意）
    flow = m.count('Google Flow動画プロンプト')
    ratio = flow / len(nar) * 100 if nar else 0
    info.append(f'動画(Google Flow) {flow}本 = 全体の{ratio:.0f}%')
    if ratio < 20:
        warns.append(f'動画比率{ratio:.0f}%が低い（羅臼岳は約26%。動きで見せる動画を増やす）')

    # 10) 冒頭=実写 / 末尾=AI動画
    body_after = m[m.find('<!-- PART: KI -->'):] if '<!-- PART: KI -->' in m else m
    first_memo = body_after.split('【制作メモ】', 1)[-1][:200] if '【制作メモ】' in body_after else ''
    if '【実写】' not in first_memo:
        warns.append('冒頭アセットが実写でない可能性（フックは実写）')
    tail = m[m.rfind('## §'):] if '## §' in m else m
    last2 = tail.rsplit('ナレーター:', 2)
    if len(last2) >= 2 and '【Lovart動画】' not in last2[-1] and '【AI動画】' not in last2[-1]:
        warns.append('末尾（視聴御礼）がAI動画でない可能性（末尾は必ず動画）')

    # 11/12) 文字が写る「静止画/背景」画像プロンプトのみを対象に、実文字指定/no text 強制＋【chatGPT推奨】必須
    #   （Google Flow動画プロンプト=映像は静止画を動かすだけなので対象外。実写アセットも対象外）
    TEXTOBJ = re.compile(r"warning sign|bear-warning|beware of|notice board|\bnotice\b|rules board|information board|newspaper|statement document|\bdocument\b|driver's licen[sc]e|licen[sc]e|signboard|placard|\bposter\b|headline|nameplate|plaque|certificate", re.I)
    LITERAL = re.compile(r"'[^']*[一-龠ぁ-んァ-ヴー々〇]+[^']*'|「[^」]+」")  # 単一引用符内に日本語を含む(reading/headed問わず)＝実文字指定とみなす
    NOTEXT  = re.compile(r"no text|no legible text|\bblank\b|not legible|blurred|unreadable", re.I)  # blurred/unreadable=個人情報の意図的非可読(遺族配慮)を許容。文字ぼかしの逃げは別途5bが捕捉
    ENGSIGN = re.compile(r'"[A-Za-z][A-Za-z ]+"\s*(?:warning\s+)?sign', re.I)
    unspoken, engs, missing_gpt = [], [], 0
    for mo in re.finditer(r'(- [^\n]*プロンプト[^\n]*:)\n```\n(.*?)\n?```', m, re.S):
        label, b = mo.group(1), mo.group(2)
        if 'no written words' in b or 'Cute cartoon character design' in b:  # キャラ立ち絵は文字/環境を持たない規則→除外（"notice"=動詞の誤検出も回避）
            continue
        if ENGSIGN.search(b):
            engs.append(b[:48])
        if TEXTOBJ.search(b) and not NOTEXT.search(b) and not LITERAL.search(b):
            unspoken.append(b[:48])
        if LITERAL.search(b) and '【chatGPT推奨】' not in label:
            missing_gpt += 1
    if engs:
        errors.append(f'看板が英語概念のまま {len(engs)}件（"beware of bears"等→画面の実文字「クマ出没注意」等を指定）')
    if unspoken:
        warns.append(f'文字要素だが実文字/no text未指定 {len(unspoken)}件（掲示/書類/新聞は描かせる文字を明記・出さないなら no text・実在物は実写）: 例「{unspoken[0]}...」')
    if missing_gpt:
        warns.append(f'実文字プロンプトなのに【chatGPT推奨】なし {missing_gpt}件（静止画/背景ラベル冒頭に付与）')

    # 13) Master.mdの各制作メモにASSET番号併記（Asset_Prompts.mdと突き合わせ用）
    memo_all = [l for l in lines if l.startswith('【制作メモ】')]
    numbered = [l for l in memo_all if l.startswith('【制作メモ】ASSET-')]
    if memo_all and len(numbered) != len(memo_all):
        warns.append(f'制作メモのASSET番号併記が不足 {len(memo_all)-len(numbered)}件（全メモに ASSET-NNN を付ける）')

    # 14-20) 生成失敗パターン+ナレ行整合のlint
    prompt_lint(m, errors, warns, info)

    # ---- 出力 ----
    print('=' * 60)
    for s in info: print('  INFO :', s)
    for s in warns: print('  WARN ⚠:', s)
    for s in errors: print('  FAIL ❌:', s)
    print('=' * 60)
    if errors:
        print(f'❌ NG: {len(errors)}件のエラー / {len(warns)}件の警告 → 修正してから提示すること')
        return 1
    print(f'✅ 全チェックPASS（警告{len(warns)}件）。提示可能。')
    return 0

def main_prompts_only(path):
    text = open(path, encoding='utf-8').read()
    errors, warns, info = [], [], []
    prompt_lint(text, errors, warns, info)
    print('=' * 60)
    for s in info: print('  INFO :', s)
    for s in warns: print('  WARN ⚠:', s)
    for s in errors: print('  FAIL ❌:', s)
    print('=' * 60)
    if errors:
        print(f'❌ NG: {len(errors)}件のエラー / {len(warns)}件の警告 → 修正してから提示すること')
        return 1
    print(f'✅ プロンプトlint PASS（警告{len(warns)}件）。')
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--prompts':
        sys.exit(main_prompts_only(sys.argv[2]))
    if len(sys.argv) != 3:
        print('usage: python3 validate_phase2_assets.py <Master.md> <台本.txt>\n'
              '       python3 validate_phase2_assets.py --prompts <任意の.md>'); sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
