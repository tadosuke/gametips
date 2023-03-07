"""戦闘パラメーター."""
from __future__ import annotations

from enum import Enum, auto


class ParameterValue:
    """パラメーターの値.

    :params value: 初期値
    """

    MIN = 0
    MAX = 999

    def __init__(self, value: int) -> None:
        if not self.MIN <= value <= self.MAX:
            raise ValueError

        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def __eq__(self, other) -> bool:
        if isinstance(other, ParameterValue):
            return self._value == other.value
        else:
            return self._value == other

    def __add__(self, other) -> ParameterValue:
        if isinstance(other, ParameterValue):
            return ParameterValue(self._value + other.value)
        return ParameterValue(self._value + other)


class ParameterId(Enum):
    """パラメーター ID."""

    ATK = auto()
    DEF = auto()
    MAT = auto()
    MDF = auto()
    DEX = auto()
    SPD = auto()
    LUK = auto()


class Parameters:
    """全パラメーター."""

    def __init__(self) -> None:
        self._values = {i: ParameterValue(0) for i in ParameterId}

    def get(self, id_: ParameterId) -> ParameterValue:
        """パラメーターを取得します.

        :params id_: パラメーター ID
        :return: パラメーター
        """
        return self._values[id_]

    def set(self, id_: ParameterId, value: ParameterValue) -> None:
        """パラメーターを設定します.

        :params id_: パラメーター ID
        :params value: 設定する値
        """
        self._values[id_] = value

    def __add__(self, other) -> Parameters:
        assert isinstance(other, Parameters)

        for i in ParameterId:
            self._values[i] += other.get(i)

        return self
