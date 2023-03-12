"""言語ファイルの読み込みモジュール."""

import csv
from collections.abc import Mapping
from pathlib import Path
import typing as tp

from language.types import AbstractReader, LanguageId, TextDictionaryDataType


class CsvReader(AbstractReader):
    """CSV ファイルから辞書データを読み込むクラス.

    :param csv_path: csv ファイルのパス
    """

    # 言語に対応する csv の列
    _LANGUAGE_ROWS: tp.ClassVar[Mapping[LanguageId, int]] = {
        LanguageId.Japanese: 1,
        LanguageId.English: 2,
    }

    def __init__(self, csv_path: Path) -> None:
        super().__init__(csv_path)

    def read(self, language: LanguageId) -> tuple[bool, TextDictionaryDataType]:
        """(override)辞書を読み込みます.

        :return: 読み込み結果（成功したら True）、辞書データ
        """
        path = self._get_path()
        try:
            with path.open(encoding='utf8', newline='') as f:
                csvreader = csv.reader(f, delimiter=',')
                data = self._read_from_reader(csvreader, language)
            return True, data
        except Exception as e:
            print(e)
            return False, {}

    def _read_from_reader(self, csvreader, language) -> dict[str, str]:
        data: dict[str, str] = {}
        for row in csvreader:
            assert 2 <= len(row)
            id_ = row[0]
            text = row[self._LANGUAGE_ROWS[language]]
            data[id_] = text
        return data


class NullReader(AbstractReader):
    """空の読み込みクラス."""

    def read(self, language: LanguageId) -> TextDictionaryDataType:
        return {}
