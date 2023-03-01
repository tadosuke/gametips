"""weapon モジュールのテスト."""

import unittest

from battlestatus.weapon import Weapon, WeaponId


class TestWeapon(unittest.TestCase):

    def test_init(self):
        w = Weapon(WeaponId.COPPER_SWORD)
        self.assertEqual(WeaponId.COPPER_SWORD, w.id)
        self.assertEqual(1, w.level)

        w = Weapon(WeaponId.STEEL_SWORD)
        self.assertEqual(WeaponId.STEEL_SWORD, w.id)

    def test_base_atk(self):
        w = Weapon(WeaponId.IRON_SWORD)
        self.assertEqual(10, w._get_base_atk())

        w = Weapon(WeaponId.STEEL_SWORD)
        self.assertEqual(15, w._get_base_atk())

    def test_level_atk(self):
        w = Weapon(WeaponId.IRON_SWORD)
        w.set_level(2)
        self.assertAlmostEqual(2.0, w._calc_level_atk())
        w.set_level(3)
        self.assertAlmostEqual(4.0, w._calc_level_atk())

        with self.assertRaises(AssertionError):
            w.set_level(-1)


if __name__ == '__main__':
    unittest.main()