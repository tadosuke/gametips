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
        self.assertEqual(LanguageId.Japanese, ds.language)

        ds = System(LanguageId.English)
        self.assertEqual(LanguageId.English, ds.language)

    def test_load_dictionary(self):
        ds = System()
        reader = CsvReader(Path('test.csv'))
        self.assertEqual(0, len(ds._dictionaries))
        ds.load_dictionary(reader)
        self.assertEqual(1, len(ds._dictionaries))

    def test_remove_dictionary(self):
        ds = System()
        reader = CsvReader(Path('test.csv'))
        ds.load_dictionary(reader)

        # 存在しない辞書
        ds.remove_dictionary('invalid')
        self.assertEqual(1, len(ds._dictionaries))

        # 存在する辞書
        ds.remove_dictionary(reader.name)
        self.assertEqual(0, len(ds._dictionaries))

    def test_change_language(self):
        ds = System()
        with mock.patch.object(ds, '_reload_all_dictionaries') as mp_reload:
            ds.change_language(LanguageId.English)
            self.assertEqual(LanguageId.English, ds.language)
            mp_reload.assert_called_once()

    def test_get_text(self):
        ds = System()
        reader = CsvReader(Path('test.csv'))
        ds.load_dictionary(reader)

        # 成功
        text = ds.get_text('test', 'hoge')
        self.assertEqual('text1', text)

        # 辞書違い
        text = ds.get_text('invalid', 'hoge')
        self.assertIsNone(text)


class TestTextDictionary(unittest.TestCase):

    def test_init(self):
        reader = CsvReader(Path('test.csv'))
        with mock.patch('language.system.TextDictionary.reload') as mp_reload:
            TextDictionary(reader)
            mp_reload.assert_called_once_with(LanguageId.Japanese)

    def test_get_text(self):
        reader = CsvReader(Path('test.csv'))

        d = TextDictionary(reader, LanguageId.Japanese)
        self.assertFalse(d.is_empty())
        text = d.get_text('hoge')
        self.assertEqual('text1', text)

    def test_reload(self):
        reader = CsvReader(Path('test.csv'))
        d = TextDictionary(reader)

        # 呼び出しチェック
        with mock.patch.object(d._reader, 'read', return_value=(False, {})) as mp_read:
            d.reload(LanguageId.English)
            mp_read.assert_called_once_with(LanguageId.English)

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
