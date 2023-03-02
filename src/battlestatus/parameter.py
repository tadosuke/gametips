"""戦闘パラメーター."""
from __future__ import annotations


class ParameterValue:
    """パラメーターの値.

    :param value: 初期値
    """

    def __init__(self, value: int) -> None:
        if value < 0:
            raise ValueError

        self._value = value

    @property
    def value(self) -> int:
        return self._value


class Parameter:
    """戦闘パラメーター."""

    def __init__(self):
        self._atk = ParameterValue(0)
        self._def = ParameterValue(0)
        self._mat = ParameterValue(0)
        self._mdf = ParameterValue(0)
        self._dex = ParameterValue(0)
        self._spd = ParameterValue(0)
        self._luk = ParameterValue(0)

    @property
    def attack(self) -> ParameterValue:
        """攻撃力."""
        return self._atk

    @property
    def defence(self) -> ParameterValue:
        """防御力."""
        return self._def

    @property
    def mattack(self) -> ParameterValue:
        """魔法攻撃力."""
        return self._mat

    @property
    def mdefence(self) -> ParameterValue:
        """魔法防御力."""
        return self._mdf

    @property
    def dexterity(self) -> ParameterValue:
        """器用さ."""
        return self._dex

    @property
    def speed(self) -> ParameterValue:
        """素早さ."""
        return self._spd

    @property
    def luck(self) -> ParameterValue:
        """運."""
        return self._luk
