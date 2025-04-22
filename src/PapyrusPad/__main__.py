print("beginning!")

import os
import sys

from dependency_injector.wiring import register_loader_containers
from PapyrusPad.di.container import set_container


def setup_development_dependencies() -> None:
    print("setup_development_dependencies() ???")
    from PapyrusPad.di.container_dev import DevelopmentContainer

    container = DevelopmentContainer()
    container.wire()
    register_loader_containers(container)
    print("Registered loader")

    set_container(DevelopmentContainer, container)

    print("Importing PapyrusPad.di.depends")
    import PapyrusPad.di.depends

    _ = PapyrusPad.di.depends.Depends  # Ensure the module is imported and executed
    print("setup_development_dependencies() done")


def setup_production_dependencies() -> None:
    print("setup_production_dependencies()")
    from PapyrusPad.di.container_prod import ProductionContainer

    container = ProductionContainer()
    container.wire()
    register_loader_containers(container)
    print("Registered loader")

    # ContainerRegistry.set_container(container)
    set_container(ProductionContainer, container)

    print("Importing PapyrusPad.di.depends")
    import PapyrusPad.di.depends

    _ = PapyrusPad.di.depends.Depends  # Ensure the module is imported and executed
    print("setup_production_dependencies() done")


def main():
    print("__main__()")
    if "--debug" in sys.argv:
        import debugpy  # type: ignore[import]

        debugpy.listen(("localhost", 5678))
        print("⏳ Waiting for VS Code debugger to attach on port 5678...")
        debugpy.wait_for_client()

    if "--light" in sys.argv:
        os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"
    elif "--dark" in sys.argv:
        os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"

    if "--dev" in sys.argv:
        print("Development mode")
        setup_development_dependencies()
        run_app(development_mode=True)
    else:
        print("Production mode")
        run_app(development_mode=False)


def run_app(development_mode: bool = False) -> None:
    print("run_app()")
    if development_mode:
        from PapyrusPad.main import dev

        dev()
    else:
        from PapyrusPad.main import prod

        prod()


if __name__ == "__main__":
    main()
