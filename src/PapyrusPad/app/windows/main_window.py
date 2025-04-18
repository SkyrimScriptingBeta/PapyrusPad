from dataclasses import field
from PySide6.QtWidgets import QLabel, QMainWindow

from qt_helpers.window import window


@window("MainWindow")
class MainWindow(QMainWindow):

    central_widget: QLabel = field(default_factory=lambda: QLabel("Hello World"))
