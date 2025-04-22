from typing import cast
from dependency_injector import containers

from typing import Protocol
from PySide6.QtWidgets import QApplication
from dependency_injector import providers

from PapyrusPad.domain.dialog.dialog_interface import IDialogService
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem

# TODO: one IContainer where each property is a callable that returns the T
# and so we can call like reset_override and have that stuff work ... does Dependency take a T?


class IContainer(Protocol):
    application = providers.Dependency(QApplication)
    document_collection = providers.Dependency(IDocumentCollection)
    filesystem = providers.Dependency(IFileSystem)
    dialog_service = providers.Dependency(IDialogService)


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


def get_container_class() -> IContainer:
    if _container_class is None:
        raise ValueError("Container class has not been set.")
    return _container_class
