from pathlib import Path
from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle

from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogType
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.document_file_operations_interface import IDocumentFileOperations
from qt_helpers.action import action
from qt_helpers.interfaces import IAction


@action("Open", shortcut="Ctrl+O", tooltip="Open a file", icon=QStyle.StandardPixmap.SP_DialogOpenButton)
class OpenFileAction(QAction, IAction):
    """Action to open a file."""

    @override
    def action(
        self,
        checked: bool,
        document_collection: IDocumentCollection = Depends[IDocumentCollection],
        document_file_operations: IDocumentFileOperations = Depends[IDocumentFileOperations],
        dialog_service: IDialogService = Depends[IDialogService],
    ) -> None:
        """
        Open a file.

        Args:
            checked: Whether the action is checked (not used)
            document_collection: The document collection service
            document_file_operations: The document file operations service
            dialog_service: The dialog service
        """
        # Show file open dialog
        file_path = dialog_service.show_file_open_dialog(title="Open File", filter="All Files (*);;Text Files (*.txt);;Papyrus Scripts (*.psc)")

        # If user cancelled, return
        if file_path is None:
            return

        try:
            # Open the file
            path = Path(file_path)
            # The document is opened and made active by the document file operations service
            document_file_operations.open_file(path, document_collection)

            # No need to do anything else, the document is now open and active
        except FileNotFoundError:
            # Show error message if file not found
            dialog_service.show_message(DialogOptions(title="Open Error", message=f"Could not open file: {file_path}", type=DialogType.ERROR))
        except Exception as e:
            # Show error message for any other error
            dialog_service.show_message(DialogOptions(title="Open Error", message=f"Error opening file: {file_path}", detail=str(e), type=DialogType.ERROR))
