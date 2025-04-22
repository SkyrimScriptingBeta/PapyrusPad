from typing import cast
from dependency_injector import containers

from PapyrusPad.di.container_interface import IContainer, IContainerClass

_container: containers.DeclarativeContainer | None = None
_container_class: type[containers.DeclarativeContainer] | None = None


def set_container(container_class: type[containers.DeclarativeContainer], container: containers.DeclarativeContainer) -> None:
    """Set the container for dependency injection.

    Args:
        new_container (containers.DeclarativeContainer): The container to be set.
    """
    global _container, _container_class
    _container = container
    _container_class = container_class
    print(f"Container set. Class: {container_class}, Instance: {container}")


def get_container() -> IContainer:
    """Get the current container.

    Returns:
        containers.DeclarativeContainer: The current container.
    """
    if _container is None:
        raise ValueError("Container has not been set.")
    return cast(IContainer, _container)


def get_container_class() -> IContainerClass:
    """Get the class of the current container.

    Returns:
        type[containers.DeclarativeContainer]: The class of the current container.
    """
    if _container_class is None:
        raise ValueError("Container class has not been set.")
    return _container_class


def reset_container() -> None:
    """Reset the container and its class to None."""
    global _container, _container_class
    _container = None
    _container_class = None
    print("Container and container class have been reset.")
