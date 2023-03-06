"""キャラクター."""

import typing as tp

from battlestatus.condition import Condition
from battlestatus.equipment import Equipment
from battlestatus.parameters import Parameters, ParameterId
from battlestatus.skill import SkillDict


class Character:
    """キャラクター.

    :param params: 初期パラメータ
    """

    def __init__(self, params: Parameters = None) -> None:
        if params is not None:
            self._params = params
        else:
            self._params = Parameters()
        self._equipment: tp.Optional[Equipment] = None
        self._condition = Condition()
        self._skills = SkillDict()

    @property
    def params(self) -> Parameters:
        """全パラメーター."""
        return self._params

    @property
    def condition(self) -> Condition:
        """状態異常."""
        return self._condition

    def set_equip(self, eq: tp.Optional[Equipment]) -> None:
        """装備品を設定します.

        :params eq: 装備。None を指定すると解除します
        """
        self._equipment = eq

    def get_equip(self) -> tp.Optional[Equipment]:
        """装備品を得ます.

        :return: 装備品。装備していないときは None
        """
        return self._equipment

    @property
    def skills(self) -> SkillDict:
        """習得しているスキル."""
        return self._skills

    def calc_atk(self) -> int:
        """装備・スキルなどを加味した攻撃力を計算します.

        :return: 攻撃力
        """
        atk = self.params.get(ParameterId.ATK).value
        atk = self._calc_atk_equip(atk)
        atk = self.condition.apply_atk(atk)
        atk = self.skills.apply_atk(atk)
        return int(atk)

    def _calc_atk_equip(self, atk: int) -> int:
        """装備品の攻撃力を適用します.

        :params atk: 適用前の攻撃力
        :return: 適用後の攻撃力
        """
        if self._equipment is not None:
            eq_param = self._equipment.calc_params()
            eq_atk = eq_param.get(ParameterId.ATK)
            if eq_atk is None:
                return atk
            atk += eq_atk.value
        return atk
