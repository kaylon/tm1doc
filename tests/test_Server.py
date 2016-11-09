import unittest

#currently there is no mock support
class test_Server(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def this_test_always_passes(self):
        self.assertTrue(True)

    def test_call_api_returns_valid_json(self):
        pass



if __name__ == '__main__':
    unittest.main()
