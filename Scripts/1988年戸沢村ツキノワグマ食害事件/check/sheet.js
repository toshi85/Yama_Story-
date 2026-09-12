// 検収シート（check/sheet.html）の動き。visual_check.py がこのファイルを check/ へ複製する。
// ⚠️ Python の文字列の中に JS を書くと、\n の扱いで3回も文法エラーを出した。だから別ファイルにしてある。
//    変えたら `node --check sheet.js` が通ること（visual_check.py が自動で検査する）。
// 期待する前提: 直前の <script> で `const V = "<動画の相対パス>";` が定義されている。
// 変更の記録は CHANGELOG.md（道具）と overrides.json の history（カットごと）。

const KEY = 'notes:' + V;
const OKEY = 'overrides:' + V;
const DKEY = 'done:' + V;
let notes = {};
let timeNotes = [];
let overrides = {};
let doneSet = {};
try { notes = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) {}
try { overrides = JSON.parse(localStorage.getItem(OKEY) || '{}'); } catch (e) {}
try { doneSet = JSON.parse(localStorage.getItem(DKEY) || '{}'); } catch (e) {}

// 動きの型（render.py の character_overlay_filter と同じ名前）
const MOTIONS = [
  ['path', '開始 → 終了 へ動く（半透明のキャラが終わりの場所）'],
  ['still', '静止'], ['drift_x', '横へすっと'], ['drift_diag', '斜めへ'],
  ['walk_cross', '横切る'], ['breathe', '呼吸（上下・小さい）'], ['lean', '小さく揺れる'], ['step_back', '後ずさり'],
  ['slide_left', '右から左へ横切る'], ['slide_right', '左から右へ横切る'], ['approach', '奥から手前へ'],
  ['shake', '小刻みに震える'], ['jump', '跳ねる'], ['zoom_in', 'ゆっくり寄る'],
];
const MOTION_NAME = Object.fromEntries(MOTIONS);
const ANIMS = [['fade', 'フェード'], ['slide_left', '右から入る'], ['slide_right', '左から入る'], ['slide_up', '下から入る'], ['pop', 'ポップ'], ['none', 'なし']];
const SHAPES = ['矢印_右', '矢印_左', '矢印_上', '矢印_下', '丸', '枠', 'ピン', '線_赤', 'ハイライト'];
const S = 0.5;               // 1280x720 → プレビュー 640x360
const pad4 = id => String(id).padStart(4, '0');
const FIELD_NAMES = {
  narration: '字幕本文', duration_sec: 'カット尺', asset_file: '素材ファイル', asset_kind: '素材形式', material_category: '素材区分',
  motion: '動き', amount: '動きの量', move_sec: '動く時間', bubble_side: '吹き出しの向き', speech: 'セリフ', telop: 'テロップ',
  map_zoom: '地形図の寄り', map_heading: '地形図の向き', map_pitch: '地形図の傾き',
  base_x: '開始位置(横)', base_y: '開始位置(縦)', drift: '移動量', bubble_dx: '吹き出し(横)', bubble_dy: '吹き出し(縦)',
  scale: '大きさ', flip: '左右反転', overlays: '挿入', bubble_delay: '吹き出しを出す秒',
  bubble_text_dx: '吹き出しの文字(横)', bubble_text_dy: '吹き出しの文字(縦)', map_pins: '地形図のピン',
};

// コマをクリック → そのカットだけを切り出した mp4（check/clips/NNNN.mp4）を、その行に出して再生
function play(id, t0, t1) {
  const row = document.getElementById('c' + id);
  const old = document.querySelector('video.cut');
  if (old) { old.pause(); old.remove(); }
  const v = document.createElement('video');
  v.className = 'cut'; v.controls = true; v.width = 480; v.playsInline = true;
  v.preload = 'auto';
  v.src = 'clips/' + pad4(id) + '.mp4';
  row.insertBefore(v, row.children[4]);
  // 🚨 2026-09-04: autoplay 属性だけに任せていたので、Chrome の自動再生制限で
  //    止まったまま（readyState 0 / paused）になっていた。クリックの流れの中で
  //    play() を呼び、断られたら消音でもう一度試す。
  v.play().catch(() => {
    v.muted = true;
    v.play().catch(err => {
      const p = document.createElement('div');
      p.style.cssText = 'color:#ff7b72;font-size:12px';
      p.textContent = '再生できませんでした（' + (err && err.name) + '）。再生ボタンを押してください';
      v.after(p);
    });
  });
  v.addEventListener('error', () => {
    const p = document.createElement('div');
    p.style.cssText = 'color:#ff7b72;font-size:12px';
    p.textContent = '動画を読めませんでした: clips/' + pad4(id) + '.mp4';
    v.after(p);
  });
}

// ---- 手で直す ----
const ED = {};   // id → 編集中の状態
// 🚨 2026-09-11: 「http でなければファイルとして開いている」と判定していたため、
//    Tailscale 経由（https）で開くと試写プレーヤーも保存も送信も止まった。
//    サーバー経由かどうかは http と https の両方で真になる。
function servedByServer() {
  return location.protocol === 'http:' || location.protocol === 'https:';
}

let CUR = null;  // 開いているパネルの id

// textarea の中身用。属性値と違って & と < も潰さないと壊れる。
function escText(t) {
  return String(t == null ? '' : t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function num(v, d) { const n = parseFloat(v); return isNaN(n) ? d : n; }
const charRows = () => [...document.querySelectorAll('.r[data-kind="character"]')].map(r => +r.id.slice(1));

async function replaceCutImage(id, input) {
  const file = input.files[0]; if (!file) return;
  try {
    const data = await new Promise((resolve, reject) => { const r = new FileReader(); r.onload = () => resolve(r.result); r.onerror = reject; r.readAsDataURL(file); });
    const response = await fetch('/upload', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name: Date.now() + '_' + file.name, data})});
    const result = await response.json();
    if (!response.ok || !result.ok) throw new Error(result.error || 'アップロードに失敗');
    document.getElementById('af' + id).value = result.file;
    const kind = document.getElementById('ak' + id); if (kind) kind.value = 'image';
    pushUndo(id);
  } catch (error) { alert(error.message); }
}

function rowDefaults(id) {
  const d = document.getElementById('c' + id).dataset;
  const drift = d.drift ? d.drift.split(',').map(Number) : [0, 0];
  let ovl = [];
  try { ovl = JSON.parse(d.overlays || '[]'); } catch (e) {}
  return {
    narration: d.narration || '', duration_sec: num(d.dur, 21.5), asset_file: d.source || '', asset_kind: d.kind || 'image', material_category: d.category || '背景',
    motion: d.motion || 'path', amount: num(d.amount, 1), move_sec: num(d.movesec, 2.4), bubble_side: d.bubble || '',
    speech: d.speechText || '', telop: d.telop || '', map_zoom: d.mapzoom || '',
    map_heading: d.mapheading === '' || d.mapheading === undefined ? null : num(d.mapheading, null),
    map_pitch: d.mappitch === '' || d.mappitch === undefined ? 0 : num(d.mappitch, 0),
    base_x: num(d.basex, 0), base_y: num(d.basey, 0), drift: [drift[0] || 0, drift[1] || 0],
    bubble_dx: num(d.bdx, 0), bubble_dy: num(d.bdy, 0), scale: num(d.scale, 1), flip: d.flip === '1',
    overlays: ovl, dur: num(d.dur, 5), bubble_delay: num(d.bdelay, 0.5),
    bubble_text_dx: num(d.btdx, 0), bubble_text_dy: num(d.btdy, 0), map_pins: {},
  };
}
function effective(id) {          // 行の既定値に、保存済みの手直しを重ねたもの
  const o = overrides[id] || {};
  const base = rowDefaults(id);
  const out = Object.assign({}, base);
  if (o.reset && document.getElementById('c' + id).dataset.profile === 'jinruishi') {
    const d = document.getElementById('c' + id).dataset;
    let original = null; try { original = JSON.parse(d.original || 'null'); } catch (e) {}
    if (original) Object.assign(out, original.fields, {duration_sec: original.frames / num(d.fps, 30), telop: (original.fields.telops || []).join(' ')});
    return out;
  }
  for (const k of Object.keys(FIELD_NAMES)) if (o[k] !== undefined && o[k] !== null) out[k] = o[k];
  // 経路つきの動きは motion_path.duration が実際に効く秒数なので、
  // 「動く時間」のスライダーにはそちらを出す（違う数字を見せない）。
  if (o.motion_path && Number.isFinite(Number(o.motion_path.duration))) {
    out.move_sec = Number(o.motion_path.duration);
  }
  return out;
}

