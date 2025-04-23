from PySide6.QtWidgets import QMenu
from qt_helpers.make import make
from qt_helpers.menu import menu
from PapyrusPad.actions.open_file_action import OpenFileAction
from PapyrusPad.actions.quit_action import QuitAction
from PapyrusPad.actions.save_action import SaveAction
from PapyrusPad.actions.save_as_action import SaveAsAction


@menu()
class FileMenu(QMenu):
    # This is one way to set the menu text
    _text = "File"

    open_file_action: OpenFileAction = make(OpenFileAction)
    save_action: SaveAction = make(SaveAction)
    save_as_action: SaveAsAction = make(SaveAsAction)
    quit_action: QuitAction = make(QuitAction)
