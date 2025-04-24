from PySide6.QtWidgets import QApplication
from dependency_injector import containers, providers
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


class TestContainer(containers.DeclarativeContainer):
    """Test container with test-specific implementations."""

    application = providers.Singleton(QApplication, [])
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(MemoryFileSystem)
    dialog_service = providers.Singleton(FakeDialogService)
    document_file_operations = providers.Singleton(DocumentFileOperations, filesystem=filesystem)
