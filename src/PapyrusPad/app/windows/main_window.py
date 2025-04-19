from typing import override
from PySide6.QtWidgets import QLabel, QMainWindow

from qt_helpers.factory import make
from qt_helpers.setup_functions_mixins import MainWindowSetupFunctionsMixin
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, MainWindowSetupFunctionsMixin):
    left_widget_example: QLabel = make(QLabel, "Left Widget Example")
    right_widget_example: QLabel = make(QLabel, "Right Widget Example")

    @override
    def setup_layout(self):
        self.add_dock_widget(self.left_widget_example)
