"""キャラクター."""

from battlestatus.condition import Condition
from battlestatus.parameter import Parameter, ParameterValue, ParameterId
from battlestatus.skill import SkillDict
from battlestatus.weapon import Weapon


class Character:
    """キャラクター.

    :param param: 初期パラメータ
    """

    def __init__(self, param: Parameter = None) -> None:
        if param is not None:
            self._param = param
        else:
            self._param = Parameter()
        self._weapon = None
        self._condition = Condition()
        self._skills = SkillDict()

    @property
    def atk(self) -> int:
        return self._param.get(ParameterId.ATK).value

    @property
    def condition(self) -> Condition:
        """状態異常."""
        return self._condition

    def equip(self, weapon: Weapon) -> None:
        """武器を装備します.

        :param weapon: 武器
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
        atk = self.atk
        atk = self._calc_atk_weapon(atk)
        atk = self.condition.apply_atk(atk)
        atk = self.skills.apply_atk(atk)
        return int(atk)

    def _calc_atk_weapon(self, atk: int) -> int:
        """武器の攻撃力を適用します.

        :param atk: 適用前の攻撃力
        :return: 適用後の攻撃力
        """
        if self.weapon is not None:
            atk += self.weapon.calc_atk()
        return atk
