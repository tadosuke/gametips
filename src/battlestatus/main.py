"""戦闘ステータス計算.

キャラクターの基本能力値、武器、スキル、状態異常などを加味した攻撃力を計算するサンプルです.
"""

from enum import Enum, auto

from battlestatus.condition import Condition
from battlestatus.weapon import Weapon


class SkillId(Enum):
    """スキル ID."""

    ATK_UP = auto()  # 攻撃力アップ
    DEF_UP = auto()  # 防御力アップ


class SkillDict:
    """スキル辞書."""

    def __init__(self) -> None:
        self._dict: dict[SkillId, int] = {}

    def add(self, skill_id: SkillId, level: int = 1) -> None:
        """スキルを追加します.

        :param skill_id: スキル ID
        :param level: スキルレベル
        """
        self._dict[skill_id] = level

    def has(self, skill_id: SkillId) -> bool:
        """指定のスキルを持っているか？

        :param skill_id: スキル ID
        :return: 持っていたら True
        """
        return skill_id in self._dict

    def get_level(self, skill_id: SkillId) -> int:
        """スキルレベルを得ます.

        :param skill_id: スキル ID
        :return: スキルレベル
        """
        if not self.has(skill_id):
            return 0
        return self._dict[skill_id]

    def apply_atk(self, atk: float) -> float:
        """スキルを攻撃力に適用します.

        :param atk: 適用前の攻撃力
        :return: 適用後の攻撃力
        """
        if self.has(SkillId.ATK_UP):
            atk += self.get_level(SkillId.ATK_UP) * 2
        return atk


class Character:
    """キャラクター.

    :param atk: 攻撃力
    """

    def __init__(self, atk=10) -> None:
        self._atk = atk
        self._weapon = None
        self._condition = Condition()
        self._skills = SkillDict()

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
        atk = self._atk
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
