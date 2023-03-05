"""武器."""
from __future__ import annotations

import typing as tp
from dataclasses import dataclass

from battlestatus.parameters import ParameterValue


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


@dataclass
class BaseParameter:
    """武器の基礎パラメーター."""

    name: ItemName = ItemName('')
    atk: ParameterValue = ParameterValue(0)


class BaseParameterDict:
    """武器の辞書.

    :params dict_: 辞書の元データ
    """

    def __init__(self, dict_: dict[tp.Hashable, BaseParameter]) -> None:
        self._dict: dict[tp.Hashable, BaseParameter] = dict_

    def get(self, id_: tp.Hashable) -> tp.Optional[BaseParameter]:
        param = self._dict.get(id_)
        if param is None:
            return None
        param.id = id_
        return param


class WeaponFactory:
    """武器生成クラス."""

    def __init__(self, base_param_dict: BaseParameterDict) -> None:
        self._base_param_dict = base_param_dict

    def create(
            self,
            id_: tp.Hashable,
            level: int = 1) -> tp.Optional[Weapon]:
        """武器を生成します.

        :params id_: 武器 ID
        :params level: 武器レベル
        :return: 武器。生成に失敗した場合は None
        """
        base_param = self._base_param_dict.get(id_)
        if base_param is None:
            return None

        weapon = Weapon(base_param)
        weapon.set_level(level)

        return weapon


class Weapon:
    """武器.

    :params base_param: 基本パラメータ
    """

    def __init__(self, base_param: BaseParameter) -> None:
        self._base_param = base_param
        self._level = 1

    @property
    def name(self) -> ItemName:
        """名前."""
        return self._base_param.name

    @property
    def level(self) -> int:
        """武器レベル."""
        return self._level

    def set_level(self, level: int) -> None:
        """武器レベルを設定します.

        :params level: 武器レベル
        """
        assert 1 <= level
        self._level = level

    def calc_atk(self) -> int:
        """武器の攻撃力を計算します.

        :return: 攻撃力
        """
        atk = self._base_param.atk.value
        atk += self._calc_level_atk()
        return int(atk)

    def _calc_level_atk(self) -> float:
        """武器レベルによる補正値を計算します.

        :return: 補正値
        """
        if self._level == 1:
            return 0
        base = self._base_param.atk.value
        ratio = float(self._level - 1.0) / 5.0
        return base * ratio



