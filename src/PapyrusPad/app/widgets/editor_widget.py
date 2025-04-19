from PySide6.QtWidgets import QLabel, QTextEdit, QWidget

from qt_helpers.factory import factory
from qt_helpers.widget import widget


@widget("editor")
class EditorWidget(QWidget):
    # TODO: I need a way to have these get initialized WITH names and optionally classes!
    lbl_title: QLabel = factory(QLabel, "<h3>Editor!</h3>")
    txt_source: QTextEdit = factory(QTextEdit, "// Editing a file...")
