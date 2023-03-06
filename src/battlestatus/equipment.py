"""装備品."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from battlestatus.parameters import Parameters, ParameterId, ParameterValue


class ItemName:
    """アイテム名."""

    MAX_LENGTH = 12

    def __init__(self, name: str) -> None:
        if self.MAX_LENGTH < len(name):
            raise ValueError
        self._name = name

    @property
    def value(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self._name

    def __eq__(self, other) -> bool:
        if isinstance(other, ItemName):
            return self._name == other.value
        return self._name == other

@dataclass
class BaseData:
    """基本データ."""

    name: ItemName = ItemName('')
    params: Parameters = Parameters()


class Equipment:
    """装備品.

    :params base_data: 基本データ
    """

    def __init__(self, base_data: BaseData) -> None:
        self._base_data = base_data
        self._level = 1

    @property
    def name(self) -> ItemName:
        """名前."""
        return self._base_data.name

    @property
    def level(self) -> int:
        """レベル."""
        return self._level

    def set_level(self, level: int) -> None:
        """レベルを設定します.

        :params level: レベル
        """
        assert 1 <= level
        self._level = level

    def calc_params(self) -> Parameters:
        """レベルを加味したパラメーターを計算します.

        :return: パラメーター
        """
        params = Parameters()

        for pid in ParameterId:
            value = self._calc_level_param(pid)
            params.set(pid, ParameterValue(value))

        return params

    def _calc_level_param(self, id_: ParameterId) -> int:
        """武器レベルによる補正値を計算します.

        :return: 補正値
        """
        if self._level == 1:
            return 0
        param = self._base_data.params.get(id_)
        if param is None:
            return 0
        base = param.value
        ratio = float(self._level - 1.0) / 5.0
        return int(base * ratio)
