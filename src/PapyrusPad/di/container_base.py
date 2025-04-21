from typing import Any, override
from dependency_injector import providers
from PapyrusPad.di.container_interface import IContainer


class BaseContainer(IContainer):
    """Base container that implements the IContainer interface."""

    # These will be overridden by subclasses
    _application = providers.Dependency()
    _document_collection = providers.Dependency()
    _filesystem = providers.Dependency()
    _dialog_service = providers.Dependency()

    @property
    @override
    def application(self) -> providers.Provider[Any]:
        """Application provider."""
        return self._application

    @property
    @override
    def document_collection(self) -> providers.Provider[Any]:
        """Document collection provider."""
        return self._document_collection

    @property
    @override
    def filesystem(self) -> providers.Provider[Any]:
        """Filesystem provider."""
        return self._filesystem

    @property
    @override
    def dialog_service(self) -> providers.Provider[Any]:
        """Dialog service provider."""
        return self._dialog_service
