"""戦闘ステータス計算.

キャラクターの基本能力値、武器、スキル、状態異常などを加味した攻撃力を計算するサンプルです.
"""

from enum import Flag, Enum, auto


class ConditionId(Flag):
    """状態異常 ID."""

    ATK_UP = auto()  # 攻撃力アップ
    ATK_DOWN = auto()  # 攻撃力ダウン


class Condition:
    """状態異常.

    :param id_: 状態異常 ID
    """

    def __init__(self, id_: ConditionId = None) -> None:
        self._id = id_

    def has(self, id_: ConditionId) -> bool:
        """状態異常を持っているか？

        :param id_: 状態異常 ID
        :return: 状態異常を持っていたら True
        """
        if self._id is None:
            return False
        return id_ in self._id

    def add(self, id_: ConditionId) -> None:
        """状態異常を付与します.

        :param id_: 状態異常 ID
        """
        if self._id is None:
            self._id = id_
        else:
            self._id |= id_
        self._offset()

    def remove(self, id_: ConditionId) -> None:
        """状態異常を解除します.

        :param id_: 状態異常 ID
        """
        if self._id is None:
            return
        self._id &= ~id_
        self._offset()

    def _offset(self) -> None:
        """同時に付与できない状態異常を相殺します."""
        both = ConditionId.ATK_UP | ConditionId.ATK_DOWN
        if both in self._id:
            self._id = None

    def apply_atk(self, atk: float) -> float:
        """状態異常を攻撃力に適用します.

        :param atk: 適用前の攻撃力
        :return: 適用後の攻撃力
        """
        if self.has(ConditionId.ATK_UP):
            atk *= 1.25
        elif self.has(ConditionId.ATK_DOWN):
            atk *= 0.75
        return atk


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


class WeaponId(Enum):
    """武器 ID."""

    COPPER_SWORD = auto()  # 銅の剣
    IRON_SWORD = auto()  # 鉄の剣
    STEEL_SWORD = auto()  # 鋼の剣


# 武器の能力辞書
_WEAPON_DICT = {
    WeaponId.COPPER_SWORD: 5,
    WeaponId.IRON_SWORD: 10,
    WeaponId.STEEL_SWORD: 15,
}


class Weapon:
    """武器.

    :param id_: 武器 ID
    :param level: 武器レベル
    """

    def __init__(self, id_: WeaponId, level: int = 1) -> None:
        assert _WEAPON_DICT.get(id_)
        assert 1 <= level

        self._id = id_
        self._level = level

    @property
    def id(self) -> WeaponId:
        """武器 ID."""
        return self._id

    @property
    def level(self) -> int:
        """武器レベル."""
        return self._level

    def set_level(self, level: int) -> None:
        """武器レベルを設定します.

        :param level: 武器レベル
        """
        assert 1 <= level
        self._level = level

    def calc_atk(self) -> int:
        """武器の攻撃力を計算します.

        :return: 攻撃力
        """
        atk = self._get_base_atk()
        atk += self._calc_level_atk()
        return int(atk)

    def _get_base_atk(self) -> int:
        """武器の基本攻撃力を得ます.

        :return: 基本攻撃力
        """
        return _WEAPON_DICT[self._id]

    def _calc_level_atk(self) -> float:
        """武器レベルによる補正値を計算します.

        :return: 補正値
        """
        if self._level == 1:
            return 0
        base = self._get_base_atk()
        ratio = float(self._level - 1.0) / 5.0
        return base * ratio


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
