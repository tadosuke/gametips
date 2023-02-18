"""position モジュールのテスト."""

import unittest

from position import GridPosition


class TestGridPosition(unittest.TestCase):

    def test_init(self):
        pos = GridPosition(1, 2)
        self.assertEqual(1, pos.x)
        self.assertEqual(2, pos.y)

        with self.assertRaises(Exception):
            pos = GridPosition(-1, -1)

    def test_shift(self):
        pos = GridPosition(1, 2)
        pos.shift(1, 2)
        self.assertEqual((2, 4), pos)

        pos = GridPosition(1, 2)
        pos.shift(-2, -3)
        self.assertEqual((0, 0), pos)

    def test_up(self):
        pos = GridPosition(1, 2)
        self.assertEqual((1, 1), pos.up())

        pos = GridPosition(1, 0)
        self.assertEqual((1, 0), pos.up())

    def test_down(self):
        pos = GridPosition(1, 2)
        self.assertEqual((1, 3), pos.down())

    def test_left(self):
        pos = GridPosition(1, 2)
        self.assertEqual((0, 2), pos.left())

        pos = GridPosition(0, 2)
        self.assertEqual((0, 2), pos.left())

    def test_right(self):
        pos = GridPosition(1, 2)
        self.assertEqual((2, 2), pos.right())

    def test_equal(self):
        pos1 = GridPosition(1, 2)
        pos2 = GridPosition(1, 2)
        pos3 = GridPosition(2, 3)
        self.assertEqual((1, 2), pos1)
        self.assertNotEqual((2, 2), pos1)
        self.assertEqual(pos1, pos2)
        self.assertIsNot(pos1, pos2)
        self.assertNotEqual(pos1, pos3)
        with self.assertRaises(TypeError):
            pos1 == 5

    def test_calc_distance(self):
        pos1 = GridPosition(1, 1)
        pos2 = GridPosition(1, 1)
        self.assertEqual(0, pos1.calc_distance(pos2))
        self.assertEqual(0, pos2.calc_distance(pos1))

        pos1 = GridPosition(1, 1)
        pos2 = GridPosition(3, 1)
        self.assertEqual(2, pos1.calc_distance(pos2))

        pos1 = GridPosition(1, 1)
        pos2 = GridPosition(1, 4)
        self.assertEqual(3, pos1.calc_distance(pos2))

        pos1 = GridPosition(1, 1)
        pos2 = GridPosition(3, 4)
        self.assertEqual(5, pos1.calc_distance(pos2))


if __name__ == '__main__':
    unittest.main()
