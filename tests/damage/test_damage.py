"""damage モジュールのテスト."""

import unittest
from unittest import mock

from damage import Damage, AttackInfo, DefenceInfo, Attribute, AttackType, Condition


class TestAttackInfo(unittest.TestCase):

    def test_init(self):
        at = AttackInfo(10)
        self.assertEqual(10, at.power)
        self.assertEqual(Attribute.NONE, at.attribute)
        self.assertEqual({}, at.condition_magnifications)
        self.assertTrue(at.is_physics())

    def test_attr_type(self):
        at = AttackInfo(10, AttackType.MAGIC, Attribute.FIRE)
        self.assertEqual(10, at.power)
        self.assertEqual(Attribute.FIRE, at.attribute)
        self.assertTrue(at.is_magic())

    def test_minus(self):
        with self.assertRaises(ValueError):
            AttackInfo(-10)

    def test_condition_magnification(self):
        cond_mag_dict = {
            Condition.POISON: 2.0,
        }
        at = AttackInfo(0, cond_mag_dict=cond_mag_dict)
        self.assertEqual(2.0, at.get_condition_magnification(Condition.POISON))
        self.assertEqual(1.0, at.get_condition_magnification(Condition.SLEEP))


class TestDefenceInfo(unittest.TestCase):

    def test_init(self):
        df = DefenceInfo(
            physics=8,
            magic=6)
        self.assertEqual(8, df.physical_power)
        self.assertEqual(6, df.magical_power)
        self.assertFalse(df.has_condition())

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

    def test_conditions(self):
        df = DefenceInfo(0, 0, conditions=Condition.POISON)
        self.assertTrue(df.has_condition())
        self.assertTrue(df.is_condition(Condition.POISON))
        self.assertFalse(df.is_condition(Condition.SLEEP))

        df = DefenceInfo(0, 0, conditions=Condition.POISON | Condition.SLEEP)
        self.assertTrue(df.is_condition(Condition.POISON))
        self.assertTrue(df.is_condition(Condition.SLEEP))


class TestDamage(unittest.TestCase):

    def test_init(self):
        at = AttackInfo(0)
        df = DefenceInfo(0, 0)
        dmg = Damage(at, df)
        self.assertEqual(at, dmg._attack)
        self.assertEqual(df, dmg._defence)

    def test_calc(self):
        """内部関数の呼び出しチェック."""

        at = AttackInfo(0)
        df = DefenceInfo(0, 0)
        dmg = Damage(at, df)

        with mock.patch.object(dmg, '_calc_basic', return_value=10) as mp_basic:
            with mock.patch.object(dmg, '_calc_cond_mag', return_value=20) as mp_cond:
                with mock.patch.object(dmg, '_calc_regist') as mp_regist:
                    dmg.calc()
                    mp_regist.assert_called_once_with(20)
                mp_cond.assert_called_once_with(10)
            mp_basic.assert_called_once()

    def test_basic_physics(self):
        at = AttackInfo(
            power=10,
            type_=AttackType.PHYSICS)

        df = DefenceInfo(
            physics=6,
            magic=4)

        dmg = Damage(at, df)
        value = dmg._calc_basic()
        self.assertEqual(4, value)

    def test_basic_magic(self):
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC)

        df = DefenceInfo(
            physics=6,
            magic=4)

        dmg = Damage(at, df)
        value = dmg._calc_basic()
        self.assertEqual(6, value)

    def test_basic_minus(self):
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC)

        df = DefenceInfo(
            physics=20,
            magic=20)

        dmg = Damage(at, df)
        value = dmg._calc_basic()
        self.assertEqual(0, value)

    def test_condition_match_single(self):
        cond_mag_dict = {
            Condition.POISON: 2.0,
        }
        at = AttackInfo(0, cond_mag_dict=cond_mag_dict)
        df = DefenceInfo(0, 0, conditions=Condition.POISON)

        dmg = Damage(at, df)
        value = dmg._calc_cond_mag(10)
        self.assertEqual(20, value)

    def test_condition_match_multi(self):
        cond_mag_dict = {
            Condition.POISON: 2.0,
            Condition.SLEEP: 1.5,
        }
        at = AttackInfo(0, cond_mag_dict=cond_mag_dict)
        conditions = Condition.POISON|Condition.SLEEP
        df = DefenceInfo(0, 0, conditions=conditions)

        dmg = Damage(at, df)
        value = dmg._calc_cond_mag(10)
        self.assertEqual(25, value)

    def test_condition_not_match(self):
        cond_mag_dict = {
            Condition.POISON: 2.0,
        }
        at = AttackInfo(0, cond_mag_dict=cond_mag_dict)
        conditions = Condition.SLEEP
        df = DefenceInfo(0, 0, conditions=conditions)

        dmg = Damage(at, df)
        value = dmg._calc_cond_mag(10)
        self.assertEqual(10, value)

    def test_regist_match(self):
        at = AttackInfo(0, attr=Attribute.FIRE)

        res_dict = {
            Attribute.FIRE: 0.5,
        }
        df = DefenceInfo(0, 0, res_dict)

        # 耐性が一致しているので、ダメージ軽減
        dmg = Damage(at, df)
        value = dmg._calc_regist(10)
        self.assertEqual(5, value)

    def test_regist_not_match(self):
        at = AttackInfo(0, attr=Attribute.FIRE)

        res_dict = {
            Attribute.EARTH: 0.5,
        }
        df = DefenceInfo(0, 0, res_dict)

        # 耐性が一致しないので軽減なし
        dmg = Damage(at, df)
        value = dmg._calc_regist(10)
        self.assertEqual(10, value)


