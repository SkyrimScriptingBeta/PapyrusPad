from typing import Any
from PySide6.QtWidgets import QApplication
from dependency_injector.wiring import Provide
from PapyrusPad.di.container import get_container_class
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.dialog.dialog_interface import IDialogService

container_class = get_container_class()


class Dependencies:
    application = Provide[container_class.application]
    document_collection = Provide[container_class.document_collection]
    filesystem = Provide[container_class.filesystem]
    dialog_service = Provide[container_class.dialog_service]


# Singleton instance
dependencies = Dependencies()

# Lookup by type
Depends: dict[type, Any] = {
    QApplication: dependencies.application,
    IDocumentCollection: dependencies.document_collection,
    IFileSystem: dependencies.filesystem,
    IDialogService: dependencies.dialog_service,
}
