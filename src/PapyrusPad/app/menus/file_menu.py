from PySide6.QtWidgets import QMenu
from qt_helpers.make import make
from qt_helpers.menu import menu
from PapyrusPad.app.actions.quit_action import QuitAction


@menu()
class FileMenu(QMenu):
    # This is one way to set the menu text
    _text = "File"

    quit_action: QuitAction = make(QuitAction)
