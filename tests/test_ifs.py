import unittest

import ifs


class IfsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = ifs.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Workshop IFS', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
