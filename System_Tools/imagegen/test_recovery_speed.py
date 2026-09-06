import unittest
from recover import already_verified


class RecoverySpeedTest(unittest.TestCase):
    def test_skip_image_load_only_after_exact_verified_request(self):
        data = {'url': 'chat', 'ready': 'complete', 'busy': False, 'users': [{'text': 'bear'}], 'images': []}
        lookup = {'bear': [{'id': 'one'}, {'id': 'two'}]}
        self.assertFalse(already_verified(data, 'chat', lookup, {'one'}))
        self.assertTrue(already_verified(data, 'chat', lookup, {'one', 'two'}))
        self.assertFalse(already_verified(data, 'other-chat', lookup, {'one', 'two'}))
        data['busy'] = True
        self.assertFalse(already_verified(data, 'chat', lookup, {'one', 'two'}))
        data['busy'] = False
        data['users'][0]['text'] = 'house'
        self.assertFalse(already_verified(data, 'chat', lookup, {'one', 'two'}))


if __name__ == '__main__':
    unittest.main()
