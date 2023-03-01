"""状態異常."""

from enum import Flag, auto


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