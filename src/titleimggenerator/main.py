from __future__ import annotations

import sys

from PIL import Image, ImageDraw, ImageFont


# フォント名
_FONT_NAME = 'HGRPP1'
# フォントサイズ
_FONT_SIZE = 50

# 背景とテキストの間隔
_PADDING_Y = 25

# 画像ファイルのあるフォルダ
_IMAGE_DIR = 'images'

# カテゴリ名→画像ファイル名の辞書
_IMAGE_FILENAME_DICT = {
	'music': 'music.png',
	'english': 'english.png',
}


class _BackGround:
	"""背景画像."""

	def __init__(self, category_name):
		image_filename = _IMAGE_FILENAME_DICT[category_name]
		image_path = f'{_IMAGE_DIR}/{image_filename}'
		self.image = Image.open(image_path)

	def paste(self, text_bg):
		"""テキスト入りの背景を貼り付ける"""
		bg_pos = (0, int(self.image.height / 2 - text_bg.image.height / 2))
		self.image.paste(text_bg.image, bg_pos, mask=text_bg.image)


class _TextInfo:
	"""テキスト情報."""

	# 改行時の間隔
	LINE_SPACE = 20

	def __init__(self, text, font):
		self.line_list = self._split_lines(text, font)
		self.text = text

	def _split_lines(self, text: str, font) -> list[_Line]:
		line_list = []
		for line_str in text.splitlines():
			line = _Line(line_str, font)
			line_list.append(line)
		return line_list

	def calc_size(self):
		width = 0
		height = 0
		for line in self.line_list:
			line_width, line_height = line.calc_size()
			width += max(width, line_width)
			height += line_height + self.LINE_SPACE
		return width, height


class _Line:
	"""行."""

	# 強調区切り文字
	_STRONG_DELIMITER = '$'
	# テキスト色：通常
	_NORMAL_RGBA = (255, 255, 255, 255)
	# テキスト色：強調
	_STRONG_RGBA = (0, 255, 255, 255)

	def __init__(self, line_str: str, font):
		self.phrase_list = self._split_phrases(line_str, font)

	def _split_phrases(self, line_str: str, font) -> list[_Phrase]:
		phrase_list = []
		for i, phrase_str in enumerate(line_str.split(self._STRONG_DELIMITER)):
			if i % 2 == 0:
				phrase = _Phrase(phrase_str, font, self._NORMAL_RGBA)
			else:
				phrase = _Phrase(phrase_str, font, self._STRONG_RGBA)
			phrase_list.append(phrase)

		return phrase_list

	def calc_size(self):
		width = 0
		height = 0
		for phrase in self.phrase_list:
			width += phrase.width
			height = max(height, phrase.height)
		return width, height


class _Phrase:
	"""文節."""

	def __init__(self, phrase_str: str, font, color):
		self.text = phrase_str
		self.color = color
		self.font = font
		_, _, self.width, self.height = self.font.getbbox(self.text)


class _TextBackGround:
	"""テキスト背景."""

	def __init__(self, width, text_info: _TextInfo, padding_y: int):
		# 背景を生成
		text_width, text_height = text_info.calc_size()
		bg_size = (width, text_height + padding_y * 2)
		bg_rgba = (0, 0, 0, 128)
		self.image = Image.new("RGBA", bg_size, bg_rgba)

		self._add_text(text_info)

	def _add_text(self, text_info: _TextInfo):
		text_draw = ImageDraw.Draw(self.image)

		text_width, text_height = text_info.calc_size()
		cur_height = self.image.height / 2 - text_height/2
		for line in text_info.line_list:
			line_width, line_height = line.calc_size()
			cur_width = self.image.width / 2 - line_width / 2
			for phrase in line.phrase_list:
				phrase_pos = (cur_width, cur_height)
				text_draw.text(phrase_pos, phrase.text, font=phrase.font, fill=phrase.color)
				cur_width += phrase.width
			# 改行
			cur_height += line_height + text_info.LINE_SPACE


def main():
	"""メイン関数."""

	# カテゴリ名
	category_name = 'english'
	# 表示するテキスト
	text = '【ボイトレ】\n$アンザッツ$4～6 を\n$一ヶ月！$'

	# 画像を読み込む
	bg_image = _BackGround(category_name)

	# フォント
	font = ImageFont.truetype(_FONT_NAME, _FONT_SIZE)
	# テキスト
	text_info = _TextInfo(text, font)
	# テキスト背景
	text_bg = _TextBackGround(bg_image.image.width, text_info, _PADDING_Y)
	# 元画像に貼り付ける
	bg_image.paste(text_bg)

	bg_image.image.show()


if __name__ == '__main__':
	main()
