from enum import Flag, Enum, auto


class ConditionId(Flag):
    """状態異常 ID."""

    ATK_UP = auto()  # 攻撃力アップ
    ATK_DOWN = auto()  # 攻撃力ダウン


class Condition:
    """状態異常."""

    def __init__(self, id_=None):
        self._id = id_

    def has(self, id_):
        if self._id is None:
            return False
        return id_ in self._id

    def add(self, id_):
        if self._id is None:
            self._id = id_
        else:
            self._id |= id_
        self._offset()

    def remove(self, id_):
        if self._id is None:
            return
        self._id &= ~id_
        self._offset()

    def _offset(self):
        both = ConditionId.ATK_UP | ConditionId.ATK_DOWN
        if both in self._id:
            self._id = None

    def apply_atk(self, atk):
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

    def __init__(self):
        self._dict: dict[SkillId, int] = {}

    def add(self, skill_id, level=1):
        self._dict[skill_id] = level

    def has(self, skill_id):
        return skill_id in self._dict

    def get_level(self, skill_id):
        if not self.has(skill_id):
            return 0
        return self._dict[skill_id]

    def apply_atk(self, atk):
        if self.has(SkillId.ATK_UP):
            atk += self.get_level(SkillId.ATK_UP) * 2
        return atk


class WeaponId:
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
    """

    def __init__(self, id_):
        assert _WEAPON_DICT.get(id_)
        self._id = id_
        self._level = 1

    @property
    def id(self):
        """武器 ID."""
        return self._id

    @property
    def level(self):
        """武器レベル."""
        return self._level

    def set_level(self, level):
        """武器レベルを設定する."""
        assert 1 <= level
        self._level = level

    def calc_atk(self):
        """武器の攻撃力を計算する."""
        atk = self._get_base_atk()
        atk += self._calc_level_atk()
        return int(atk)

    def _get_base_atk(self):
        """基本攻撃力を得る."""
        return _WEAPON_DICT[self._id]

    def _calc_level_atk(self):
        """レベルによる補正値を計算する."""
        if self._level == 1:
            return 0
        base = self._get_base_atk()
        ratio = float(self._level-1.0) / 5.0
        return base * ratio


class Character:
    """キャラクター.

    :param atk: 攻撃力
    """

    def __init__(self, atk=10):
        self._atk = atk
        self._weapon = None
        self._condition = Condition()
        self._skills = SkillDict()

    @property
    def condition(self):
        return self._condition

    def equip(self, weapon):
        self._weapon = weapon

    def unequip(self):
        self._weapon = None

    @property
    def weapon(self):
        return self._weapon

    @property
    def skills(self):
        return self._skills

    def calc_atk(self):
        atk = self._atk
        atk = self._calc_atk_weapon(atk)
        atk = self.condition.apply_atk(atk)
        atk = self.skills.apply_atk(atk)
        return int(atk)

    def _calc_atk_weapon(self, atk):
        if self.weapon is not None:
            atk += self.weapon.calc_atk()
        return atk