async function openEditor(id) {
  const row = document.getElementById('c' + id);
  const old = document.getElementById('ed' + id);
  if (old) { old.remove(); delete ED[id]; CUR = null; return; }
  // 開いているパネルは1つだけ（前のカットの拡大が残らないように）
  document.querySelectorAll('.edbox').forEach(b => b.remove());
  Object.keys(ED).forEach(k => delete ED[k]);
  const pv = document.querySelector('video.cut'); if (pv) { pv.pause(); pv.remove(); }
  CUR = id;
  const d = row.dataset;
  const isChar = d.kind === 'character';
  const isMap = d.map === '1';
  const e = effective(id);
  const st = ED[id] = {
    baseX: e.base_x, baseY: e.base_y, dx: e.drift[0], dy: e.drift[1], bdx: e.bubble_dx, bdy: e.bubble_dy,
    scale: e.scale, flip: e.flip, mode: 'start', meta: null, undo: [], redo: [], isChar,
    overlays: JSON.parse(JSON.stringify(e.overlays || [])), dur: e.dur, selOv: -1,
    // 経路の中間地点（1280x720 の人物中心）。保存済みの経路があればそれを引き継ぐ。
    mids: (((overrides[id] || {}).motion_path || {}).midpoints || []).map(p => [p[0], p[1]]),
    selMid: -1,
  };
  const esc = t => String(t).replace(/"/g, '&quot;');

  let ctl = '<div class=edctl>';
  if (d.profile === 'jinruishi') {
    ctl += '<label>素材区分 <select id="cat' + id + '">' + ['カヤ','犬','背景','図解'].map(c => '<option' + (c === e.material_category ? ' selected' : '') + '>' + c + '</option>').join('') + '</select></label>';
    ctl += '<label>字幕本文<textarea id="nar' + id + '" style="width:100%;min-height:90px">' + String(e.narration).replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</textarea></label>';
    ctl += '<label>カット尺（秒）<input type=number id="dur' + id + '" min=1 max=120 step=0.1 value="' + e.duration_sec + '"' + (d.timing !== 'estimated' ? ' disabled' : '') + '></label>';
    ctl += '<label>素材ファイル<input id="af' + id + '" value="' + esc(e.asset_file) + '" style="width:100%"></label>';
    ctl += '<label>素材の種類<select id="ak' + id + '">' + [['image','静止画'],['video','動画']].map(k => '<option value="' + k[0] + '"' + (k[0] === e.asset_kind ? ' selected' : '') + '>' + k[1] + '</option>').join('') + '</select></label>';
    ctl += '<label>画像を差し替える<input type=file accept="image/*" onchange="replaceCutImage(' + id + ',this)"></label>';
    if (!isChar) ctl += '<label>画面の動き<select id="mo' + id + '">' + [['still','静止'],['zoom_in','ゆっくり寄る'],['zoom_out','ゆっくり引く'],['pan_left','緩い左パン'],['pan_right','緩い右パン']].map(m => '<option value="' + m[0] + '"' + (e.motion === m[0] ? ' selected' : '') + '>' + m[1] + '</option>').join('') + '</select></label>';
  }
  ctl += '<div class=rowbtns>' +
    '<button class="primary big" onclick="previewCut(' + id + ')" id="pvb' + id + '">▶ プレビュー</button>' +
    '<button onclick="undoEd(' + id + ')" title="⌘Z">↶ 元に戻す</button>' +
    '<button onclick="redoEd(' + id + ')" title="⇧⌘Z">↷ やり直す</button>' +
    '<label class=hint><input type=checkbox id="gd' + id + '" checked onchange="toggleGuides(' + id + ')"> ガイド線</label></div>';
  if (isChar) {
    ctl += '<label>動き <select id="mo' + id + '">' +
      MOTIONS.map(m => '<option value="' + m[0] + '"' + (e.motion === m[0] ? ' selected' : '') + '>' + m[1] + '</option>').join('') +
      '</select></label>';
    ctl += '<label>動く時間 <input type=range id="sc' + id + '" min=0.4 max=4 step=0.1 value="' + e.move_sec + '"> <span id="scv' + id + '">' + e.move_sec + '秒</span></label>';
    ctl += '<label>動きの量 <input type=range id="am' + id + '" min=0 max=2 step=0.1 value="' + e.amount + '"> <span id="amv' + id + '">' + e.amount + '</span></label>';
    ctl += '<label>大きさ <input type=range id="sz' + id + '" min=0.5 max=1.6 step=0.05 value="' + e.scale + '"> <span id="szv' + id + '">' + e.scale + '倍</span>' +
           ' <label class=hint><input type=checkbox id="fl' + id + '"' + (e.flip ? ' checked' : '') + '> 左右反転</label></label>';
    if (d.speech === '1' || e.speech) {
      ctl += '<label>吹き出しの向き <select id="bs' + id + '">' +
        [['', '自動'], ['left', '頭の左'], ['right', '頭の右'], ['top', '頭の上']]
          .map(o => '<option value="' + o[0] + '"' + (e.bubble_side === o[0] ? ' selected' : '') + '>' + o[1] + '</option>').join('') +
        '</select></label>';
    }
    // 2026-09-10: <input> は改行を打てないので <textarea> に。
    //   render.py の _bubble_lines は改行があれば自動の折り返しより優先する作りで、
    //   吹き出しの行割りを手で決められる。入れ物だけが追いついていなかった。
    ctl += '<label>セリフ <textarea id="sp' + id + '" rows=2 style="width:200px;resize:vertical"' +
           ' placeholder="空なら吹き出し無し／改行するとそこで行が変わります">' + escText(e.speech) + '</textarea>' +
           '<button id="spins' + id + '" onclick="insertSpeech(' + id + ')">吹き出しを入れる</button>' +
           '<span class=hint>入れると画面に吹き出しが出て、ドラッグで位置を直せます。改行した所で行が変わります</span></label>';
    ctl += '<label>中間地点（経路の途中で通る場所）' +
           '<button onclick="addMid(' + id + ')">＋足す</button>' +
           '<button onclick="delMid(' + id + ')">選んだ点を消す</button>' +
           '<span class=hint id="midn' + id + '"></span>' +
           '<span class=hint>点をドラッグで移動／クリックで選ぶ（Delete でも消せる）。動きが「開始→終了へ動く」のときだけ効きます</span></label>';
    ctl += '<label>吹き出しを出す <input type=range id="bd' + id + '" min=0 max="' + Math.max(0.5, Math.round((e.dur - 0.3) * 10) / 10) + '" step=0.1 value="' + e.bubble_delay + '"> <span id="bdv' + id + '">' + (e.bubble_delay > 0 ? e.bubble_delay + '秒後' : '最初から') + '</span></label>';
    ctl += '<label class=hint>吹き出しの文字の位置 横<input type=number id="btx' + id + '" value="' + e.bubble_text_dx + '" step=1 style="width:60px">px 縦<input type=number id="bty' + id + '" value="' + e.bubble_text_dy + '" step=1 style="width:60px">px（プレビューで確認）</label>';
    ctl += '<div class=guide><b>位置の直し方</b><br>' +
      '① 動かしたい絵（キャラ／吹き出し／挿入したもの）を<b>クリックして選ぶ</b>（手のカーソルが出る所）<br>' +
      '② <b>空いている所をクリック</b>すると、選んだ絵がそこへ移動（ドラッグでも動かせる）<br>' +
      '<span class=hint>細かく: 矢印キーで1px（<kbd>⇧</kbd>で10px）。<kbd>⌘Z</kbd>で戻す。' +
      '動きを「開始→終了へ動く」にすると<b>半透明のキャラ</b>が出る＝動き終わりの場所</span></div>';
    ctl += '<div class=rowbtns>' +
      '<button onclick="copyFromPrev(' + id + ')">前のキャラのカットと同じにする</button>' +
      '<button onclick="copyToNext(' + id + ')">次のキャラのカットへコピー</button></div>';
  } else {
    ctl += '<div class=guide><b>位置の直し方</b><br>挿入したテキスト・図形を<b>クリックして選び</b>、空いている所をクリックするとそこへ移動（ドラッグでも可）。矢印キーで1px、<kbd>⌘Z</kbd>で戻す</div>';
  }
  ctl += '<div class=selnow>いま選んでいるもの: <b id="sel' + id + '">' + (isChar ? 'キャラ' : '（なし）') + '</b></div>';
  ctl += '<div id="pos' + id + '" class=hint></div>';
  if (isMap) {
    const hd = e.map_heading === null || e.map_heading === undefined ? '' : e.map_heading;
    // 寄りは高度の倍率（小さいほど寄る）。昔の near/far も読む
    const zmap = { near: 0.55, far: 1.7 };
    const zraw = e.map_zoom;
    const zoomVal = (zraw === '' || zraw === null || zraw === undefined) ? 1
      : (zmap[zraw] !== undefined ? zmap[zraw] : parseFloat(zraw) || 1);
    const zoomLabel = (zraw === '' || zraw === null || zraw === undefined) ? '既定'
      : (Math.round(zoomVal * 100) / 100) + '倍' + (zoomVal < 1 ? '（寄る）' : zoomVal > 1 ? '（引く）' : '');
    ctl += '<div class=guide><b>地形図のカメラ</b>（数値を変えると左の画面にすぐ反映される）<br>' +
      '<label>寄り <input type=range id="mz' + id + '" min=0.3 max=2.5 step=0.05 value="' + zoomVal + '">' +
      ' <span id="mzv' + id + '">' + zoomLabel + '</span>' +
      ' <button onclick="document.getElementById(\'mz' + id + '\').dataset.clear=1;document.getElementById(\'mzv' + id + '\').textContent=\'既定\';document.getElementById(\'mz' + id + '\').dispatchEvent(new Event(\'change\'))">既定に戻す</button></label>' +
      '<label>向き <input type=range id="mh' + id + '" min=0 max=359 step=1 value="' + (hd === '' ? 70 : hd) + '"> <span id="mhv' + id + '">' + (hd === '' ? '既定' : hd + '°') + '</span>' +
      ' <button onclick="document.getElementById(\'mh' + id + '\').dataset.clear=1;document.getElementById(\'mhv' + id + '\').textContent=\'既定\'">既定に戻す</button></label>' +
      '<label>傾き <input type=range id="mp' + id + '" min=-20 max=20 step=1 value="' + (e.map_pitch || 0) + '"> <span id="mpv' + id + '">' + (e.map_pitch || 0) + '°</span></label></div>';
    let pinInfo = [];
    try { pinInfo = JSON.parse(d.pins || '[]'); } catch (e2) {}
    const pins = Array.isArray(pinInfo) ? pinInfo : (pinInfo.pins || []);
    st.pins = pins;
    // ⚠️ 向き0（真北）は正しい値なので `||` で拾わない
  st.mapHeading = (!Array.isArray(pinInfo) && pinInfo.heading !== undefined) ? pinInfo.heading : 70;
    if (pins.length) {
      const mp = e.map_pins || {};
      ctl += '<div class=guide><b>ピンの調整</b>（矢印で前後左右へ150mずつ。数値は南北・東西のメートル。左の画面にすぐ反映）<br>' +
        pins.map((p, i) => {
          const pe = mp[p] || {};
          return '<div class=ovrow>' +
            '<label><input type=checkbox id="ph' + id + '_' + i + '"' + (pe.hide ? '' : ' checked') + '> 表示</label>' +
            '<input id="pl' + id + '_' + i + '" value="' + String(pe.label || p).replace(/"/g, '&quot;') + '" style="width:110px" title="ラベル">' +
            '<span class=pinpad>' +
            '<button onclick="movePin(' + id + ',' + i + ',0,1)" title="奥へ">↑</button>' +
            '<button onclick="movePin(' + id + ',' + i + ',-1,0)" title="左へ">←</button>' +
            '<button onclick="movePin(' + id + ',' + i + ',1,0)" title="右へ">→</button>' +
            '<button onclick="movePin(' + id + ',' + i + ',0,-1)" title="手前へ">↓</button>' +
            '</span>' +
            '<label class=tag>南北<input type=number id="pn' + id + '_' + i + '" value="' + (pe.dn || 0) + '" step=50 style="width:70px">m</label>' +
            '<label class=tag>東西<input type=number id="pe' + id + '_' + i + '" value="' + (pe.de || 0) + '" step=50 style="width:70px">m</label>' +
            '</div>';
        }).join('') + '</div>';
    }
  }
  ctl += '<label>テロップ（左上の白抜き） <input id="tp' + id + '" style="width:220px" value="' + esc(e.telop) + '" placeholder="空なら出さない"></label>';

  // テキスト・画像・図形の挿入
  ctl += '<div class=guide><b>テキスト・画像・図形を足す</b>（位置は上のプレビューでクリック／ドラッグ。出す時間はこのカットの中の秒）<br>' +
    '<div class=rowbtns>' +
    '<button onclick="addOverlay(' + id + ',\'text\')">＋テキスト</button>' +
    '<label><button onclick="document.getElementById(\'up' + id + '\').click()">＋画像（ファイル）</button><input type=file id="up' + id + '" accept="image/*" style="display:none" onchange="uploadImage(' + id + ',this)"></label>' +
    '<select id="shp' + id + '" onchange="addShape(' + id + ')"><option value="">＋図形を選ぶ…</option>' +
    SHAPES.map(n => '<option value="' + n + '">' + n + '</option>').join('') + '</select></div>' +
    '<div class=ovlist id="ovl' + id + '"></div></div>';

  ctl += '<div id="pv' + id + '"></div>';
  ctl += '<div><button class=primary onclick="saveEditor(' + id + ')">この調整を保存</button> ' +
         '<button onclick="resetEditor(' + id + ')">最初の状態に戻す</button></div>';
  ctl += '<div class=hint>保存したら上の「③下書きを作り直す」で反映。何カットでもまとめて保存してから押してよい</div>';
  ctl += '</div>';

  const bgCss = isChar ? 'url(bg/' + pad4(id) + '.jpg),url(frames/' + pad4(id) + '_1.jpg)' : 'url(frames/' + pad4(id) + '_1.jpg)';
  let stage = '<div class=ed id="st' + id + '" style="background-image:' + bgCss + '">' +
              '<div class=guides id="gl' + id + '"><div class=v></div><div class=safe></div><div class=sub></div></div>';
  if (isChar) {
    stage += '<img class=layer id="lyE' + id + '" src="layers/' + pad4(id) + '_char.png" draggable=false style="opacity:.45" title="終了位置">' +
             '<img class=layer id="ly' + id + '" src="layers/' + pad4(id) + '_char.png" draggable=false title="開始位置">' +
             '<img class=layer id="lyB' + id + '" src="layers/' + pad4(id) + '_bub.png" draggable=false title="吹き出し" onerror="this.style.display=\'none\'">';
  }
  if (isChar) stage += '<div id="mids' + id + '"></div>';
  stage += '<div id="ovs' + id + '"></div></div>';

  const box = document.createElement('div');
  box.className = 'edbox'; box.id = 'ed' + id;
  box.innerHTML = stage + ctl;
  row.after(box);

  if (isChar) {
    const am = document.getElementById('am' + id);
    am.addEventListener('input', () => { document.getElementById('amv' + id).textContent = am.value; });
    const sc = document.getElementById('sc' + id);
    sc.addEventListener('input', () => { document.getElementById('scv' + id).textContent = sc.value + '秒'; });
    const sz = document.getElementById('sz' + id);
    sz.addEventListener('input', () => { st.scale = parseFloat(sz.value); document.getElementById('szv' + id).textContent = sz.value + '倍'; placeAll(id); });
    sz.addEventListener('change', () => pushUndo(id));
    const fl = document.getElementById('fl' + id);
    fl.addEventListener('change', () => { st.flip = fl.checked; pushUndo(id); placeAll(id); });
    const bd = document.getElementById('bd' + id);
    bd.addEventListener('input', () => { document.getElementById('bdv' + id).textContent = parseFloat(bd.value) > 0 ? bd.value + '秒後' : '最初から'; });
    const mo = document.getElementById('mo' + id);
    mo.addEventListener('change', () => { pushUndo(id); placeAll(id); });
    try {
      st.meta = await (await fetch('layers/' + pad4(id) + '.json', { cache: 'no-store' })).json();
      // 🚨 2026-09-10: この層は「そのとき効いていた吹き出しのずれ」で作られている。
      //    ずれ0のときの形に戻しておかないと、動かすたびに幅の計算が狂う。
      st.metaBdx = num((overrides[id] || {}).bubble_dx, 0);
      st.metaBdy = num((overrides[id] || {}).bubble_dy, 0);
    } catch (e2) { st.meta = null; }
  } else {
    st.mode = 'none';
  }
  if (isMap) {
    const mz = document.getElementById('mz' + id);
    mz.addEventListener('input', () => {
      delete mz.dataset.clear;
      const v = parseFloat(mz.value);
      document.getElementById('mzv' + id).textContent =
        v + '倍' + (v < 1 ? '（寄る）' : v > 1 ? '（引く）' : '');
    });
    const mh = document.getElementById('mh' + id), mp = document.getElementById('mp' + id);
    mh.addEventListener('input', () => { delete mh.dataset.clear; document.getElementById('mhv' + id).textContent = mh.value + '°'; });
    mp.addEventListener('input', () => { document.getElementById('mpv' + id).textContent = mp.value + '°'; });
    bindMapLive(id);
  }
  renderOverlayList(id);
  setupDrag(id);
  snapshotInit(id);
}

// ---- 元に戻す／やり直す ----
function snap(id) {
  const st = ED[id];
  const mo = document.getElementById('mo' + id);
  return { baseX: st.baseX, baseY: st.baseY, dx: st.dx, dy: st.dy, bdx: st.bdx, bdy: st.bdy, scale: st.scale, flip: st.flip,
           motion: mo ? mo.value : '', fields: Object.fromEntries(['nar','af','ak','cat','dur'].map(k => [k, document.getElementById(k + id)?.value])), overlays: JSON.parse(JSON.stringify(st.overlays || [])) };
}
function applySnap(id, s) {
  const st = ED[id];
  Object.assign(st, { baseX: s.baseX, baseY: s.baseY, dx: s.dx, dy: s.dy, bdx: s.bdx, bdy: s.bdy, scale: s.scale, flip: s.flip,
                      overlays: JSON.parse(JSON.stringify(s.overlays || [])) });
  const mo = document.getElementById('mo' + id); if (mo && s.motion) mo.value = s.motion;
  for (const [key, value] of Object.entries(s.fields || {})) { const el = document.getElementById(key + id); if (el && value !== undefined) el.value = value; }
  const sz = document.getElementById('sz' + id); if (sz) { sz.value = s.scale; document.getElementById('szv' + id).textContent = s.scale + '倍'; }
  const fl = document.getElementById('fl' + id); if (fl) fl.checked = !!s.flip;
  renderOverlayList(id);
  placeAll(id);
}
function snapshotInit(id) {
  ED[id].last = snap(id);
  for (const key of ['nar','af','ak','cat','dur']) { const el = document.getElementById(key + id); if (el) el.addEventListener('change', () => pushUndo(id)); }
}
function pushUndo(id) {
  const st = ED[id]; if (!st) return;
  const now = snap(id);
  if (JSON.stringify(now) === JSON.stringify(st.last)) return;
  st.undo.push(st.last); if (st.undo.length > 50) st.undo.shift();
  st.redo = []; st.last = now;
}
function undoEd(id) { const st = ED[id]; if (!st || !st.undo.length) return; st.redo.push(snap(id)); const s = st.undo.pop(); st.last = s; applySnap(id, s); }
function redoEd(id) { const st = ED[id]; if (!st || !st.redo.length) return; st.undo.push(snap(id)); const s = st.redo.pop(); st.last = s; applySnap(id, s); }

function toggleGuides(id) {
  const g = document.getElementById('gl' + id), c = document.getElementById('gd' + id);
  if (g && c) g.style.display = c.checked ? '' : 'none';
}

// ---- 挿入（テキスト・画像・図形） ----
function addOverlay(id, type, extra) {
  const st = ED[id]; if (!st) return;
  const o = Object.assign({ type, x: 640, y: type === 'text' ? 200 : 360, start: 0, end: Math.round(st.dur * 10) / 10, anim: 'fade' },
    type === 'text' ? { text: 'テキスト', size: 56, color: '#FFFFFF' } : { file: '', w: 320 }, extra || {});
  st.overlays.push(o);
  st.selOv = st.overlays.length - 1; st.mode = 'ov';
  renderOverlayList(id); placeAll(id); pushUndo(id);
  const el = document.getElementById('sel' + id); if (el) el.textContent = ovName(o);
}
function addShape(id) {
  // 選んだ瞬間に足す（ボタンは無し）。選び直せるよう見出しへ戻す
  const sel = document.getElementById('shp' + id);
  const name = sel.value;
  sel.value = '';
  if (!name) return;
  const w = name.startsWith('線') ? 400 : (name === '矢印_上' || name === '矢印_下' || name === 'ピン') ? 100 : 240;
  addOverlay(id, 'image', { file: '挿入/図形/' + name + '.png', w });
}
function uploadImage(id, input) {
  const f = input.files && input.files[0]; if (!f) return;
  const rd = new FileReader();
  rd.onload = async () => {
    try {
      const r = await fetch('/upload', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: f.name, data: rd.result }) });
      const j = await r.json();
      if (!j.ok) { alert('アップロードに失敗'); return; }
      addOverlay(id, 'image', { file: j.file, w: 320 });
    } catch (e) { alert('アップロードに失敗: ' + e); }
    input.value = '';
  };
  rd.readAsDataURL(f);
}
function ovName(o) { return o.type === 'text' ? 'テキスト「' + (o.text || '') + '」' : '画像 ' + (o.file || '').split('/').pop(); }
function removeOverlay(id, i) { const st = ED[id]; st.overlays.splice(i, 1); st.selOv = -1; st.mode = st.isChar ? 'start' : 'none'; renderOverlayList(id); placeAll(id); pushUndo(id); }
function selectOverlay(id, i) { const st = ED[id]; st.selOv = i; st.mode = 'ov'; renderOverlayList(id); placeAll(id); const el = document.getElementById('sel' + id); if (el) el.textContent = ovName(st.overlays[i]); }
function updOverlay(id, i, k, v) {
  const st = ED[id]; const o = st.overlays[i]; if (!o) return;
  if (['size', 'w', 'start', 'end', 'x', 'y'].includes(k)) v = parseFloat(v);
  o[k] = v; placeAll(id); pushUndo(id);
}
function renderOverlayList(id) {
  const st = ED[id]; const box = document.getElementById('ovl' + id); if (!box) return;
  const esc = t => String(t).replace(/"/g, '&quot;');
  box.innerHTML = st.overlays.map((o, i) => {
    const sel = i === st.selOv ? ' sel' : '';
    let h = '<div class="ovrow' + sel + '" onclick="selectOverlay(' + id + ',' + i + ')">';
    h += '<span class=tag>' + (i + 1) + '</span>';
    if (o.type === 'text') {
      h += '<input value="' + esc(o.text) + '" style="width:160px" oninput="updOverlay(' + id + ',' + i + ',\'text\',this.value)" placeholder="文字">';
      h += '<label class=tag>大きさ <input type=number min=16 max=200 value="' + o.size + '" onchange="updOverlay(' + id + ',' + i + ',\'size\',this.value)"></label>';
      h += '<input type=color value="' + (o.color || '#FFFFFF') + '" oninput="updOverlay(' + id + ',' + i + ',\'color\',this.value)">';
    } else {
      h += '<span class=tag>' + (o.file || '').split('/').pop() + '</span>';
      h += '<label class=tag>幅 <input type=number min=40 max=1280 step=10 value="' + o.w + '" onchange="updOverlay(' + id + ',' + i + ',\'w\',this.value)"></label>';
    }
    h += '<label class=tag>出す <input type=number min=0 max="' + st.dur + '" step=0.1 value="' + o.start + '" onchange="updOverlay(' + id + ',' + i + ',\'start\',this.value)">秒〜';
    h += '<input type=number min=0 max="' + st.dur + '" step=0.1 value="' + o.end + '" onchange="updOverlay(' + id + ',' + i + ',\'end\',this.value)">秒</label>';
    h += '<select onchange="updOverlay(' + id + ',' + i + ',\'anim\',this.value)">' + ANIMS.map(a => '<option value="' + a[0] + '"' + (o.anim === a[0] ? ' selected' : '') + '>' + a[1] + '</option>').join('') + '</select>';
    h += '<button onclick="event.stopPropagation();removeOverlay(' + id + ',' + i + ')">削除</button>';
    h += '</div>';
    return h;
  }).join('') || '<span class=hint>（まだ何も足していない）</span>';
}
function placeOverlays(id) {
  const st = ED[id]; const box = document.getElementById('ovs' + id); if (!box) return;
  box.innerHTML = '';
  st.overlays.forEach((o, i) => {
    let el;
    if (o.type === 'text') {
      el = document.createElement('div'); el.className = 'ov text'; el.textContent = o.text || '';
      el.style.fontSize = (o.size * S) + 'px'; el.style.color = o.color || '#fff';
    } else {
      el = document.createElement('img'); el.className = 'ov'; el.src = '../' + o.file; el.style.width = (o.w * S) + 'px';
    }
    if (i === st.selOv) el.classList.add('sel');
    el.style.left = (o.x * S) + 'px'; el.style.top = (o.y * S) + 'px';
    el.dataset.i = i;
    box.appendChild(el);
  });
}

// 描画側の式（2倍空間）: x = (W-w)/2 + base_x (+ dx*ease), y = H - h - 0.10H + base_y (+ dy*ease)
// 🚨 2026-09-10: 吹き出しを動かすと層の幅がその分だけ広がり、層は中央揃えで
//    置かれるので全体が半分だけ逆へ動く。パネルは開いた時点の幅を使い続けて
//    いたため、ドラッグ量の半分がそのままズレになっていた（実測: ずれ+20 で
//    層の幅 506→526、吹き出しは+20 だが中央揃えで全体が10左へ寄る）。
//    レンダラー（build_character_layer）と同じ手順で幅を組み直す。
// 人物本体の中心（層の中の位置）。経路の各点はここが乗る場所。
// char_center は render.py が層と一緒に書き出す。無い古い層は本体の箱の中心で代用する。
function charCenter(st, box) {
  const m = st.meta || {};
  const c = m.char_center;
  if (Array.isArray(c) && c.length === 2) return [box.padL + c[0], box.padT + c[1]];
  return [box.padL + (m.char_w || 396) / 2, box.padT + (m.char_h || 396) / 2];
}

// 画面（1280x720）での人物中心。開始位置＝経路の1点目。
function charCenterOnScreen(id) {
  const st = ED[id]; const g = groupOrigin(id);
  const c = charCenter(st, g.box);
  return [g.gx + c[0] * g.k, g.gy + c[1] * g.k];
}

function layerBox(st) {
  const m = st.meta || { cw: 400, ch: 396, pad_l: 0, pad_t: 0, char_w: 400, char_h: 396 };
  if (!m.bubble) return { cw: m.cw, ch: m.ch, padL: m.pad_l, padT: m.pad_t, bx: 0, by: 0, m };
  // ずれ0のときの形へ戻す（層を作ったときのずれを取り除く）
  const b0x = m.bubble[0] - m.pad_l - num(st.metaBdx, 0);
  const b0y = m.bubble[1] - m.pad_t - num(st.metaBdy, 0);
  const bw = m.bubble[2], bh = m.bubble[3];
  const bx = b0x + st.bdx, by = b0y + st.bdy;
  const left = Math.min(0, bx), top = Math.min(0, by);
  const right = Math.max(m.char_w, bx + bw), bottom = Math.max(m.char_h, by + bh);
  return { cw: right - left, ch: bottom - top, padL: -left, padT: -top,
           bx: bx - left, by: by - top, m };
}

function groupOrigin(id) {
  const st = ED[id];
  const box = layerBox(st);
  const m = box.m;
  const k = st.scale / (st.metaScale || 1);
  const cw = box.cw * k, chh = box.ch * k;
  const gx = (1280 - cw) / 2 + st.baseX / 2;
  const gy = 720 - chh - 72 + st.baseY / 2;
  return { gx, gy, m, k, cw, chh, box };
}

// 中間地点（経路の途中で通る場所）。ドラッグで動かし、選んで Delete で消す。
function placeMids(id) {
  const st = ED[id]; const host = document.getElementById('mids' + id);
  if (!host) return;
  const usePath = (document.getElementById('mo' + id) || {}).value === 'path';
  host.innerHTML = (usePath ? st.mids : []).map((p, i) =>
    '<div class="mid' + (st.selMid === i ? ' sel' : '') + '" data-mid="' + i + '"' +
    ' style="left:' + (p[0] * S) + 'px;top:' + (p[1] * S) + 'px">' + (i + 1) + '</div>').join('');
}

// セリフを入れて吹き出しを画面へ出す（掴めるようにする）。
// 🚨 2026-09-10: もともとセリフの無いカットは吹き出しの層が無く、セリフを打っても
//    画面に何も出ないのでドラッグできなかった。ここで層を作り直して置き換える。
async function insertSpeech(id) {
  const st = ED[id]; if (!st) return;
  const btn = document.getElementById('spins' + id);
  const before = btn ? btn.textContent : '';
  if (btn) { btn.disabled = true; btn.textContent = '作成中…'; }
  rowBusy(id, true, '吹き出しを作っています');
  try {
    const sp = document.getElementById('sp' + id);
    const bs = document.getElementById('bs' + id);
    const btx = document.getElementById('btx' + id), bty = document.getElementById('bty' + id);
    const ov = {
      speech: sp ? sp.value : '',
      bubble_side: bs ? bs.value : '',
      bubble_dx: Math.round(st.bdx), bubble_dy: Math.round(st.bdy),
      scale: st.scale, flip: !!st.flip,
      bubble_text_dx: Math.round(parseFloat(btx && btx.value) || 0),
      bubble_text_dy: Math.round(parseFloat(bty && bty.value) || 0),
    };
    const r = await fetch('/build_layer', { method: 'POST', headers: { 'Content-Type': 'application/json' },
                                            body: JSON.stringify({ id: id, override: ov }) });
    const j = await r.json();
    if (!j.ok) { alert('吹き出しを作れませんでした。\n\n' + (j.error || '')); return; }
    st.meta = j.meta || st.meta;
    st.metaBdx = ov.bubble_dx; st.metaBdy = ov.bubble_dy;
    const t = Date.now();
    for (const [el, suf] of [[document.getElementById('ly' + id), '_char.png'],
                             [document.getElementById('lyE' + id), '_char.png'],
                             [document.getElementById('lyB' + id), '_bub.png']]) {
      if (!el) continue;
      el.style.display = (suf === '_bub.png' && !j.has_bubble) ? 'none' : '';
      el.src = 'layers/' + pad4(id) + suf + '?t=' + t;
    }
    if (j.has_bubble) { st.mode = 'bubble'; const sel = document.getElementById('sel' + id); if (sel) sel.textContent = '吹き出し'; }
    placeAll(id); pushUndo(id);
  } catch (e) { alert('通信できませんでした: ' + e); }
  finally { rowBusy(id, false); if (btn) { btn.disabled = false; btn.textContent = before || '吹き出しを入れる'; } }
}

function addMid(id) {
  const st = ED[id]; if (!st || !st.meta) return;
  const [sx, sy] = charCenterOnScreen(id);
  const ex = sx + st.dx / 2, ey = sy + st.dy / 2;
  // 直前の点と終わりの真ん中に置く（続けて押すと点が増えていく）
  const from = st.mids.length ? st.mids[st.mids.length - 1] : [sx, sy];
  st.mids.push([Math.round((from[0] + ex) / 2), Math.round((from[1] + ey) / 2)]);
  st.selMid = st.mids.length - 1;
  const mo = document.getElementById('mo' + id); if (mo) mo.value = 'path';
  placeAll(id); pushUndo(id);
}

function delMid(id) {
  const st = ED[id]; if (!st || st.selMid < 0) return;
  st.mids.splice(st.selMid, 1); st.selMid = -1;
  placeAll(id); pushUndo(id);
}

function placeAll(id) {
  const st = ED[id]; if (!st) return;
  placeOverlays(id);
  placeMids(id);
  const pos = document.getElementById('pos' + id);
  if (!st.isChar) {
    if (pos && st.mode === 'ov' && st.overlays[st.selOv]) { const o = st.overlays[st.selOv]; pos.textContent = ovName(o) + ' 位置 横' + Math.round(o.x) + ' 縦' + Math.round(o.y) + '（1280x720基準 px）'; }
    return;
  }
  const { gx, gy, m, k, cw, chh, box } = groupOrigin(id);
  const ly = document.getElementById('ly' + id), lyE = document.getElementById('lyE' + id), lyB = document.getElementById('lyB' + id);
  const cwc = (ly.naturalWidth || m.char_w) * k;
  const flipCss = st.flip ? 'scaleX(-1)' : '';
  ly.style.width = (cwc * S) + 'px'; ly.style.transform = flipCss;
  ly.style.left = ((gx + box.padL * k) * S) + 'px';
  ly.style.top = ((gy + box.padT * k) * S) + 'px';
  const mo = document.getElementById('mo' + id);
  const usePath = mo && mo.value === 'path';
  lyE.style.display = usePath ? '' : 'none';
  lyE.style.width = (cwc * S) + 'px'; lyE.style.transform = flipCss;
  lyE.style.left = ((gx + box.padL * k + st.dx / 2) * S) + 'px';
  lyE.style.top = ((gy + box.padT * k + st.dy / 2) * S) + 'px';
  if (lyB && lyB.style.display !== 'none') {
    // 吹き出しは層の中の位置で置く（層の幅は上で組み直してある）
    lyB.style.width = (m.bubble ? m.bubble[2] * k * S : cw * S) + 'px';
    lyB.style.left = ((gx + box.bx * k) * S) + 'px';
    lyB.style.top = ((gy + box.by * k) * S) + 'px';
  }
  if (pos) {
    if (st.mode === 'ov' && st.overlays[st.selOv]) { const o = st.overlays[st.selOv]; pos.textContent = ovName(o) + ' 位置 横' + Math.round(o.x) + ' 縦' + Math.round(o.y); }
    else pos.textContent = '開始 横' + Math.round(st.baseX / 2) + ' 縦' + Math.round(st.baseY / 2) +
      (usePath ? ' ／ 移動 横' + Math.round(st.dx / 2) + ' 縦' + Math.round(st.dy / 2) : '') +
      ' ／ 吹き出しのずれ 横' + Math.round(st.bdx) + ' 縦' + Math.round(st.bdy) + ' ／ 大きさ' + st.scale + '倍（1280x720基準 px）';
  }
}

function moveTo(id, cx, cy) {
  // クリック位置（1x px）へ、選んでいるものの中心を持っていく
  const st = ED[id]; if (!st) return;
  const mode = st.mode || 'start';
  if (mode === 'ov') {
    const o = st.overlays[st.selOv]; if (!o) return;
    o.x = Math.round(cx); o.y = Math.round(cy);
    placeAll(id); pushUndo(id); return;
  }
  if (!st.meta) return;
  const { gx, gy, m, k, cw, chh, box } = groupOrigin(id);
  if (mode === 'start') {
    const targetGx = cx - box.padL * k - m.char_w * k / 2;     // キャラの足元中央をクリック位置へ
    const targetGy = cy - chh;
    st.baseX = (targetGx - (1280 - cw) / 2) * 2;
    st.baseY = (targetGy - (720 - chh - 72)) * 2;
  } else if (mode === 'end') {
    const startCx = gx + box.padL * k + m.char_w * k / 2, startCy = gy + chh;
    st.dx = (cx - startCx) * 2; st.dy = (cy - startCy) * 2;
    const mo = document.getElementById('mo' + id); if (mo) mo.value = 'path';
  } else if (mode === 'bubble' && m.bubble) {
    // ずれを変えると層の幅が変わり、中央揃えの原点 gx も動く。
    // 1回の計算では合わないので、狙った位置に落ちるまで数回詰める。
    const bw = m.bubble[2], bh = m.bubble[3];
    for (let i = 0; i < 40; i++) {
      const g = groupOrigin(id);
      const nowX = g.gx + g.box.bx * g.k + bw * g.k / 2;
      const nowY = g.gy + g.box.by * g.k + bh * g.k / 2;
      if (Math.abs(nowX - cx) < 0.25 && Math.abs(nowY - cy) < 0.25) break;
      st.bdx += (cx - nowX) / g.k;
      st.bdy += (cy - nowY) / g.k;
    }
  }
  placeAll(id);
  pushUndo(id);
}

// 矢印キーで1px（⇧で10px）
function nudge(id, dx, dy) {
  const st = ED[id]; if (!st) return;
  const mode = st.mode || 'start';
  if (mode === 'ov') { const o = st.overlays[st.selOv]; if (!o) return; o.x += dx; o.y += dy; }
  else if (mode === 'start') { st.baseX += dx * 2; st.baseY += dy * 2; }
  else if (mode === 'end') { st.dx += dx * 2; st.dy += dy * 2; }
  else if (mode === 'bubble') { st.bdx += dx; st.bdy += dy; }
  else if (mode === 'mid' && st.mids[st.selMid]) { st.mids[st.selMid][0] += dx; st.mids[st.selMid][1] += dy; }
  else return;
  placeAll(id);
  pushUndo(id);
}

function setupDrag(id) {
  const st = ED[id];
  const stage = document.getElementById('st' + id);
  const els = { bubble: document.getElementById('lyB' + id), start: document.getElementById('ly' + id), end: document.getElementById('lyE' + id) };
  const alphaCache = {};

  // 挿入したもの（矩形）→ 吹き出し → キャラ → 終了位置 の順に当たりを見る。透明な所は当たりにしない
  const hitTest = (px, py) => {
    // 中間地点の丸が最優先（小さいので他より先に拾う）
    for (const el of [...document.querySelectorAll('#mids' + id + ' .mid')].reverse()) {
      const r = el.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      const l = r.left - sr.left, t = r.top - sr.top;
      if (px >= l && px <= l + r.width && py >= t && py <= t + r.height) return 'mid:' + el.dataset.mid;
    }
    const ovEls = [...document.querySelectorAll('#ovs' + id + ' .ov')].reverse();
    for (const el of ovEls) {
      const r = el.getBoundingClientRect(), sr = stage.getBoundingClientRect();
      const l = r.left - sr.left, t = r.top - sr.top;
      if (px >= l && px <= l + r.width && py >= t && py <= t + r.height) return 'ov:' + el.dataset.i;
    }
    for (const name of ['bubble', 'start', 'end']) {
      const el = els[name];
      if (!el || el.style.display === 'none' || !el.naturalWidth) continue;
      const left = parseFloat(el.style.left) || 0, top = parseFloat(el.style.top) || 0;
      const w = parseFloat(el.style.width) || el.naturalWidth * S;
      const scale = w / el.naturalWidth;
      const h = el.naturalHeight * scale;
      if (px < left || py < top || px > left + w || py > top + h) continue;
      let c = alphaCache[name];
      if (!c) {
        c = document.createElement('canvas'); c.width = el.naturalWidth; c.height = el.naturalHeight;
        try { c.getContext('2d').drawImage(el, 0, 0); } catch (e) { return name; }
        alphaCache[name] = c;
      }
      let ix = Math.floor((px - left) / scale);
      if (name !== 'bubble' && st.flip) ix = el.naturalWidth - 1 - ix;
      const iy = Math.floor((py - top) / scale);
      try {
        const a = c.getContext('2d').getImageData(ix, iy, 1, 1).data[3];
        if (a > 30) return name;
      } catch (e) { return name; }
    }
    return null;
  };
  const NAMES = { start: 'キャラ', end: '半透明のキャラ（動き終わりの場所）', bubble: '吹き出し' };
  const setMode = v => {
    if (v.startsWith('ov:')) { st.selOv = +v.slice(3); st.mode = 'ov'; st.selMid = -1; renderOverlayList(id); const el = document.getElementById('sel' + id); if (el) el.textContent = ovName(st.overlays[st.selOv]); return; }
    if (v.startsWith('mid:')) { st.selMid = +v.slice(4); st.mode = 'mid'; placeMids(id); const el = document.getElementById('sel' + id); if (el) el.textContent = '中間地点 ' + (st.selMid + 1) + '（Delete で消せます）'; return; }
    st.selMid = -1; st.mode = v; const el = document.getElementById('sel' + id); if (el) el.textContent = NAMES[v] || v;
  };
  const pos = e => { const r = stage.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };

  let drag = null, moved = false;
  stage.addEventListener('pointermove', e => {
    const [px, py] = pos(e);
    if (drag) {
      if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) > 3) moved = true;
      const mx = (e.clientX - drag.x) / S, my = (e.clientY - drag.y) / S, s0 = drag.snap;
      if (drag.target === 'start') { st.baseX = s0.baseX + mx * 2; st.baseY = s0.baseY + my * 2; }
      else if (drag.target === 'end') { st.dx = s0.dx + mx * 2; st.dy = s0.dy + my * 2; }
      else if (drag.target === 'bubble') { st.bdx = s0.bdx + mx; st.bdy = s0.bdy + my; }
      else if (drag.target.startsWith('ov:')) { const o = st.overlays[+drag.target.slice(3)]; if (o) { o.x = Math.round(s0.ox + mx); o.y = Math.round(s0.oy + my); } }
      else if (drag.target.startsWith('mid:')) { const p = st.mids[+drag.target.slice(4)]; if (p) { p[0] = Math.round(s0.mx0 + mx); p[1] = Math.round(s0.my0 + my); } }
      placeAll(id);
      return;
    }
    stage.style.cursor = hitTest(px, py) ? 'pointer' : (st.mode === 'none' ? 'default' : 'crosshair');
  });
  stage.addEventListener('pointerdown', e => {
    const [px, py] = pos(e);
    const hit = hitTest(px, py);
    if (hit) {
      setMode(hit);
      const o = hit.startsWith('ov:') ? st.overlays[+hit.slice(3)] : null;
      const mp = hit.startsWith('mid:') ? st.mids[+hit.slice(4)] : null;
      drag = { x: e.clientX, y: e.clientY, target: hit,
               snap: { baseX: st.baseX, baseY: st.baseY, dx: st.dx, dy: st.dy, bdx: st.bdx, bdy: st.bdy, ox: o ? o.x : 0, oy: o ? o.y : 0,
                       mx0: mp ? mp[0] : 0, my0: mp ? mp[1] : 0 } };
      moved = false;
      stage.setPointerCapture(e.pointerId);
      stage.style.cursor = 'grabbing';
    }
    e.preventDefault();
  });
  stage.addEventListener('pointerup', e => {
    const [px, py] = pos(e);
    if (drag) { drag = null; stage.style.cursor = 'pointer'; if (moved) pushUndo(id); return; }
    if (!hitTest(px, py) && st.mode !== 'none') moveTo(id, px / S, py / S);
  });
  const ready = () => placeAll(id);
  for (const el of Object.values(els)) {
    if (!el) continue;
    el.style.pointerEvents = 'none';
    if (el.complete && el.naturalWidth) ready(); else el.onload = ready;
  }
  placeAll(id);
}

