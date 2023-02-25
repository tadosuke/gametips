import unittest
from unittest import mock

from battlestatus import Character, Condition, ConditionId, Weapon, SkillId, Skill, SkillDict


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


class TestWeapon(unittest.TestCase):

    def test_init(self):
        w = Weapon(4)
        self.assertEqual(4, w._atk)


class TestSkillDict(unittest.TestCase):

    def test_init(self):
        sd = SkillDict()
        self.assertEqual({}, sd._dict)

    def test_add(self):
        sd = SkillDict()
        self.assertFalse(sd.has(SkillId.ATK_UP))
        sd.add(SkillId.ATK_UP)
        self.assertTrue(sd.has(SkillId.ATK_UP))

    def test_get_level(self):
        sd = SkillDict()
        self.assertEqual(0, sd.get_level(SkillId.ATK_UP))
        sd.add(SkillId.ATK_UP, 2)
        self.assertEqual(2, sd.get_level(SkillId.ATK_UP))

    def test_apply_atk(self):
        sd = SkillDict()
        self.assertEqual(10, sd.apply_atk(10))
        sd.add(SkillId.DEF_UP)
        self.assertEqual(10, sd.apply_atk(10))
        sd.add(SkillId.ATK_UP)
        self.assertEqual(12, sd.apply_atk(10))
        sd.add(SkillId.ATK_UP, 3)
        self.assertEqual(16, sd.apply_atk(10))


class TestSkill(unittest.TestCase):

    def test_init(self):
        s = Skill(SkillId.ATK_UP)
        self.assertEqual(SkillId.ATK_UP, s.id)
        self.assertEqual(1, s.level)

    def test_level(self):
        s = Skill(SkillId.ATK_UP)

        s.set_level(2)
        self.assertEqual(2, s.level)

        with self.assertRaises(AssertionError):
            s.set_level(-1)

    def test_apply_atk(self):
        s = Skill(SkillId.ATK_UP)
        atk = s.apply_atk(10)
        self.assertEqual(12, atk)

        s = Skill(SkillId.DEF_UP)
        atk = s.apply_atk(10)
        self.assertEqual(10, atk)


class TestCharacter(unittest.TestCase):

    def test_init(self):
        c = Character()
        self.assertEqual(10, c._atk)
        self.assertIsInstance(c.condition, Condition)
        self.assertIsNotNone(c.skills)

    def test_equip(self):
        c = Character()

        w = Weapon(4)
        c.equip(w)
        self.assertIs(w, c.weapon)

        c.unequip()
        self.assertIsNone(c.weapon)

    def test_calc_atk(self):
        c = Character(10)
        self.assertEqual(10, c.calc_atk())

        c = Character(10)
        c.skills.add(SkillId.ATK_UP)
        self.assertEqual(12, c.calc_atk())

        c = Character(10)
        c.condition.add(ConditionId.ATK_UP)
        self.assertEqual(12, c.calc_atk())

    def test_calc_atk_weapon(self):
        c = Character()
        atk = c._calc_atk_weapon(5)
        self.assertEqual(5, atk)

        c = Character()
        w = Weapon(4)
        c.equip(w)
        atk = c._calc_atk_weapon(5)
        self.assertEqual(9, atk)


if __name__ == '__main__':
    unittest.main()
