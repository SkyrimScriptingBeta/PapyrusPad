from typing import override
from PySide6.QtGui import QAction
from PapyrusPad.dependencies import Depends
from qt_helpers.action import action
from qt_helpers.interfaces import IAction
from PySide6.QtWidgets import QApplication, QMessageBox, QStyle


# And this is an alternative to attributes, pass everything to the decorator :)
@action("About", tooltip="Show information about the application", icon=QStyle.StandardPixmap.SP_MessageBoxQuestion)
class ShowAboutAction(QAction, IAction):

    @override
    def action(self, checked: bool, app: QApplication = Depends[QApplication]):
        # TODO: make this a widget
        # show a popup with the app name / version
        msg = QMessageBox()
        msg.setText(f"{app.applicationName()} {app.applicationVersion()}")
        msg.setInformativeText("This is a simple text editor.")
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
