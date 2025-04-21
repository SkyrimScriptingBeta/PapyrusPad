from typing import override
from PySide6.QtWidgets import QMainWindow

from PapyrusPad.widgets.editor_widget import EditorWidget
from PapyrusPad.menus.file_menu import FileMenu
from PapyrusPad.menus.help_menu import HelpMenu
from qt_helpers.dock_manager import IDockManager, get_dock_manager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make, make_later
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    dock_manager: IDockManager = make_later(IDockManager)
    central_widget: EditorWidget = make(EditorWidget, text="Untitled")
    file_menu: FileMenu = make(FileMenu)
    help_menu: HelpMenu = make(HelpMenu)

    @override
    def setup(self):
        self.resize(1024, 1024)
        self.dock_manager = get_dock_manager(self)
