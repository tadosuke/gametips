"""言語ファイルの読み込みモジュール."""

import csv
import logging
import traceback
from pathlib import Path

from language.types import AbstractReader, LanguageId, DictionaryDataType


class CsvReader(AbstractReader):
    """CSV ファイルから辞書データを読み込むクラス.

    :param csv_path: csv ファイルのパス
    """

    def __init__(self, csv_path: Path) -> None:
        super().__init__(csv_path)

    def read(self, language: LanguageId) -> tuple[bool, DictionaryDataType]:
        """(override)辞書を読み込みます.

        :return: 読み込み結果（成功したら True）、辞書データ
        """
        path = self._get_path()
        try:
            data: dict[str, str] = {}
            with path.open(encoding='utf8', newline='') as f:
                csvreader = csv.reader(f, delimiter=',')
                for row in csvreader:
                    assert 2 <= len(row)
                    id_ = row[0]
                    text = row[1]
                    data[id_] = text
            return True, data
        except Exception as e:
            print(e)
            return False, {}


class NullReader(AbstractReader):
    """空の読み込みクラス."""

    def read(self, language: LanguageId) -> DictionaryDataType:
        return {}
