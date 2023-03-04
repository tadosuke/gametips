"""weapon モジュールのテスト."""

import unittest
from enum import Enum, auto

from battlestatus.parameters import ParameterValue
from battlestatus.weapon import Weapon, BaseParameter, BaseParameterDict, WeaponFactory, ItemName


class WeaponId(Enum):
    """武器 ID."""

    COPPER_SWORD = auto()  # 銅の剣
    IRON_SWORD = auto()  # 鉄の剣
    STEEL_SWORD = auto()  # 鋼の剣


# 武器の能力辞書
_BASE_PARAMETER_DICT = {
    WeaponId.COPPER_SWORD:
        BaseParameter(name=ItemName('銅の剣'), atk=ParameterValue(5)),
    WeaponId.IRON_SWORD:
        BaseParameter(name=ItemName('鉄の剣'), atk=ParameterValue(10)),
    WeaponId.STEEL_SWORD:
        BaseParameter(name=ItemName('鋼の剣'), atk=ParameterValue(15)),
}


class TestItemName(unittest.TestCase):

    def test_init(self):
        name = ItemName('123456789012')
        self.assertEqual('123456789012', name.value)
        self.assertIs(str(name), name.value)

        with self.assertRaises(ValueError):
            ItemName('1234567890123')


class TestBaseParameterDict(unittest.TestCase):

    def test_init(self):
        wdict = BaseParameterDict(_BASE_PARAMETER_DICT)
        param = wdict.get(WeaponId.COPPER_SWORD)
        self.assertEqual('銅の剣', param.name.value)
        self.assertEqual(5, param.atk.value)

        param = wdict.get(-1)
        self.assertIsNone(param)


class TestWeaponFactory(unittest.TestCase):

    def setUp(self) -> None:
        self.dict = BaseParameterDict(_BASE_PARAMETER_DICT)
        self.factory = WeaponFactory(self.dict)

    def test_init(self):
        self.assertIs(self.dict, self.factory._base_param_dict)

    def test_create(self):
        w = self.factory.create(WeaponId.COPPER_SWORD, 2)
        self.assertEqual(2, w.level)


class TestWeapon(unittest.TestCase):

    def test_init(self):
        param = _BASE_PARAMETER_DICT[WeaponId.COPPER_SWORD]
        param.id = WeaponId.COPPER_SWORD
        w = Weapon(param)
        self.assertIs(param, w._base_param)
        self.assertEqual(5, param.atk.value)
        self.assertEqual('銅の剣', param.name.value)

    def test_calc_atk(self):
        param = _BASE_PARAMETER_DICT[WeaponId.IRON_SWORD]
        w = Weapon(param)
        atk = w.calc_atk()
        self.assertEqual(w._base_param.atk.value + w._calc_level_atk(), atk)

    def test_level_atk(self):
        param = _BASE_PARAMETER_DICT[WeaponId.IRON_SWORD]
        w = Weapon(param)
        w.set_level(2)
        self.assertAlmostEqual(2.0, w._calc_level_atk())
        w.set_level(3)
        self.assertAlmostEqual(4.0, w._calc_level_atk())

        with self.assertRaises(AssertionError):
            w.set_level(-1)


if __name__ == '__main__':
    unittest.main()
