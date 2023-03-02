"""戦闘パラメーター."""
from __future__ import annotations

from enum import Enum, auto


class ParameterValue:
    """パラメーターの値.

    :param value: 初期値
    """

    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError

        self._value = value

    @property
    def value(self) -> int:
        return self._value


class ParameterId(Enum):
    """パラメーター ID."""

    ATK = auto()
    DEF = auto()
    MAT = auto()
    MDF = auto()
    DEX = auto()
    SPD = auto()
    LUK = auto()


class Parameter:
    """戦闘パラメーター."""

    def __init__(self):
        self._values = {i: ParameterValue(0) for i in ParameterId}

    def get(self, id_: ParameterId) -> ParameterValue:
        """パラメーターを取得します.

        :return: パラメーター
        """
        return self._values[id_]
