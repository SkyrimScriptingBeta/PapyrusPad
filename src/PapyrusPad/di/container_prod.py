from dependency_injector import containers, providers
from PapyrusPad.application import Application
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem
from PapyrusPad.domain.dialog.dialog_qt import QtDialogService


class ProductionContainer(containers.DeclarativeContainer):
    """Production container with real implementations."""

    application = providers.Singleton(Application)
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(MemoryFileSystem)
    dialog_service = providers.Singleton(QtDialogService)
