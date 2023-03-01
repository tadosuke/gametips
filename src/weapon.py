"""武器モジュール."""


class Weapon:

    def __init__(self, id_: int) -> None:
        self._id = id_

    @property
    def id(self) -> int:
        return self._id
