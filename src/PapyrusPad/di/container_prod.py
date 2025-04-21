from dependency_injector import providers
from PapyrusPad.di.container_base import BaseContainer
from PapyrusPad.application import Application
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem
from PapyrusPad.domain.dialog.dialog_qt import QtDialogService


class ProductionContainer(BaseContainer):
    """Production container with real implementations."""

    # Override the dependency providers with actual implementations
    _application = providers.Singleton(Application)
    _document_collection = providers.Singleton(DocumentCollection)
    _filesystem = providers.Singleton(MemoryFileSystem)
    _dialog_service = providers.Singleton(QtDialogService)
