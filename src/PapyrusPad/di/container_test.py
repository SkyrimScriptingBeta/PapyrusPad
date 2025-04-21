from PySide6.QtWidgets import QApplication
from dependency_injector import providers
from PapyrusPad.di.container_base import BaseContainer
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


class TestContainer(BaseContainer):
    """Test container with test-specific implementations."""

    # Use a test QApplication that doesn't try to connect to a display
    _application = providers.Singleton(QApplication, [])

    # Use the real document collection
    _document_collection = providers.Singleton(DocumentCollection)

    # Use the real memory filesystem
    _filesystem = providers.Singleton(MemoryFileSystem)

    # Use the fake dialog service for testing
    _dialog_service = providers.Singleton(FakeDialogService)