// 保存したあとに1つ戻す（サーバーが保存直前の overrides.json を積んでいる）
// 2026-09-10: ⌘Z はパネルを開いている間しか効かず、閉じると履歴ごと消えていた。
async function undoSaved() {
  try {
    const r = await fetch('/undo_overrides', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    const j = await r.json();
    if (!j.ok) { alert(j.error || '戻せませんでした'); return; }
    alert('保存を1つ戻しました（あと' + j.left + '回戻せます）。\n\n' +
          '「下書きを作り直す」を押すと動画に反映されます。');
    location.reload();
  } catch (e) { alert('通信できませんでした: ' + e); }
}

// キーボード: ⌘Z / ⇧⌘Z / 矢印（入力欄にいないとき）
document.addEventListener('keydown', e => {
  const tag = (e.target.tagName || '').toLowerCase();
  if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
  // パネルを閉じていても、保存した分を1つ戻せる
  if (CUR === null || !ED[CUR]) {
    if ((e.metaKey || e.ctrlKey) && !e.shiftKey && e.key.toLowerCase() === 'z') { e.preventDefault(); undoSaved(); }
    return;
  }
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'z') { e.preventDefault(); e.shiftKey ? redoEd(CUR) : undoEd(CUR); return; }
  if ((e.key === 'Delete' || e.key === 'Backspace') && ED[CUR].mode === 'mid') { e.preventDefault(); delMid(CUR); return; }
  const step = e.shiftKey ? 10 : 1;
  const map = { ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step] };
  if (map[e.key]) { e.preventDefault(); nudge(CUR, map[e.key][0], map[e.key][1]); }
});

