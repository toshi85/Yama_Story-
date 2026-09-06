/* chatgpt.com のページに注入して動かす自動生成ループ。

   前提: window.__yamaQueue に [{id, prompt}, ...] を先に流し込んでおく。
   chatgpt.com は CSP で localhost への通信を遮断するため、サーバー方式は使えない。
   生成画像はページ内で blob 化し、Chrome のダウンロードとして
   「アセット番号.png」の名前で ~/Downloads に落とす（ローカル側で images/ へ回収する）。

   ⚠️ 生成中も画像要素は出る（途中経過のプレビュー）。掴んでいいのは
   停止ボタンが消えてから。ここを見ないと絵柄の崩れた半端な絵が保存される。

   開始: __yamaRun()          停止: __yamaGen.stop = true
   状況: __yamaGen.status()                                              */
(() => {
  // 再注入で running を戻すと、古い非同期ループと新しいループが競合する。
  if (window.__yamaGen?.running) {
    console.log('[yama] 既存ループが稼働中。再注入しません');
    return;
  }
  // タブがリロードされるとページに入れたものは全部消える。進捗だけは localStorage に
  // 残しておき、入れ直したときに続きから拾えるようにする（実測でリロードが起きた）。
  const SAVE_KEY = 'yamaDone';
  const loadDone = () => { try { return JSON.parse(localStorage.getItem(SAVE_KEY)) || []; } catch (e) { return []; } };
  const saveDone = (d) => { try { localStorage.setItem(SAVE_KEY, JSON.stringify(d)); } catch (e) {} };

  const S = (window.__yamaGen = window.__yamaGen || {});
  Object.assign(S, {
    stop: false, done: S.done || loadDone(), failed: S.failed || [], current: null, running: false,
    forget: () => { S.done = []; saveDone([]); },
    status: () => ({
      running: S.running, current: S.current,
      done: S.done.length, failed: S.failed.length,
      queue: (window.__yamaQueue || []).length,
      lastLog: S.log.slice(-6),
    }),
    log: S.log || [],
    waitState: null, limitEvidence: null,
    limitUntil: S.limitUntil || null,   // 解除予定の時刻（epochミリ秒）。run.py が読む
  });

  const LIMIT_WAIT_MIN = 20;     // 投げ直す間隔の上限（解除が近いほど短くする）
  const LIMIT_MAX_TRIES = 240;   // 8分×240 = 32時間ぶん粘る

  // 🚨 Chromeは隠れたタブのタイマーを凍結する。凍結されると「動いているのに進まない」
  //    という一番気づきにくい壊れ方をするので、自分で時計のずれを測って知らせる。
  //    起動オプション --disable-backgrounding-occluded-windows などが外れると再発する。
  const sleep = async (ms) => {
    const t0 = Date.now();
    await new Promise((r) => setTimeout(r, ms));
    const drift = Date.now() - t0;
    if (drift > ms * 5 + 10000 && !S.frozeNoted) {
      S.frozeNoted = true;
      note(`⚠ タイマーが間引かれています（${ms}ms待つはずが${drift}ms）— Chromeの起動オプションを確認してください`);
    }
    return drift;
  };
  const q = (s) => document.querySelector(s);
  const note = (m) => { S.log.push(`${new Date().toLocaleTimeString()} ${m}`); if (S.log.length > 200) S.log.shift(); };

  // 生成中は送信ボタンが停止ボタンに変わる。これが「まだ描いている」の唯一の証拠。
  const busy = () => !!q('[data-testid="stop-button"]');

  // ページに出ている画像。生成中のプレビューもここに入るので、単独では完了の証拠にならない。
  // 🚨 naturalWidth で選ばない。裏のタブでは画像がデコードされず 0 のままになり、
  //    「完了したのに画像が無い」と誤診する（実測）。実体の確認は後段の blob サイズで行う。
  const imgEls = () => [...document.querySelectorAll('main img')]
    .filter((i) => i.src && /backend-api\/estuary\/content|oaiusercontent/.test(i.src));
  const norm = (s) => s.replace(/\n(?:表示を増やす|表示を減らす|Show more|Show less)\s*$/, '').replace(/\s+/g, ' ').trim();
  const users = () => [...document.querySelectorAll('[data-message-author-role="user"]')];
  const matchedUser = (prompt) => {
    const list = users();
    return list.length === 1 && norm(list[0].innerText) === norm(prompt) ? list[0] : null;
  };

  const completedImages = (prompt) => {
    if (!matchedUser(prompt)) return [];
    return imgEls().filter(img => {
      if (!img.complete || !img.naturalWidth) return false;
      let parent = img;
      for (let i = 0; i < 5 && parent; i++, parent = parent.parentElement) {
        const buttons = [...parent.querySelectorAll('button')];
        const edit = buttons.some(b => /^(画像を編集|Edit image)$/i.test(b.getAttribute('aria-label') || ''));
        const share = buttons.some(b => /^(この画像を共有する|Share image|Share this image)$/i.test(b.getAttribute('aria-label') || ''));
        if (edit && share) return true;
      }
      return false;
    });
  };

  const retryBtn = () => [...document.querySelectorAll('button')]
    .find((b) => b.textContent.includes('再試行') || b.textContent.includes('Retry'));

  // 生成上限に当たっていないか（実際に出た文面: 「画像を使い切りました」
  // 「画像生成の利用上限に達しています…21:49までお待ちください」
  //  "You've hit the Plus plan limit for image generations requests." ）
  // 判定は会話部分だけを見る。body だと左の履歴一覧のチャット名まで拾ってしまい、
  // 過去に「Image Generation Limit」という名前のチャットが並んだだけで
  // 永久に「上限中」と誤判定する（実測: 一晩まるごと空回りした）。
  const convText = () => {
    const main = document.querySelector('main');
    if (!main) return '';
    const copy = main.cloneNode(true);
    copy.querySelectorAll('[data-message-author-role="user"],#prompt-textarea').forEach(x=>x.remove());
    return (copy.innerText || copy.textContent || '').slice(-5000);
  };
  const classifyLimitText = (text, source) => {
    const image = /画像を使い切りました|画像(?:の生成|生成)?(?:の利用)?上限に達|画像生成[^。\n]{0,50}(?:利用上限|上限に達)|hit the [^.\n]{0,30}plan limit for image generation|limit for image generations? requests|(?:reached|exceeded)[^.\n]{0,50}image generation limit/i;
    const access = /リクエストが多すぎ|リクエストの頻度が高|Too many requests|rate limit exceeded/i;
    const match = text.match(image) || text.match(access);
    if (!match) return null;
    return {kind:image.test(text)?'image_limit':'access_limit', source,
      text:text.slice(Math.max(0,match.index-40),match.index+360).trim(), observedAt:Date.now()/1000};
  };
  const readLimitEvidence = () => {
    for (const d of document.querySelectorAll('[role=dialog],[role=alertdialog]')) {
      const e = classifyLimitText(d.innerText || '', 'dialog');
      if (e) return e;
    }
    return classifyLimitText(convText(), 'current_conversation');
  };
  const limitHit = () => {
    const evidence = readLimitEvidence();
    if (evidence) S.limitEvidence = evidence;
    return !!evidence;
  };
  window.__yamaLimitEvidence = readLimitEvidence;

  // 断り文句に書かれた「あと何分で解除か」を読む。読めなければ null。
  // 🚨 文面は何通りもある。実際に出たものを全部拾う（2026-09-04 に「明日の14:33に
  //    もう一度お試しください」「上限は17時間後にリセットされ」を取りこぼして、
  //    20分おきに17時間投げ直し続け、77/311枚で一晩止まっていた）。
  function limitLeftMin() {
    const t = S.limitEvidence?.text || "";
    const now = new Date();
    const atTime = (h, mi, tomorrow) => {
      const d = new Date();
      d.setHours(h, mi, 0, 0);
      if (tomorrow) d.setDate(d.getDate() + 1);
      while (d <= now) d.setDate(d.getDate() + 1);
      return Math.round((d - now) / 60000);
    };
    let m;

    // ① 「明日の 14:33にもう一度お試しください」「今日の 21:49 に」
    m = t.match(/(明日|今日|翌日)の?\s*(\d{1,2}):(\d{2})/);
    if (m) return atTime(+m[2], +m[3], m[1] !== '今日');
    m = t.match(/(tomorrow|today)\s*at\s*(\d{1,2}):(\d{2})\s*(AM|PM)?/i);
    if (m) {
      let h = +m[2];
      if (/pm/i.test(m[4] || '') && h < 12) h += 12;
      if (/am/i.test(m[4] || '') && h === 12) h = 0;
      return atTime(h, +m[3], !/today/i.test(m[1]));
    }

    // ② 「21:49までお待ちください」
    m = t.match(/(\d{1,2}):(\d{2})\s*(?:まで(?:お待ち|待って)|にもう一度|に再度)/);
    if (m) return atTime(+m[1], +m[2], false);

    // ③ 「◯時間後にリセット」/ "resets in 3 hours and 20 minutes"（丸めた値なので最後に見る）/ "resets in 3 hours and 20 minutes"
    m = t.match(/上限は\s*(\d+)\s*時間(?:\s*(\d+)\s*分)?後にリセット/);
    if (m) return (+m[1]) * 60 + (+m[2] || 0);
    m = t.match(/(\d+)\s*時間後/);
    if (m) return (+m[1]) * 60;
    m = t.match(/resets? in (?:(\d+)\s*hours?)?(?:\s*and\s*)?(?:(\d+)\s*minutes?)?/i);
    if (m && (m[1] || m[2])) return (+m[1] || 0) * 60 + (+m[2] || 0);

    return null;
  }

  // 次に投げ直すまでの分数。書かれた解除時刻は「目安」に使うが鵜呑みにはしない。
  // 遠いうちは間隔を空け、近づくほど詰める。表示が外れて早く空いても最大20分で気づく。
  function nextProbeMin() {
    const left = limitLeftMin();
    if (left === null) return LIMIT_WAIT_MIN;
    // 解除がまだ遠いうちは1時間おきでいい。20分おきに17時間投げ続けると
    // 「画像生成上限通知」の断りチャットが50本以上溜まる（実測）。
    if (left > 90) return Math.min(60, left - 30);
    return Math.min(LIMIT_WAIT_MIN, Math.max(2, Math.ceil(left / 4)));
  }

  function limitNote() {
    const left = limitLeftMin();
    S.limitUntil = left === null ? null : Date.now() + left * 60000;
    if (left === null) return '解除予定の表示なし';
    const at = new Date(S.limitUntil);
    const hhmm = `${String(at.getHours()).padStart(2, '0')}:${String(at.getMinutes()).padStart(2, '0')}`;
    return `解除まで残り約${left}分（${hhmm}ごろ）`;
  }

  // 停止ボタンが消えるまで待つ（＝生成が終わるまで）
  async function waitIdle(timeoutMs, prompt) {
    const t0 = Date.now();
    let quiet = 0;
    let stableSince = 0, stableImage = '';
    while (Date.now() - t0 < timeoutMs) {
      await sleep(2000);
      if (limitHit()) return 'limit';
      if (busy()) {
        quiet = 0;
        const ready = prompt ? completedImages(prompt) : [];
        const key = ready.length ? [...new Set(ready.map(x=>x.src))].join('|') : '';
        if (!key || key !== stableImage) { stableSince = key ? Date.now() : 0; stableImage = key; }
        if (key && Date.now() - stableSince >= 20000) {
          note('完成画像の表示が安定していますが停止ボタンが残っています。同じ会話を再読込して保存を確認します');
          location.reload();
          await new Promise(()=>{});
        }
        continue;
      }
      quiet += 2000;
      if (quiet >= 6000) return true;    // 6秒続けて停止ボタンが無ければ完了
      if (limitHit()) return 'limit';
    }
    return false;
  }

  async function newChat() {
    const btn = q('[data-testid="create-new-chat-button"]');
    if (btn) btn.click();                 // SPA遷移（フルリロードするとこのループが死ぬ）
    for (let i = 0; i < 24; i++) {
      await sleep(500);
      if (q('#prompt-textarea') && imgEls().length === 0 && users().length === 0 && !location.pathname.startsWith('/c/')) return;
    }
    throw new Error('新しいチャットへ移れていないため送信しません');
  }

  async function send(prompt) {
    const el = q('#prompt-textarea');
    if (!el) throw new Error('入力欄が無い');
    // 前の生成が走っていると送信ボタンが出ない。必ず空くまで待つ。
    for (let i = 0; i < 120 && busy(); i++) await sleep(2000);
    if (busy()) throw new Error('前の生成が終わらない');
    el.focus();
    document.execCommand('selectAll', false, null);
    document.execCommand('insertText', false, prompt);
    for (let i = 0; i < 24; i++) {
      await sleep(300);
      const b = q('[data-testid="send-button"]');
      if (b && !b.disabled) {
        if (norm(el.innerText) !== norm(prompt)) throw new Error('入力欄が要求文と不一致');
        b.click();
        for (let j = 0; j < 40; j++) {
          await sleep(500);
          if (matchedUser(prompt)) return;
        }
        throw new Error('送信した要求文の表示を確認できません');
      }
    }
    throw new Error('送信ボタンが出ない');
  }

  // 生成が終わるまで待って、完成画像を返す。エラー表示が出たら 'retry' を返す
  async function waitImage(prompt, timeoutMs = 600000) {
    const t0 = Date.now();
    // まず生成が始まるのを確認する（停止ボタンが出る）
    for (let i = 0; i < 20 && !busy(); i++) {
      await sleep(1000);
      if (retryBtn()) return 'retry';
      if (limitHit()) return 'limit';
    }
    const idle = await waitIdle(timeoutMs - (Date.now() - t0), prompt);
    if (idle === 'limit') return 'limit';
    if (!idle) throw new Error('生成タイムアウト');
    if (retryBtn()) return 'retry';
    if (limitHit()) return 'limit';
    await sleep(2000);
    if (!matchedUser(prompt)) throw new Error('生成結果と要求文の対応が不一致');
    const imgs = imgEls();
    if (!imgs.length) throw new Error('完了したのに画像が無い');
    return imgs;
  }

  // 候補を新しい順に試して、中身のある1枚を落とす。
  // 完了判定は停止ボタンで見ているので、ここは「明らかに壊れている」だけを弾く。
  // 平坦な1:1のキャラ絵は 240KB 程度で正常なことがある（しきい値を上げると取りこぼす）。
  async function saveAs(imgs, item) {
    if (!matchedUser(item.prompt) || busy()) throw new Error('保存前の要求文・完了確認に失敗');
    let blob = null, last = '';
    for (const img of [...imgs].reverse()) {
      try {
        const res = await fetch(img.src, { credentials: 'include' });
        if (!res.ok) { last = 'HTTP ' + res.status; continue; }
        const b = await res.blob();
        if (b.size < 80000) { last = '小さすぎる ' + b.size; continue; }
        blob = b; break;
      } catch (e) { last = e.message; }
    }
    if (!blob) throw new Error('使える画像が無い（' + last + '）');
    if (!matchedUser(item.prompt) || busy()) throw new Error('画像取得中に会話が変わりました');
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${item.id}.png`;
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 5000);
    const hash = async (bytes) => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');
    const receipt = {id:item.id, sha256:await hash(await blob.arrayBuffer()),
      prompt_sha256:await hash(new TextEncoder().encode(item.prompt)),
      conversation:location.href, message_id:matchedUser(item.prompt).getAttribute('data-message-id'),
      method:'single-turn exact prompt match and completed generated image', at:Date.now()/1000};
    const receiptUrl = URL.createObjectURL(new Blob([JSON.stringify(receipt)], {type:'application/json'}));
    const receiptLink = document.createElement('a');
    receiptLink.href = receiptUrl; receiptLink.download = `${item.id}.receipt.json`;
    document.body.appendChild(receiptLink); receiptLink.click();
    setTimeout(()=>{URL.revokeObjectURL(receiptUrl);receiptLink.remove();},5000);
    return blob.size;
  }

  async function run() {
    if (S.running) { note('すでに動作中'); return; }
    S.running = true; S.stop = false;
    const queue = window.__yamaQueue || [];

    for (const item of queue) {
      if (S.stop) { note('停止指示'); break; }
      if (S.done.includes(item.id)) continue;
      S.current = item.id;

      try {
        let img;
        if (!busy() && completedImages(item.prompt).length) {
          note(`${item.id} 同じ会話の完成結果を保存します（再送なし）`);
          await waitIdle(15000, item.prompt);
          img = completedImages(item.prompt);
        } else if (matchedUser(item.prompt) && busy()) {
          note(`${item.id} 同じ会話の処理を引き継ぎます（再送なし）`);
          img = await waitImage(item.prompt);
        } else {
          await newChat();
          await sleep(1500);
          S.waitState = null;
          await send(item.prompt);
          img = await waitImage(item.prompt);
        }

        // 回数では制限を確定しない。明示された表示と観測時刻を保持する。
        if (img === 'limit' && !S.limitEvidence) throw new Error('制限表示の根拠を確認できません');
        // 上限は「書いてある時刻まで待つ」のではなく、一定間隔で投げ直して
        // 通った瞬間に再開する。これなら解除が5時間後でも20時間後でも取りこぼさない。
        let waits = 0;
        while (img === 'limit' && !S.stop && waits < LIMIT_MAX_TRIES) {
          waits++;
          const wait = S.limitEvidence.kind === 'access_limit' ? 3 : nextProbeMin();
          const detail = limitNote();
          S.waitState = {kind:S.limitEvidence.kind, evidence:S.limitEvidence, retryAt:Date.now()/1000+wait*60};
          note(`${S.waitState.kind === 'image_limit' ? '画像生成の上限表示を確認' : 'アクセス頻度の制限表示を確認'}（${detail}）— ${wait}分後に再試行 (${waits}回目)`);
          for (let m = 0; m < wait && !S.stop; m++) await sleep(60000);
          if (S.stop) break;
          await newChat();
          await sleep(1500);
          S.waitState = null;
          await send(item.prompt);
          img = await waitImage(item.prompt);
        }
        if (S.stop) break;
        if (img === 'limit') { note('上限が32時間空かなかったので停止'); S.stop = true; break; }

        if (img === 'retry') {
          note(`${item.id} エラー → 再試行`);
          retryBtn().click();
          img = await waitImage(item.prompt);
          if (img === 'limit') { note('再試行中に上限 — 次の周回で拾い直します'); throw new Error('上限'); }
          if (img === 'retry') throw new Error('2回続けて生成エラー');
        }

        S.waitState = null;
        const bytes = await saveAs(img, item);
        S.done.push(item.id);
        saveDone(S.done);
        note(`${item.id} 保存 ${Math.round(bytes / 1024)}KB (${S.done.length}/${queue.length})`);
      } catch (e) {
        S.failed.push({ id: item.id, error: e.message });
        note(`${item.id} 失敗: ${e.message}`);
      }
      await sleep(4000);   // 連投しすぎない
    }
    S.current = null;
    S.running = false;
    note(`ループ終了 完了${S.done.length} 失敗${S.failed.length}`);
  }

  window.__yamaRun = run;
  console.log('[yama] 準備OK。__yamaRun() で開始');
})();
