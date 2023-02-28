"""slgmove モジュールのテスト."""

import unittest

from slgmove.position import GridPosition
from slgmove.slgmove import Unit, Map, MoveMap, Ground

_GROUND_TYPES1 = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
]

_GROUND_TYPES2 = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1],
]

_GROUND_DICT = {
    0: Ground(1),
    1: Ground(Ground.COST_FORBIDDEN),
    2: Ground(2),
}


def _create_map1():
    return Map(_GROUND_TYPES1, _GROUND_DICT)


def _create_map2():
    return Map(_GROUND_TYPES2, _GROUND_DICT)


class TestUnit(unittest.TestCase):

    def test_init(self):
        unit = Unit(
            position=GridPosition(2, 1),
            move=3,
            name='chara1')
        self.assertEqual((2, 1), unit.position)
        self.assertEqual(3, unit.move)
        self.assertEqual('chara1', unit.name)

    def test_move(self):
        unit = Unit(GridPosition(2, 1))

        unit.set_position(GridPosition(3, 2))
        self.assertEqual((3, 2), unit.position)


class TestMap(unittest.TestCase):

    def test_init(self):
        map_ = _create_map1()
        self.assertEqual(5, map_.width)
        self.assertEqual(4, map_.height)

    def test_add_unit(self):
        unit = Unit(GridPosition(3, 2))
        map_ = _create_map1()
        map_.add_unit(unit)

        ret_unit = map_.find_unit_from_pos(
            GridPosition(3, 2))
        self.assertIs(unit, ret_unit)
        ret_unit = map_.find_unit_from_pos(
            GridPosition(4, 3))
        self.assertIsNone(ret_unit)

    def test_get_cost(self):
        map_ = _create_map1()
        self.assertEqual(Ground.COST_FORBIDDEN, map_.get_cost(GridPosition(0, 0)))
        self.assertEqual(1, map_.get_cost(GridPosition(1, 1)))

        map_ = _create_map2()
        self.assertEqual(2, map_.get_cost(GridPosition(2, 2)))

    def test_get_ground(self):
        map_ = _create_map1()
        g = map_.get_ground(GridPosition(0, 0))
        self.assertIs(_GROUND_DICT[1], g)

    def test_is_range(self):
        map_ = _create_map1()
        self.assertTrue(
            map_.is_range(GridPosition(0, 0)))
        self.assertTrue(
            map_.is_range(GridPosition(4, 3)))
        self.assertFalse(
            map_.is_range(GridPosition(5, 3)))
        self.assertFalse(
            map_.is_range(GridPosition(4, 4)))

    def test_can_move(self):
        map_ = _create_map1()

        # 移動可
        pos = GridPosition(2, 1)
        can = map_.can_move(pos, 1)
        self.assertTrue(can)

        # 範囲外
        pos = GridPosition(9, 9)
        can = map_.can_move(pos, 5)
        self.assertFalse(can)

        # 進入不可
        pos = GridPosition(2, 0)
        can = map_.can_move(pos, 1)
        self.assertFalse(can)

        # 移動力不足
        pos = GridPosition(2, 2)
        can = map_.can_move(pos, 0)
        self.assertFalse(can)

        # コスト2の位置
        map_ = _create_map2()
        pos = GridPosition(2, 2)
        can = map_.can_move(pos, 2)
        self.assertTrue(can)
        can = map_.can_move(pos, 1)
        self.assertFalse(can)

        # 他のユニットがいる
        unit = Unit(GridPosition(2, 1))
        map_.add_unit(unit)
        can = map_.can_move(pos, 1)
        self.assertFalse(can)


class TestGround(unittest.TestCase):

    def test_init(self):
        g = Ground(2)
        self.assertEqual(2, g.cost)

        g = Ground(Ground.COST_FORBIDDEN)
        self.assertEqual(Ground.COST_FORBIDDEN, g.cost)
        self.assertTrue(g.is_forbidden())

        with self.assertRaises(AssertionError):
            g = Ground(-10)