// パネルの今の値を集める（保存はしない）
function collectEditor(id) {
  const row = document.getElementById('c' + id);
  const st = ED[id] || {};
  const o = Object.assign({}, overrides[id] || {});
  delete o.reset;
  o.asset_id = row.dataset.asset;
  for (const [prefix, key] of [['nar','narration'], ['af','asset_file'], ['ak','asset_kind'], ['cat','material_category']]) {
    const input = document.getElementById(prefix + id); if (input) o[key] = input.value;
  }
  const du = document.getElementById('dur' + id); if (du && !du.disabled) o.duration_sec = Number(du.value);
  const mo = document.getElementById('mo' + id); if (mo) o.motion = mo.value;
  const am = document.getElementById('am' + id); if (am) o.amount = parseFloat(am.value);
  const sc = document.getElementById('sc' + id); if (sc) o.move_sec = parseFloat(sc.value);
  // 🚨 2026-09-10: 経路つきの動き（motion=path）で実際に効くのは motion_path.duration で、
  //    「動く時間」のスライダーは見ていなかった。スライダーを短くしても経路の秒数が
  //    そのまま残るので「ずっと動いている」ように見えていた。スライダーへ合わせる。
  //    カット尺を超える値は profiles.py が弾くので、ここで収める。
  // 中間地点があるカットは、経路（motion_path）として保存する。
  // 中間地点が無いときは今までどおり drift（開始→終了の直線）のままにして、
  // 既にある全カットの動きを変えない。
  if (st.isChar && st.meta && st.mids && st.mids.length && o.motion === 'path') {
    const [sx, sy] = charCenterOnScreen(id);
    o.motion_path = {
      start: [Math.round(sx), Math.round(sy)],
      midpoints: st.mids.map(p => [Math.round(p[0]), Math.round(p[1])]),
      end: [Math.round(sx + st.dx / 2), Math.round(sy + st.dy / 2)],
      duration: o.motion_path ? o.motion_path.duration : o.move_sec,
    };
  } else if (st.isChar && st.mids && !st.mids.length) {
    o.motion_path = null;      // 点を全部消したら直線へ戻す
  }
  if (o.motion_path && Number.isFinite(o.move_sec)) {
    const cut = parseFloat(row.dataset.dur) || 0;
    const dur = Math.max(0.1, cut ? Math.min(o.move_sec, cut) : o.move_sec);
    o.motion_path = Object.assign({}, o.motion_path, { duration: Math.round(dur * 100) / 100 });
  }
  const bs = document.getElementById('bs' + id); if (bs) o.bubble_side = bs.value;
  const mz = document.getElementById('mz' + id); if (mz) o.map_zoom = mz.dataset.clear ? '' : parseFloat(mz.value);
  const mh = document.getElementById('mh' + id); if (mh) o.map_heading = mh.dataset.clear ? null : parseFloat(mh.value);
  const mp = document.getElementById('mp' + id); if (mp) o.map_pitch = parseFloat(mp.value);
  const sp = document.getElementById('sp' + id); if (sp) o.speech = sp.value;
  const bd = document.getElementById('bd' + id); if (bd) o.bubble_delay = parseFloat(bd.value);
  const btx = document.getElementById('btx' + id); if (btx) o.bubble_text_dx = Math.round(parseFloat(btx.value) || 0);
  const bty = document.getElementById('bty' + id); if (bty) o.bubble_text_dy = Math.round(parseFloat(bty.value) || 0);
  if (st.pins && st.pins.length) {
    const mp = {};
    st.pins.forEach((p, i) => {
      const h = document.getElementById('ph' + id + '_' + i); if (!h) return;
      const lab = document.getElementById('pl' + id + '_' + i).value;
      const dn = parseFloat(document.getElementById('pn' + id + '_' + i).value) || 0;
      const de = parseFloat(document.getElementById('pe' + id + '_' + i).value) || 0;
      const ent = {};
      if (!h.checked) ent.hide = true;
      if (lab && lab !== p) ent.label = lab;
      if (dn) ent.dn = dn;
      if (de) ent.de = de;
      if (Object.keys(ent).length) mp[p] = ent;
    });
    o.map_pins = mp;
  }
  const tp = document.getElementById('tp' + id); if (tp) o.telop = tp.value;
  if (st.isChar && st.meta !== undefined) {
    o.base_x = Math.round(st.baseX); o.base_y = Math.round(st.baseY);
    o.drift = [Math.round(st.dx), Math.round(st.dy)];
    o.bubble_dx = Math.round(st.bdx); o.bubble_dy = Math.round(st.bdy);
    o.scale = Math.round(st.scale * 100) / 100; o.flip = !!st.flip;
  }
  if (st.overlays) o.overlays = JSON.parse(JSON.stringify(st.overlays));
  return o;
}

