"""reader モジュールのテスト."""

import unittest
from pathlib import Path

from language.reader import CsvReader
from language.types import LanguageId


class TestCsvReader(unittest.TestCase):

    def test_read(self):
        reader = CsvReader(Path('test.csv'))

        # 日本語
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertTrue(is_success)
        self.assertEqual('こんにちは', data.get('hello'))
        self.assertEqual('ありがとう', data.get('thanks'))
        self.assertIsNone(data.get('hoge'))

        # 英語
        is_success, data = reader.read(LanguageId.English)
        self.assertTrue(is_success)
        self.assertEqual('Hello!', data.get('hello'))
        self.assertEqual('Thank you!', data.get('thanks'))
        self.assertIsNone(data.get('hoge'))

        # 存在しないファイル
        reader = CsvReader(Path('./invalid.csv'))
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertFalse(is_success)
        self.assertEqual({}, data)

        # csv 以外のファイル
        reader = CsvReader(Path('./test.txt'))
        is_success, data = reader.read(LanguageId.Japanese)
        self.assertFalse(is_success)


if __name__ == '__main__':
    unittest.main()
