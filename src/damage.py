"""ダメージ計算モジュール."""
from __future__ import annotations

from enum import Enum, Flag, auto


class AttackType(Enum):
    """攻撃タイプ."""

    PHYSICS = auto()  # 物理攻撃
    MAGIC = auto()  # 魔法攻撃


class Attribute(Enum):
    """属性."""

    NONE = auto()  # 無
    FIRE = auto()  # 火
    WATER = auto()  # 水
    WIND = auto()  # 風
    EARTH = auto()  # 土


class Condition(Flag):
    """状態異常."""

    POISON = auto()  # 毒
    SLEEP = auto()  # 眠り


# [型エイリアス] 属性耐性の辞書（属性：ダメージ倍率）
AttributeResistanceDictType = dict[Attribute, float]

# [型エイリアス] 状態異常特攻の辞書（状態異常：ダメージ倍率）
ConditionMagnificationDictType = dict[Condition, float]


class AttackInfo:
    """攻撃情報.

    :param power: 威力
    :param type_: 攻撃タイプ
    :param attr: 属性
    """

    def __init__(
            self,
            power: int,
            type_: AttackType = AttackType.PHYSICS,
            attr: Attribute = Attribute.NONE,
            cond_mag_dict: ConditionMagnificationDictType = None) -> None:
        if power < 0:
            raise ValueError

        self._power = power
        self._type = type_
        self._attr = attr
        if cond_mag_dict is not None:
            self._cond_mag_dict = cond_mag_dict
        else:
            self._cond_mag_dict = {}

    @property
    def power(self) -> int:
        """威力."""

        return self._power

    @property
    def attribute(self) -> Attribute:
        """属性."""

        return self._attr

    @property
    def condition_magnifications(self) -> ConditionMagnificationDictType:
        """状態異常特攻の辞書."""

        return self._cond_mag_dict

    def is_physics(self) -> bool:
        """物理攻撃か？"""

        return self._type == AttackType.PHYSICS

    def is_magic(self) -> bool:
        """魔法攻撃か？"""

        return self._type == AttackType.MAGIC

    def get_condition_magnification(self, cond: Condition) -> float:
        """指定した状態異常特攻の倍率を得ます."""

        mag = self._cond_mag_dict.get(cond)
        if mag is None:
            return 1.0
        return mag


class DefenceInfo:
    """防御情報.

    :param physics: 物理防御力
    :param magic: 魔法防御力
    :param res_dict: 属性抵抗率の辞書（属性→抵抗率）
    :param conditions: 状態異常。正常時は None
    """

    def __init__(
            self,
            physics: int,
            magic: int,
            res_dict: AttributeResistanceDictType = None,
            conditions: Condition = None) -> None:
        if physics < 0:
            raise ValueError
        if magic < 0:
            raise ValueError

        self._physics = physics
        self._magic = magic
        if res_dict is None:
            self._res_dict = {}
        else:
            self._res_dict = res_dict
        self._conditions = conditions

    @property
    def physical_power(self) -> int:
        """物理防御力."""

        return self._physics

    @property
    def magical_power(self) -> int:
        """魔法防御力."""

        return self._magic

    def get_regist(self, attr: Attribute) -> float:
        """属性抵抗率を得ます.

        :param attr: 属性
        :return: 属性抵抗率。見つからない場合は 1.0
        """

        res = self._res_dict.get(attr)
        if res is None:
            return 1.0
        return res

    def has_condition(self) -> bool:
        """状態異常を持っているか？"""

        return self._conditions is not None

    def is_condition(self, condition: Condition) -> bool:
        """指定の状態異常を持っているか？"""

        if self._conditions is None:
            return False
        
        return bool(self._conditions & condition)


class Damage:
    """ダメージ.

    :param attack: 攻撃情報
    :param defence: 防御情報
    """

    def __init__(
            self,
            attack: AttackInfo,
            defence: DefenceInfo) -> None:
        self._attack = attack
        self._defence = defence
        self._value = 0

    @property
    def value(self) -> int:
        """ダメージ値."""

        return self._value

    def calc(self) -> int:
        """ダメージ値を計算します.

        丸め誤差を少なくするため、ギリギリまで float で計算し、最後に int で丸めた値を返します。

        :return: ダメージ値
        """

        # 基本ダメージ
        val = self._calc_basic()
        # 状態異常特攻
        val = self._calc_cond_mag(val)
        # 属性抵抗
        val = self._calc_regist(val)

        return int(val)

    def _calc_basic(self) -> float:
        """基本ダメージ値を計算します.

        :return: 基本ダメージ値
        """

        at_pow = self._attack.power

        if self._attack.is_physics():
            # 物理ダメージ
            df_pow = self._defence.physical_power
        elif self._attack.is_magic():
            # 魔法ダメージ
            df_pow = self._defence.magical_power
        else:
            raise NotImplementedError

        return float(max(0, at_pow - df_pow))

    def _calc_cond_mag(self, val: float) -> float:
        """異状態異常特攻を適用したダメージ値を計算します.

        複数の状態異常と一致する場合は、足し合わせた倍率が適用されます.
        倍率 1.5 の特攻が３つある場合、2.5倍になります.

        :param val: ダメージ値
        :return: 適用後のダメージ値
        """

        matches = []
        for cond, mag in self._attack.condition_magnifications.items():
            if self._defence.is_condition(cond):
                matches.append(mag)

        sum_mag = 1.0
        for mag in matches:
            sum_mag += (mag - 1.0)

        return val * sum_mag

    def _calc_regist(self, val: float) -> float:
        """属性抵抗を適用したダメージ値を計算します.

        :param val: ダメージ値
        :return: 適用後のダメージ値
        """

        attr = self._attack.attribute
        ratio = self._defence.get_regist(attr)
        return val * ratio
