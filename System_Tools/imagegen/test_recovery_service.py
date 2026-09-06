import fcntl
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import time
import unittest

from recovery_service import run_worker


class RecoveryServiceTest(unittest.TestCase):
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
