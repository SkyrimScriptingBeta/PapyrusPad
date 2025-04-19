from typing import override
from PySide6.QtWidgets import QLabel, QMainWindow

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.factory import make
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow):
    central_widget: EditorWidget = make(EditorWidget)

    left_widget_example: QLabel = make(QLabel, "Left Widget Example")
    right_widget_example: QLabel = make(QLabel, "Right Widget Example")

    # @override
    def setup_layout(self):
        #     print("Hello?")
        print(self.left_widget_example)

    #     self.add_dock_widget(self.left_widget_example)
