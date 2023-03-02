"""character モジュールのテスト."""

import unittest

from battlestatus.character import Character
from battlestatus.condition import Condition, ConditionId
from battlestatus.skill import SkillId
from battlestatus.weapon import BaseParameter, WeaponFactory, BaseParameterDict


# 武器の能力辞書
_BASE_PARAMETER_DICT = {
    0: BaseParameter(atk=5)
}


class TestCharacter(unittest.TestCase):

    def setUp(self) -> None:
        dict_ = BaseParameterDict(_BASE_PARAMETER_DICT)
        self.factory = WeaponFactory(dict_)

    def test_init(self):
        c = Character()
        self.assertEqual(10, c._atk)
        self.assertIsInstance(c.condition, Condition)
        self.assertIsNotNone(c.skills)

    def test_equip(self):
        c = Character()

        w = self.factory.create(0)
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
        w = self.factory.create(0)
        c.equip(w)
        atk = c._calc_atk_weapon(5)
        self.assertEqual(10, atk)


if __name__ == '__main__':
    unittest.main()
