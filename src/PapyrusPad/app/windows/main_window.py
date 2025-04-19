from typing import override
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLabel, QTabWidget

from qt_helpers.factory import make
from qt_helpers.main_window_base import MainWindowBase
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(MainWindowBase):
    left_widget_example: QLabel = make(QLabel, "Left Widget Example")
    right_widget_example: QLabel = make(QLabel, "Right Widget Example")

    @override
    def setup(self):
        self.resize(1000, 1000)

    @override
    def setup_dock_widgets(self):
        self.setDockNestingEnabled(True)
        left_dock_widget = self.add_dock_widget(
            self.left_widget_example,
            areas=Qt.DockWidgetArea.LeftDockWidgetArea,
            title="LEFT!",
        )
        right_dock_widget = self.make_dock_widget(
            self.right_widget_example,
            areas=Qt.DockWidgetArea.RightDockWidgetArea,
            title="RIGHT!",
        )
        self.tabifyDockWidget(left_dock_widget, right_dock_widget)
        self.setTabPosition(
            Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North
        )
