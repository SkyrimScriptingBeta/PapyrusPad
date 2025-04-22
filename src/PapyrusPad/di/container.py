from typing import cast
from dependency_injector import containers

from typing import Protocol
from PySide6.QtWidgets import QApplication
from dependency_injector import providers

from PapyrusPad.domain.dialog.dialog_interface import IDialogService
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class IContainerClass(Protocol):
    application = providers.Dependency()
    document_collection = providers.Dependency()
    filesystem = providers.Dependency()
    dialog_service = providers.Dependency()


class IContainer(Protocol):
    def application(self) -> QApplication: ...
    def document_collection(self) -> IDocumentCollection: ...
    def filesystem(self) -> IFileSystem: ...
    def dialog_service(self) -> IDialogService: ...


_container: containers.DeclarativeContainer | None = None
_container_class: type[containers.DeclarativeContainer] | None = None


def set_container(container_class: type[containers.DeclarativeContainer], container: containers.DeclarativeContainer) -> None:
    global _container, _container_class
    _container = container
    _container_class = container_class
    print(f"Container set. Class: {container_class}, Instance: {container}")


def get_container() -> IContainer:
    if _container is None:
        raise ValueError("Container has not been set.")
    return cast(IContainer, _container)


def get_container_class() -> IContainerClass:
    if _container_class is None:
        raise ValueError("Container class has not been set.")
    return _container_class


def reset_container() -> None:
    global _container, _container_class
    _container = None
    _container_class = None
    print("Container and container class have been reset.")