// 何が変わったかを言葉にする（保存の履歴に残す）
function describeChanges(before, after) {
  const parts = [];
  for (const k of Object.keys(FIELD_NAMES)) {
    if (after[k] === undefined) continue;
    const a = before[k], b = after[k];
    if (JSON.stringify(a) === JSON.stringify(b)) continue;
    if (k === 'overlays') { parts.push('挿入 ' + ((a || []).length) + '→' + ((b || []).length) + '個'); continue; }
    if (k === 'map_pins') { parts.push('地形図のピンを調整'); continue; }
    const fmt = v => Array.isArray(v) ? '(' + Math.round(v[0] / 2) + ',' + Math.round(v[1] / 2) + ')'
      : k === 'base_x' || k === 'base_y' ? Math.round(v / 2) : k === 'motion' ? (MOTION_NAME[v] || v)
      : k === 'flip' ? (v ? 'あり' : 'なし') : (v === '' || v === null ? '（既定）' : v);
    parts.push(FIELD_NAMES[k] + ' ' + fmt(a) + '→' + fmt(b));
  }
  return parts;
}

// 学習用の生の差分 {項目: [直す前, 直した後]}。
// 表示用の changes は日本語の文字列なので、learn.py が読み違えないよう機械可読の形も残す。
// 位置や量は「何を何に変えたか」の差でしか癖が出ないので、後の値だけでなく前の値も要る。
const DELTA_SKIP = { overlays: 1, map_pins: 1, speech: 1, telop: 1 };
function rawDelta(before, after) {
  const d = {};
  for (const k of Object.keys(FIELD_NAMES)) {
    if (DELTA_SKIP[k] || after[k] === undefined) continue;
    const a = before[k], b = after[k];
    if (JSON.stringify(a) === JSON.stringify(b)) continue;
    d[k] = [a === undefined ? null : a, b];
  }
  return d;
}

// このカットだけ、今の設定で作って見る（保存前でもよい）
async function previewCut(id) {
  if (!servedByServer()) { alert('サーバー経由で開いたときだけ使えます'); return; }
  const box = document.getElementById('pv' + id);
  const btn = document.getElementById('pvb' + id);
  if (btn) { btn.disabled = true; btn.textContent = 'プレビュー作成中…'; }
  const t0 = Date.now();
  box.innerHTML = '<div class=loading><span class=spinner></span><span>プレビュー作成中… <b id="pvt' + id + '">0</b>秒（ふつう10〜40秒）</span></div>';
  const timer = setInterval(() => { const el = document.getElementById('pvt' + id); if (el) el.textContent = Math.round((Date.now() - t0) / 1000); }, 500);
  const done = () => { clearInterval(timer); if (btn) { btn.disabled = false; btn.textContent = '▶ プレビュー'; } };
  try {
    const r = await fetch('/preview', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: id, override: collectEditor(id) }) });
    const j = await r.json();
    done();
    if (!j.ok) { box.innerHTML = '<span style="color:#ff7b72">作れませんでした: ' + (j.error || '') + '</span>'; return; }
    box.innerHTML = '<div class=hint>できました（' + Math.round((Date.now() - t0) / 1000) + '秒）。左の画面で再生中 — ✕で編集に戻る</div>';
    showStageVideo(id, j.url);
  } catch (e) { done(); box.innerHTML = '<span style="color:#ff7b72">失敗: ' + e + '</span>'; }
}

// 動画プレビューは左のステージ画面で再生する（下に出さない）
function showStageVideo(id, url) {
  const stage = document.getElementById('st' + id);
  if (!stage) return;
  let v = document.getElementById('pvv' + id);
  if (!v) {
    v = document.createElement('video');
    v.id = 'pvv' + id; v.controls = true; v.autoplay = true; v.loop = true;
    v.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;background:#000;z-index:5';
    stage.appendChild(v);
    const x = document.createElement('button');
    x.id = 'pvx' + id; x.textContent = '✕ 編集に戻る';
    x.style.cssText = 'position:absolute;top:6px;right:6px;z-index:6';
    x.onclick = () => { v.pause(); v.remove(); x.remove(); };
    stage.appendChild(x);
  }
  v.src = url; v.style.display = ''; 
  const x2 = document.getElementById('pvx' + id); if (x2) x2.style.display = '';
}

// 地形図: カメラ・ピンの数値を変えたら、その場で左の画面へ（中間の1枚絵を描き直す・1〜3秒）
function bindMapLive(id) {
  let timer = null, busy = false, again = false;
  const refresh = async () => {
    if (busy) { again = true; return; }
    busy = true;
    const pos = document.getElementById('pos' + id);
    if (pos) pos.textContent = '地形図を描いています…';
    try {
      const r = await fetch('/map_frame', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id, override: collectEditor(id) }) });
      const j = await r.json();
      if (j.ok) {
        const stage = document.getElementById('st' + id);
        if (stage) stage.style.backgroundImage = "url('" + j.url + "')";
        if (pos) pos.textContent = '左の画面に反映しました（動画で見るなら ▶ プレビュー。全体は「下書きを作り直す」）';
      } else if (pos) pos.textContent = '描けませんでした: ' + (j.error || '');
    } catch (e) { if (pos) pos.textContent = '描けませんでした: ' + e; }
    busy = false;
    if (again) { again = false; refresh(); }
  };
  const arm = () => { clearTimeout(timer); timer = setTimeout(refresh, 900); };
  const sels = ['#mz' + id, '#mh' + id, '#mp' + id];
  ['ph', 'pl', 'pn', 'pe'].forEach(pre => {
    document.querySelectorAll('[id^="' + pre + id + '_"]').forEach(el => sels.push('#' + el.id));
  });
  sels.forEach(sel => {
    const el = document.querySelector(sel);
    if (el) { el.addEventListener('change', arm); el.addEventListener('input', arm); }
  });
}

// ピンを画面の前後左右へ動かす（画面の向きに合わせて南北・東西へ換算する）
const PIN_STEP_M = 150;
function movePin(id, i, right, deep) {
  const st = ED[id]; if (!st) return;
  const th = (st.mapHeading || 70) * Math.PI / 180;
  const dn = document.getElementById('pn' + id + '_' + i);
  const de = document.getElementById('pe' + id + '_' + i);
  // 画面の右＝方位の直交方向、画面の奥＝方位の向き（描画側と同じ式）
  let addE = right * PIN_STEP_M * Math.cos(th) + deep * PIN_STEP_M * Math.sin(th);
  let addN = -right * PIN_STEP_M * Math.sin(th) + deep * PIN_STEP_M * Math.cos(th);
  de.value = Math.round((parseFloat(de.value) || 0) + addE);
  dn.value = Math.round((parseFloat(dn.value) || 0) + addN);
  de.dispatchEvent(new Event('change'));
}

function postOverride(id, o) {
  if (!servedByServer()) return Promise.resolve();
  return fetch('/overrides', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ shots: { [id]: o } }) }).then(r => r.json()).catch(e => alert('保存に失敗: ' + e));
}

function markRow(id, on) { const r = document.getElementById('c' + id); if (r) r.style.outline = on ? '2px solid #ffcc44' : ''; }

function showHistory(id) {
  const o = overrides[id]; const row = document.getElementById('c' + id); if (!row) return;
  let h = row.querySelector('.hist');
  if (!o || !o.history || !o.history.length) { if (h) h.remove(); return; }
  if (!h) { h = document.createElement('div'); h.className = 'hist'; row.querySelector('.n').appendChild(h); }
  h.textContent = '手で直した: ' + o.history.slice(-3).map(x => x.time.slice(0, 16) + ' ' + x.summary).join(' ／ ');
}

function saveEditor(id) {
  const before = effective(id);
  const o = collectEditor(id);
  const parts = describeChanges(before, o);
  const prev = overrides[id] || {};
  o.history = (prev.history || []).slice(-19);
  if (parts.length) o.history.push({ time: new Date().toISOString().replace('T', ' ').slice(0, 16), summary: parts.join('、'), changes: parts, delta: rawDelta(before, o) });
  overrides[id] = o;
  try { localStorage.setItem(OKEY, JSON.stringify(overrides)); } catch (e) {}
  markRow(id, true);
  showHistory(id);
  postOverride(id, o).then(() => count());
  count();
  const msg = document.getElementById('pos' + id);
  if (msg) msg.textContent = (parts.length ? '保存: ' + parts.join('、') : '保存しました（変更なし）');
}

function resetEditor(id) {
  delete overrides[id];
  const row = document.getElementById('c' + id);
  if (row.dataset.profile === 'jinruishi') {
    let original = null; try { original = JSON.parse(row.dataset.original || 'null'); } catch (e) {}
    if (original) overrides[id] = Object.assign({}, original.fields, {
      reset: true, duration_sec: original.frames / num(row.dataset.fps, 30),
      telop: (original.fields.telops || []).join(' '),
    });
  }
  try { localStorage.setItem(OKEY, JSON.stringify(overrides)); } catch (e) {}
  postOverride(id, { asset_id: document.getElementById('c' + id).dataset.asset, reset: true });
  const ed = document.getElementById('ed' + id); if (ed) ed.remove();
  delete ED[id];
  markRow(id, false); showHistory(id);
  openEditor(id);
  count();
}

// 設定のコピー（位置・動き・大きさ・吹き出しの向き。セリフ・テロップ・挿入は写さない）
const COPY_KEYS = ['motion', 'amount', 'move_sec', 'bubble_side', 'base_x', 'base_y', 'drift', 'bubble_dx', 'bubble_dy', 'scale', 'flip'];
function neighborChar(id, dir) {
  const ids = charRows(); const i = ids.indexOf(id);
  return i < 0 ? null : (ids[i + dir] !== undefined ? ids[i + dir] : null);
}
function copyFromPrev(id) {
  const p = neighborChar(id, -1); if (p === null) { alert('前にキャラのカットがありません'); return; }
  const src = effective(p);
  const st = ED[id]; if (!st) return;
  pushUndo(id);
  st.baseX = src.base_x; st.baseY = src.base_y; st.dx = src.drift[0]; st.dy = src.drift[1];
  st.bdx = src.bubble_dx; st.bdy = src.bubble_dy; st.scale = src.scale; st.flip = src.flip;
  const set = (elId, v) => { const el = document.getElementById(elId + id); if (el) el.value = v; };
  set('mo', src.motion); set('am', src.amount); set('sc', src.move_sec); set('bs', src.bubble_side); set('sz', src.scale);
  const fl = document.getElementById('fl' + id); if (fl) fl.checked = !!src.flip;
  document.getElementById('amv' + id).textContent = src.amount; document.getElementById('scv' + id).textContent = src.move_sec + '秒'; document.getElementById('szv' + id).textContent = src.scale + '倍';
  placeAll(id); pushUndo(id);
  const msg = document.getElementById('pos' + id); if (msg) msg.textContent = '#' + p + ' の設定を写しました（保存で確定）';
}
function copyToNext(id) {
  const n = neighborChar(id, +1); if (n === null) { alert('次にキャラのカットがありません'); return; }
  const cur = collectEditor(id);
  const before = effective(n);
  const o = Object.assign({}, overrides[n] || {}, { asset_id: document.getElementById('c' + n).dataset.asset });
  for (const k of COPY_KEYS) if (cur[k] !== undefined) o[k] = cur[k];
  const parts = describeChanges(before, o);
  o.history = ((overrides[n] || {}).history || []).slice(-19);
  o.history.push({ time: new Date().toISOString().replace('T', ' ').slice(0, 16), summary: '#' + id + ' からコピー: ' + (parts.join('、') || '変更なし'), changes: parts, delta: rawDelta(before, o) });
  overrides[n] = o;
  try { localStorage.setItem(OKEY, JSON.stringify(overrides)); } catch (e) {}
  markRow(n, true); showHistory(n);
  postOverride(n, o).then(() => count());
  count();
  const msg = document.getElementById('pos' + id); if (msg) msg.textContent = '#' + n + ' へコピーしました（次のカットの調整を開くと反映されています）';
}

// 下書き（または本画質）を作り直す
async function rebuild(final) {
  if (!servedByServer()) { alert('サーバー経由で開いたときだけ使えます'); return; }
  const r = await fetch('/rebuild', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ final: !!final }) });
  const j = await r.json();
  document.getElementById('cnt').textContent = ' ' + (j.backend || '') + ' ' + (j.state || '');
  watch();
}

