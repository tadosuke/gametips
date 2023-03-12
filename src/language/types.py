"""言語システム共通の型定義."""

from __future__ import annotations
import typing as tp
from enum import Enum
from pathlib import Path


# 辞書の内部データ型
TextDictionaryDataType = dict[str, str]


class LanguageId(Enum):
    """言語 ID."""

    Japanese = 'ja'
    English = 'en'


class AbstractReader:
    """言語辞書を読み込む抽象クラス."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self, language: LanguageId) -> tuple[bool, TextDictionaryDataType]:
        """指定した言語で辞書を読み込みます.

        :param language: 言語
        :return: 辞書データ
        """
        raise NotImplementedError

    def _get_path(self) -> Path:
        return self._path

    @property
    def name(self) -> str:
        return self._path.stem
