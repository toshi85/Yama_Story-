import unittest
from run import observed_generation_state


class LimitReportingTest(unittest.TestCase):
    def test_old_log_does_not_mean_current_limit(self):
        state = {'last': '生成上限—20分待ち', 'busy': True}
        self.assertEqual(observed_generation_state(state)['status'], 'generating')

    def test_error_is_not_a_quota(self):
        self.assertEqual(observed_generation_state({'retryVisible': True, 'busy': True})['status'], 'retrying')

    def test_quota_requires_current_explicit_evidence(self):
        evidence = {'kind': 'image_limit', 'text': '画像生成の利用上限に達しました', 'observedAt': 123}
        self.assertEqual(observed_generation_state({'liveLimit': evidence})['status'], 'limit_wait')
        self.assertEqual(observed_generation_state({'waitState': {'evidence': evidence, 'retryAt': 456}})['status'], 'scheduled_wait')


if __name__ == '__main__':
    unittest.main()
