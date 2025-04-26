from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle

from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogType
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.document_file_operations_interface import IDocumentFileOperations
from qt_helpers.action import action
from qt_helpers.interfaces import IAction


@action("Save", shortcut="Ctrl+S", tooltip="Save the current document", icon=QStyle.StandardPixmap.SP_DialogSaveButton)
class SaveAction(QAction, IAction):
    """Action to save the current document."""

    @override
    def action(
        self,
        checked: bool,
        document_collection: IDocumentCollection = Depends[IDocumentCollection],
        document_file_operations: IDocumentFileOperations = Depends[IDocumentFileOperations],
        dialog_service: IDialogService = Depends[IDialogService],
    ) -> None:
        """
        Save the current document.

        Args:
            checked: Whether the action is checked (not used)
            document_collection: The document collection service
            document_file_operations: The document file operations service
            dialog_service: The dialog service
        """
        # Get the active document
        document = document_collection.active_document

        # If no document is active, show an error message
        if document is None:
            dialog_service.show_message(DialogOptions(title="Save Error", message="No document is currently active", type=DialogType.WARNING))
            return

        # If document has no path, use Save As functionality
        if document.path is None:
            # Import here to avoid circular imports
            from PapyrusPad.actions.save_as_action import SaveAsAction

            save_as = SaveAsAction()
            save_as.action(checked, document_collection=document_collection, document_file_operations=document_file_operations, dialog_service=dialog_service)
            return

        # Save the document
        success = document_file_operations.save_document(document)

        # Show error message if save failed
        if not success:
            dialog_service.show_message(DialogOptions(title="Save Error", message=f"Failed to save document: {document.name}", type=DialogType.ERROR))
