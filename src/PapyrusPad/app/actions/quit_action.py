from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle
from qt_helpers.action import action
from qt_helpers.interfaces import IAction


@action()
class QuitAction(QAction, IAction):
    # this is one way... using attributes...
    _text = "Quit"
    _shortcut = "Ctrl+Q"
    _tooltip = "Exit the application"
    _icon = QStyle.StandardPixmap.SP_TitleBarCloseButton

    @override
    def action(self, checked: bool) -> None:
        print("Exiting the application...")

        # Logic to quit the application
        import sys

        sys.exit(0)
