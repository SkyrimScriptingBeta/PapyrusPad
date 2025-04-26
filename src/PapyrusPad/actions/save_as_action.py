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


@action("Save As", shortcut="Ctrl+Shift+S", tooltip="Save the document with a new name", icon=QStyle.StandardPixmap.SP_DialogSaveButton)
class SaveAsAction(QAction, IAction):
    """Action to save the current document with a new name."""

    @override
    def action(
        self,
        checked: bool,
        document_collection: IDocumentCollection = Depends[IDocumentCollection],
        document_file_operations: IDocumentFileOperations = Depends[IDocumentFileOperations],
        dialog_service: IDialogService = Depends[IDialogService],
    ) -> None:
        """
        Save the current document with a new name.

        Args:
            checked: Whether the action is checked (not used)
            document_collection: The document collection service
            document_file_operations: The document file operations service
            dialog_service: The dialog service
        """
        # Get the active document
        document = document_collection.get_active()

        # If no document is active, show an error message
        if document is None:
            dialog_service.show_message(DialogOptions(title="Save Error", message="No document is currently active", type=DialogType.WARNING))
            return

        # Show file save dialog
        default_name = document.name if document.name else "Untitled.txt"
        file_path = dialog_service.show_file_save_dialog(title="Save As", default_path=default_name, filter="All Files (*);;Text Files (*.txt);;Papyrus Scripts (*.psc)")
        print(f"File path from dialog: {file_path}")

        # If user cancelled, return
        if file_path is None:
            return

        # Save the document to the new path
        path = Path(file_path)
        success = document_file_operations.save_document_as(document, path)

        # Show error message if save failed
        if not success:
            dialog_service.show_message(DialogOptions(title="Save Error", message=f"Failed to save document: {document.name}", type=DialogType.ERROR))
