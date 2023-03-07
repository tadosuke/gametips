"""装備品."""
from __future__ import annotations

from dataclasses import dataclass
import typing as tp

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

    name: ItemName = ItemName('')  # 名前
    part_id: int = 0  # 装備部位
    params: Parameters = Parameters()  # パラメーター


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
    def part_id(self) -> int:
        """装備部位 ID."""
        return self._base_data.part_id

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
            base_param = self._base_data.params.get(pid)
            if base_param is None:
                continue
            level_value = self._calc_level_param(pid)
            params.set(pid, ParameterValue(base_param.value + level_value))

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


class AllEquipments:
    """全部位の装備."""

    def __init__(self):
        self._equipments: dict[int, tp.Optional[Equipment]] = {}

    def set(self, eq: Equipment) -> tp.Optional[Equipment]:
        """装備品を設定します.

        同じ部位に既に装備があった場合は入れ替わります.

        :param eq: 装備品
        :return: 入れ替わった装備。空の場合は None
        """
        before = self._equipments.get(eq.part_id)
        self._equipments[eq.part_id] = eq
        return before

    def get(self, part_id: int) -> tp.Optional[Equipment]:
        """指定部位の装備を取得します.

        :param part_id: 部位 ID
        :return: 装備品。装備していない場合は None
        """
        return self._equipments.get(part_id)

    def pop(self, part_id: int) -> tp.Optional[Equipment]:
        """指定部位の装備を外します.

        :param part_id: 部位 ID
        :return: 装備。装備していなかった場合は None
        """
        before = self._equipments.pop(part_id, None)
        return before

    def calc_params(self) -> Parameters:
        """全部位の装備パラメーターの合計値を得ます."""
        params = Parameters()
        for eq in self._equipments.values():
            params += eq.calc_params()
        return params
