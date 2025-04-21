from PySide6.QtWidgets import QMenu
from qt_helpers.make import make
from qt_helpers.menu import menu
from PapyrusPad.app.windows.main.menus.file.actions.quit import QuitAction


@menu(name="File")
class FileMenu(QMenu):
    quit_action: QuitAction = make(QuitAction)
