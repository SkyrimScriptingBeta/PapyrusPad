from typing import override
from PySide6.QtWidgets import QMainWindow

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.dock_manager import DockManager, DockWidgetLocation, IDockManager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make_later
from qt_helpers.make_widget import make_widget
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    # central_widget: QLabel = make_widget(QLabel, ["central_widget"], "Hello!")

    left_widget_example: EditorWidget = make_widget(EditorWidget, ["editor"])
    right_widget_example: EditorWidget = make_widget(EditorWidget, ["editor"])

    dock_manager: IDockManager = make_later(DockManager)

    @override
    def setup(self):
        self.resize(1000, 1000)

        print(f"LEFT WIDGET: {self.left_widget_example}")
        print(f"RIGHT WIDGET: {self.right_widget_example}")

        self.dock_manager = DockManager(self)
        self.dock_manager.add_dock_widget(
            self.left_widget_example, "Left Dock", DockWidgetLocation.LEFT
        )
        self.dock_manager.add_dock_widget(
            self.right_widget_example, "Right Dock", DockWidgetLocation.RIGHT
        )
