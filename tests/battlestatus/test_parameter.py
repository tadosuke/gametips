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


if __name__ == '__main__':
    unittest.main()
