from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle
from qt_helpers.action import action
from qt_helpers.interfaces import IAction


@action("Quit", shortcut="Ctrl+Q", tooltip="Exit the application", icon=QStyle.StandardPixmap.SP_TitleBarCloseButton)
class QuitAction(QAction, IAction):

    @override
    def action(self):
        print("Exiting the application...")

        # Logic to quit the application
        import sys

        sys.exit(0)
