"""レベルアップ計算."""

import typing as tp


class Calculator:
    """レベルアップ計算機.

    :params exps: レベルごとの経験値
    """

    def __init__(
            self,
            exps: tp.Sequence[int]) -> None:
        assert exps
        self._exps = tuple(exps)

    def calc(self, exp: int) -> int:
        """経験値に対応するレベルを計算します.

        :params exp: 経験値
        :return: レベル
        """
        assert 0 <= exp

        for lv, e in enumerate(self._exps):
            if exp < e:
                return lv
        return self.get_max_level()

    def get_max_level(self) -> int:
        """最大レベルを得ます.

        :return: 最大レベル
        """
        return len(self._exps)


class Character:
    """キャラクター.

    :params calculator: レベル計算オブジェクト
    :params exp: 初期経験値
    """

    def __init__(
            self,
            calculator: Calculator,
            exp: int = 0,
            name: str = '') -> None:
        assert 0 <= exp

        self._calculator = calculator
        self._name = name
        self._exp = exp
        self._level = 0

        self._update_level()

    @property
    def exp(self) -> int:
        """経験値."""
        return self._exp

    @property
    def name(self) -> str:
        """名前."""
        return self._name

    @property
    def level(self) -> int:
        """レベル."""
        return self._level

    def add_exp(self, exp: int) -> int:
        """経験値を加算します.

        :params exp: 経験値
        :return: レベルの上昇量
        """
        assert 0 <= exp
        self._exp += exp
        diff = self._update_level()

        return diff

    def _update_level(self) -> int:
        """レベルを計算し直す.

        :return レベルの上昇量
        """
        before = self._level
        self._level = self._calculator.calc(self._exp)
        return self.level - before

    def __str__(self) -> str:
        return f'{self.name}: LV={self.level}, EXP={self.exp}'
