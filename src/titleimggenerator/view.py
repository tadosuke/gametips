"""TitleImageGenerator を扱う GUI モジュール."""

from __future__ import annotations

from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog

from model import TitleImageGenerator

# 画像ファイルのあるフォルダ
_IMAGE_DIR = 'images'

# カテゴリ名→画像ファイル名の辞書
_IMAGE_FILENAME_DICT = {
    'music': 'music.png',
    'english': 'english.png',
}


class _MainWidget(QtWidgets.QWidget):
    """メインウィジェット."""

    def __init__(
            self,
            parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self._setup_ui()

    def _setup_ui(self):
        self._edit_category = QtWidgets.QLineEdit()
        self._edit_title = QtWidgets.QLineEdit()
        button_save = QtWidgets.QPushButton('保存')
        button_save.clicked.connect(self._on_save)

        layout = QtWidgets.QFormLayout()
        layout.addRow('カテゴリ', self._edit_category)
        layout.addRow('タイトル', self._edit_title)
        layout.addWidget(button_save)
        self.setLayout(layout)

    def _on_save(self):
        if self._edit_category.text() == "":
            return
        if self._edit_title.text() == "":
            return

        out_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            '保存先を選択してください。',
            '')
        if out_path == "":
            return

        generator = TitleImageGenerator(_IMAGE_DIR, _IMAGE_FILENAME_DICT)
        generator.generate(self._edit_category.text(), self._edit_title.text(), out_path)

        message = QtWidgets.QMessageBox()
        message.setText('保存しました。')
        message.show()


class MainWindow(QtWidgets.QMainWindow):
    """メインウィンドウ."""

    def __init__(
            self,
            parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent=parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('TitleImageGenerator')

        widget = _MainWidget(self)

        self.setCentralWidget(widget)


def main():
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
