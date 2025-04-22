from typing import Protocol
from dependency_injector import providers


class IContainer(Protocol):
    """Test container with test-specific implementations."""

    application = providers.Dependency()
    document_collection = providers.Dependency()
    filesystem = providers.Dependency()
    dialog_service = providers.Dependency()
