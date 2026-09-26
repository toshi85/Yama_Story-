/* Canvasアニメをコマ送りでPNGに書き出す（Chrome DevTools Protocol直叩き・依存なし）
   使い方: node capture.mjs <html> <outDir> [startFrame] [endFrame]
   Node 22+ の組み込み WebSocket / fetch を使う。Playwrightのブラウザ配置は不要。 */
import { spawn } from 'node:child_process';
import { mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { tmpdir } from 'node:os';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const html = resolve(process.argv[2] || 'kazuno_sample.html');
const outDir = resolve(process.argv[3] || 'frames');
const argStart = process.argv[4] ? parseInt(process.argv[4], 10) : null;
const argEnd = process.argv[5] ? parseInt(process.argv[5], 10) : null;
const PORT = 9333 + (process.pid % 200);

mkdirSync(outDir, { recursive: true });

const profile = `${tmpdir()}/cdpcap-${process.pid}`;
const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
  '--hide-scrollbars', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  '--force-device-scale-factor=1', '--window-size=1920,1080',
  '--disable-lcd-text', '--font-render-hinting=none',
  'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe'] });
chrome.stderr.on('data', () => {});

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function wsUrl() {
  for (let i = 0; i < 100; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/list`);
      const list = await r.json();
      const page = list.find(t => t.type === 'page');
      if (page?.webSocketDebuggerUrl) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(120);
  }
  throw new Error('Chrome の DevTools に接続できませんでした');
}

class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.waiting = new Map(); this.events = new Map();
    ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && this.waiting.has(m.id)) {
        const { ok, ng } = this.waiting.get(m.id); this.waiting.delete(m.id);
        m.error ? ng(new Error(JSON.stringify(m.error))) : ok(m.result);
      } else if (m.method && this.events.has(m.method)) {
        this.events.get(m.method).forEach(fn => fn(m.params));
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((ok, ng) => { this.waiting.set(id, { ok, ng }); this.ws.send(JSON.stringify({ id, method, params })); });
  }
  on(method, fn) { if (!this.events.has(method)) this.events.set(method, []); this.events.get(method).push(fn); }
}

const url = await wsUrl();
const ws = new WebSocket(url);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
const cdp = new CDP(ws);

await cdp.send('Page.enable');
await cdp.send('Runtime.enable');
await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: 'window.__capture=true;' });

const loaded = new Promise(r => cdp.on('Page.loadEventFired', r));
await cdp.send('Page.navigate', { url: `file://${html}` });
await loaded;
await sleep(500);

const meta = (await cdp.send('Runtime.evaluate', { expression: 'JSON.stringify(window.META)', returnByValue: true })).result.value;
const { TOTAL, FPS } = JSON.parse(meta);
const start = argStart ?? 0;
const end = argEnd ?? TOTAL;
console.log(`frames ${start}..${end - 1} / total ${TOTAL} @ ${FPS}fps -> ${outDir}`);

// FRAMES=60,270,690 のように指定すると、その番号だけ書き出す（見栄えの確認用）
const picks = process.env.FRAMES
  ? process.env.FRAMES.split(',').map(s => parseInt(s.trim(), 10)).filter(n => Number.isFinite(n))
  : null;
const list = picks || Array.from({ length: end - start }, (_, i) => start + i);

const t0 = Date.now();
for (const f of list) {
  const name = `${outDir}/f_${String(f).padStart(5, '0')}.png`;
  if (existsSync(name)) continue;                 // 中断再開できるようにスキップ
  await cdp.send('Runtime.evaluate', { expression: `window.stopPlayback&&window.stopPlayback();renderFrame(${f})`, returnByValue: true });
  const shot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false, fromSurface: true });
  writeFileSync(name, Buffer.from(shot.data, 'base64'));
  if ((f - start) % 60 === 0) {
    const el = (Date.now() - t0) / 1000;
    console.log(`  ${f}/${end}  ${el.toFixed(1)}s  (${((f - start + 1) / Math.max(el, 0.001)).toFixed(1)} fps)`);
  }
}
console.log(`DONE ${((Date.now() - t0) / 1000).toFixed(1)}s`);
ws.close();
chrome.kill();
process.exit(0);
