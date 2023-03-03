"""キャラクター."""

from battlestatus.condition import Condition
from battlestatus.parameters import Parameters, ParameterId, ParameterValue
from battlestatus.skill import SkillDict
from battlestatus.weapon import Weapon


class Character:
    """キャラクター.

    :param params: 初期パラメータ
    """

    def __init__(self, params: Parameters = None) -> None:
        if params is not None:
            self._params = params
        else:
            self._params = Parameters()
        self._weapon = None
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

    def equip(self, weapon: Weapon) -> None:
        """武器を装備します.

        :params weapon: 武器
        """
        self._weapon = weapon

    def unequip(self) -> None:
        """武器の装備を解除します."""
        self._weapon = None

    @property
    def weapon(self) -> Weapon:
        """武器."""
        return self._weapon

    @property
    def skills(self) -> SkillDict:
        """習得しているスキル."""
        return self._skills

    def calc_atk(self) -> int:
        """武器・スキルなどを加味した攻撃力を計算します.

        :return: 攻撃力
        """
        atk = self.params.get(ParameterId.ATK).value
        atk = self._calc_atk_weapon(atk)
        atk = self.condition.apply_atk(atk)
        atk = self.skills.apply_atk(atk)
        return int(atk)

    def _calc_atk_weapon(self, atk: int) -> int:
        """武器の攻撃力を適用します.

        :params atk: 適用前の攻撃力
        :return: 適用後の攻撃力
        """
        if self.weapon is not None:
            atk += self.weapon.calc_atk()
        return atk
