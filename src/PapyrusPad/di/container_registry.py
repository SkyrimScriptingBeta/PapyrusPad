from dependency_injector.wiring import register_loader_containers
from PapyrusPad.di.container_interface import IContainer


class ContainerRegistry:
    """Registry to manage the active container."""

    _instance: IContainer | None = None

    @classmethod
    def get_container(cls) -> IContainer | None:
        """Get the active container instance.

        Returns:
            IContainer: The active container instance.
        """
        return cls._instance

    @classmethod
    def set_container(cls, container: IContainer) -> None:
        """Set the active container instance.

        Args:
            container (IContainer): The container instance to set as active.
        """
        cls._instance = container

        container.wire()
        register_loader_containers(container)
