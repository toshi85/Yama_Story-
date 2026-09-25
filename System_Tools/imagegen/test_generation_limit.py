import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import run
# 並列配分の単体テスト。関所（generation_gate.py）は test_generation_gate.py で別に検査し、ここでは本物の合格票・見本枠に触れない
run.generation_gate_filter = lambda work, todo: todo


class AccessLimitTest(unittest.TestCase):
    def test_access_limit_message_reports_exit_and_external_restart(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / '.imagegen').mkdir()
            with patch.object(run, 'js', side_effect=[True, None]), \
                    patch.object(run.time, 'time', return_value=1000), \
                    patch.object(run.time, 'sleep') as sleep, \
                    patch('builtins.print') as output:
                with self.assertRaises(SystemExit) as raised:
                    run.handle_access_limit(work)
            self.assertEqual(raised.exception.code, 75)
            sleep.assert_not_called()
            message = output.call_args.args[0]
            self.assertIn('終了コード75で停止', message)
            self.assertIn('外部から実行', message)
            self.assertNotIn('自動再開', message)

    def test_detected_limit_stops_sending_and_waits_before_retry(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / '.imagegen').mkdir()
            with patch.object(run, 'js', side_effect=[True, None]) as js, patch.object(run.time, 'time', return_value=1000):
                with self.assertRaises(SystemExit) as raised:
                    run.handle_access_limit(work)
                self.assertEqual(raised.exception.code, 75)
                self.assertEqual(js.call_count, 2)
            self.assertEqual(json.loads((work / '.imagegen/access_limit.json').read_text())['until'], 1180)
            with patch.object(run, 'js', return_value=True) as js, patch.object(run.time, 'time', return_value=1100):
                with self.assertRaises(SystemExit):
                    run.handle_access_limit(work)
                js.assert_called_once()
                self.assertIn('b.click()', js.call_args.args[0])
                self.assertEqual(json.loads((work / '.imagegen/access_limit.json').read_text())['until'], 1180)
            with patch.object(run, 'js', return_value=False), patch.object(run.time, 'time', return_value=1181):
                run.handle_access_limit(work)
            self.assertFalse((work / '.imagegen/access_limit.json').exists())


class ParallelAccessWaitTest(unittest.TestCase):
    def simulate(self, limits=1, save_between=False):
        class Clock:
            now = 1000.0
            def sleep(self, seconds):
                self.now += seconds
        clock = Clock()
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            queue = [{'id':'a','prompt':'pa'},{'id':'b','prompt':'pb'}]
            (work/'image_queue.json').write_text(json.dumps(queue))
            completed, active, detections, resumes = set(), {}, [], []
            phase = 0
            targets=[{'id':'w1'},{'id':'w2'}]
            def snapshot(target, key):
                worker=target['id']
                state=dict(installed=True,running=False,busy=False,failed=[],liveLimit=None,shared=None,until=0)
                item=active.get(worker)
                if not item:
                    return state
                state['running']=True
                if phase < limits:
                    if save_between and phase==1 and worker=='w1':
                        completed.add(item)
                        state['running']=False
                    elif worker==('w2' if save_between and phase>=1 else 'w1'):
                        state['liveLimit']={'kind':'access_limit','source':'dialog','text':'リクエストが多すぎます。数分待ってから。'}
                else:
                    completed.add(item)
                    state['running']=False
                return state
            def resume(targets, scheduler, key, pacer):
                nonlocal phase
                phase += 1
                resumes.append(clock.now)
                scheduler.stopped=False
            original_detect=run.AccessCooldown.detect
            def detect(access, evidence):
                result=original_detect(access,evidence)
                detections.append({'at':clock.now,'until':access.until,'count':access.consecutive})
                return result
            with patch.object(run.bridge,'tabs',return_value=[]), \
                 patch.object(run.bridge,'new_window',side_effect=targets), \
                 patch.object(run,'ParallelDownloads'), patch.object(run,'js',return_value=True), \
                 patch.object(run,'collect'), \
                 patch.object(run,'remaining',side_effect=lambda w:(queue,[q for q in queue if q['id'] not in completed])), \
                 patch.object(run,'parallel_state',side_effect=snapshot), \
                 patch.object(run,'install_parallel',side_effect=lambda t,i,k:active.update({t['id']:i['id']})), \
                 patch.object(run,'stop_parallel',return_value=[]), \
                 patch.object(run,'dismiss_access_notice',return_value=True) as dismiss, \
                 patch.object(run,'resume_access_targets',side_effect=resume), \
                 patch.object(run.AccessCooldown,'detect',detect), \
                 patch.object(run.time,'time',side_effect=lambda:clock.now), \
                 patch.object(run.time,'sleep',side_effect=clock.sleep), patch('builtins.print'):
                code=0
                try:
                    run.run_parallel(work,2)
                except SystemExit as exc:
                    code=exc.code
            state=json.loads((work/'.imagegen/parallel_state.json').read_text())
            cooldown=json.loads((work/'.imagegen/access_limit.json').read_text())
            return dict(code=code,state=state,cooldown=cooldown,detections=detections,resumes=resumes,
                        dismiss=dismiss.call_count,has_image_limit=(work/'.imagegen/limit_until.json').exists())

    def test_access_limit_waits_five_minutes_then_resumes(self):
        result=self.simulate()
        self.assertEqual(result['code'],0)
        self.assertEqual(result['state']['status'],'finished')
        self.assertEqual(result['resumes'][0]-result['detections'][0]['at'],300)
        self.assertEqual(result['dismiss'],2)
        self.assertFalse(result['has_image_limit'])

    def test_four_consecutive_limits_exit_75_with_twenty_minute_cooldown(self):
        result=self.simulate(limits=4)
        self.assertEqual(result['code'],75)
        self.assertEqual(result['state']['status'],'access_stopped')
        self.assertEqual([x['until']-x['at'] for x in result['detections']],[300,600,900,1200])
        self.assertEqual(len(result['resumes']),3)
        self.assertEqual(result['cooldown']['consecutive'],4)
        self.assertFalse(result['has_image_limit'])

    def test_saved_image_resets_consecutive_limit_count(self):
        result=self.simulate(limits=3,save_between=True)
        self.assertEqual(result['code'],0)
        self.assertEqual([x['count'] for x in result['detections']],[1,1,2])
        self.assertEqual([x['until']-x['at'] for x in result['detections']],[300,300,600])
        self.assertEqual(result['cooldown']['consecutive'],0)

    def test_retry_count_is_not_a_generic_failure(self):
        result=self.simulate(limits=3)
        self.assertEqual(result['code'],0)
        self.assertEqual(result['state']['failures'],0)


if __name__ == '__main__':
    unittest.main()
