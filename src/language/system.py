"""言語システム."""

from __future__ import annotations
import typing as tp

from language.types import AbstractReader, LanguageId

# 辞書の内部データ型
DictionaryDataType = dict[str, str]


class System:
    """言語システムクラス."""

    def __init__(
            self,
            language: LanguageId = LanguageId.Japanese) -> None:
        self._dictionaries: dict[str, TextDictionary] = {}
        self._language = language

    def load_dictionary(self, reader: AbstractReader) -> None:
        """辞書を読み込みます.

        :param reader: 辞書の読み込みオブジェクト
        """
        self._dictionaries = TextDictionary(reader, self._language)

    def add_dictionary(self, dictionary: TextDictionary) -> None:
        """辞書を追加します..

        :param dictionary: 辞書
        """
        self._dictionaries[dictionary.name] = dictionary

    def remove_dictionary(self, dictionary_name: str) -> None:
        """辞書を削除します.

        :param dictionary_name: 辞書名
        """
        self._dictionaries.pop(dictionary_name, None)

    def get_dictionary(self, dictionary_name: str) -> tp.Optional[TextDictionary]:
        """辞書を得ます.

        :param dictionary_name: 辞書名
        :return: 辞書。見つからない場合は None
        """
        return self._dictionaries.get(dictionary_name)

    def change_language(self, language: LanguageId):
        """言語を変更します."""
        self._language = language

    @property
    def language(self) -> LanguageId:
        """現在の言語."""
        return self._language

    def _reload_all_dictionaries(self) -> None:
        """全ての辞書を再読み込みします."""
        for dict_ in self._dictionaries.values():
            dict_.reload(self._language)


class TextDictionary:
    """テキスト辞書クラス.

    :param reader: 読み込みオブジェクト
    :param language: 言語
    """

    def __init__(
            self,
            reader: AbstractReader,
            language: LanguageId = LanguageId.Japanese) -> None:
        self._reader = reader
        self._data: DictionaryDataType = {}
        self.reload(language)

    @property
    def name(self) -> str:
        """辞書名."""
        return self._reader.name

    def is_empty(self) -> bool:
        """辞書が空か？"""
        return not self._data

    def get_text(self, key: str) -> tp.Optional[str]:
        """テキストを得ます.

        :param key: テキストのキー
        :return: テキスト。見つからない場合は None
        """
        return self._data.get(key)

    def reload(self, language: LanguageId) -> None:
        """指定した言語で辞書を再読み込みします.

        :param language: 言語
        """
        is_success, data = self._reader.read(language)
        if is_success:
            self._data = data
        else:
            self._data = {}
