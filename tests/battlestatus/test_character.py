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

    def test_calc_atk(self):
        param = Parameters()
        c = Character(param)
        self.assertEqual(0, c.calc_atk())

        # 武器補正
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        c = Character(param)
        with mock.patch.object(c, '_calc_param_equip') as mp_equip:
            c.calc_atk()
            mp_equip.assert_called_once_with(ParameterId.ATK, 10)

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

    def test_calc_param_equip(self):
        c = Character()
        atk = c._calc_param_equip(ParameterId.ATK, 5)
        self.assertEqual(5, atk)

        c = Character()
        eqs = c.equipments
        eq = _create_equipment()
        eqs.set(eq)
        atk = c._calc_param_equip(ParameterId.ATK, 5)
        self.assertEqual(10, atk)

    def test_can_act(self):
        c = Character()
        with mock.patch.object(c.condition, 'can_act', return_value=True):
            self.assertTrue(c.can_act())
        with mock.patch.object(c.condition, 'can_act', return_value=False):
            self.assertFalse(c.can_act())


if __name__ == '__main__':
    unittest.main()
