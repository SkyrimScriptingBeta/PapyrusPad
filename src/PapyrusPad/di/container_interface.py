from typing import Protocol
from PySide6.QtWidgets import QApplication
from dependency_injector import providers

from PapyrusPad.domain.dialog.dialog_interface import IDialogService
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class IContainerClass(Protocol):
    """Test container with test-specific implementations."""

    application = providers.Dependency()
    document_collection = providers.Dependency()
    filesystem = providers.Dependency()
    dialog_service = providers.Dependency()


class IContainer(Protocol):
    """Test container with test-specific implementations."""

    def application(self) -> QApplication: ...
    def document_collection(self) -> IDocumentCollection: ...
    def filesystem(self) -> IFileSystem: ...
    def dialog_service(self) -> IDialogService: ...
