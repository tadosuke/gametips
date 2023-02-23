"""levelup モジュールのテスト."""

import unittest

from levelup import Calculator, Character

# レベルごとの累積経験値
_EXP_TABLE = (
    0,
    10,
    30,
    60,
    100,
)


class TestCalculator(unittest.TestCase):

    def test_init(self):
        cal = Calculator(_EXP_TABLE)

        self.assertTupleEqual(_EXP_TABLE, cal._exps)
        with self.assertRaises(AssertionError):
            Calculator(())

    def test_calc(self):
        cal = Calculator(_EXP_TABLE)

        self.assertEqual(1, cal.calc(0))
        self.assertEqual(2, cal.calc(10))
        self.assertEqual(5, cal.calc(101))
        with self.assertRaises(AssertionError):
            cal.calc(-1)


class TestCharacter(unittest.TestCase):

    def test_init(self):
        cal = Calculator(_EXP_TABLE)

        chara = Character(cal, name='Hoge')
        self.assertEqual(0, chara.exp)
        self.assertEqual(1, chara.level)
        self.assertEqual('Hoge', chara.name)

        chara = Character(cal, 15)
        self.assertEqual(15, chara.exp)
        self.assertEqual(2, chara.level)

        with self.assertRaises(AssertionError):
            Character(cal, -5)

    def test_add_exp(self):
        cal = Calculator(_EXP_TABLE)

        chara = Character(cal, 0)
        diff = chara.add_exp(15)
        self.assertEqual(15, chara.exp)
        self.assertEqual(1, diff)
        self.assertEqual(2, chara.level)

        chara = Character(cal)
        diff = chara.add_exp(200)
        self.assertEqual(200, chara.exp)
        self.assertEqual(4, diff)
        self.assertEqual(5, chara.level)


class TestLevelUp(unittest.TestCase):
    """各機能を利用したサンプル."""

    def test_levelup(self):
        print('')
        print('[レベルアップ計算サンプル]')

        cal = Calculator(_EXP_TABLE)
        chara = Character(cal, exp=0, name='Hoge')
        before_lv = chara.level
        print(chara)

        exp = 5
        print(f'{chara.name} は {exp} の経験値を得た。')
        diff = chara.add_exp(exp)
        print(chara)

        exp = 80
        print(f'{chara.name} は {exp} の経験値を得た。')
        diff = chara.add_exp(exp)
        for i in range(diff):
            now_level = before_lv + i + 1
            print(f'{chara.name} はレベル{now_level}に上がった！')
        print(chara)


if __name__ == '__main__':
    unittest.main()
