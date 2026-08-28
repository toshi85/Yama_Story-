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
  const S = (window.__yamaGen = window.__yamaGen || {});
  Object.assign(S, {
    stop: false, done: S.done || [], failed: S.failed || [], current: null, running: false,
    status: () => ({
      running: S.running, current: S.current,
      done: S.done.length, failed: S.failed.length,
      queue: (window.__yamaQueue || []).length,
      lastLog: S.log.slice(-6),
    }),
    log: S.log || [],
  });

  const LIMIT_WAIT_MIN = 20;   // 生成上限に当たったときに待つ分数

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const q = (s) => document.querySelector(s);
  const note = (m) => { S.log.push(`${new Date().toLocaleTimeString()} ${m}`); if (S.log.length > 200) S.log.shift(); };

  // 生成中は送信ボタンが停止ボタンに変わる。これが「まだ描いている」の唯一の証拠。
  const busy = () => !!q('[data-testid="stop-button"]');

  // ページに出ている画像。生成中のプレビューもここに入るので、単独では完了の証拠にならない。
  const imgEls = () => [...document.querySelectorAll('[class*="imagegen-image"] img')]
    .filter((i) => i.src && i.naturalWidth > 256);

  const retryBtn = () => [...document.querySelectorAll('button')]
    .find((b) => b.textContent.includes('再試行') || b.textContent.includes('Retry'));

  // 生成上限に当たっていないか
  const limitHit = () => /画像の生成上限|上限に達しました|rate limit|generation limit|しばらくお待ち/i
    .test(document.body.innerText.slice(-3000));

  // 停止ボタンが消えるまで待つ（＝生成が終わるまで）
  async function waitIdle(timeoutMs) {
    const t0 = Date.now();
    let quiet = 0;
    while (Date.now() - t0 < timeoutMs) {
      await sleep(2000);
      if (busy()) { quiet = 0; continue; }
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
      if (q('#prompt-textarea') && imgEls().length === 0) return;
    }
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
      if (b && !b.disabled) { b.click(); return; }
    }
    throw new Error('送信ボタンが出ない');
  }

  // 生成が終わるまで待って、完成画像を返す。エラー表示が出たら 'retry' を返す
  async function waitImage(timeoutMs = 600000) {
    const t0 = Date.now();
    // まず生成が始まるのを確認する（停止ボタンが出る）
    for (let i = 0; i < 20 && !busy(); i++) {
      await sleep(1000);
      if (retryBtn()) return 'retry';
      if (limitHit()) return 'limit';
    }
    const idle = await waitIdle(timeoutMs - (Date.now() - t0));
    if (idle === 'limit') return 'limit';
    if (!idle) throw new Error('生成タイムアウト');
    if (retryBtn()) return 'retry';
    if (limitHit()) return 'limit';
    await sleep(2000);
    const imgs = imgEls();
    if (!imgs.length) throw new Error('完了したのに画像が無い');
    return imgs.slice(-1)[0];
  }

  async function saveAs(img, filename) {
    const res = await fetch(img.src, { credentials: 'include' });
    if (!res.ok) throw new Error('画像取得 HTTP ' + res.status);
    const blob = await res.blob();
    if (blob.size < 300000) throw new Error('画像が小さすぎる（途中経過の疑い） ' + blob.size);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 5000);
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
        await newChat();
        await sleep(1500);
        await send(item.prompt);

        let img = await waitImage();

        // 生成上限は「終わり」ではなく「待てば空く」。夜通し回すので待って続ける。
        let waits = 0;
        while (img === 'limit' && !S.stop && waits < 24) {
          waits++;
          note(`生成上限 — ${LIMIT_WAIT_MIN}分待って再開します (${waits}回目)`);
          for (let m = 0; m < LIMIT_WAIT_MIN && !S.stop; m++) await sleep(60000);
          if (S.stop) break;
          await newChat();
          await sleep(1500);
          await send(item.prompt);
          img = await waitImage();
        }
        if (S.stop) break;
        if (img === 'limit') { note('上限待ちが続きすぎたので停止'); S.stop = true; break; }

        if (img === 'retry') {
          note(`${item.id} エラー → 再試行`);
          retryBtn().click();
          img = await waitImage();
          if (img === 'limit') { note('再試行中に上限 — 次の周回で拾い直します'); throw new Error('上限'); }
          if (img === 'retry') throw new Error('2回続けて生成エラー');
        }

        const bytes = await saveAs(img, `${item.id}.png`);
        S.done.push(item.id);
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
