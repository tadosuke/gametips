from enum import Flag, Enum, auto


class ConditionId(Flag):
    ATK_UP = auto()  # 攻撃力アップ
    ATK_DOWN = auto()  # 攻撃力ダウン


class Condition:

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
    ATK_UP = auto()  # 攻撃力アップ
    DEF_UP = auto()  # 防御力アップ


class SkillDict:

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


class Skill:

    def __init__(self, id_, level=1):
        assert 1 <= level

        self._id = id_
        self._level = level

    @property
    def id(self):
        return self._id

    @property
    def level(self):
        return self._level

    def set_level(self, level):
        assert 1 <= level

        self._level = level

    def apply_atk(self, atk):
        if self.id == SkillId.ATK_UP:
            atk += self.level * 2
        return atk


class Weapon:

    def __init__(self, atk):
        self._atk = atk

    @property
    def atk(self):
        return self._atk


class Character:

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
            atk += self.weapon.atk
        return atk
