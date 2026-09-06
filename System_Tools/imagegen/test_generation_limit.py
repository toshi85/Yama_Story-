import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import run


class AccessLimitTest(unittest.TestCase):
    def test_detected_limit_stops_sending_and_waits_before_retry(self):
        with TemporaryDirectory() as tmp:
            work = Path(tmp)
            (work / '.imagegen').mkdir()
            with patch.object(run, 'js', side_effect=['リクエストが多すぎます', None]) as js, patch.object(run.time, 'time', return_value=1000):
                with self.assertRaises(SystemExit) as raised:
                    run.handle_access_limit(work)
                self.assertEqual(raised.exception.code, 75)
                self.assertEqual(js.call_count, 2)
            self.assertEqual(json.loads((work / '.imagegen/access_limit.json').read_text())['until'], 1900)
            with patch.object(run, 'js') as js, patch.object(run.time, 'time', return_value=1800):
                with self.assertRaises(SystemExit):
                    run.handle_access_limit(work)
                js.assert_not_called()
            with patch.object(run, 'js', side_effect=['リクエストが多すぎます', None]), patch.object(run.time, 'time', return_value=1901):
                run.handle_access_limit(work)
            self.assertFalse((work / '.imagegen/access_limit.json').exists())


if __name__ == '__main__':
    unittest.main()
