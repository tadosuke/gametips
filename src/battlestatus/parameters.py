"""戦闘パラメーター."""
from __future__ import annotations

from enum import Enum, auto


class ParameterValue:
    """パラメーターの値.

    :params value: 初期値
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
