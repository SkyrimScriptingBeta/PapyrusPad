from typing import override
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QWidget

from PapyrusPad.domain.document.document_interface import IDocument
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("editor")
class EditorWidget(QWidget, IWidget):
    document: IDocument

    lbl_title: QLabel = make(QLabel)
    txt_source: QPlainTextEdit = make(QPlainTextEdit)

    @override
    def setup(self) -> None:
        self.lbl_title.setText(self.document.name)
        self.txt_source.setPlainText(self.document.content)