class TestModule(unittest.TestCase):
    """各機能を利用したサンプル."""

    def test_case(self):
        print('【ダメージ計算テスト】')

        print('威力10、物理攻撃 → 物理防御力8')
        at = AttackInfo(
            power=10,
            type_=AttackType.PHYSICS)
        df = DefenceInfo(
            physics=8,
            magic=6)
        dmg = Damage(at, df)
        val = dmg.calc()
        print(f'  {val} のダメージ!')

        print('威力10、火属性魔法攻撃 → 魔法防御力4、耐性なし')
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC,
            attr=Attribute.FIRE)
        df = DefenceInfo(
            physics=10,
            magic=4)
        dmg = Damage(at, df)
        val = dmg.calc()
        print(f'  {val} のダメージ!')

        print('威力10、火属性魔法攻撃 → 魔法防御力4、火耐性50%')
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC,
            attr=Attribute.FIRE)
        res_dict = {Attribute.FIRE: 0.5}
        df = DefenceInfo(
            physics=10,
            magic=4,
            res_dict=res_dict)
        dmg = Damage(at, df)
        val = dmg.calc()
        print(f'  {val} のダメージ!')

        print('威力10、物理攻撃、毒特攻2倍 → 物理防御力5、毒')
        cond_mag_dict = {Condition.POISON: 2.0}
        at = AttackInfo(
            power=10,
            type_=AttackType.PHYSICS,
            cond_mag_dict=cond_mag_dict)
        df = DefenceInfo(
            physics=5,
            magic=4,
            conditions=Condition.POISON)
        dmg = Damage(at, df)
        val = dmg.calc()
        print(f'  {val} のダメージ!')

        print('威力10、水属性魔法攻撃、眠り特攻1.5倍 → 魔法防御力2、水耐性75%、眠り')
        cond_mag_dict = {Condition.SLEEP: 1.5}
        at = AttackInfo(
            power=10,
            type_=AttackType.MAGIC,
            attr=Attribute.WATER,
            cond_mag_dict=cond_mag_dict)
        res_dict = {Attribute.WATER: 0.25}
        df = DefenceInfo(
            physics=4,
            magic=2,
            res_dict=res_dict,
            conditions=Condition.SLEEP)
        dmg = Damage(at, df)
        val = dmg.calc()
        print(f'  {val} のダメージ!')


if __name__ == '__main__':
    unittest.main()
