"""parameter モジュールのテスト."""

import unittest

from battlestatus.parameters import Parameters, ParameterValue, ParameterId


class TestParameterValue(unittest.TestCase):

    def test_init(self):
        value = ParameterValue(10)
        self.assertEqual(10, value.value)
        value = ParameterValue(999)
        self.assertEqual(999, value.value)

        with self.assertRaises(ValueError):
            ParameterValue(-1)
        with self.assertRaises(ValueError):
            ParameterValue(1000)

    def test_equal(self):
        value = ParameterValue(10)
        self.assertEqual(ParameterValue(10), value)
        self.assertEqual(10, value)

    def test_add(self):
        value = ParameterValue(2)

        # ParameterValue
        sum_value = value + ParameterValue(3)
        self.assertEqual(5, sum_value.value)

        # 値
        sum_value = value + 4
        self.assertEqual(6, sum_value.value)


class TestParameter(unittest.TestCase):

    def test_init(self):
        param = Parameters()
        self.assertEqual(0, param.get(ParameterId.ATK).value)
        self.assertEqual(0, param.get(ParameterId.DEF).value)
        self.assertEqual(0, param.get(ParameterId.MAT).value)
        self.assertEqual(0, param.get(ParameterId.MDF).value)
        self.assertEqual(0, param.get(ParameterId.DEX).value)
        self.assertEqual(0, param.get(ParameterId.SPD).value)
        self.assertEqual(0, param.get(ParameterId.LUK).value)

    def test_get_set(self):
        param = Parameters()
        param.set(ParameterId.ATK, ParameterValue(10))
        self.assertEqual(10, param.get(ParameterId.ATK).value)
        param.set(ParameterId.DEF, ParameterValue(15))
        self.assertEqual(15, param.get(ParameterId.DEF).value)

    def test_add(self):
        param1 = Parameters()
        param1.set(ParameterId.ATK, ParameterValue(2))
        param1.set(ParameterId.DEF, ParameterValue(3))

        param2 = Parameters()
        param2.set(ParameterId.ATK, ParameterValue(3))
        param2.set(ParameterId.SPD, ParameterValue(4))

        sum_param = param1 + param2
        self.assertEqual(5, sum_param.get(ParameterId.ATK))
        self.assertEqual(3, sum_param.get(ParameterId.DEF))
        self.assertEqual(4, sum_param.get(ParameterId.SPD))


if __name__ == '__main__':
    unittest.main()
