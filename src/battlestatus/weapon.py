"""武器."""

from enum import Enum, auto


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
