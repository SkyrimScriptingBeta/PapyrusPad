from PySide6.QtWidgets import QMenu
from qt_helpers.make import make
from qt_helpers.menu import menu
from PapyrusPad.app.windows.main.menus.file.actions.quit import QuitAction


@menu()
class FileMenu(QMenu):
    # This is one way to set the menu text
    _text = "File"

    quit_action: QuitAction = make(QuitAction)
