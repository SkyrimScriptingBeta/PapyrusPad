from typing import Any
from PySide6.QtWidgets import QApplication
from dependency_injector.wiring import Provide
from PapyrusPad.di.container import get_container_class
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.document_file_operations_interface import IDocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.dialog.dialog_interface import IDialogService
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider

container_class = get_container_class()


class Dependencies:
    application = Provide[container_class.application]
    document_collection = Provide[container_class.document_collection]
    filesystem = Provide[container_class.filesystem]
    dialog_service = Provide[container_class.dialog_service]
    document_file_operations = Provide[container_class.document_file_operations]
    document_type_registry = Provide[container_class.document_type_registry]
    capability_registry = Provide[container_class.capability_registry]
    document_capability_provider = Provide[container_class.document_capability_provider]


# Singleton instance
dependencies = Dependencies()

# Lookup by type
Depends: dict[type, Any] = {
    QApplication: dependencies.application,
    IDocumentCollection: dependencies.document_collection,
    IFileSystem: dependencies.filesystem,
    IDialogService: dependencies.dialog_service,
    IDocumentFileOperations: dependencies.document_file_operations,
    DocumentTypeRegistry: dependencies.document_type_registry,
    CapabilityRegistry: dependencies.capability_registry,
    DocumentCapabilityProvider: dependencies.document_capability_provider,
}
