from dataclasses import field
from typing import List, override
from PySide6.QtWidgets import QDockWidget, QLabel, QMainWindow, QWidget

from qt_helpers.interfaces import IWidget
from qt_helpers.make_widget import make_widget
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    # Create a bunch of example widgets to fill the docking areas
    left_widget: QWidget = make_widget(QLabel, [], "Left Panel")
    right_widget: QWidget = make_widget(QLabel, [], "Right Panel")
    bottom_widget: QWidget = make_widget(QLabel, [], "Bottom Panel")
    top_widget: QWidget = make_widget(QLabel, [], "Top Panel")

    # Let's start with the "center area" with 3x widgets, and we'll tabify them to start
    center_widget_one = make_widget(QLabel, [], "Center Panel 1")
    center_widget_two = make_widget(QLabel, [], "Center Panel 2")
    center_widget_three = make_widget(QLabel, [], "Center Panel 3")

    # dock_manager: IDockManager = make_later(DockManager)
    editor_docks: List[QDockWidget] = field(default_factory=lambda: [])

    @override
    def setup(self):
        self.resize(2048, 1152)
        # self.dock_manager = DockManager(self)
