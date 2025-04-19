from PySide6.QtWidgets import QLabel, QWidget

from qt_helpers.factory import create_widget
from qt_helpers.widget import widget


@widget()
class MyWidget(QWidget):
    label1: QLabel = create_widget(QLabel, "Hi from widget!")
    label2: QLabel = create_widget(QLabel, "Another!")
    label3: QLabel = create_widget(QLabel, "this one too!")
