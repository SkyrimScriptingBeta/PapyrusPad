from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle

from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogType
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
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
        filesystem: IFileSystem = Depends[IFileSystem],
        dialog_service: IDialogService = Depends[IDialogService],
    ) -> None:
        """
        Save the current document.

        Args:
            checked: Whether the action is checked (not used)
            document_collection: The document collection service
            filesystem: The filesystem service
            dialog_service: The dialog service
        """
        # Get the active document
        document = document_collection.get_active()

        # If no document is active, show an error message
        if document is None:
            dialog_service.show_message(DialogOptions(title="Save Error", message="No document is currently active", type=DialogType.WARNING))
            return

        # If document has no path, we need to implement "Save As" functionality
        # For now, just show an error message
        if document.path is None:
            dialog_service.show_message(DialogOptions(title="Save Error", message="Document has no path. Save As functionality not yet implemented.", type=DialogType.WARNING))
            return

        # Save the document
        success = document.save(filesystem)

        # Show error message if save failed
        if not success:
            dialog_service.show_message(DialogOptions(title="Save Error", message=f"Failed to save document: {document.name}", type=DialogType.ERROR))
