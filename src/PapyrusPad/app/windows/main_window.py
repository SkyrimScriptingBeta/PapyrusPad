from PySide6.QtWidgets import QMainWindow

from PapyrusPad.app.widgets.my_widget import MyWidget
from qt_helpers.factory import create_widget
from qt_helpers.window import window


@window("MainWindow", title="PapyrusPad")
class MainWindow(QMainWindow):
    central_widget: MyWidget = create_widget(MyWidget)
