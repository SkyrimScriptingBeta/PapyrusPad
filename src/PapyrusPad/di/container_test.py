from PySide6.QtWidgets import QApplication
from dependency_injector import containers, providers
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider


class TestContainer(containers.DeclarativeContainer):
    """Test container with test-specific implementations."""

    application = providers.Singleton(QApplication, [])
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(MemoryFileSystem)
    dialog_service = providers.Singleton(FakeDialogService)
    document_file_operations = providers.Singleton(DocumentFileOperations, filesystem=filesystem)

    # Document type and capability system
    document_type_registry = providers.Singleton(DocumentTypeRegistry)
    capability_registry = providers.Singleton(CapabilityRegistry)
    document_capability_provider = providers.Singleton(DocumentCapabilityProvider, _document_type_registry=document_type_registry, _capability_registry=capability_registry)
