from abc import abstractmethod
from typing import Any
from dependency_injector import containers, providers


class IContainer(containers.DeclarativeContainer):
    """Interface defining the required providers for a container."""

    @property
    @abstractmethod
    def application(self) -> providers.Provider[Any]:
        """Application provider."""
        ...

    @property
    @abstractmethod
    def document_collection(self) -> providers.Provider[Any]:
        """Document collection provider."""
        ...

    @property
    @abstractmethod
    def filesystem(self) -> providers.Provider[Any]:
        """Filesystem provider."""
        ...

    @property
    @abstractmethod
    def dialog_service(self) -> providers.Provider[Any]:
        """Dialog service provider."""
        ...
