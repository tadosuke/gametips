"""reader モジュールのテスト."""

import unittest
from pathlib import Path

from language.reader import CsvReader
from language.types import LanguageId


class TestCsvReader(unittest.TestCase):

    def test_read(self):
        reader = CsvReader(Path('./language/test.csv'))
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertTrue(is_success)
        self.assertEqual('text1', data.get('hoge'))
        self.assertEqual('text2', data.get('fuga'))
        self.assertIsNone(data.get('piyo'))

        # 存在しないファイル
        reader = CsvReader(Path('./language/invalid.csv'))
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertFalse(is_success)
        self.assertEqual({}, data)

        # csv 以外のファイル
        reader = CsvReader(Path('./language/test.txt'))
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertFalse(is_success)


if __name__ == '__main__':
    unittest.main()
