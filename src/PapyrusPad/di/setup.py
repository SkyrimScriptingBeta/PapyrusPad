from dependency_injector import containers
from dependency_injector.wiring import register_loader_containers

from PapyrusPad.di.container import set_container


def setup_development_dependencies() -> None:
    from PapyrusPad.di.container_dev import DevelopmentContainer

    setup_dependencies(DevelopmentContainer)


def setup_production_dependencies() -> None:
    from PapyrusPad.di.container_prod import ProductionContainer

    setup_dependencies(ProductionContainer)


def setup_test_dependencies() -> None:
    from PapyrusPad.di.container_test import TestContainer

    setup_dependencies(TestContainer)


def setup_dependencies(container_class: type[containers.DeclarativeContainer]) -> None:
    container = container_class()
    container.wire()
    register_loader_containers(container)

    set_container(container_class, container)

    import PapyrusPad.di.depends

    _ = PapyrusPad.di.depends.Depends
