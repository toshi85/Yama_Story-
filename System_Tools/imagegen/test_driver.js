const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const src = fs.readFileSync(__dirname + '/driver.js', 'utf8');

// 再注入は、進行中のループと状態を変更しない。
const active = {running:true, current:'ASSET-111', done:['CHAR-01']};
const context = {window:{__yamaGen:active},console:{log(){}}};
vm.runInNewContext(src,context);
assert.equal(active.running,true);
assert.equal(active.current,'ASSET-111');
assert.deepEqual(active.done,['CHAR-01']);

// SPA遷移失敗時、以前の画像を新しい要求へ割り当てない。
const image = {src:'https://chatgpt.com/backend-api/estuary/content?id=file_old'};
const user = {innerText:'old prompt'};
const sandbox = {
  window:{}, console:{log(){}}, localStorage:{getItem(){return null;},setItem(){}},
  document:{querySelector(s){return s==='#prompt-textarea'?{}:null;},querySelectorAll(s){return s==='main img'?[image]:s.includes('data-message-author-role')?[user]:[];}},
  location:{pathname:'/c/old'},setTimeout(fn){fn();},Date,Promise,
};
vm.runInNewContext(src.replace('window.__yamaRun = run;', 'window.__test = {newChat, matchedUser, imgEls}; window.__yamaRun = run;'),sandbox);
assert.equal(sandbox.window.__test.matchedUser('new prompt'),null);
assert.equal(sandbox.window.__test.imgEls().length,1);
assert.rejects(sandbox.window.__test.newChat(),/新しいチャットへ移れていない/).then(()=>console.log('driver regression checks passed'));
