"""言語システム共通の型定義."""

from enum import Enum
from pathlib import Path


# 辞書の内部データ型
DictionaryDataType = dict[str, str]


class LanguageId(Enum):
    """言語 ID."""

    Japanese = 'ja'
    English = 'en'


class AbstractDictionary:
    """テキスト辞書の抽象クラス.

    :param data: 辞書データ
    """

    def __init__(self, data: DictionaryDataType) -> None:
        self._data = data

    def _get_data(self) -> DictionaryDataType:
        return self._data


class AbstractReader:
    """言語辞書を読み込む抽象クラス."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self, language: LanguageId):
        """指定した言語で辞書を読み込みます.

        :param language: 言語
        """
        return None

    def _get_path(self) -> Path:
        return self._path
