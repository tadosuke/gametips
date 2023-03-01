"""スキル."""

from enum import Enum, auto


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
