import os
import sys

from PapyrusPad.di.setup import setup_development_dependencies, setup_production_dependencies


def main():
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
        setup_development_dependencies()
        run_app(development_mode=True)
    else:
        setup_production_dependencies()
        run_app(development_mode=False)


# Ensure the module is imported and executed


def run_app(development_mode: bool = False) -> None:
    if development_mode:
        from PapyrusPad.main import dev

        dev()
    else:
        from PapyrusPad.main import prod

        prod()


if __name__ == "__main__":
    main()
