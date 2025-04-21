from typing import override
from PySide6.QtWidgets import QLabel, QTextEdit, QWidget

from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("editor")
class EditorWidget(QWidget, IWidget):
    text: str

    lbl_title: QLabel = make(QLabel)
    txt_source: QTextEdit = make(QTextEdit)

    @override
    def setup(self) -> None:
        self.title = self.text

    @property
    def title(self) -> str:
        return self.lbl_title.text()

    @title.setter
    def title(self, text: str) -> None:
        self.lbl_title.setText(f"<h3>{text}</h3>")