// 済みチェックと絞り込み
document.querySelectorAll('.donebox').forEach(cb => {
  const id = cb.dataset.id;
  if (doneSet[id]) { cb.checked = true; document.getElementById('c' + id).classList.add('isdone'); }
  cb.addEventListener('change', () => {
    if (cb.checked) doneSet[id] = true; else delete doneSet[id];
    document.getElementById('c' + id).classList.toggle('isdone', cb.checked);
    try { localStorage.setItem(DKEY, JSON.stringify(doneSet)); } catch (e) {}
    count(); filterAttn(); trimAttnList();
  });
});

// ── 注意リストから「済」を消す（2026-09-04 新設）────────────────
// 242件が並んだままだと、どれを見ればいいか分からない。
// 「済」を入れたカットはリンクを消し、残り件数を出す。全部済んだら行ごと消す。
function trimAttnList() {
  const box = document.getElementById('attn');
  if (!box) return;
  const links = box.querySelectorAll('a.atl');
  let left = 0;
  links.forEach(a => {
    const done = !!doneSet[a.dataset.id];
    a.style.display = done ? 'none' : '';
    if (!done) left++;
  });
  const head = document.getElementById('attn-head');
  const total = box.dataset.total || links.length;
  if (left === 0) {
    box.classList.add('cleared');
    box.innerHTML = '<b>注意リストは全部見ました</b>（' + total + '件）';
  } else if (head && left < total) {
    head.textContent = '注意リスト（残り ' + left + ' / ' + total + '件）';
  }
}
trimAttnList();

function filterAttn() {
  const onlyA = document.getElementById('onlyAttn').checked;
  const onlyT = (document.getElementById('onlyTodo') || {}).checked;
  document.querySelectorAll('.r').forEach(r => {
    const okA = !onlyA || r.classList.contains('attn') || r.classList.contains('bad');
    const okT = !onlyT || !r.classList.contains('isdone');
    r.style.display = (okA && okT) ? '' : 'none';
  });
}

// 修正メモはブラウザに自動保存
document.querySelectorAll('textarea').forEach(t => {
  const id = t.dataset.id;
  if (notes[id]) { t.value = notes[id]; t.classList.add('has'); }
  t.addEventListener('input', () => {
    if (t.value.trim()) { notes[id] = t.value; t.classList.add('has'); }
    else { delete notes[id]; t.classList.remove('has'); }
    try { localStorage.setItem(KEY, JSON.stringify(notes)); } catch (e) {}
    count();
  });
});

function count() {
  const total = document.querySelectorAll('.r').length;
  document.getElementById('cnt').textContent =
    ' メモ ' + Object.keys(notes).length + '件 ／ 手で直した ' + Object.keys(overrides).length + '件 ／ 確認済み ' + Object.keys(doneSet).length + '/' + total;
}

// 送り先（Claude Code / Codex）は覚えておく
(function () {
  const b = document.getElementById('backend');
  try { b.value = localStorage.getItem('ai_backend') || ''; } catch (e) {}
  b.addEventListener('change', () => { try { localStorage.setItem('ai_backend', b.value); } catch (e) {} });
})();

function payload() {
  const out = Object.keys(notes).sort((a, b) => a - b).map(id => ({ shot_id: +id, note: notes[id] }));
  return { video: V, corrections: out.concat(timeNotes), backend: document.getElementById('backend').value };
}

// AI につながるか試す（受講生の最初の確認用）
async function aiCheck() {
  if (!servedByServer()) { alert('サーバー経由で開いたときだけ使えます'); return; }
  const cnt = document.getElementById('cnt');
  cnt.textContent = ' AIにつながるか試しています…（30秒ほど）';
  try {
    const r = await fetch('/ai_check', { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ backend: document.getElementById('backend').value }) });
    const j = await r.json();
    cnt.textContent = (j.ok ? ' ✅ ' : ' ❌ ') + j.message.split('\n')[0];
    if (!j.ok) alert('AIにつながりませんでした\n\n' + j.message);
  } catch (e) { cnt.textContent = ' ❌ 確認できませんでした: ' + e; }
}

// 送信 → サーバーが check/corrections.json に保存し、AI を裏で起動する
// 🚨 2026-09-10: 押しても何も起きないように見えた。反応が離れた場所の
//    細い文字（#cnt）だけで、ボタン自身は変わらず、作り直し中に弾かれた
//    （already_running）ときも同じ細い文字にしか出ていなかった。
//    → ボタンを「送信中…」にし、結果は必ず画面の帯か alert で知らせる。
async function send() {
  const btn = document.getElementById('sendbtn');
  const label = btn ? btn.textContent : '';
  const restore = () => { if (btn) { btn.disabled = false; btn.textContent = label || '送信'; } };
  if (btn) { btn.disabled = true; btn.textContent = '送信中…'; }
  try {
    if (servedByServer()) {
      try { await loadTimeNotes(); }
      catch (error) { alert('保存済みの時刻メモを確認できません: ' + error.message); return; }
    }
    const p = payload();
    if (!p.corrections.length) { alert('修正メモが1件もありません。\n\n各カットの「修正メモ」に書くか、試写の「ここを指摘」で記録してください。'); return; }
    if (!servedByServer()) { alert('サーバー経由で開いていないので、代わりにファイルへ書き出します'); dl(); return; }
    let j;
    try {
      const r = await fetch('/corrections', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) });
      j = await r.json();
    } catch (e) { alert('送信できませんでした（サーバーにつながりません）: ' + e); return; }
    const ai = j.ai || {};
    document.getElementById('cnt').textContent =
      ' 送信 ' + j.count + '件 → ' + (ai.backend || '') + '（' + (ai.state || '') + (ai.error ? ' ' + ai.error : '') + '）';
    if (ai.state === 'already_running') {
      alert('メモ ' + j.count + '件は保存しました。\n\n' +
            'ただし、いま別の作業（' + (ai.started || '') + ' 開始）が動いているので、AIはまだ始めていません。\n' +
            '終わってからもう一度「送信」を押してください。');
      return;
    }
    if (ai.state === 'error' || ai.error) {
      alert('メモ ' + j.count + '件は保存しましたが、AIを起動できませんでした。\n\n' + (ai.error || ''));
      return;
    }
    showSent(j.count, ai);
    watch();
  } finally { restore(); }
}

// 「18:27:14 開始」から今までの経過。AIの作業は進み具合が数字で出ないので、
// せめて何分動いているかを見せる。
function elapsedOf(started) {
  const m = /^(\d{1,2}):(\d{2}):(\d{2})$/.exec(String(started || ''));
  if (!m) return '';
  const now = new Date();
  const t0 = new Date(now); t0.setHours(+m[1], +m[2], +m[3], 0);
  let sec = Math.floor((now - t0) / 1000);
  if (sec < 0) sec += 86400;                       // 日付をまたいだとき
  if (sec > 12 * 3600) return '';
  return '（' + (sec >= 60 ? Math.floor(sec / 60) + '分' + (sec % 60) + '秒' : sec + '秒') + '経過）';
}

// 行そのものに「作っています」を出す（fal の動画化・吹き出しの作成など）。
// 2026-09-10 本人の要望「生成中はそのカットの所でローディングを出してほしい」。
function rowBusy(id, on, label) {
  const row = document.getElementById('c' + id);
  if (!row) return;
  row.classList.toggle('working', !!on);
  let tag = row.querySelector('.rowbadge');
  if (!on) { if (tag) tag.remove(); return; }
  if (!tag) {
    tag = document.createElement('div');
    tag.className = 'rowbadge';
    const idcell = row.querySelector('.id');
    if (idcell) idcell.appendChild(tag);
  }
  tag.innerHTML = '<span class=spin></span>' + (label || '作っています');
}

// ── カットの行に直接ようすを出す（2026-09-10 本人の要望）──────────────
// 「AIが質問するなら、そのカットの所でやり取りしたい」「作っている最中はその行に
//  ローディングを出してほしい」。上端の帯だけだと、どのカットの話か分からなかった。

let MARKED = { active: [], ask: null, stale: [] };

function markRows(s) {
  const active = s.active_shots || [];
  const stale = s.stale_shots || [];
  const ask = (s.awaiting_answer && s.ask_shot != null) ? s.ask_shot : null;
  const same = JSON.stringify([active, ask, stale]) === JSON.stringify([MARKED.active, MARKED.ask, MARKED.stale]);
  if (same) return;
  MARKED = { active: active, ask: ask, stale: stale };

  document.querySelectorAll('.r.working, .r.needs, .r.asking').forEach(el => {
    el.classList.remove('working', 'needs', 'asking');
    const b = el.querySelector('.rowbadge'); if (b) b.remove();
  });
  document.querySelectorAll('.rowask').forEach(el => el.remove());

  const badge = (id, cls, html) => {
    const row = document.getElementById('c' + id);
    if (!row) return null;
    row.classList.add(cls);
    const idcell = row.querySelector('.id');
    if (idcell) {
      const tag = document.createElement('div');
      tag.className = 'rowbadge';
      tag.innerHTML = html;
      idcell.appendChild(tag);
    }
    return row;
  };
  stale.forEach(id => badge(id, 'needs', '未反映'));
  active.forEach(id => badge(id, 'working', '<span class=spin></span>作業中'));

  if (ask != null) {
    const row = badge(ask, 'asking', '確認待ち');
    if (row) {
      const box = document.createElement('div');
      box.className = 'rowask';
      box.innerHTML = '<b>AIがこのカットについて確認しています</b>' +
        '<div class=msg>' + escText(s.message || '') + '</div>' +
        '<textarea id=rowans rows=2 placeholder="ここに答えると、このカットの続きから直します"></textarea>' +
        '<button onclick="sendAiReply(\'rowans\')">返事を送る</button>';
      row.after(box);
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }
}

// 送ったメモのうち、どのカットが直って、どれが残っているか。
// AIの自己申告ではなく、カット表が実際に変わったかで数える。
function doneSummary(s) {
  let t = '';
  if (s.asked_shots && s.asked_shots.length) {
    const ch = s.changed_shots || [], pd = s.pending_shots || [];
    t += '　直った ' + ch.length + '件';
    if (ch.length) t += '（#' + ch.join(' #') + '）';
    if (pd.length) t += '／<b>残り ' + pd.length + '件（#' + pd.join(' #') + '）</b>';
  }
  // 🚨 いちばん大事な行。カット表は直っていても動画に入っていないことがある。
  //    2026-09-10 はこれが見えず、3回の修正が全部落ちていた。
  if (s.stale_shots && s.stale_shots.length) {
    t += '　<b class=warn>動画に未反映 ' + s.stale_shots.length + '件（#' +
         s.stale_shots.slice(0, 12).join(' #') + (s.stale_shots.length > 12 ? ' …' : '') + '）</b>' +
         ' <button onclick="rebuild(false)">いま動画へ反映する</button>';
  }
  return t;
}

// 開いた時点で未反映が残っていないか見る（前回の作業が落ちていても気づける）
function checkStale() {
  fetch('/status', { cache: 'no-store' }).then(r => r.json()).then(s => {
    if (s.state === 'running' || s.state === 'started') return;
    if (!s.stale_shots || !s.stale_shots.length) return;
    const el = workingBar();
    el.className = 'ask';
    el.innerHTML = '<b>動画に入っていない直しが ' + s.stale_shots.length + '件あります</b>' +
      '　#' + s.stale_shots.slice(0, 12).join(' #') + (s.stale_shots.length > 12 ? ' …' : '') +
      ' <button onclick="rebuild(false)">いま動画へ反映する</button>' +
      ' <button onclick="this.closest(\'#working\').remove()">閉じる</button>';
  }).catch(() => {});
}

// AIの質問に画面から返事する（同じ会話の続きとして届く）
async function sendAiReply(fieldId) {
  const ta = document.getElementById(fieldId || 'aians') || document.getElementById('aians');
  const text = ta ? ta.value.trim() : '';
  if (!text) { alert('返事を書いてください'); return; }
  const backend = (document.getElementById('backend') || {}).value || '';
  try {
    const r = await fetch('/ai_reply', { method: 'POST', headers: { 'Content-Type': 'application/json' },
                                         body: JSON.stringify({ text: text, backend: backend }) });
    const j = await r.json();
    if (!j.ok) { alert(j.error || '送れませんでした'); return; }
    const ai = j.ai || {};
    if (ai.state === 'already_running') { alert('いま別の作業が動いています。終わってからもう一度どうぞ。'); return; }
    if (ai.state === 'error' || ai.error) { alert('AIを起動できませんでした。\n\n' + (ai.error || '')); return; }
    showSent(1, ai);
    watch();
  } catch (e) { alert('通信できませんでした: ' + e); }
}

// 画面上端の帯。見た目の指定は1回だけ入れる（showWorking と showSent で共用）。
function workingBar() {
  let el = document.getElementById('working');
  if (el) return el;
  el = document.createElement('div');
  el.id = 'working';
  document.body.appendChild(el);
  if (!document.getElementById('workingcss')) {
    const st = document.createElement('style');
    st.id = 'workingcss';
    st.textContent =
      '#working{position:fixed;left:0;right:0;top:0;z-index:9999;padding:10px 16px;' +
      'background:#1b2a4a;color:#e8eefc;font-size:14px;box-shadow:0 2px 10px rgba(0,0,0,.5)}' +
      '#working.done{background:#14532d}#working.failed{background:#5b1a1a}#working.ask{background:#5a4410}' +
      '#working .msg{margin:6px 0;padding:8px;background:#0006;border-radius:6px;max-height:150px;overflow:auto;white-space:pre-wrap;font-size:13px}' +
      '#working .askrow{display:flex;gap:8px;align-items:flex-start}' +
      '#working .warn{background:#7a1f1f;padding:2px 6px;border-radius:4px}' +
      '#working textarea{flex:1;min-height:44px;font:inherit;padding:6px;border-radius:6px}' +
      '#working .bar{height:8px;background:#0d1730;border-radius:4px;margin-top:6px;overflow:hidden}' +
      '#working .bar>i{display:block;height:100%;background:#ffd34d;width:0;transition:width .4s}' +
      '#working .spin{display:inline-block;width:12px;height:12px;margin-right:8px;border:2px solid #ffd34d;' +
      'border-right-color:transparent;border-radius:50%;animation:sp 1s linear infinite;vertical-align:-1px}' +
      '@keyframes sp{to{transform:rotate(360deg)}}' +
      '#working button{margin-left:10px}';
    document.head.appendChild(st);
  }
  return el;
}

// 送信した直後の帯（AIの進捗が届くまでの間も、押したことが分かるように）
function showSent(count, ai) {
  const el = workingBar();
  el.className = '';
  el.innerHTML = '<span class=spin></span><b>AIに送りました（メモ ' + count + '件）</b>' +
    '　' + ((ai && ai.backend) || '') + ' が作業中' + (ai && ai.started ? '　' + ai.started + ' 開始' : '') +
    '　<small>この帯が緑になったら終わりです</small><div class=bar><i style="width:3%"></i></div>';
}

// AI／作り直しの進捗を5秒ごとに表示
async function watch() {
  // 🚨 2026-09-10: 生ログをそのまま流していたので画面が端末の出力で埋まっていた。
  //    帯に段階とカット数が日本語で出るようになったので、ふだんは畳んでおき、
  //    失敗したときだけ自分から開く。
  let box = document.getElementById('ai');
  if (!box) {
    const wrap = document.createElement('details');
    wrap.id = 'aiwrap';
    wrap.innerHTML = '<summary>実行の記録（うまくいかないときに開く）</summary>';
    box = document.createElement('pre');
    box.id = 'ai';
    wrap.appendChild(box);
    document.getElementById('bar').after(wrap);
  }
  const tick = async () => {
    try {
      const r = await fetch('/status', { cache: 'no-store' });
      const s = await r.json();
      let text = (s.backend || 'AI') + ': ' + s.state + (s.started ? '（' + s.started + '開始）' : '') + '\n';
      text += s.reply ? ('\n=== 返答 ===\n' + s.reply) : (s.log_tail || '');
      if (s.state === 'done') text += '\n\n完了。ページを再読み込みすると新しいコマと切り出しになります';
      box.textContent = text;
      markRows(s);
      const wrap = document.getElementById('aiwrap');
      if (wrap && String(s.state).startsWith('failed')) wrap.open = true;
      showWorking(s);
      if (s.state === 'running' || s.state === 'started') setTimeout(tick, 3000);
    } catch (e) { box.textContent = '状態取得に失敗: ' + e; setTimeout(tick, 5000); }
  };
  tick();
}

// サーバー無しで開いたとき用: corrections.json をダウンロード
function dl() {
  const blob = new Blob([JSON.stringify(payload(), null, 1)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'corrections.json';
  a.click();
}

// 手で直した印と履歴を復元
Object.keys(overrides).forEach(id => { markRow(id, true); showHistory(+id); });
count();


// ── 静止画を動かす（fal / H3 Max Turbo image-to-video）2026-09-04 新設 ──
// Ken Burns の置き換え。1本 約8円かかるので、必ず確認を挟む。
async function animateCut(id) {
  const card = document.getElementById('c' + id);
  if (!card) return;
  const btn = card.querySelector('.anim');
  // 🚨 2026-09-04: 最初は .k の textContent を改行で割って拾っていたが、
  //    <br> は textContent で改行にならないため「静止画がありません」と誤判定していた。
  //    カードの data-file を使い、無ければ文字列から正規表現で拾う。
  let name = card.dataset.file || '';
  if (!/\.(png|jpe?g|webp)$/i.test(name)) {
    const t = (card.querySelector('.k') || {}).textContent || '';
    const m = t.match(/(?:ASSET|CHAR)[\w\-]*\.(?:png|jpe?g|webp)/i) ||
              t.match(/[A-Za-z0-9_\-]+\.(?:png|jpe?g|webp)/i);
    name = m ? m[0] : '';
  }
  if (!name) { alert('この カット には静止画がありません'); return; }
  if (falReady === false) {
    alert('動画にする準備がまだです。\n\n上の「⑤動画にする準備」で、\n' +
          '「APIキーを登録」→「接続を確認」の順に済ませてください。');
    return;
  }
  const motion = await askMotion(id, name);
  if (motion === null) return;

  const before = btn ? btn.textContent : '';
  if (btn) { btn.disabled = true; btn.textContent = '作成中…'; }
  rowBusy(id, true, '動画にしています');
  try {
    const r = await fetch('/animate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: id, asset_file: name, duration: 5, prompt: motion })
    });
    const j = await r.json();
    if (!j.ok) {
      alert('作れませんでした。\n\n' + (j.error || '').slice(0, 400));
      return;
    }
    // 差し替えを overrides に書いて、下書きを作り直せば反映される
    await fetch('/overrides', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ shots: { [id]: { asset_file: j.file, asset_kind: 'video' } } })
    });
    markRow(id, true);
    if (btn) btn.textContent = '動画にした';
    alert('できました: ' + j.file + '\n\n「下書きを作り直す」を押すと動画に反映されます。');
  } catch (e) {
    alert('通信できませんでした: ' + e);
  } finally {
    rowBusy(id, false);
    if (btn && btn.textContent === '作成中…') { btn.disabled = false; btn.textContent = before; }
  }
}


