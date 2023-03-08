"""condition モジュールのテスト."""

import unittest
from unittest import mock

from battlestatus.condition import Condition, ConditionId
from battlestatus.parameters import ParameterId


class TestCondition(unittest.TestCase):

    def test_init(self):
        cond = Condition()
        self.assertIsNone(cond._id)

    def test_add_remove(self):
        cond = Condition()
        cond.add(ConditionId.ATK_UP)
        self.assertTrue(
            cond.has(ConditionId.ATK_UP))

        cond.remove(ConditionId.ATK_UP)
        self.assertFalse(
            cond.has(ConditionId.ATK_UP))

    def test_offset(self):
        cond = Condition()
        cond.add(ConditionId.ATK_UP)
        cond.add(ConditionId.ATK_DOWN)
        self.assertFalse(
            cond.has(ConditionId.ATK_UP))
        self.assertFalse(
            cond.has(ConditionId.ATK_DOWN))

    def test_apply_param(self):
        c = Condition()
        with mock.patch.object(c, '_apply_atk') as mp_atk:
            c.apply_param(ParameterId.ATK, 10)
            mp_atk.assert_called_once_with(10)
        with mock.patch.object(c, '_apply_atk') as mp_atk:
            c.apply_param(ParameterId.DEF, 10)
            mp_atk.assert_not_called()

    def test_apply_atk(self):
        c = Condition()
        atk = c._apply_atk(10)
        self.assertEqual(10, atk)

        c = Condition()
        c.add(ConditionId.ATK_UP)
        atk = c._apply_atk(10)
        self.assertAlmostEqual(12.5, atk)

        c = Condition()
        c.add(ConditionId.ATK_DOWN)
        atk = c._apply_atk(10)
        self.assertAlmostEqual(7.5, atk)

    def test_can_act(self):
        c = Condition()
        self.assertTrue(c.can_act())

        c.add(ConditionId.ATK_UP)
        self.assertTrue(c.can_act())

        c.add(ConditionId.SLEEP)
        self.assertFalse(c.can_act())

        c.remove(ConditionId.SLEEP)
        self.assertTrue(c.can_act())


if __name__ == '__main__':
    unittest.main()
