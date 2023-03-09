"""言語システム."""

import typing as tp

from language.dictionary import Dictionaries


class System:
    """言語システム."""

    def __init__(self) -> None:
        self._dictionaries = Dictionaries()

    @property
    def dictionaries(self) -> Dictionaries:
        """辞書の集合."""
        return self._dictionaries
