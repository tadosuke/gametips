"""キャラクター."""

from battlestatus.condition import Condition
from battlestatus.equipment import AllEquipments
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
        self._equipments = AllEquipments()
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

    @property
    def equipments(self) -> AllEquipments:
        """全部位の装備."""
        return self._equipments

    @property
    def skills(self) -> SkillDict:
        """習得しているスキル."""
        return self._skills

    def calc_atk(self) -> int:
        """装備・スキルなどを加味した攻撃力を計算します.

        :return: 攻撃力
        """
        id_ = ParameterId.ATK
        atk = self.params.get(id_).value
        atk = self._calc_param_equip(id_, atk)
        atk = self.condition.apply_param(id_, atk)
        atk = self.skills.apply_param(id_, atk)
        return int(atk)

    def _calc_param_equip(self, id_: ParameterId, value: int) -> int:
        """装備品のパラメーターを適用します.

        :param id_: パラメーター ID
        :param value: 適用前のパラメーター値
        :return: 適用後のパラメーター値
        """
        params = self._equipments.calc_params()
        return value + params.get(id_).value

    def can_act(self) -> bool:
        """行動可能か？

        :return: 行動可能なら True
        """
        can_act = True
        can_act &= self.condition.can_act()
        return can_act
