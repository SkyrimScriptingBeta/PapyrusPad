from PySide6.QtWidgets import QLabel, QWidget

from qt_helpers.factory import factory
from qt_helpers.widget import widget


@widget()
class MyWidget(QWidget):
    label1: QLabel = factory(QLabel, "Hi from widget!")
    label2: QLabel = factory(QLabel, "Another!")
    label3: QLabel = factory(QLabel, "this one too!")