class TestMoveMap(unittest.TestCase):

    def test_init(self):
        map_ = _create_map1()
        move_map = MoveMap(map_)
        self.assertIs(map_, move_map._map)
        self.assertEqual(map_.height, len(move_map._moves))
        self.assertEqual(map_.width, len(move_map._moves[0]))
        self.assertEqual(MoveMap.UNSET_VALUE, move_map.get_step(GridPosition(1, 1)))

    def test_calc(self):
        map_ = _create_map2()
        other_unit = Unit(GridPosition(1, 3))
        map_.add_unit(other_unit)
        move_map = MoveMap(map_)
        unit = Unit(
            GridPosition(3, 3),
            move=3)
        move_map.calc(unit)

        expected = [
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, 0, 1, 0, -1, -1],
            [-1, -1, 0, 2, 1, 0, -1],
            [-1, -1, 2, 3, 1, 0, -1],
            [-1, 0, 1, 2, 1, 0, -1],
            [-1, -1, -1, -1, -1, -1, -1],
        ]
        self.assertEqual(expected, move_map._moves)

    def test_calc_step(self):
        map_ = _create_map1()
        move_map = MoveMap(map_)

        # その場
        move_map._reset()
        start = GridPosition(2, 1)
        move_map._calc_step(start, 0)
        self.assertEqual(0, move_map.get_step(start))
        move_map._calc_step(start, 2)
        target = GridPosition(2, 1)
        self.assertEqual(
            2, move_map.get_step(target))

        move_map._reset()
        start = GridPosition(2, 1)
        move_map._calc_step(start, 2)

        # 下
        target = GridPosition(2, 2)
        self.assertEqual(
            1, move_map.get_step(target))
        target = GridPosition(2, 3)
        self.assertEqual(
            MoveMap.UNSET_VALUE, move_map.get_step(target))

        # 左
        target = GridPosition(1, 1)
        self.assertEqual(
            1, move_map.get_step(target))
        target = GridPosition(0, 1)
        self.assertEqual(
            MoveMap.UNSET_VALUE, move_map.get_step(target))

        # 右
        target = GridPosition(3, 1)
        self.assertEqual(
            1, move_map.get_step(target))
        target = GridPosition(4, 1)
        self.assertEqual(
            MoveMap.UNSET_VALUE, move_map.get_step(target))

        # 上
        move_map._reset()
        start = GridPosition(2, 2)
        move_map._calc_step(start, 2)
        target = GridPosition(2, 1)
        self.assertEqual(
            1, move_map.get_step(target))
        target = GridPosition(2, 0)
        self.assertEqual(
            MoveMap.UNSET_VALUE, move_map.get_step(target))

    def test_can_move(self):
        map_ = _create_map2()
        move_map = MoveMap(map_)
        unit = Unit(
            GridPosition(3, 3),
            move=3)
        move_map.calc(unit)

        self.assertFalse(
            move_map.can_move(GridPosition(1, 1)))
        self.assertTrue(
            move_map.can_move(GridPosition(2, 1)))
        self.assertTrue(
            move_map.can_move(GridPosition(5, 4)))
        self.assertFalse(
            move_map.can_move(GridPosition(5, 5)))


class TestSLGMove(unittest.TestCase):
    """各機能を利用したサンプル."""

    def test_case(self):
        map_ = _create_map2()
        print('')
        print('[Map]')
        map_.dump()
        print('')

        unit = Unit(
            GridPosition(3, 3),
            move=3,
            name='Hoge')
        print('[Unit]')
        print(unit)
        map_.add_unit(unit)

        move_map = MoveMap(map_)
        move_map.calc(unit)
        print('')
        print(f'[MoveMap for {unit.name}]')
        move_map.dump()
        print('')

        pos = GridPosition(1, 1)
        self._move_unit(unit, move_map, pos)

        pos = GridPosition(1, 2)
        self._move_unit(unit, move_map, pos)

        move_map.calc(unit)
        print('')
        print(f'[MoveMap for {unit.name}]')
        move_map.dump()
        print('')

    def _move_unit(self, unit, move_map, pos):
        if move_map.can_move(pos):
            unit.set_position(pos)
            print(f'{pos}に移動します。')
        else:
            print(f'{pos}には移動できません。')


if __name__ == '__main__':
    unittest.main()
