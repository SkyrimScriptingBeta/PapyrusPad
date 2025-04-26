from typing import override
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QWidget

from PapyrusPad.domain.document.document_interface import IDocument
from qt_helpers.bind_fields import bind_fields
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

    @override
    def setup_bindings(self) -> None:
        bind_fields([(self.txt_source, "plainText", self.document.content_observable)])
        bind_fields([(self.lbl_title, "text", self.document.display_name_observable)])
        bind_fields([(self, "windowTitle", self.document.display_name_observable)])

    def _on_btn_test_clicked(self) -> None:
        self.document.content = "CHANGED the MODEL!"
