import os
import sys
import PapyrusPad.app.dependencies  # Import from __main__ so DI can wire up the whole app's modules

# Don't remove this import :)
DEPS = PapyrusPad.app.dependencies


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
        from PapyrusPad.main import dev

        dev()
    else:
        from PapyrusPad.main import prod

        prod()


if __name__ == "__main__":
    main()
