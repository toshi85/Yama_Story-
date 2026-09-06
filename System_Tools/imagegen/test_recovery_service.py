import fcntl
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import unittest
import json
from unittest.mock import patch
import recovery_service

from recovery_service import run_worker


class RecoveryServiceTest(unittest.TestCase):
    def test_recovery_automatically_transitions_to_generation(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / 'image_queue.json').write_text(json.dumps([{'id': 'one'}]))
            argv = ['service', tmp, '--history', str(work / 'history'), '--generate-missing']
            with patch.object(sys, 'argv', argv), patch.object(recovery_service.signal, 'signal'), patch.object(recovery_service, 'notify'), patch.object(recovery_service, 'run_worker', return_value=0) as worker, patch.object(recovery_service, 'verified_ids', side_effect=[set(), {'one'}]):
                recovery_service.main()
            self.assertEqual(worker.call_count, 2)
            self.assertTrue(worker.call_args_list[0].args[0][2].endswith('recover.py'))
            self.assertTrue(worker.call_args_list[1].args[0][2].endswith('run.py'))
            self.assertEqual(json.loads((work / '.imagegen/service.json').read_text())['status'], 'finished')

    def test_hung_worker_is_killed_and_next_worker_runs(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / '.imagegen').mkdir()
            started = time.time()
            self.assertEqual(run_worker([sys.executable, '-c', 'import time; time.sleep(60)'], work, stall=.2, poll=.02), 124)
            self.assertLess(time.time() - started, 3)
            self.assertEqual(run_worker([sys.executable, '-c', 'pass'], work, poll=.02), 0)

    def test_generation_lock_prevents_recovery_start(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            with (work / '.imagegen.lock').open('w') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                result = subprocess.run([sys.executable, str(Path(__file__).with_name('recover.py')), str(work), '--history', str(work / 'unused')], capture_output=True, timeout=5)
                self.assertEqual(result.returncode, 75)


if __name__ == '__main__':
    unittest.main()
