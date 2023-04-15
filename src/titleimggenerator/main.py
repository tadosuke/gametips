from __future__ import annotations

from titleimggenerator.model import TitleImageGenerator


# 画像ファイルのあるフォルダ
_IMAGE_DIR = 'images'

# カテゴリ名→画像ファイル名の辞書
_IMAGE_FILENAME_DICT = {
    'music': 'music.png',
    'english': 'english.png',
}


def main():
    """メイン関数."""

    # カテゴリ名
    category_name = 'english'
    # 表示するテキスト
    text = '【ボイトレ】\n$アンザッツ$4～6 を\n$一ヶ月！$'
    # 出力先
    out_path = 'images/out.png'

    generator = TitleImageGenerator(_IMAGE_DIR, _IMAGE_FILENAME_DICT)
    generator.generate(category_name, text, out_path)


if __name__ == '__main__':
    main()
