"""中央配分と全体停止を、ChatGPTへ送信せず検査する。"""
import contextlib
import json
import io
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import run
# 並列配分の単体テスト。関所（generation_gate.py）は test_generation_gate.py で別に検査し、ここでは本物の合格票・見本枠に触れない
run.generation_gate_filter = lambda work, todo: todo


class QueueTests(unittest.TestCase):
    def queue(self, count=6):
        return run.ParallelQueue([{'id': str(i), 'prompt': f'p{i}'} for i in range(count)])

    def test_no_duplicates_or_omissions_with_uneven_workers(self):
        q = self.queue()
        assigned = []
        for worker in ['a', 'b', 'c', 'b', 'b', 'a']:
            if worker in q.inflight:
                q.finish(worker, True)
            assigned.append(q.assign(worker)['id'])
            self.assertEqual(len(set(q.inflight.values())), len(q.inflight))
        self.assertEqual(set(assigned), set('012345'))
        self.assertEqual(len(assigned), 6)
        self.assertIsNone(q.assign('d'))

    def test_busy_worker_does_not_receive_second_item(self):
        q = self.queue()
        q.assign('a')
        self.assertIsNone(q.assign('a'))
        self.assertEqual(len(q.pending), 5)

    def test_failure_requeues_once_without_loss(self):
        q = self.queue(2)
        q.assign('a')
        q.assign('b')
        q.finish('a', False)
        self.assertEqual(q.assign('a')['id'], '0')
        q.finish('a', True)
        q.finish('b', True)
        self.assertFalse(q.pending)
        self.assertFalse(q.inflight)
        self.assertEqual((q.failures, q.retries), (1, 1))

    def test_second_failure_gives_up_that_item_and_keeps_going(self):
        # 2026-09-26: 2回失敗したカットだけ外し、残りを作り続ける（全体を止めると数分〜9分止まっていた）
        q = self.queue()
        first = q.assign('a')['id']; q.finish('a', False)
        ids = []
        while True:
            item = q.assign('a')
            if item is None:
                break
            ids.append(item['id'])
            q.finish('a', item['id'] != first)
        self.assertFalse(q.stopped)
        self.assertEqual(q.gave_up, [first])
        self.assertEqual(ids[-1], first)            # やり直しは列の最後
        self.assertEqual(len(set(ids)), len(q.items))  # 他のカットは全部回った

    def test_limit_stops_all_workers(self):
        q = self.queue()
        q.assign('a'); q.assign('b')
        q.stop()
        q.finish('a', True)
        for worker in ['a', 'b', 'c']:
            self.assertIsNone(q.assign(worker))
        self.assertEqual(sum(q.attempts.values()), 2)

    def test_duplicate_input_rejected(self):
        with self.assertRaises(ValueError):
            run.ParallelQueue([{'id': 'a'}, {'id': 'a'}])

    def test_regen_invocation_keeps_work_only_interface(self):
        args = run.parse_args(['/tmp/regen_work'])
        self.assertEqual(args.work, '/tmp/regen_work')
        self.assertEqual(args.parallel, run.DEFAULT_PARALLEL)
        self.assertEqual(run.parse_args(['/tmp/work', '--parallel', '3']).parallel, 3)

    def test_invalid_parallel(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            run.parse_args(['/tmp/work', '--parallel', '0'])


class IntegrationTests(unittest.TestCase):
    def simulate(self, failure=False, limit=False, budget=None, external=False, exclude='', exclude_slots='', count=3):
        with TemporaryDirectory() as temp:
            work = Path(temp)
            queue = [{'id': str(i), 'prompt': f'p{i}', 'slot': ('bg' if i == 3 else 'still' if i == 4 else 'char')} for i in range(6)]
            (work / 'images').mkdir()
            (work / 'image_queue.json').write_text(json.dumps(queue))
            completed, active, attempts, stops = set(), {}, [], []
            targets = [{'id': str(i), 'webSocketDebuggerUrl': f'ws://{i}'} for i in range(3)]
            ticks = 0
            def snapshot(target, key):
                nonlocal ticks
                ticks += 1
                worker = target['id']
                item = active.pop(worker, None)
                failed = []
                evidence = None
                if item:
                    if failure and item == '0' and attempts.count(item) == 1:
                        failed = [{'id': item, 'error': 'mock failure'}]
                    elif limit and item == '1':
                        evidence = {'kind': 'image_limit', 'text': '画像生成の利用上限に達しました'}
                    else:
                        completed.add(item)
                return dict(installed=True, running=False, busy=False, failed=failed,
                            liveLimit=evidence, shared=None, until=9999999999000,
                            done=list(completed), text='', log=[])
            def install(target, item, key):
                self.assertNotIn(item['id'], active.values())
                active[target['id']] = item['id']
                attempts.append(item['id'])
                if external and len(attempts) == 1:
                    # 最初の生成中に別プロセスが次の画像を保存する。
                    subprocess.run([run.sys.executable, '-B', '-c',
                                    'from pathlib import Path; import sys; Path(sys.argv[1]).write_bytes(b"png")',
                                    str(work / 'images/1.png')], check=True)
            with patch.object(run.bridge, 'tabs', return_value=[]), \
                 patch.object(run.bridge, 'new_window', side_effect=targets), \
                 patch.object(run, 'ParallelDownloads'), \
                 patch.object(run, 'js', return_value=True), \
                 patch.object(run, 'collect'), \
                 patch.object(run, 'remaining', side_effect=lambda w: (queue, [q for q in queue if q['id'] not in completed])), \
                 patch.object(run, 'parallel_state', side_effect=snapshot), \
                 patch.object(run, 'install_parallel', side_effect=install), \
                 patch.object(run, 'stop_parallel', side_effect=lambda ts,k: stops.extend(ts) or []), \
                 patch.object(run.time, 'sleep'):
                try:
                    run.run_parallel(work, count, max_attempts=budget, exclude=exclude, exclude_slots=exclude_slots)
                    exit_code = 0
                except SystemExit as exc:
                    exit_code = exc.code
                except RuntimeError:
                    exit_code = 1
            state = json.loads((work / '.imagegen/parallel_state.json').read_text())
            until = work / '.imagegen/limit_until.json'
            return attempts, stops, state, exit_code, until.exists()

    def test_external_save_skipped_at_next_dispatch(self):
        for count in (1, 3):
            with self.subTest(count=count):
                attempts, _, state, code, _ = self.simulate(external=True, count=count)
                self.assertEqual(attempts, ['0', '2', '3', '4', '5'])
                self.assertEqual((code, state['status'], state['retries']), (0, 'finished', 0))

    def test_exclude_ids_are_never_dispatched(self):
        attempts, _, state, code, _ = self.simulate(exclude='1,4')
        self.assertEqual(attempts, ['0', '2', '3', '5'])
        self.assertEqual((code, state['remaining_ids']), (0, []))

    def test_exclude_slots_uses_queue_metadata(self):
        attempts, _, state, code, _ = self.simulate(exclude_slots='bg,still')
        self.assertEqual(attempts, ['0', '1', '2', '5'])
        self.assertEqual((code, state['remaining_ids']), (0, []))

    def test_combined_exclusions(self):
        attempts, _, _, code, _ = self.simulate(exclude='1', exclude_slots='bg,still')
        self.assertEqual(attempts, ['0', '2', '5'])
        self.assertEqual(code, 0)

    def test_all_excluded_does_not_open_windows_or_change_queue(self):
        with TemporaryDirectory() as temp:
            work = Path(temp)
            queue = [{'id': 'x', 'slot': 'bg', 'prompt': 'p'}]
            path = work / 'image_queue.json'
            path.write_text(json.dumps(queue))
            before = path.read_bytes()
            with patch.object(run, 'collect'), patch.object(run.bridge, 'new_window') as create:
                run.run_parallel(work, 2, exclude_slots='bg')
            create.assert_not_called()
            self.assertEqual(path.read_bytes(), before)

    def test_skip_logs_reasons_and_does_not_count_attempts(self):
        with TemporaryDirectory() as temp:
            work = Path(temp)
            (work / 'images').mkdir()
            (work / 'images/a.png').write_bytes(b'png')
            queue = [{'id': 'a'}, {'id': 'b'}, {'id': 'c'}]
            skip = run.DispatchFilter(work, queue, exclude='b')
            scheduler = run.ParallelQueue(queue)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(scheduler.assign('w', skip)['id'], 'c')
            self.assertEqual(scheduler.attempts, {'c': 1})
            self.assertIn('飛ばした：a（保存済み）', output.getvalue())
            self.assertIn('飛ばした：b（除外指定）', output.getvalue())

    def test_cli_accepts_both_exclusions(self):
        args = run.parse_args(['/tmp/work', '--exclude', 'a,b', '--exclude-slots', 'bg,still'])
        self.assertEqual((args.exclude, args.exclude_slots), ('a,b', 'bg,still'))

    def test_single_window_uses_dispatch_filter(self):
        with TemporaryDirectory() as temp, patch.object(run, 'prepare_work'), \
                patch.object(run, 'acquire_lock'), patch.object(run.bridge, 'start'), \
                patch.object(run, 'run_parallel') as start, \
                patch.object(run.sys, 'argv', ['run.py', temp, '--parallel', '1', '--exclude-slots', 'bg,still']):
            run.main()
            self.assertEqual(start.call_args.args[1], 1)
            self.assertEqual(start.call_args.kwargs['exclude_slots'], 'bg,still')

    def test_complete_saves_all_six(self):
        attempts, stops, state, code, _ = self.simulate()
        self.assertEqual(len(attempts), 6)
        self.assertEqual(len(set(attempts)), 6)
        self.assertEqual((code, state['status'], state['failures']), (0, 'finished', 0))
        self.assertEqual(len(stops), 3)

    def test_real_loop_requeues_failed_item(self):
        attempts, _, state, code, _ = self.simulate(failure=True)
        self.assertEqual((len(attempts), attempts.count('0')), (7, 2))
        self.assertEqual((code, state['failures'], state['retries']), (0, 1, 1))

    def test_limit_seen_after_success_stops_before_dispatch(self):
        attempts, stops, state, code, limit_file = self.simulate(limit=True)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(len(stops), 3)
        self.assertEqual((code, state['status'], limit_file), (75, 'limit_wait', True))
        self.assertEqual(state['evidence']['kind'], 'image_limit')

    def test_bench_budget_bounds_retry_dispatch(self):
        attempts, _, state, code, _ = self.simulate(failure=True, budget=6)
        self.assertEqual(len(attempts), 6)
        self.assertEqual(code, 1)

    def test_new_window_waits_for_execution_context(self):
        with patch.object(run, 'js', side_effect=[RuntimeError('Cannot find default execution context'), False, True]) as js, patch.object(run.time, 'sleep'):
            run.wait_parallel_login({'id': 'new'})
        self.assertEqual(js.call_count, 3)

    def test_login_does_not_hide_other_errors(self):
        with patch.object(run, 'js', side_effect=RuntimeError('connection lost')), self.assertRaisesRegex(RuntimeError, 'connection lost'):
            run.wait_parallel_login({'id': 'new'})

    def test_saved_limit_blocks_before_opening_browser(self):
        with TemporaryDirectory() as temp:
            work = Path(temp)
            (work / '.imagegen').mkdir()
            (work / '.imagegen/limit_until.json').write_text(json.dumps({'until': 9999999999}))
            with patch.object(run.bridge, 'new_window') as create, self.assertRaises(SystemExit) as error:
                run.run_parallel(work, 3)
            self.assertEqual(error.exception.code, 75)
            create.assert_not_called()

    def test_targeted_js_uses_requested_window(self):
        response = {'result': {'result': {'value': 7}}}
        with patch.object(run.bridge, 'tabs') as tabs, patch.object(run.bridge, 'command', return_value=response) as cmd:
            self.assertEqual(run.js('7', target={'webSocketDebuggerUrl': 'ws://second'}), 7)
            self.assertEqual(cmd.call_args.args[0], 'ws://second')
            tabs.assert_not_called()

    def test_new_window_uses_cdp_new_window_flag(self):
        bridge = run.bridge
        with patch.object(bridge, '_http', return_value={'webSocketDebuggerUrl': 'ws://browser'}), \
             patch.object(bridge, 'command', return_value={'result': {'targetId': 'new'}}) as cmd, \
             patch.object(bridge, 'tabs', return_value=[{'id': 'new'}]):
            self.assertEqual(bridge.new_window()['id'], 'new')
        self.assertEqual(cmd.call_args.args[2], {'url': 'https://chatgpt.com/', 'newWindow': True})

    def test_driver_shared_limit_prevents_sending_and_isolates_progress(self):
        script = r"""
const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
let shared={}, localWrites=0, sessionWrites=0;
const ctx={window:{__yamaParallel:{limitKey:'test'}},Date,console:{log(){}},
  localStorage:{getItem:k=>shared[k]||null,setItem(k,v){shared[k]=v;localWrites++;}},
  sessionStorage:{getItem:()=>null,setItem(){sessionWrites++;}},
  document:{querySelector:()=>null,querySelectorAll:()=>[]}};
let src=fs.readFileSync(process.argv[1],'utf8').replace('window.__yamaRun = run;',
  'window.test={checkSending,limitHit}; window.__yamaRun=run;');
vm.runInNewContext(src,ctx);
ctx.window.__yamaGen.forget();
assert.equal(sessionWrites,1);assert.equal(localWrites,0);
ctx.window.test.checkSending();
shared.test=JSON.stringify({evidence:{kind:'image_limit'}});
assert.throws(()=>ctx.window.test.checkSending(),/投入停止/);
shared={};
ctx.document.querySelectorAll=s=>s.includes('role=dialog')?[{innerText:'画像生成の利用上限に達しました。上限は3時間後にリセット'}]:[];
assert.equal(ctx.window.test.limitHit(),true);
assert.equal(JSON.parse(shared.test).evidence.kind,'image_limit');
assert.ok(JSON.parse(shared.test).until > Date.now());
assert.throws(()=>ctx.window.test.checkSending(),/投入停止/);
console.log('shared limit / session progress PASS');
"""
        result = subprocess.run(['node', '-e', script, str(run.DRIVER)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


class DownloadSessionTests(unittest.TestCase):
    class Socket:
        def __init__(self, response):
            import struct
            payload = json.dumps(response).encode()
            self.data = b'HTTP/1.1 101 Switching Protocols\r\n\r\n' + bytes([129, 126]) + struct.pack('>H', len(payload)) + payload
            self.closed = False
            self.sent = []
        def sendall(self, data):
            self.sent.append(data)
        def recv(self, size):
            result, self.data = self.data[:size], self.data[size:]
            return result
        def close(self):
            self.closed = True

    def test_download_policy_session_stays_open_until_collection_finishes(self):
        sock = self.Socket({'id': 1, 'result': {}})
        with TemporaryDirectory() as tmp, patch.object(run.bridge, '_http', return_value={'webSocketDebuggerUrl': 'ws://localhost:9222/devtools/browser/test'}), patch.object(run.socket, 'create_connection', return_value=sock):
            downloads = run.ParallelDownloads(Path(tmp) / 'images')
            self.assertFalse(sock.closed, '設定応答直後に切断すると保存先が既定値へ戻る')
            frame = sock.sent[1]
            length = int.from_bytes(frame[2:4], 'big')
            mask, payload = frame[4:8], frame[8:8+length]
            command = json.loads(bytes(b ^ mask[i % 4] for i,b in enumerate(payload)))
            self.assertEqual(command['method'], 'Browser.setDownloadBehavior')
            self.assertEqual(command['params']['downloadPath'], str((Path(tmp)/'images').resolve()))
            downloads.close()
            self.assertTrue(sock.closed)

    def test_download_policy_error_closes_session(self):
        sock = self.Socket({'id': 1, 'error': {'message': 'denied'}})
        with TemporaryDirectory() as tmp, patch.object(run.bridge, '_http', return_value={'webSocketDebuggerUrl': 'ws://localhost:9222/devtools/browser/test'}), patch.object(run.socket, 'create_connection', return_value=sock), self.assertRaisesRegex(RuntimeError, 'denied'):
            run.ParallelDownloads(tmp)
        self.assertTrue(sock.closed)


class SendPacingTests(unittest.TestCase):
    def test_two_windows_use_actual_send_ack_and_sixty_seconds(self):
        pacer = run.SendPacer(60)
        self.assertTrue(pacer.reserve('window1', {'id':'a', 'token':'a1'}, 1000))
        # ウィンドウ1が遅れて実際に送ったのは30秒後。割当て時刻からは数えない。
        self.assertFalse(pacer.reserve('window2', {'id':'b', 'token':'b1'}, 1100))
        pacer.observe({'window1': {'sentToken':'a1','sentAt':1030}}, 1032)
        self.assertFalse(pacer.reserve('window2', {'id':'b', 'token':'b1'}, 1091.99))
        self.assertTrue(pacer.reserve('window2', {'id':'b', 'token':'b1'}, 1092))
        pacer.observe({'window2': {'sentToken':'b1','sentAt':1092.2}}, 1094)
        self.assertGreaterEqual(pacer.sends[1]['sent_at']-pacer.sends[0]['sent_at'], 60)

    def test_interval_survives_restart(self):
        pacer = run.SendPacer(60, {'last_sent_at':1032})
        self.assertFalse(pacer.ready(1091))
        self.assertTrue(pacer.ready(1092))

    def test_cancelled_unconfirmed_grant_keeps_safe_gap(self):
        pacer = run.SendPacer(60)
        pacer.reserve('w1', {'id':'a','token':'a1'}, 1000)
        pacer.cancel(1050)
        self.assertFalse(pacer.ready(1109))
        self.assertTrue(pacer.ready(1110))

    def test_only_assigned_id_gets_a_grant(self):
        pacer=run.SendPacer(60)
        targets=[{'id':'w1'},{'id':'w2'}]
        states={'w1':{'sendRequest':{'id':'wrong','token':'x'}},
                'w2':{'sendRequest':{'id':'b','token':'b1'}}}
        with patch.object(run, 'js', return_value=True) as js, patch.object(run.time, 'time', return_value=1000):
            run.grant_next_send(pacer, targets, states, {'w1':'a','w2':'b'}, lambda:None)
        self.assertEqual(js.call_count,1)
        self.assertEqual(js.call_args.kwargs['target']['id'],'w2')
        self.assertEqual(pacer.pending['id'],'b')

    def test_interval_argument_default_and_validation(self):
        self.assertEqual(run.parse_args(['work']).min_interval,60)
        self.assertEqual(run.parse_args(['work','--min-interval','90']).min_interval,90)
        for value in ['-1','nan','inf']:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                run.parse_args(['work','--min-interval',value])

    def test_driver_does_not_send_without_python_grant(self):
        script = r"""
const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
let clock=1000000,sent=0,timers=[];
class Clock extends Date {static now(){return clock;}}
const editor={innerText:'approved prompt',focus(){}};
const button={disabled:false,click(){sent++}};
const ctx={window:{__yamaParallel:{limitKey:'limit',paced:true}},Date:Clock,Math,Promise,
 console:{log(){}},sessionStorage:{getItem:()=>null,setItem(){}},localStorage:{getItem:()=>null,setItem(){}},
 document:{execCommand(){},querySelector:s=>s==='#prompt-textarea'?editor:s.includes('send-button')?button:null,
  querySelectorAll:s=>s.includes('data-message-author-role')&&sent?[{innerText:'approved prompt'}]:[]},
 setTimeout(fn,ms){timers.push({at:clock+ms,fn})}};
let src=fs.readFileSync(process.argv[1],'utf8').replace('window.__yamaRun = run;', 'window.testSend=send; window.__yamaRun=run;');
vm.runInNewContext(src,ctx);ctx.window.__yamaGen.current='a';
async function tick(ms){clock+=ms;const due=timers.filter(t=>t.at<=clock);timers=timers.filter(t=>t.at>clock);due.forEach(t=>t.fn());for(let i=0;i<10;i++)await Promise.resolve();}
(async()=>{
 const promise=ctx.window.testSend('approved prompt');
 await tick(300);assert.equal(sent,0);assert.ok(ctx.window.__yamaGen.sendRequest);
 await tick(60000);assert.equal(sent,0,'60秒経過だけでは送信しない');
 const token=ctx.window.__yamaGen.sendRequest.token;
 ctx.window.__yamaGen.sendGrant=token;
 await tick(200);assert.equal(sent,1);assert.equal(ctx.window.__yamaGen.sentToken,token);
 await tick(500);await promise;assert.equal(ctx.window.__yamaGen.sendRequest,null);
 console.log('driver central grant PASS');
})().catch(e=>{console.error(e);process.exitCode=1});
"""
        result=subprocess.run(['node','-e',script,str(run.DRIVER)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('central grant PASS',result.stdout)


if __name__ == '__main__':
    unittest.main()
