"""言語辞書."""

from __future__ import annotations

import typing as tp


class Dictionaries:
    """辞書の集合."""

    def __init__(self) -> None:
        self._dictionaries: dict[str, Dictionary] = {}

    def get(self, dictionary_name: str) -> tp.Optional[Dictionary]:
        """辞書を得ます.

        :param dictionary_name: 辞書名
        :return: 辞書。見つからない場合は None
        """
        return self._dictionaries.get(dictionary_name)


class Dictionary:
    """辞書."""

    def __init__(self, dictionary_name: str) -> None:
        self._name = dictionary_name
        self._category_dict: dict[str, Category] = {}

    @property
    def name(self) -> str:
        return self._name

    def get_category(self, name: str) -> tp.Optional[Category]:
        return self._category_dict.get(name)


class Category:
    """カテゴリ."""

    def __init__(self, category_name: str) -> None:
        self._name = category_name
        self._text_dict: dict[str, str] = {}

    @property
    def name(self) -> str:
        return self._name

    def get_text(self, assign_name: str) -> tp.Optional[str]:
        return self._text_dict.get(assign_name)
