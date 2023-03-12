"""language パッケージの利用サンプル."""
from pathlib import Path

from language.reader import CsvReader
from language.system import System
from language.types import LanguageId


def main():
    system = System(LanguageId.Japanese)

    # 辞書を読み込む
    system.load_dictionary(CsvReader(Path('samplefiles/test.csv')))
    system.load_dictionary(CsvReader(Path('samplefiles/test2.csv')))

    print('[日本語]')
    print(system.get_text('test', 'hello'))
    print(system.get_text('test', 'thanks'))
    print(system.get_text('test2', 'weapon_1'))
    print(system.get_text('test2', 'weapon_2'))
    print('')

    # 英語に切り替える
    system.change_language(LanguageId.English)

    print('[英語]')
    print(system.get_text('test', 'hello'))
    print(system.get_text('test', 'thanks'))
    print(system.get_text('test2', 'weapon_1'))
    print(system.get_text('test2', 'weapon_2'))


if __name__ == '__main__':
    main()