from typing import override
from PySide6.QtGui import QAction
from PapyrusPad.app.application import Application
from PapyrusPad.app.dependencies import DI
from qt_helpers.action import action
from qt_helpers.interfaces import IAction
from PySide6.QtWidgets import QMessageBox, QStyle


# And this is an alternative to attributes, pass everything to the decorator :)
@action("About", tooltip="Show information about the application", icon=QStyle.StandardPixmap.SP_MessageBoxQuestion)
class ShowAboutAction(QAction, IAction):

    @override
    def action(self, checked: bool, app: Application = DI.application):
        # TODO: make this a widget
        # show a popup with the app name / version
        msg = QMessageBox()
        msg.setText(f"{app.applicationName()} {app.applicationVersion()}")
        msg.setInformativeText("This is a simple text editor.")
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
