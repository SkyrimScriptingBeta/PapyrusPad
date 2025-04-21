from typing import override
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtCore import QEvent, Qt, QObject

from qt_helpers.dock_manager import DockManager, IDockManager


class EditorWidget(QWidget):
    def __init__(self, filename: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{filename}</b>"))
        layout.addWidget(QTextEdit(f"// Editing {filename}"))
        self.setLayout(layout)


class PanelWidget(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h3>{title}</h3>"))
        layout.addWidget(QPushButton(f"{title} Button"))
        layout.addStretch()
        self.setLayout(layout)


class IDEExampleWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.dock_manager: IDockManager = DockManager(self)

        self.setWindowTitle("Qt Docking — No Lies Edition")
        self.resize(2048, 1152)

        self.left_panel_widget = PanelWidget("Left Panel")
        self.right_panel_widget = PanelWidget("Right Panel")
        self.top_panel_widget = PanelWidget("Top Panel")
        self.bottom_panel_widget = PanelWidget("Bottom Panel")

        top_panel_dock = self.dock_manager.dock(self.top_panel_widget, Qt.DockWidgetArea.TopDockWidgetArea, "Top Panel")
        bottom_panel_dock = self.dock_manager.dock(self.bottom_panel_widget, Qt.DockWidgetArea.BottomDockWidgetArea, "Bottom Panel")
        left_panel_dock = self.dock_manager.dock(self.left_panel_widget, Qt.DockWidgetArea.LeftDockWidgetArea, "Left Panel")

        self.editor_one = EditorWidget("main.cpp")
        self.editor_two = EditorWidget("engine.cpp")
        self.editor_three = EditorWidget("ui.cpp")

        # Add Right
        right_panel_dock = self.dock_manager.dock(self.right_panel_widget, Qt.DockWidgetArea.RightDockWidgetArea, "Right Panel")

        # # SPLIT right Right, with the editor ending up on the left:
        editor_one_dock = self.dock_manager.dock(self.editor_one, Qt.DockWidgetArea.RightDockWidgetArea, "main.cpp")
        self.splitDockWidget(editor_one_dock, right_panel_dock, Qt.Orientation.Horizontal)

        # # Now TABIFY the second and third editor docks to the first one:
        editor_two_dock = self.dock_manager.dock(self.editor_two, Qt.DockWidgetArea.RightDockWidgetArea, "engine.cpp")
        self.tabifyDockWidget(editor_one_dock, editor_two_dock)

        editor_three_dock = self.dock_manager.dock(self.editor_three, Qt.DockWidgetArea.RightDockWidgetArea, "ui.cpp")
        self.tabifyDockWidget(editor_one_dock, editor_three_dock)

        self.resizeDocks(  # type: ignore
            [left_panel_dock, editor_one_dock, right_panel_dock],
            [200, 1648, 200],
            Qt.Orientation.Horizontal,
        )
        self.resizeDocks(  # type: ignore
            [top_panel_dock, editor_one_dock, bottom_panel_dock],
            [100, 902, 150],
            Qt.Orientation.Vertical,
        )

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self.dock_manager.on_eventFilter(watched, event)
        return super().eventFilter(watched, event)
