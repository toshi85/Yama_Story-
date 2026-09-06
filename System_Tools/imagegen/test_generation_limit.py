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


if __name__ == '__main__':
    unittest.main()
