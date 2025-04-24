from dependency_injector import containers, providers
from PapyrusPad.application import Application
from PapyrusPad.domain.dialog.dialog_qt import QtDialogService
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_qt import QtFileSystem


class DevelopmentContainer(containers.DeclarativeContainer):
    """Development container with development-specific overrides."""

    application = providers.Singleton(Application)
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(QtFileSystem)
    dialog_service = providers.Singleton(QtDialogService)
    document_file_operations = providers.Singleton(DocumentFileOperations, filesystem=filesystem)
