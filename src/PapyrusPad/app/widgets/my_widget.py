from PySide6.QtWidgets import QLabel, QWidget

from qt_helpers.widget import widget
from qt_helpers.widget_factory import make_widget


@widget()
class MyWidget(QWidget):
    label1: QLabel = make_widget(QLabel, "label1", "This is label 1")
    label2: QLabel = make_widget(QLabel, "label2", "This is label 2")
    label3: QLabel = make_widget(QLabel, "label3", "This is label 3")
