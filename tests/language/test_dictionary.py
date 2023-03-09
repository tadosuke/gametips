"""dictionary モジュールのテスト."""

import unittest

from language.dictionary import Dictionary, Category, Dictionaries


class TestDictionaries(unittest.TestCase):

    def test_init(self):
        d = Dictionaries()
        self.assertEqual({}, d._dictionaries)


class TestDictionary(unittest.TestCase):

    def test_init(self):
        d = Dictionary('dictionary1')
        self.assertEqual('dictionary1', d.name)


class TestCategory(unittest.TestCase):

    def test_init(self):
        c = Category('category1')
        self.assertEqual('category1', c.name)


if __name__ == '__main__':
    unittest.main()
