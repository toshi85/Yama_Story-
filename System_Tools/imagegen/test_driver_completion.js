const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const source = fs.readFileSync(__dirname + '/driver.js', 'utf8');
let clock = 0, busy = true, reloads = 0;
class Clock extends Date { static now() { return clock; } }
const buttons = ['画像を編集', 'この画像を共有する'].map(label => ({getAttribute:()=>label}));
const card = {querySelectorAll:()=>buttons,parentElement:null};
const img = {src:'https://chatgpt.com/backend-api/estuary/content?id=file_test',complete:true,naturalWidth:1024,querySelectorAll:()=>[],parentElement:card};
const context = {
  window:{},console:{log(){}},localStorage:{getItem:()=>null,setItem(){}},
  document:{body:{innerText:''},
    querySelector:s=>s.includes('stop-button')&&busy?{}:null,
    querySelectorAll:s=>s==='main img'?[img]:s.includes('data-message-author-role')?[{innerText:'approved prompt'}]:[],
  },
  location:{reload(){reloads++;}},Date:Clock,Promise,
  setTimeout(fn, ms){clock+=ms;fn();},
};
vm.runInNewContext(source.replace('window.__yamaRun = run;', 'window.__test={completedImages,waitIdle};window.__yamaRun=run;'),context);
(async()=>{
  const t=context.window.__test;
  assert.equal(t.completedImages('wrong prompt').length,0);
  img.complete=false;
  assert.equal(t.completedImages('approved prompt').length,0);
  await t.waitIdle(6000,'approved prompt');
  assert.equal(reloads,0,'途中画像は再読込しない');
  img.complete=true;
  assert.equal(t.completedImages('approved prompt').length,1);
  t.waitIdle(60000,'approved prompt');
  for(let n=0;n<100&&reloads===0;n++)await Promise.resolve();
  assert.equal(reloads,1,'完成操作の表示が20秒安定したら同じ会話を再読込');
  busy=false;
  assert.equal(await t.waitIdle(15000,'approved prompt'),true);
  assert.equal(reloads,1,'正常完了時は再読込不要');
  console.log('completion-state regression checks passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
