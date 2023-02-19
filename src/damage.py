"""ダメージ計算モジュール."""

from enum import Enum, auto


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
            attr: Attribute = Attribute.NONE) -> None:
        if power < 0:
            raise ValueError

        self._power = power
        self._type = type_
        self._attr = attr

    @property
    def power(self) -> int:
        """威力."""

        return self._power

    @property
    def attribute(self) -> Attribute:
        """属性."""

        return self._attr

    def is_physics(self) -> bool:
        """物理攻撃か？"""

        return self._type == AttackType.PHYSICS

    def is_magic(self) -> bool:
        """魔法攻撃か？"""

        return self._type == AttackType.MAGIC


class DefenceInfo:
    """防御情報.

    :param physics: 物理防御力
    :param magic: 魔法防御力
    :param res_dict: 属性抵抗率の辞書（属性→抵抗率）
    """

    def __init__(
            self,
            physics: int,
            magic: int,
            res_dict: dict[Attribute, float] = None) -> None:
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
        self._value = self._calc()

    @property
    def value(self) -> int:
        """ダメージ値."""

        return self._value

    def _calc(self) -> int:
        """ダメージ値を計算します.

        丸め誤差を少なくするため、ギリギリまで float で計算し、最後に int で丸めた値を返します。

        :return: ダメージ値
        """

        at_pow = self._attack.power

        if self._attack.is_physics():
            df_pow = self._defence.physical_power
        elif self._attack.is_magic():
            df_pow = self._defence.magical_power
        else:
            raise NotImplementedError

        # 基本ダメージ
        val = at_pow - df_pow
        if val <= 0:
            return 0

        # 属性抵抗
        val = self._apply_regist(val)

        return int(val)

    def _apply_regist(self, val: float) -> float:
        """属性抵抗率を適用します.

        :param val: ダメージ値
        :return: 適用後のダメージ値
        """

        attr = self._attack.attribute
        ratio = self._defence.get_regist(attr)
        return val * ratio
