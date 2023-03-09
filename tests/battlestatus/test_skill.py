"""skill モジュールのテスト."""

import unittest
from unittest import mock

from battlestatus.parameters import ParameterId
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

    def test_apply_param(self):
        sd = SkillDict()
        with mock.patch.object(sd, '_apply_atk') as mp_atk:
            sd.apply_param(ParameterId.ATK, 10)
            mp_atk.assert_called_once_with(10)
        with mock.patch.object(sd, '_apply_atk') as mp_atk:
            ret = sd.apply_param(ParameterId.DEF, 10)
            self.assertEqual(10, ret)
            mp_atk.assert_not_called()

    def test_apply_atk(self):
        sd = SkillDict()
        self.assertEqual(10, sd._apply_atk(10))
        sd.add(SkillId.DEF_UP)
        self.assertEqual(10, sd._apply_atk(10))
        sd.add(SkillId.ATK_UP)
        self.assertEqual(12, sd._apply_atk(10))
        sd.add(SkillId.ATK_UP, 3)
        self.assertEqual(16, sd._apply_atk(10))


if __name__ == '__main__':
    unittest.main()
