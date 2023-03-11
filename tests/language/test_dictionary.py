"""dictionary モジュールのテスト."""

import unittest

from language.dictionary import Dictionary, Dictionaries, CsvReader


class TestDictionaries(unittest.TestCase):

    def test_init(self):
        ds = Dictionaries()
        self.assertEqual({}, ds._dictionaries)

    def test_add(self):
        d1 = Dictionary('d1')
        ds = Dictionaries()
        self.assertIsNone(ds.get('d1'))
        ds.add(d1)
        self.assertIs(d1, ds.get('d1'))

    def test_remove(self):
        d1 = Dictionary('d1')
        ds = Dictionaries()
        ds.remove('d1')  # 無い辞書を指定しても例外は出ない
        ds.add(d1)
        self.assertIs(d1, ds.get('d1'))
        ds.remove('d1')
        self.assertIsNone(ds.get('d1'))


class TestDictionary(unittest.TestCase):

    def test_init(self):
        d1 = Dictionary('d1')
        self.assertEqual('d1', d1.name)
        self.assertEqual({}, d1._text_dict)
        self.assertIsNone(d1.get_text('hoge'))

        d2 = Dictionary('d2', {'hoge': 'fuga'})
        self.assertEqual('fuga', d2.get_text('hoge'))


class TestCsvReader(unittest.TestCase):

    def test_read(self):
        reader = CsvReader()
        with self.assertRaises(FileNotFoundError):
            reader.read('./language/invalid.csv')
        with self.assertRaises(ValueError):
            reader.read('./language/test.txt')

        d = reader.read('./language/test.csv')
        self.assertIsNotNone(d)
        self.assertEqual('text1', d.get_text('hoge'))
        self.assertEqual('text2', d.get_text('fuga'))
        self.assertIsNone(d.get_text('piyo'))


if __name__ == '__main__':
    unittest.main()
