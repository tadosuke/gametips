"""parameter モジュールのテスト."""

import unittest
from enum import Enum, auto

from battlestatus.parameter import Parameter, ParameterValue


class TestParameterValue(unittest.TestCase):

    def test_init(self):
        value = ParameterValue(10)
        self.assertEqual(10, value.value)

        with self.assertRaises(ValueError):
            ParameterValue(-10)


class TestParameter(unittest.TestCase):

    def test_init(self):
        param = Parameter()
        self.assertEqual(0, param.attack.value)
        self.assertEqual(0, param.defence.value)
        self.assertEqual(0, param.mattack.value)
        self.assertEqual(0, param.mdefence.value)
        self.assertEqual(0, param.dexterity.value)
        self.assertEqual(0, param.speed.value)
        self.assertEqual(0, param.luck.value)


if __name__ == '__main__':
    unittest.main()
