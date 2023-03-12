"""system モジュールのテスト."""

import unittest
from pathlib import Path
from unittest import mock

from language.reader import CsvReader
from language.system import System, TextDictionary
from language.types import LanguageId


class TestSystem(unittest.TestCase):

    def test_init(self):
        system = System()
        self.assertEqual({}, system._dictionaries)
        self.assertEqual(LanguageId.Japanese, system.language)

        system = System(LanguageId.English)
        self.assertEqual(LanguageId.English, system.language)

    def test_load_dictionary(self):
        system = System()
        reader = CsvReader(Path('test.csv'))
        self.assertEqual(0, len(system._dictionaries))
        system.load_dictionary(reader)
        self.assertEqual(1, len(system._dictionaries))
        reader = CsvReader(Path('test2.csv'))
        system.load_dictionary(reader)
        self.assertEqual(2, len(system._dictionaries))

    def test_remove_dictionary(self):
        system = System()
        reader = CsvReader(Path('test.csv'))
        system.load_dictionary(reader)

        # 存在しない辞書
        system.remove_dictionary('invalid')
        self.assertEqual(1, len(system._dictionaries))

        # 存在する辞書
        system.remove_dictionary(reader.name)
        self.assertEqual(0, len(system._dictionaries))

    def test_change_language(self):
        system = System()
        with mock.patch.object(system, '_reload_all_dictionaries') as mp_reload:
            system.change_language(LanguageId.English)
            self.assertEqual(LanguageId.English, system.language)
            mp_reload.assert_called_once()

    def test_get_text(self):
        system = System()
        reader = CsvReader(Path('test.csv'))
        system.load_dictionary(reader)
        reader = CsvReader(Path('test2.csv'))
        system.load_dictionary(reader)

        # 成功
        text = system.get_text('test', 'hello')
        self.assertEqual('こんにちは', text)
        text = system.get_text('test2', 'weapon_1')
        self.assertEqual('銅の剣', text)

        # 英語
        system.change_language(LanguageId.English)
        text = system.get_text('test', 'hello')
        self.assertEqual('Hello!', text)
        text = system.get_text('test2', 'weapon_2')
        self.assertEqual('Iron sword', text)

        # 辞書違い
        text = system.get_text('test', 'weapon_1')
        self.assertIsNone(text)


class TestTextDictionary(unittest.TestCase):

    def test_init(self):
        reader = CsvReader(Path('test.csv'))
        with mock.patch('language.system.TextDictionary.reload') as mp_reload:
            TextDictionary(reader)
            mp_reload.assert_called_once_with(LanguageId.Japanese)

    def test_get_text(self):
        reader = CsvReader(Path('test.csv'))

        # 日本語
        d = TextDictionary(reader, LanguageId.Japanese)
        self.assertFalse(d.is_empty())
        text = d.get_text('hello')
        self.assertEqual('こんにちは', text)

        # 英語
        d = TextDictionary(reader, LanguageId.English)
        self.assertFalse(d.is_empty())
        text = d.get_text('hello')
        self.assertEqual('Hello!', text)

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