// ── 作業中の表示（2026-09-04 新設）──────────────────────────
// 「下書きを作り直す」を押しても何も起きないように見え、シートも古いままなので
// 終わったかどうかが分からなかった。画面をふさぐ帯と進捗バーで、作業中だと分かるようにする。
function showWorking(s) {
  const running = (s.state === 'running' || s.state === 'started');
  let el = document.getElementById('working');
  if (!running) {
    // 🚨 2026-09-10: AIが質問して止まっても画面に何も出ず、待ち続けることになっていた。
    //    報告（AI_REPLY.md）が書かれていなければ「返事待ち」。最後に言ったことを出して、
    //    その場で返事を送れるようにする（会話は続きになる）。
    if (s.awaiting_answer && (s.state === 'done' || String(s.state).startsWith('failed'))) {
      el = el || workingBar();
      el.className = 'ask';
      el.innerHTML = '<b>AIが確認を待っています</b>' + doneSummary(s) +
        '<div class=msg>' + escText(s.message || '（返答が読めません。下の記録を見てください）') + '</div>' +
        '<div class=askrow><textarea id=aians rows=2 placeholder="返事を書いて送ると、さっきの続きから直します"></textarea>' +
        '<button onclick="sendAiReply()">返事を送る</button>' +
        '<button onclick="this.closest(\'#working\').remove()">閉じる</button></div>';
      return;
    }
    if (el) {
      if (s.state === 'done') {
        el.className = 'done';
        el.innerHTML = '<b>できました</b>' + doneSummary(s) +
          '　このページを再読み込みすると、新しいコマになります' +
          ' <button onclick="location.reload()">再読み込み</button>' +
          ' <button onclick="this.closest(\'#working\').remove()">閉じる</button>';
      } else if (String(s.state).startsWith('failed')) {
        el.className = 'failed';
        el.innerHTML = '<b>失敗しました（' + s.state + '）</b>　下の記録を見てください' +
          ' <button onclick="this.closest(\'#working\').remove()">閉じる</button>';
      } else {
        el.remove();
      }
    }
    return;
  }
  if (!el) {
    el = workingBar();
  }
  el.className = '';
  const backend = String(s.backend || '');
  const label = backend.indexOf('final') >= 0 ? '仕上げ（本画質）'
    : backend.indexOf('rebuild') >= 0 ? '下書きを作り直しています'
    : (backend === 'claude' || backend === 'codex') ? ('AIが直しています（' + backend + '）')
    : '作業しています';
  let line = '<span class=spin></span><b>' + label + '</b>';
  if (s.started) line += '　' + s.started + ' 開始' + elapsedOf(s.started);
  if (s.step) line += '　' + s.step;
  let pct = null;
  if (s.total) {
    pct = Math.round(s.done / s.total * 100);
    // 🚨 2026-09-10: この数はカットの準備だけを数えている。準備が終わったあとに
    //    結合・字幕の焼き込み・シートの作り直しが続くので、100%のまま数分止まって
    //    見えた。数え終わったら「準備は完了」と書き、残りは段階名で示す。
    if (s.done >= s.total) {
      line += '　カットの準備は' + s.total + '本とも完了';
      pct = null;                        // 満タンのバーで「終わった」と誤解させない
    } else {
      line += '　カット ' + s.done + ' / ' + s.total + '（' + pct + '%）';
    }
  }
  line += '　<small>終わるまでページを閉じないでください</small>';
  // 🚨 2026-09-10: AIの作業はカット数が出ないので、バーが3%のまま動かず
  //    「止まっている」ように見えた。カット数が無いときはバーを出さず、
  //    経過時間と、いまログに出ている最後の行を見せる。
  if (pct === null) {
    // AIは終わりが読めないので、いくつ作業したかと、いま触っているものを出す
    if (s.ai_steps) line += '　' + s.ai_steps + '手め';
    const tail = String(s.log_tail || '').trim().split('\n').filter(x => x.trim()).pop() || '';
    el.innerHTML = line + (tail ? '<div class=tail>' + escText(tail.slice(-160)) + '</div>' : '');
  } else {
    el.innerHTML = line + '<div class=bar><i style="width:' + pct + '%"></i></div>';
  }
}

// 押した直後から出す（サーバーの応答を待たずに反応させる）
(function () {
  const orig = window.rebuild;
  if (typeof orig !== 'function') return;
  window.rebuild = function (final) {
    showWorking({ state: 'running', backend: final ? 'rebuild(final)' : 'rebuild(draft)' });
    return orig.apply(this, arguments);
  };
})();

// 開いた時点で既に走っていたら拾う（ページを開き直した場合）
if (servedByServer()) {
  // 🚨 2026-09-10: 読み込み時に1回だけ状態を見て終わっていたので、ページを開き直すと
  //    そこで見張りが止まり、AIが終わっても帯が出たままになっていた。走っていれば見張る。
  fetch('/status', { cache: 'no-store' }).then(r => r.json()).then(s => {
    showWorking(s);
    markRows(s);
    if (s.state === 'running' || s.state === 'started' || s.awaiting_answer) watch();
    else checkStale();
  }).catch(() => {});
}

// ── fal の準備（2026-09-04 新設）────────────────────────────
// 「動かす」を使う前に、この画面の中で 状態確認 → キー登録 まで済ませられるようにする。
// 🚨 キーはブラウザの入力欄を通さない。登録は Mac の標準ダイアログが受け取る。
// 受講生が迷わないよう、①状態を色で常に出す ②失敗したら次にすることを書く
// ③fal の該当ページへのリンクを出す ④未準備なら「動かす」で課金しない。
let falReady = null;   // null=未確認 / true=使える / false=まだ

const FAL_LINKS = {
  no_key: ['fal でキーを作る', 'https://fal.ai/dashboard/keys'],
  bad_key: ['fal でキーを作り直す', 'https://fal.ai/dashboard/keys'],
  no_credit: ['fal でチャージする', 'https://fal.ai/dashboard/billing']
};

function falMsg(j, plain) {
  const el = document.getElementById('falst');
  if (!el) return;
  if (plain) { el.innerHTML = ' ' + plain; el.style.color = ''; falPanel(null); return; }
  const link = FAL_LINKS[j.state];
  el.innerHTML = ' <b>' + (j.ok ? '準備できています' : '準備がまだです') + '</b>　' +
    (j.message || '') + (link ? ' <a href="' + link[1] + '" target=_blank>' + link[0] + '</a>' : '');
  el.style.color = j.ok ? '#7ee787' : '#ffb454';
  falReady = !!j.ok;
  falPanel(j);
}

// 準備ができていないときだけ、手順を順番に出す（2026-09-04 新設）
// 実際に初心者の動きをたどると「アカウントがまだ無い」ところで詰まる。
// リンク先はログイン必須のページなので、①登録 から並べる。
let falGuideForced = false;
function falGuide() { falGuideForced = true; falCheck(true).then(j => falPanel(j || {}, true)); }

function falPanel(j, forced) {
  let el = document.getElementById('falguide');
  if ((!j || j.ok) && !(forced || falGuideForced)) { if (el) el.remove(); return; }
  if (!el) {
    el = document.createElement('div');
    el.id = 'falguide';
    document.getElementById('bar').after(el);
  }
  const step = j.ok ? 5 : ({ no_key: 2, bad_key: 2, no_credit: 3 }[j.state] || 1);
  const li = (n, title, body) =>
    '<li class="' + (n < step ? 'done' : (n === step ? 'now' : '')) + '">' +
    '<b>' + title + '</b><br><span>' + body + '</span></li>';
  el.innerHTML =
    '<div class=hd>動画にする準備（初めての方へ・10分ほど）' +
    '<button style="float:right;padding:2px 8px;font-size:12px" ' +
    'onclick="falGuideForced=false;this.closest(\'#falguide\').remove()">閉じる</button></div><ol>' +
    li(1, 'fal に登録する',
       '<a href="https://fal.ai" target=_blank>fal.ai を開く</a> → Sign up。' +
       '「For myself」→「Build with Code」を選びます（コードは書きません）。') +
    li(2, 'キーを作ってコピーする',
       '<a href="https://fal.ai/dashboard/keys" target=_blank>API Keys を開く</a> → 「＋ Add key」→ ' +
       'Scope は API、名前は何でも可 → <b>Copy Key</b>。' +
       '<br><b style="color:#ffb454">このキーは人に見せないでください。</b>' +
       'この画面でしか表示されません。') +
    li(3, 'ここに貼り付ける',
       '<input type=password id=falkey placeholder="ここにキーを貼り付け（⌘V）" autocomplete=off ' +
       'onkeydown="if(event.key===\'Enter\')falSaveKey()"> ' +
       '<button onclick="falSaveKey()">登録する</button>' +
       '<br><small>入力は見えません。この画面の中だけで保存され、外へは送られません。' +
       ' <a href="#" onclick="falRegister();return false">別の窓で入力する</a></small>') +
    li(4, '残高を入れる',
       '<a href="https://fal.ai/dashboard/billing" target=_blank>Credits を開く</a> → まず $5 で足ります。' +
       '<br><small>画像なら約120枚、5秒の動画なら約470本ぶんです。</small>') +
    '</ol><div class=ft>できたら <button onclick="falCheck()">接続を確認</button> を押してください（無料）。</div>';
}

