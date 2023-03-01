"""skill モジュールのテスト."""

import unittest

from battlestatus.skill import SkillDict, SkillId


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


if __name__ == '__main__':
    unittest.main()
