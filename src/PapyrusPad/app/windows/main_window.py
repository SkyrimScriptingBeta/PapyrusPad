from typing import override
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QMainWindow

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.dock_manager import IDockManager, get_dock_manager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make, make_later
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    dock_manager: IDockManager = make_later(IDockManager)
    central_widget: EditorWidget = make(EditorWidget, text="Untitled")

    @override
    def setup(self):
        self.resize(1024, 1024)
        self.dock_manager = get_dock_manager(self)

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self.dock_manager.on_eventFilter(watched, event)
        return super().eventFilter(watched, event)