async function falCheck(quiet) {
  if (!quiet) falMsg(null, '確かめています…');
  try {
    const r = await fetch('/fal_check', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    const j = await r.json();
    falMsg(j);
    if (!quiet && !j.ok) {
      alert(j.message + (FAL_LINKS[j.state] ? '\n\n' + FAL_LINKS[j.state][1] : ''));
    }
    return j;
  } catch (e) {
    falMsg(null, '確認できませんでした: ' + e);
    return { ok: false };
  }
}

async function falRegister() {
  falMsg(null, '登録の画面を出しました。そちらにキーを貼り付けてください…');
  try {
    const r = await fetch('/fal_register', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' });
    const j = await r.json();
    falMsg(j);
    alert(j.message || '登録の結果が分かりませんでした');
  } catch (e) { falMsg(null, '登録できませんでした: ' + e); }
}

// 画面を開いたら、黙って一度だけ状態を見る（キーが無ければ課金は起きない）
if (servedByServer()) {
  fetch('/fal_check', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{"quiet":1}' })
    .then(r => r.json()).then(falMsg).catch(() => {});
}

// ── サーバーが古いと、押しても何も起きない（2026-09-04）────────
// 実際に起きた: 8/30 に起動したサーバーが動いたままで、その日に足した入口を知らず
// 404 を返していた。ボタンは押せているのに無反応に見える。
// シート側が期待する版と食い違ったら、はっきり知らせる。
const SHEET_BUILD = '2026-09-04';
if (servedByServer()) {
  fetch('/status', { cache: 'no-store' }).then(r => r.json()).then(s => {
    if (s.build !== SHEET_BUILD) {
      const d = document.createElement('div');
      d.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9999;padding:10px 16px;' +
        'background:#5b3a1a;color:#ffe9c9;font-size:13px';
      d.innerHTML = '<b>道具が新しくなっています</b>　いま動いている検収サーバーは古い版' +
        (s.build ? '（' + s.build + '）' : '') + 'なので、新しいボタンが反応しません。' +
        'ターミナルの検収サーバーを Ctrl+C で止めて、もう一度「動画を作る」を開き直してください。' +
        ' <button onclick="this.closest(\'div\').remove()">閉じる</button>';
      document.body.appendChild(d);
    }
  }).catch(() => {});
}

// ページの中でキーを保存する（2026-09-04 新設）
// 別ウィンドウがブラウザの後ろに隠れて気づかない事故があったので、この画面で完結させる。
// 🚨 localhost の中だけで受け渡す。サーバーはこの中身をログに出さない（log_message は無効）。
async function falSaveKey() {
  const f = document.getElementById('falkey');
  if (!f) return;
  const k = f.value.trim();
  if (!k) { alert('キーを貼り付けてください'); return; }
  falMsg(null, '登録しています…');
  try {
    const r = await fetch('/fal_key', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ key: k })
    });
    const j = await r.json();
    f.value = '';                     // 画面から即座に消す
    falMsg(j);
    if (!j.ok) alert(j.message || '登録できませんでした');
  } catch (e) {
    f.value = '';
    falMsg(null, '登録できませんでした: ' + e);
  }
}

// 古い sheet.js のままだと、新しいボタンの onclick が黙って失敗する（2026-09-04）。
// 実際に「押しても反応がない」が2回起きた。理由が分かるようにする。
function callJs(name) {
  const f = window[name];
  if (typeof f !== 'function') {
    alert('この画面は古い版のままです。\n\n' +
          'Shift を押しながら再読み込み（⌘⇧R）してください。\n' +
          'それでも直らないときは、検収サーバーを止めて開き直してください。');
    return;
  }
  return f();
}

// ── 動かし方の指定（2026-09-04 新設）──────────────────────
// 「動かす」を押したとき、そのカットをどう動かすかを決める。
// 何も選ばなければ「わずかな自然な動き」（構図を変えない安全な既定）。
const MOTION_PRESETS = [
  ['そのまま（わずかに動く）',
   'Keep the subject and composition exactly as in the photo. Add only subtle natural motion: ' +
   'slow drifting air, gentle light change, faint movement of leaves or water. ' +
   'No camera cuts, no new objects, no people appearing.'],
  ['ゆっくり寄る',
   'Slow steady push-in toward the main subject. Keep the composition and subject unchanged. ' +
   'Subtle natural motion in the environment. No cuts, no new objects, no people appearing.'],
  ['ゆっくり引く',
   'Slow steady pull-back revealing more of the scene. Keep the subject unchanged. ' +
   'Subtle natural motion. No cuts, no new objects, no people appearing.'],
  ['風が流れる',
   'Wind moves through the scene: leaves, grass and branches sway gently. Camera stays still. ' +
   'Keep composition unchanged. No cuts, no new objects, no people appearing.'],
  ['水面が揺れる',
   'The water surface ripples slowly and reflections shift. Camera stays still. ' +
   'Keep composition unchanged. No cuts, no new objects, no people appearing.'],
  ['霧が動く',
   'Mist and fog drift slowly through the scene. Camera stays still. Keep composition unchanged. ' +
   'No cuts, no new objects, no people appearing.']
];

async function askMotion(id, name) {
  // 元の画像を作ったときの英語プロンプトを持ってくる（あれば下敷きにする）
  let base = '';
  try {
    const r = await fetch('/asset_prompt', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asset_file: name })
    });
    base = (await r.json()).prompt || '';
  } catch (e) {}

  return new Promise(resolve => {
    const bg = document.createElement('div');
    bg.className = 'modalbg';
    const presets = MOTION_PRESETS.map((p, i) =>
      '<button type=button class=mp data-i="' + i + '">' + p[0] + '</button>').join(' ');
    bg.innerHTML =
      '<div class=modal><div class=hd>#' + id + ' を動画にする</div>' +
      '<div class=sub>' + name + ' → 5秒（MiniMax H3 Max Turbo・768p・約8円）</div>' +
      (base ? '<details class=basep><summary>この画像を作ったときのプロンプト</summary><div>' +
              base.replace(/</g, '&lt;') + '</div></details>' : '') +
      '<div class=lbl>実際に送る文（英語）<span class=note id=mtsrc></span></div>' +
      '<textarea id=mtext class=en rows=3></textarea>' +
      '<div class=presets>' + presets + '</div>' +
      '<div class=lbl style="margin-top:12px">どう動かしたいですか（日本語で書いてください）</div>' +
      '<textarea id=mja class=ja rows=5 placeholder="例: 霧がゆっくり左から右へ流れる。看板は動かない。カメラは固定。"></textarea>' +
      '<div class=aigen><button type=button class=primary id=mgen>AIに英語のプロンプトを作らせる</button>' +
      '<span id=mgst class=note></span></div>' +
      '<div class=note>人を新しく出す指示は書かないでください（実在の人に見える絵が出ます）。</div>' +
      '<div class=btns><button type=button id=mcancel>やめる</button>' +
      '<button type=button class=primary id=mok>この内容で作る（約8円）</button></div></div>';
    document.body.appendChild(bg);
    const ta = bg.querySelector('#mtext');
    const KEEP = ' Animate this still image with subtle natural motion only. ' +
      'Keep the subject and composition exactly as in the image. ' +
      'No cuts, no new objects, and do not introduce any people who are not already there.';
    const src = bg.querySelector('#mtsrc');
    if (base) {
      ta.value = base + KEEP;
      src.textContent = '　台本のプロンプトから作りました';
    } else {
      ta.value = '';
      ta.placeholder = '空のままでも作れます（そのままわずかに動く動画になります）';
      src.textContent = '　台本にこのカットのプロンプトが見つかりませんでした';
    }

    bg.querySelectorAll('.mp').forEach(b => b.addEventListener('click', () => {
      ta.value = (base ? base + ' ' : '') + MOTION_PRESETS[+b.dataset.i][1];
      bg.querySelectorAll('.mp').forEach(x => x.classList.remove('on'));
      b.classList.add('on');
    }));

    const gen = bg.querySelector('#mgen');
    const ja = bg.querySelector('#mja');
    const gst = bg.querySelector('#mgst');
    gen.addEventListener('click', async () => {
      const jaText = ja.value.trim();
      if (!jaText) { alert('どう動かしたいかを、上の欄に日本語で書いてください'); return; }
      gen.disabled = true; gst.textContent = ' AIが考えています…';
      try {
        const r = await fetch('/motion_prompt', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ japanese: jaText, base: base,
                                 backend: (document.getElementById('backend') || {}).value || '' })
        });
        const j = await r.json();
        if (j.ok) { ta.value = j.prompt; gst.textContent = ' できました'; src.textContent = '　AIが作りました'; }
        else { gst.textContent = ''; alert('作れませんでした\n\n' + (j.message || '')); }
      } catch (e) { gst.textContent = ''; alert('AIを呼べませんでした: ' + e); }
      finally { gen.disabled = false; }
    });
    ja.addEventListener('keydown', e => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) gen.click(); });

    const done = v => { bg.remove(); resolve(v); };
    bg.querySelector('#mcancel').addEventListener('click', () => done(null));
    bg.querySelector('#mok').addEventListener('click', () => done(ta.value.trim() || MOTION_PRESETS[0][1]));
    bg.addEventListener('click', e => { if (e.target === bg) done(null); });
    ja.focus();
  });
}


// ---- 全編を再生しながら時刻で指摘（保存だけではAIを起動しない） ----
async function loadTimeNotes() {
  const response = await fetch('/check/corrections.json', {cache: 'no-store'});
  if (response.status === 404) { timeNotes = []; return; }
  if (!response.ok) throw new Error('修正メモの読み込みに失敗');
  const data = await response.json();
  timeNotes = (data.corrections || []).filter(item => Number.isFinite(item.time_sec));
}

(async function setupTimeReview() {
  const bar = document.getElementById('bar');
  if (!bar || !servedByServer()) return;
  const section = document.createElement('section');
  section.id = 'time-review';
  section.setAttribute('aria-label', '試写動画と時刻の指摘');
  section.innerHTML = '<h2>試写しながら指摘</h2>' +
    '<video id="review-video" controls playsinline preload="metadata" tabindex="0" aria-label="試写動画"></video>' +
    '<p><button id="point-time" class="primary" disabled>ここを指摘</button> ' +
    '<span>プレーヤーにフォーカスして Space：再生・一時停止 ／ Enter：ここを指摘</span></p>' +
    '<p id="time-status" role="status">読み込み中…</p><ul id="time-notes"></ul>' +
    '<dialog id="time-dialog"><form id="time-form"><h3 id="time-label"></h3>' +
    '<label>修正してほしい内容<textarea id="time-note" required></textarea></label>' +
    '<p id="time-error" role="alert"></p><button type="submit" class="primary">指摘を保存</button> ' +
    '<button type="button" id="time-cancel">キャンセル</button></form></dialog>';
  bar.before(section);
  const video = document.getElementById('review-video');
  const button = document.getElementById('point-time');
  const status = document.getElementById('time-status');
  const dialog = document.getElementById('time-dialog');
  const form = document.getElementById('time-form');
  const comment = document.getElementById('time-note');
  const error = document.getElementById('time-error');
  let selectedTime = null;
  let saving = false;
  function showNotes() {
    const list = document.getElementById('time-notes');
    list.replaceChildren();
    for (const item of timeNotes) {
      const li = document.createElement('li');
      li.textContent = item.time_sec.toFixed(2) + '秒 ／ カット ' + item.shot_id + '：' + item.note;
      list.append(li);
    }
  }
  try {
    const response = await fetch('/time_review', {cache: 'no-store'});
    const data = await response.json();
    if (!response.ok || !data.ok) throw new Error(data.error || '試写情報を取得できません');
    video.src = data.video_url;
    await loadTimeNotes();
    showNotes();
    if (data.timing_status === 'awaiting_measured_audio') throw new Error('時刻記録はできません（音声未同期）');
    if (!data.shots.length || data.shots.some(s => !Number.isFinite(s.start_frame) || !Number.isFinite(s.end_frame))) {
      throw new Error('時刻付きカット表が必要です');
    }
    status.textContent = '指摘を保存してから、上部の「送信」でAIに修正を依頼できます。';
    button.disabled = false;
    button.addEventListener('click', () => {
      video.pause();
      selectedTime = video.currentTime;
      const matches = data.shots.filter(s => s.start_frame <= selectedTime * 30 && selectedTime * 30 < s.end_frame);
      if (matches.length !== 1) { status.textContent = 'この時刻に対応するカットを特定できません。'; return; }
      document.getElementById('time-label').textContent = selectedTime.toFixed(2) + '秒 ／ カット ' + matches[0].id;
      comment.value = ''; error.textContent = '';
      dialog.showModal(); comment.focus();
    });
    // 動画だけに限定し、入力欄や既存の調整ショートカットを妨げない。
    video.addEventListener('keydown', event => {
      if (event.repeat || event.isComposing || event.ctrlKey || event.metaKey || event.altKey) return;
      if (event.code === 'Space') {
        event.preventDefault();
        if (video.paused) video.play().catch(e => { status.textContent = e.message; });
        else video.pause();
      } else if (event.key === 'Enter') {
        event.preventDefault(); button.click();
      }
    });
    document.getElementById('time-cancel').addEventListener('click', () => { if (!saving) dialog.close(); });
    dialog.addEventListener('cancel', event => { if (saving) event.preventDefault(); });
    dialog.addEventListener('close', () => video.focus());
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (saving) return;
      saving = true;
      const submit = form.querySelector('[type="submit"]');
      submit.disabled = true; error.textContent = '';
      try {
        const response = await fetch('/time_corrections', {method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({time_sec: selectedTime, note: comment.value})});
        const result = await response.json();
        if (!response.ok || !result.ok) throw new Error(result.error || '保存に失敗');
        timeNotes.push({shot_id: result.shot_id, note: result.note, time_sec: result.time_sec});
        showNotes(); dialog.close();
        status.textContent = 'カット ' + result.shot_id + ' の指摘を保存しました。「送信」でAIに依頼できます。';
      } catch (e) { error.textContent = e.message; }
      finally { saving = false; submit.disabled = false; }
    });
  } catch (e) { status.textContent = e.message; }
})();
