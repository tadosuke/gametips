"""weapon モジュールのテスト."""

import unittest

from weapon import Weapon


class TestWeapon(unittest.TestCase):

    def test_init(self):
        w = Weapon(0)
        self.assertEqual(0, w.id)


if __name__ == '__main__':
    unittest.main()
