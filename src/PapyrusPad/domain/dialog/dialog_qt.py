from typing import override
from PySide6.QtWidgets import QMessageBox

from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogType, DialogResult


class QtDialogService(IDialogService):
    """Qt implementation of the dialog service."""

    @override
    def show_message(self, options: DialogOptions) -> DialogResult:
        """
        Show a message dialog with OK button using Qt's QMessageBox.

        Args:
            options: Configuration options for the dialog

        Returns:
            DialogResult.OK when the dialog is closed
        """
        msg_box = QMessageBox()
        msg_box.setText(options.message)
        msg_box.setWindowTitle(options.title)

        if options.detail:
            msg_box.setInformativeText(options.detail)

        if options.type == DialogType.INFO:
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif options.type == DialogType.WARNING:
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif options.type == DialogType.ERROR:
            msg_box.setIcon(QMessageBox.Icon.Critical)
        elif options.type == DialogType.QUESTION:
            msg_box.setIcon(QMessageBox.Icon.Question)

        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

        return DialogResult.OK

    @override
    def show_question(self, options: DialogOptions) -> DialogResult:
        """
        Show a question dialog with Yes/No buttons using Qt's QMessageBox.

        Args:
            options: Configuration options for the dialog

        Returns:
            DialogResult.YES if the user clicked Yes, DialogResult.NO otherwise
        """
        msg_box = QMessageBox()
        msg_box.setText(options.message)
        msg_box.setWindowTitle(options.title)

        if options.detail:
            msg_box.setInformativeText(options.detail)

        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            return DialogResult.YES
        else:
            return DialogResult.NO
