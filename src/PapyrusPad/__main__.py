import os
import sys
from PapyrusPad.di.container_registry import ContainerRegistry


def main():
    if "--debug" in sys.argv:
        import debugpy  # type: ignore[import]

        debugpy.listen(("localhost", 5678))
        print("⏳ Waiting for VS Code debugger to attach on port 5678...")
        debugpy.wait_for_client()

    # Set up the appropriate container based on arguments
    if "--dev" in sys.argv:
        from PapyrusPad.di.container_dev import DevelopmentContainer

        ContainerRegistry.set_container(DevelopmentContainer())
    else:
        from PapyrusPad.di.container_prod import ProductionContainer

        ContainerRegistry.set_container(ProductionContainer())

    # The container is now set up and ready to be used by the application
    # No need to import PapyrusPad.di.depends here as the container registry
    # already initializes everything we need

    if "--light" in sys.argv:
        os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"
    elif "--dark" in sys.argv:
        os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"

    if "--dev" in sys.argv:
        from PapyrusPad.main import dev

        dev()
    else:
        from PapyrusPad.main import prod

        prod()


if __name__ == "__main__":
    main()
