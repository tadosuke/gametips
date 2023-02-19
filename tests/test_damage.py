"""damage モジュールのテスト."""

import unittest
from unittest import mock

from damage import Damage, AttackInfo, DefenceInfo, Attribute, AttackType


class TestAttackInfo(unittest.TestCase):

    def test_init(self):
        at = AttackInfo(10)
        self.assertEqual(10, at.power)
        self.assertEqual(Attribute.NONE, at.attribute)
        self.assertTrue(at.is_physics())

    def test_attr_type(self):
        at = AttackInfo(10, AttackType.MAGIC, Attribute.FIRE)
        self.assertEqual(10, at.power)
        self.assertEqual(Attribute.FIRE, at.attribute)
        self.assertTrue(at.is_magic())

    def test_minus(self):
        with self.assertRaises(ValueError):
            AttackInfo(-10)


class TestDefenceInfo(unittest.TestCase):

    def test_init(self):
        df = DefenceInfo(
            physics=8,
            magic=6)
        self.assertEqual(8, df.physical_power)
        self.assertEqual(6, df.magical_power)

    def test_minus(self):
        with self.assertRaises(ValueError):
            DefenceInfo(
                physics=-10,
                magic=10)
        with self.assertRaises(ValueError):
            DefenceInfo(
                physics=10,
                magic=-10)

    def test_regist(self):
        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(
            physics=10,
            magic=10,
            res_dict=res_dict)
        self.assertAlmostEqual(
            0.5,
            df.get_regist(Attribute.FIRE))
        self.assertAlmostEqual(
            1.0,
            df.get_regist(Attribute.WIND))


class TestDamage(unittest.TestCase):

    def test_physics(self):
        # 威力10、無属性の物理攻撃
        at = AttackInfo(
            power=10,
            type_=AttackType.PHYSICS)

        # 物理防御力6
        df = DefenceInfo(
            physics=6,
            magic=4)

        dmg = Damage(at, df)
        self.assertEqual(4, dmg.value)

    def test_physics_attr_match(self):
        # 威力10、火属性の物理攻撃
        at = AttackInfo(
            power=10,
            type_=AttackType.PHYSICS,
            attr=Attribute.FIRE)

        # 物理防御6、火耐性50%
        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(
            physics=6,
            magic=4,
            res_dict=res_dict)

        # 耐性が一致しているので、ダメージ軽減
        dmg = Damage(at, df)
        self.assertEqual(2, dmg.value)

    def test_minus(self):
        at = AttackInfo(power=10)
        df = DefenceInfo(
            physics=20,
            magic=20)

        with mock.patch('damage.Damage._apply_regist') as mp_regist:
            dmg = Damage(at, df)
            self.assertEqual(0, dmg.value)
            mp_regist.assert_not_called()

    def test_magic_attr_not_match(self):
        # 威力10、火属性の魔法攻撃
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC,
            attr=Attribute.FIRE)

        # 魔法防御4、土耐性50%
        res_dict = {
            Attribute.EARTH: 0.5,
        }
        df = DefenceInfo(
            physics=6,
            magic=4,
            res_dict=res_dict)

        # 耐性が一致しないので軽減なし
        dmg = Damage(at, df)
        self.assertEqual(6, dmg.value)

    def test_magic_attr_match(self):
        # 威力10、火属性の魔法攻撃
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC,
            attr=Attribute.FIRE)

        # 魔法防御4、火耐性50%
        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(
            physics=6,
            magic=4,
            res_dict=res_dict)

        # 耐性が一致しているので、ダメージ軽減
        dmg = Damage(at, df)
        self.assertEqual(3, dmg.value)


if __name__ == '__main__':
    unittest.main()
