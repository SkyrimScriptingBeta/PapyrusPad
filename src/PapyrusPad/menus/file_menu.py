from PySide6.QtWidgets import QMenu
from qt_helpers.make import make
from qt_helpers.menu import menu
from PapyrusPad.actions.confirm_action import ConfirmAction
from PapyrusPad.actions.quit_action import QuitAction
from PapyrusPad.actions.save_action import SaveAction


@menu()
class FileMenu(QMenu):
    # This is one way to set the menu text
    _text = "File"

    save_action: SaveAction = make(SaveAction)
    confirm_action: ConfirmAction = make(ConfirmAction)
    quit_action: QuitAction = make(QuitAction)
