from dataclasses import field
from typing import List, override
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QDockWidget, QLabel, QMainWindow, QWidget

from qt_helpers.dock_manager import IDockManager, get_dock_manager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make_later
from qt_helpers.make_widget import make_widget
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    dock_manager: IDockManager = make_later(IDockManager)

    # Create a bunch of example widgets to fill the docking areas
    left_widget: QWidget = make_widget(QLabel, [], "Left Panel")
    right_widget: QWidget = make_widget(QLabel, [], "Right Panel")
    bottom_widget: QWidget = make_widget(QLabel, [], "Bottom Panel")
    top_widget: QWidget = make_widget(QLabel, [], "Top Panel")

    # Let's start with the "center area" with 3x widgets, and we'll tabify them to start
    center_widget_one: QLabel = make_widget(QLabel, [], "Center Panel 1")
    center_widget_two: QLabel = make_widget(QLabel, [], "Center Panel 2")
    center_widget_three: QLabel = make_widget(QLabel, [], "Center Panel 3")

    # dock_manager: IDockManager = make_later(DockManager)
    editor_docks: List[QDockWidget] = field(default_factory=lambda: [])

    @override
    def setup(self):
        self.resize(2048, 1152)
        self.dock_manager = get_dock_manager(self)
        self.dock_manager.dock(self.left_widget, Qt.DockWidgetArea.LeftDockWidgetArea, "LEFT")
        self.dock_manager.dock(self.right_widget, Qt.DockWidgetArea.RightDockWidgetArea, "RIGHT")
        self.dock_manager.dock(self.bottom_widget, Qt.DockWidgetArea.BottomDockWidgetArea, "BOTTOM")
        self.dock_manager.dock(self.top_widget, Qt.DockWidgetArea.TopDockWidgetArea, "TOP")

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self.dock_manager.on_eventFilter(watched, event)
        return super().eventFilter(watched, event)
