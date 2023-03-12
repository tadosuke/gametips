"""system モジュールのテスト."""

import unittest
from pathlib import Path
from unittest import mock

from language.reader import CsvReader
from language.system import System, TextDictionary
from language.types import LanguageId


class TestSystem(unittest.TestCase):

    def test_init(self):
        ds = System()
        self.assertEqual({}, ds._dictionaries)

    def test_load_dictionary(self):
        pass


class TestTextDictionary(unittest.TestCase):

    def test_init(self):
        reader = CsvReader(Path('language/test.csv'))
        with mock.patch('language.system.TextDictionary.reload') as mp_reload:
            TextDictionary(reader)
            mp_reload.assert_called_once_with(LanguageId.Japanese)

    def test_get_text(self):
        reader = CsvReader(Path('language/test.csv'))
        d = TextDictionary(reader)
        self.assertFalse(d.is_empty())
        text = d.get_text('hoge')
        self.assertEqual('text1', text)

    def test_reload(self):
        reader = CsvReader(Path('language/test.csv'))
        d = TextDictionary(reader)

        # 成功
        with mock.patch.object(d._reader, 'read', return_value=(True, {'hoge': 'fuga'})):
            d.reload(LanguageId.Japanese)
            self.assertFalse(d.is_empty())

        # 失敗
        with mock.patch.object(d._reader, 'read', return_value=(False, {})):
            d.reload(LanguageId.Japanese)
            self.assertTrue(d.is_empty())


if __name__ == '__main__':
    unittest.main()
