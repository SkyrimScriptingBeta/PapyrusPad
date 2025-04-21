from typing import Any
from PySide6.QtWidgets import QApplication
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, register_loader_containers

from PapyrusPad.application import Application
from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


# Dependencies
class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)
    document_collection = providers.Singleton(DocumentCollection)
    filesystem = providers.Singleton(MemoryFileSystem)


# Global container
container = Container()
container.wire()
register_loader_containers(container)


# Lookup by dependency name
class Dependencies:
    application: Application = Provide[Container.application]
    document_collection: DocumentCollection = Provide[Container.document_collection]
    filesystem: MemoryFileSystem = Provide[Container.filesystem]


# Lookup by type
Depends: dict[type, Any] = {
    Application: Dependencies.application,
    QApplication: Dependencies.application,
    IDocumentCollection: Dependencies.document_collection,
    IFileSystem: Dependencies.filesystem,
}
