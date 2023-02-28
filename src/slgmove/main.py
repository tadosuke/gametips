"""戦略SLG風移動システム."""

from __future__ import annotations

import typing as tp

from slgmove.position import GridPosition


class Unit:
    """ユニット.

    :param position: 位置
    :param move: 移動力
    :param name: ユニットの名前
    """

    _DEFAULT_MOVE = 4

    def __init__(
            self,
            position=GridPosition(),
            move=_DEFAULT_MOVE,
            name='') -> None:
        self._pos = position
        self._move = move
        self._name = name

    @property
    def position(self) -> GridPosition:
        """位置."""

        return self._pos

    @property
    def move(self) -> int:
        """移動力."""

        return self._move

    @property
    def name(self) -> str:
        """名前."""
        
        return self._name

    def set_position(self, pos) -> None:
        """位置を設定します."""
        
        self._pos = pos

    def __str__(self) -> str:
        return f'{self.name}: Pos={self.position}, Move={self.move}'


class Map:
    """マップ.

    :param ground_types: 地面タイプの二次元リスト
    :param ground_dict: 地面タイプ → Ground の辞書
    """

    def __init__(
            self,
            ground_types: list[list[int]],
            ground_dict: dict[int, Ground]) -> None:
        assert 0 < len(ground_types)
        assert 0 < len(ground_types[0])

        self._ground_types = ground_types
        self._ground_dict = ground_dict
        self._unit_set = set()

    @property
    def width(self) -> int:
        """幅."""

        return len(self._ground_types[0])

    @property
    def height(self) -> int:
        """高さ."""

        return len(self._ground_types)

    def get_ground(self, pos: GridPosition) -> Ground:
        """指定位置の地面を得ます.

        :param pos: 位置
        :return: 地面
        """

        type_ = self.get_type(pos)
        return self._ground_dict[type_]

    def get_type(self, pos: GridPosition) -> int:
        """指定位置の地面タイプを得ます.

        :param pos: 位置
        :return: 地面タイプ
        """

        return self._ground_types[pos.y][pos.x]

    def get_cost(self, pos: GridPosition) -> int:
        """指定位置の移動コストを得ます.

        :param pos:
        :return: 移動コスト
        """

        g = self.get_ground(pos)
        return g.cost

    def add_unit(self, unit: Unit) -> None:
        """ユニットを追加します.

        既に存在するユニットを指定した場合は無視します.

        :param unit: ユニット
        """

        self._unit_set.add(unit)

    def find_unit_from_pos(self, pos: GridPosition) -> tp.Optional[Unit]:
        """指定位置にいるユニットを得ます.

        :param pos: 位置
        :return: ユニット。指定位置にいない場合は None
        """

        for unit in self._unit_set:
            if unit.position == pos:
                return unit
        return None

    def is_range(self, pos: GridPosition) -> bool:
        """指定位置がマップ範囲内か？

        :param pos: 位置
        :return: 範囲内ならTrue
        """

        if self.width <= pos.x:
            return False
        if self.height <= pos.y:
            return False
        return True

    def can_move(self, pos: GridPosition, move: int) -> bool:
        """指定位置に移動可能か？

        :param pos: 位置
        :param move: 移動力
        :return: 移動可能ならTrue
        """

        if not self.is_range(pos):
            return False

        cost = self.get_cost(pos)
        if cost == Ground.COST_FORBIDDEN:
            return False
        if move < cost:
            return False

        if self.find_unit_from_pos(pos) is not None:
            return False

        return True

    def dump(self) -> None:
        """マップの情報を出力します."""

        for line in self._ground_types:
            for x in line:
                print(x, end=' ')
            print('')


class Ground:
    """地面.

    :param cost: 移動コスト
    """

    # 進入禁止
    COST_FORBIDDEN = -1

    def __init__(self, cost: int) -> None:
        assert 0 <= cost or cost == self.COST_FORBIDDEN

        self._cost = cost

    @property
    def cost(self) -> int:
        """移動コスト."""

        return self._cost

    def is_forbidden(self) -> bool:
        """進入禁止か？"""

        return self._cost == self.COST_FORBIDDEN


class MoveMap:
    """移動範囲マップ.

    計算結果は、ユニットのいる位置を起点に、移動力を減らしながら書き込まれます.
    移動できない位置は UNSET_VALUE のままになります.

    :param map_: マップ
    """

    # 書き込みされていない値
    UNSET_VALUE = -1

    def __init__(self, map_: Map) -> None:
        self._map = map_
        self._moves = []
        self._reset()

    def _reset(self) -> None:
        """計算結果をリセットします."""

        self._moves.clear()
        for y in range(self._map.height):
            line = [self.UNSET_VALUE] * self._map.width
            self._moves.append(line)

    def calc(self, unit) -> None:
        """指定ユニットの移動範囲を計算します.

        :param unit: ユニット
        """

        self._reset()
        self._calc_step(unit.position, unit.move)

    def _calc_step(self, pos: GridPosition, move: int) -> None:
        """一歩分の移動範囲を計算します.

        この関数は移動できなくなるまで再帰的に呼び出されます.

        :param pos: 計算する位置
        :param move: 移動力
        """

        self._write(pos, move)
        if move == 0:
            return

        self._calc_step_next(pos.down(), move)
        self._calc_step_next(pos.up(), move)
        self._calc_step_next(pos.left(), move)
        self._calc_step_next(pos.right(), move)

    def _calc_step_next(self, next_pos: GridPosition, move: int) -> None:
        """次の位置への移動を計算します.

        :param next_pos: 移動先の位置
        :param move: 移動力
        """

        if not self._map.can_move(next_pos, move):
            return

        next_cost = self._map.get_cost(next_pos)
        self._calc_step(
            next_pos, move - next_cost)

    def _write(self, pos: GridPosition, move: int) -> None:
        """指定位置に移動力を書き込みます.

        :param pos: 位置
        :param move: 移動力
        """

        if move <= self._moves[pos.y][pos.x]:
            return
        self._moves[pos.y][pos.x] = move

    def can_move(self, pos: GridPosition) -> bool:
        """指定位置に移動できるか？

        :param pos: 位置
        :return: 移動できればTrue
        """

        if not self._map.is_range(pos):
            return False

        step = self.get_step(pos)
        if step == self.UNSET_VALUE:
            return False
        return True

    def get_step(self, pos: GridPosition) -> int:
        """指定位置の計算結果を得ます.

        :param pos: 位置
        :return: 計算結果
        """

        return self._moves[pos.y][pos.x]

    def dump(self) -> None:
        """現在の情報を出力します."""

        for line in self._moves:
            for x in line:
                print(f'{x:2}', end=' ')
            print('')
