"""character モジュールのテスト."""

import unittest
from unittest import mock

from battlestatus.character import Character
from battlestatus.condition import Condition, ConditionId
from battlestatus.parameters import Parameters, ParameterValue, ParameterId
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
        atk = c.params.get(ParameterId.ATK).value
        self.assertEqual(0, atk)
        self.assertIsInstance(c.condition, Condition)
        self.assertIsNotNone(c.skills)

        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(15))
        c = Character(param)
        atk = c.params.get(ParameterId.ATK).value
        self.assertEqual(15, atk)

    def test_equip(self):
        c = Character()

        w = self.factory.create(0)
        c.equip(w)
        self.assertIs(w, c.weapon)

        c.unequip()
        self.assertIsNone(c.weapon)

    def test_calc_atk(self):
        param = Parameters()
        c = Character(param)
        self.assertEqual(0, c.calc_atk())

        # 武器補正
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        c = Character(param)
        with mock.patch.object(c, '_calc_atk_weapon') as mp_weapon:
            c.calc_atk()
            mp_weapon.assert_called_once_with(10)

        # スキル補正
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        c = Character(param)
        c.skills.add(SkillId.ATK_UP)
        self.assertEqual(12, c.calc_atk())

        # 状態異常補正
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        c = Character(param)
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
