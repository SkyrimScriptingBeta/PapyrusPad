from typing import Any
from PySide6.QtWidgets import QApplication
from dependency_injector.wiring import Provide
from PapyrusPad.di.container_interface import IContainer
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.dialog.dialog_interface import IDialogService


class Dependencies:
    application = Provide[IContainer.application]
    document_collection = Provide[IContainer.document_collection]
    filesystem = Provide[IContainer.filesystem]
    dialog_service = Provide[IContainer.dialog_service]


# Singleton instance
dependencies = Dependencies()

# Lookup by type
Depends: dict[type, Any] = {
    QApplication: dependencies.application,
    IDocumentCollection: dependencies.document_collection,
    IFileSystem: dependencies.filesystem,
    IDialogService: dependencies.dialog_service,
}
