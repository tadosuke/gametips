"""言語辞書."""

from __future__ import annotations

import csv
import os
import typing as tp


class Dictionaries:
    """辞書の集合."""

    def __init__(self) -> None:
        self._dictionaries: dict[str, Dictionary] = {}

    def add(self, dictionary: Dictionary) -> None:
        """辞書を追加します..

        :param dictionary: 辞書
        """
        self._dictionaries[dictionary.name] = dictionary

    def remove(self, dictionary_name: str) -> None:
        """辞書を削除します.

        :param dictionary_name: 辞書名
        """
        self._dictionaries.pop(dictionary_name, None)

    def get(self, dictionary_name: str) -> tp.Optional[Dictionary]:
        """辞書を得ます.

        :param dictionary_name: 辞書名
        :return: 辞書。見つからない場合は None
        """
        return self._dictionaries.get(dictionary_name)


class Dictionary:
    """辞書."""

    def __init__(
            self,
            dictionary_name: str,
            data: dict[tp.Hashable, str] = None) -> None:
        self._name = dictionary_name
        if data is not None:
            self._text_dict = data
        else:
            self._text_dict: dict[tp.Hashable, str] = {}

    @property
    def name(self) -> str:
        """辞書名."""
        return self._name

    def get_text(self, id_: tp.Hashable) -> tp.Optional[str]:
        """テキストを得ます.

        :param id_: テキスト ID
        :return: テキスト。見つからない場合は None
        """
        return self._text_dict.get(id_)


class AbstractReader:
    """辞書を読み込む抽象クラス."""

    def read(self, *args) -> tp.Optional[Dictionary]:
        """辞書を読み込みます."""
        return None


class CsvReader(AbstractReader):
    """CSV ファイルから辞書を読み込むクラス."""

    def read(self, csv_path: str) -> tp.Optional[Dictionary]:
        """(override)辞書を読み込みます.

        :param csv_path: CSV ファイルのパス
        :except FileNotFoundError: ファイルが存在しないとき
        :except ValueError: CSV 以外のファイルを指定したとき
        :return: 辞書。辞書名にはファイル名が入ります
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError
        ext = os.path.splitext(csv_path)[1]
        if ext != '.csv':
            raise ValueError

        data: dict[str, str] = {}
        with open(csv_path, encoding='utf8', newline='') as f:
            csvreader = csv.reader(f, delimiter=',')
            for row in csvreader:
                assert 2 <= len(row)
                id_ = row[0]
                text = row[1]
                data[id_] = text

        return Dictionary(os.path.basename(csv_path), data)

