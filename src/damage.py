"""ダメージ計算モジュール."""

from enum import Enum, auto


class Attribute(Enum):
    """攻撃属性."""

    NONE = auto()
    FIRE = auto()
    WATER = auto()
    WIND = auto()
    EARTH = auto()


class AttackInfo:
    """攻撃情報.

    :param power: 攻撃力
    :param attr: 属性
    """

    def __init__(
            self,
            power: int,
            attr: Attribute = Attribute.NONE) -> None:
        if power < 0:
            raise ValueError

        self._power = power
        self._attr = attr

    @property
    def power(self) -> int:
        """攻撃力."""

        return self._power

    @property
    def attribute(self) -> Attribute:
        """属性."""

        return self._attr


class DefenceInfo:
    """防御情報.

    :param power: 攻撃力
    :param res_dict: 属性抵抗率の辞書（属性→抵抗率）
    """

    def __init__(
            self,
            power: int,
            res_dict: dict[Attribute, float] = None) -> None:
        if power < 0:
            raise ValueError

        self._power = power
        if res_dict is None:
            self._res_dict = {}
        else:
            self._res_dict = res_dict

    @property
    def power(self) -> int:
        """防御力."""

        return self._power

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
    def value(self) -> float:
        """ダメージ値."""

        return self._value

    def _calc(self) -> float:
        """ダメージ値を計算します.

        :return: ダメージ値
        """

        at_pow = self._attack.power
        df_pow = self._defence.power
        val = at_pow - df_pow
        val = self._apply_regist(val)
        return val

    def _apply_regist(self, val: float) -> float:
        """属性抵抗率を適用します.

        :param val: ダメージ値
        :return: 適用後のダメージ値
        """

        attr = self._attack.attribute
        ratio = self._defence.get_regist(attr)
        return val * ratio

