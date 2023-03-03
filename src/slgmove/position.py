"""位置クラス."""
from __future__ import annotations


class GridPosition:
    """グリッド上の位置を表すクラス.

    負の数は扱いません.

    :params x: X座標
    :params y: Y座標
    """

    def __init__(self, x: int = 0, y: int = 0) -> None:
        assert 0 <= x
        assert 0 <= y

        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        """X座標."""

        return self._x

    @property
    def y(self) -> int:
        """Y座標."""

        return self._y

    def get(self) -> tuple[int, int]:
        """X,Y座標をタプル形式で得ます.

        :return: X,Y座標のタプル
        """

        return self._x, self._y

    def shift(self, dx: int, dy: int) -> None:
        """指定したX, Yの分だけ移動します.

        :params dx: Xの移動量
        :params dy: Yの移動量
        """

        self._x = max(0, self._x + dx)
        self._y = max(0, self._y + dy)

    def up(self) -> GridPosition:
        """一つ上の座標を返します.

        :return: 一つ上の座標
        """

        return GridPosition(
            self._x, max(0, self._y - 1))

    def down(self) -> GridPosition:
        """一つ下の座標を返します.

        :return: 一つ下の座標
        """

        return GridPosition(self._x, self._y + 1)

    def left(self) -> GridPosition:
        """一つ左の座標を返します.

        :return: 一つ左の座標
        """

        return GridPosition(
            max(0, self._x - 1), self._y)

    def right(self) -> GridPosition:
        """一つ右の座標を返します.

        :return: 一つ右の座標
        """

        return GridPosition(self._x + 1, self._y)

    def calc_distance(self, pos: GridPosition) -> int:
        """指定した座標との距離を計算します.

        グリッド単位での距離となります.
        斜め上の座標を指定した場合、斜め1マスではなく、横→縦で2マスとなる点に注意してください.

        :params pos: 比較先の座標
        :return: 距離
        """

        dx = abs(pos.x - self.x)
        dy = abs(pos.y - self.y)
        return dx + dy

    def __eq__(self, other) -> bool:
        if isinstance(other, tuple):
            x, y = other
        elif isinstance(other, GridPosition):
            x, y = other.get()
        else:
            raise TypeError

        return self.x == x and self.y == y

    def __str__(self):
        return f'({self._x},{self._y})'
