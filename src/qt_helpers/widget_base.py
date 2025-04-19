from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget

from qt_helpers.setup_functions_protocols import WidgetProtocol


if TYPE_CHECKING:

    class WidgetBase(QWidget, WidgetProtocol): ...

else:
    WidgetBase = QWidget
