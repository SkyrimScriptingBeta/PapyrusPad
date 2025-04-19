from typing import TYPE_CHECKING

from PySide6.QtWidgets import QMainWindow

from qt_helpers.setup_functions_protocols import MainWindowProtocol


if TYPE_CHECKING:

    class MainWindowBase(QMainWindow, MainWindowProtocol): ...

else:
    MainWindowBase = QMainWindow
