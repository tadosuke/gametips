"""equipment モジュールのテスト."""

import unittest
from enum import IntEnum, auto

from battlestatus.equipment import Equipment, BaseData, ItemName, AllEquipments
from battlestatus.parameters import Parameters, ParameterId, ParameterValue


class TestItemName(unittest.TestCase):

    def test_init(self):
        name = ItemName('123456789012')
        self.assertEqual('123456789012', name)
        self.assertEqual(ItemName('123456789012'), name)
        self.assertEqual('123456789012', name.value)
        self.assertIs(str(name), name.value)

        with self.assertRaises(ValueError):
            ItemName('1234567890123')


class PartId(IntEnum):

    ARM = auto()
    BODY = auto()
    HEAD = auto()


class TestEquipment(unittest.TestCase):

    def setUp(self) -> None:
        params = Parameters()
        params.set(ParameterId.ATK, ParameterValue(5))
        self.base_data = BaseData(
            name=ItemName('銅の剣'),
            part_id=PartId.ARM,
            params=params)

    def test_init(self):
        eq = Equipment(self.base_data)
        self.assertEqual(1, eq.level)
        self.assertEqual('銅の剣', eq.name)
        self.assertEqual(PartId.ARM, eq.part_id)

    def test_calc_params(self):
        params = Parameters()
        params.set(ParameterId.ATK, ParameterValue(10))
        params.set(ParameterId.DEF, ParameterValue(8))
        base_data = BaseData(
            name=ItemName('魔法の剣'),
            params=params)
        eq = Equipment(base_data)
        eq.set_level(6)
        ret_params = eq.calc_params()
        self.assertEqual(20, ret_params.get(ParameterId.ATK))
        self.assertEqual(16, ret_params.get(ParameterId.DEF))

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


class TestEquipments(unittest.TestCase):

    def test_init(self):
        eqs = AllEquipments()
        self.assertEqual({}, eqs._equipments)

    def test_set_equip(self):
        eqs = AllEquipments()

        # 装備
        eq1 = Equipment(BaseData(name=ItemName('eq1'), part_id=PartId.ARM))
        eqs.set(eq1)
        self.assertIs(eq1, eqs.get(PartId.ARM))
        self.assertIsNone(eqs.get(PartId.BODY))

        # 装備：同じ部位
        eq2 = Equipment(BaseData(name=ItemName('eq2'), part_id=PartId.ARM))
        before = eqs.set(eq2)
        self.assertIs(eq2, eqs.get(PartId.ARM))
        self.assertIs(eq1, before)

        # 装備：違う部位
        eq3 = Equipment(BaseData(name=ItemName('eq3'), part_id=PartId.BODY))
        before = eqs.set(eq3)
        self.assertIs(eq2, eqs.get(PartId.ARM))
        self.assertIs(eq3, eqs.get(PartId.BODY))
        self.assertIsNone(before)

        # 外す：装備していない部位
        before = eqs.pop(PartId.HEAD)
        self.assertIsNone(before)
        self.assertIsNotNone(eqs.get(PartId.ARM))

        # 外す：装備している部位
        before = eqs.pop(PartId.ARM)
        self.assertIs(eq2, before)
        self.assertIsNone(eqs.get(PartId.ARM))
        self.assertIs(eq3, eqs.get(PartId.BODY))


if __name__ == '__main__':
    unittest.main()
