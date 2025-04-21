from dependency_injector import providers
from PapyrusPad.di.container_prod import ProductionContainer
from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


class DevelopmentContainer(ProductionContainer):
    """Development container with development-specific overrides."""

    # Override with development-specific implementations if needed
    # For example, we could use a different filesystem implementation
    _filesystem = providers.Singleton(MemoryFileSystem)

    # Could add development-specific services
    # _debug_service = providers.Singleton(DebugService)
