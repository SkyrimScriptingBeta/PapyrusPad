from typing import override
from PySide6.QtWidgets import QLabel, QTextEdit, QWidget

from PapyrusPad.app.widgets.my_widget import MyWidget
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("editor")
class EditorWidget(QWidget, IWidget):
    text: str

    lbl_title: QLabel = make(QLabel, "<h3>Editor!</h3>")
    txt_source: QTextEdit = make(QTextEdit, "// Editing a file...")
    my_widget: MyWidget = make(MyWidget)

    @override
    def setup(self) -> None:
        self.lbl_title.setText(f"<h3>{self.text}</h3>")
        self.txt_source.setPlainText("// Editing a file: " + self.text)
