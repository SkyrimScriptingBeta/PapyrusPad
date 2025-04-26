from dependency_injector import containers, providers
from PapyrusPad.application import Application
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_qt import QtFileSystem
from PapyrusPad.domain.dialog.dialog_qt import QtDialogService
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider


class ProductionContainer(containers.DeclarativeContainer):
    """Production container with real implementations."""

    application = providers.Singleton(Application)
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(QtFileSystem)
    dialog_service = providers.Singleton(QtDialogService)

    # Document type and capability system
    document_type_registry = providers.Singleton(DocumentTypeRegistry)
    capability_registry = providers.Singleton(CapabilityRegistry)
    document_capability_provider = providers.Singleton(DocumentCapabilityProvider, _document_type_registry=document_type_registry, _capability_registry=capability_registry)

    # File operations (depends on document type registry)
    document_file_operations = providers.Singleton(DocumentFileOperations, filesystem=filesystem, document_type_registry=document_type_registry)
