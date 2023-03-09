"""system モジュールのテスト."""

import unittest

from language.system import System


class TestSystem(unittest.TestCase):

    def test_init(self):
        system = System()
        self.assertIsNotNone(system.dictionaries)


if __name__ == '__main__':
    unittest.main()
