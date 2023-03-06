"""character モジュールのテスト."""

import unittest
from unittest import mock

from battlestatus.character import Character
from battlestatus.condition import Condition, ConditionId
from battlestatus.equipment import Equipment, ItemName, BaseData
from battlestatus.parameters import Parameters, ParameterValue, ParameterId
from battlestatus.skill import SkillId


def _create_equipment() -> Equipment:
    params = Parameters()
    params.set(ParameterId.ATK, ParameterValue(5))
    base_data = BaseData(
        name=ItemName('銅の剣'),
        params=params)
    eq = Equipment(base_data)
    return eq


class TestCharacter(unittest.TestCase):

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

        eq = _create_equipment()
        c.set_equip(eq)
        self.assertIs(eq, c.get_equip())

        c.set_equip(None)
        self.assertIsNone(c.get_equip())

    def test_calc_atk(self):
        param = Parameters()
        c = Character(param)
        self.assertEqual(0, c.calc_atk())

        # 武器補正
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        c = Character(param)
        with mock.patch.object(c, '_calc_atk_equip') as mp_weapon:
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

    def test_calc_atk_equip(self):
        c = Character()
        atk = c._calc_atk_equip(5)
        self.assertEqual(5, atk)

        c = Character()
        eq = _create_equipment()
        c.set_equip(eq)
        atk = c._calc_atk_equip(5)
        self.assertEqual(10, atk)


if __name__ == '__main__':
    unittest.main()
