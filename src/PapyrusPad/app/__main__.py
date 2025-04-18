import os
import sys


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
        from PapyrusPad.app.main import dev

        dev()
    else:
        from PapyrusPad.app.main import prod

        prod()


if __name__ == "__main__":
    main()
