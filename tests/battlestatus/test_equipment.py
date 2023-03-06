"""equipment モジュールのテスト."""

import unittest

from battlestatus.equipment import Equipment, BaseData
from battlestatus.parameters import Parameters, ParameterId, ParameterValue
from battlestatus.weapon import ItemName


class TestItemName(unittest.TestCase):

    def test_init(self):
        name = ItemName('123456789012')
        self.assertEqual('123456789012', name.value)
        self.assertIs(str(name), name.value)

        with self.assertRaises(ValueError):
            ItemName('1234567890123')


class TestEquipment(unittest.TestCase):

    def setUp(self) -> None:
        params = Parameters()
        params.set(ParameterId.ATK, ParameterValue(5))
        self.base_data = BaseData(
            name=ItemName('銅の剣'),
            params=params)

    def test_init(self):
        eq = Equipment(self.base_data)
        self.assertEqual(1, eq.level)

    def test_calc_params(self):
        params = Parameters()
        params.set(ParameterId.ATK, ParameterValue(10))
        params.set(ParameterId.DEF, ParameterValue(8))
        base_data = BaseData(
            name=ItemName('魔法の剣'),
            params=params)
        eq = Equipment(base_data)
        eq.set_level(11)
        ret_params = eq.calc_params()
        self.assertEqual(20, ret_params.get(ParameterId.ATK).value)
        self.assertEqual(16, ret_params.get(ParameterId.DEF).value)

    def test_calc_level_param(self):
        eq = Equipment(self.base_data)
        value = eq._calc_level_param(ParameterId.ATK)
        self.assertEqual(0, value)

        eq.set_level(2)
        value = eq._calc_level_param(ParameterId.ATK)
        self.assertEqual(1, value)

        eq.set_level(6)
        value = eq._calc_level_param(ParameterId.ATK)
        self.assertEqual(5, value)


if __name__ == '__main__':
    unittest.main()
