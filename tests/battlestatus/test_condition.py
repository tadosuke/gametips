"""condition モジュールのテスト."""

import unittest

from battlestatus.condition import Condition, ConditionId


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

    def test_apply_atk(self):
        c = Condition()
        atk = c.apply_atk(10)
        self.assertEqual(10, atk)

        c = Condition()
        c.add(ConditionId.ATK_UP)
        atk = c.apply_atk(10)
        self.assertAlmostEqual(12.5, atk)

        c = Condition()
        c.add(ConditionId.ATK_DOWN)
        atk = c.apply_atk(10)
        self.assertAlmostEqual(7.5, atk)


if __name__ == '__main__':
    unittest.main()
