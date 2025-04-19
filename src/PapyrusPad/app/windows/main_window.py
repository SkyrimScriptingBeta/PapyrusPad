from PySide6.QtWidgets import QMainWindow

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.factory import make
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow):
    central_widget: EditorWidget = make(EditorWidget)
