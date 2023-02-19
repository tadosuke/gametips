"""damage モジュールのテスト."""

import unittest

from damage import Damage, AttackInfo, DefenceInfo, Attribute


class TestAttackInfo(unittest.TestCase):

    def test_init(self):
        at = AttackInfo(10, Attribute.FIRE)
        self.assertEqual(10, at.power)
        self.assertEqual(
            Attribute.FIRE, at.attribute)

    def test_minus(self):
        with self.assertRaises(ValueError):
            AttackInfo(-10)


class TestDefenceInfo(unittest.TestCase):

    def test_init(self):
        df = DefenceInfo(8)
        self.assertEqual(8, df.power)

    def test_minus(self):
        with self.assertRaises(ValueError):
            DefenceInfo(-10)

    def test_regist(self):
        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(10, res_dict)
        self.assertAlmostEqual(
            0.5,
            df.get_regist(Attribute.FIRE))
        self.assertAlmostEqual(
            1.0,
            df.get_regist(Attribute.WIND))


class TestDamage(unittest.TestCase):

    def test_init(self):
        at = AttackInfo(10)
        df = DefenceInfo(6)
        dmg = Damage(at, df)
        self.assertEqual(4, dmg.value)

    def test_attr_match(self):
        at = AttackInfo(10, Attribute.FIRE)

        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(6, res_dict)

        dmg = Damage(at, df)
        self.assertEqual(2, dmg.value)

    def test_attr_not_match(self):
        at = AttackInfo(10, Attribute.FIRE)

        res_dict = {
            Attribute.EARTH: 0.5,
        }
        df = DefenceInfo(6, res_dict)

        dmg = Damage(at, df)
        self.assertEqual(4, dmg.value)


if __name__ == '__main__':
    unittest.main()
