from typing import override
from PySide6.QtWidgets import QMessageBox, QFileDialog

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

    @override
    def show_file_save_dialog(self, title: str, default_path: str = "", filter: str = "") -> str | None:
        """
        Show a file save dialog using Qt's QFileDialog.

        Args:
            title: The dialog title
            default_path: Optional default path or filename
            filter: Optional file type filter

        Returns:
            The selected file path, or None if the dialog was cancelled
        """
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle(title)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)

        if default_path:
            file_dialog.selectFile(default_path)

        if filter:
            file_dialog.setNameFilter(filter)
        else:
            # Default filter for text files and Papyrus scripts
            file_dialog.setNameFilter("All Files (*);;Text Files (*.txt);;Papyrus Scripts (*.psc)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]

        return None

    @override
    def show_file_open_dialog(self, title: str, default_path: str = "", filter: str = "") -> str | None:
        """
        Show a file open dialog using Qt's QFileDialog.

        Args:
            title: The dialog title
            default_path: Optional default path or directory
            filter: Optional file type filter

        Returns:
            The selected file path, or None if the dialog was cancelled
        """
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle(title)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if default_path:
            file_dialog.selectFile(default_path)

        if filter:
            file_dialog.setNameFilter(filter)
        else:
            # Default filter for text files and Papyrus scripts
            file_dialog.setNameFilter("All Files (*);;Text Files (*.txt);;Papyrus Scripts (*.psc)")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                return selected_files[0]

        return None
