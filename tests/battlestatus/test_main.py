"""main モジュールのテスト."""

import unittest

from battlestatus.condition import ConditionId, Condition
from battlestatus.main import Character, SkillId, SkillDict
from battlestatus.weapon import WeaponId, Weapon


class TestSkillDict(unittest.TestCase):

    def test_init(self):
        sd = SkillDict()
        self.assertEqual({}, sd._dict)

    def test_add(self):
        sd = SkillDict()
        self.assertFalse(sd.has(SkillId.ATK_UP))
        sd.add(SkillId.ATK_UP)
        self.assertTrue(sd.has(SkillId.ATK_UP))

    def test_get_level(self):
        sd = SkillDict()
        self.assertEqual(0, sd.get_level(SkillId.ATK_UP))
        sd.add(SkillId.ATK_UP, 2)
        self.assertEqual(2, sd.get_level(SkillId.ATK_UP))

    def test_apply_atk(self):
        sd = SkillDict()
        self.assertEqual(10, sd.apply_atk(10))
        sd.add(SkillId.DEF_UP)
        self.assertEqual(10, sd.apply_atk(10))
        sd.add(SkillId.ATK_UP)
        self.assertEqual(12, sd.apply_atk(10))
        sd.add(SkillId.ATK_UP, 3)
        self.assertEqual(16, sd.apply_atk(10))


class TestCharacter(unittest.TestCase):

    def test_init(self):
        c = Character()
        self.assertEqual(10, c._atk)
        self.assertIsInstance(c.condition, Condition)
        self.assertIsNotNone(c.skills)

    def test_equip(self):
        c = Character()

        w = Weapon(WeaponId.COPPER_SWORD)
        c.equip(w)
        self.assertIs(w, c.weapon)

        c.unequip()
        self.assertIsNone(c.weapon)

    def test_calc_atk(self):
        c = Character(10)
        self.assertEqual(10, c.calc_atk())

        c = Character(10)
        c.skills.add(SkillId.ATK_UP)
        self.assertEqual(12, c.calc_atk())

        c = Character(10)
        c.condition.add(ConditionId.ATK_UP)
        self.assertEqual(12, c.calc_atk())

    def test_calc_atk_weapon(self):
        c = Character()
        atk = c._calc_atk_weapon(5)
        self.assertEqual(5, atk)

        c = Character()
        w = Weapon(WeaponId.COPPER_SWORD)
        c.equip(w)
        atk = c._calc_atk_weapon(5)
        self.assertEqual(10, atk)

        c = Character()
        w = Weapon(WeaponId.IRON_SWORD)
        c.equip(w)
        atk = c._calc_atk_weapon(5)
        self.assertEqual(15, atk)

        c = Character()
        w = Weapon(WeaponId.IRON_SWORD)
        w.set_level(2)
        c.equip(w)
        atk = c._calc_atk_weapon(5)
        self.assertEqual(17, atk)


class TestBattleStatus(unittest.TestCase):
    """各機能を利用したサンプル."""

    def test_case(self):
        print('')
        print('[BattleStatus]')

        chara = Character(10)
        print(f'力={chara._atk}')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        w = Weapon(WeaponId.COPPER_SWORD, 1)
        chara.equip(w)
        print(f'力={chara._atk}, 武器={w.id.name}(Lv.{w.level})')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        w = Weapon(WeaponId.COPPER_SWORD, 5)
        chara.equip(w)
        print(f'力={chara._atk}, 武器={w.id.name}(Lv.{w.level})')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        chara.condition.add(ConditionId.ATK_UP)
        print(f'力={chara._atk}, 状態={ConditionId.ATK_UP.name}')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        chara.condition.add(ConditionId.ATK_DOWN)
        print(f'力={chara._atk}, 状態={ConditionId.ATK_DOWN.name}')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        skill_level = 1
        chara.skills.add(SkillId.ATK_UP, skill_level)
        print(f'力={chara._atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        skill_level = 4
        chara.skills.add(SkillId.ATK_UP, skill_level)
        print(f'力={chara._atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
        print(f'　→ 総攻撃力={chara.calc_atk()}')

        chara = Character(10)
        w = Weapon(WeaponId.STEEL_SWORD, 5)
        chara.equip(w)
        chara.condition.add(ConditionId.ATK_UP)
        skill_level = 5
        chara.skills.add(SkillId.ATK_UP, skill_level)
        print(f'力={chara._atk}, '
              f'武器={w.id.name}(Lv.{w.level}), '
              f'スキル={SkillId.ATK_UP.name}(Lv.{skill_level}), '
              f'状態={ConditionId.ATK_UP.name}')
        print(f'　→ 総攻撃力={chara.calc_atk()}')


if __name__ == '__main__':
    unittest.main()
