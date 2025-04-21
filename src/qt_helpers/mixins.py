from dataclasses import dataclass
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QBoxLayout, QStyle, QWidget


@dataclass
class SetupFunctionsMixin:
    def setup(self) -> None:
        pass

    def setup_layout(self) -> None:
        pass

    def setup_styles(self) -> None:
        pass

    def setup_events(self) -> None:
        pass

    def setup_signals(self) -> None:
        pass


class WidgetMixin(SetupFunctionsMixin):
    layout: QBoxLayout | None

    def __init__(self):
        super().__init__()
        self.layout = None


class MainWindowMixin(SetupFunctionsMixin):
    central_widget: QWidget | None

    def __init__(self):
        super().__init__()
        self.central_widget = None


class MenuMixin:
    def __init__(self):
        super().__init__()


class ActionMixin:
    _text: str | None = None
    _shortcut: str | None = None
    _tooltip: str | None = None
    _icon: str | QPixmap | QIcon | QStyle.StandardPixmap | None = None

    def __init__(self):
        super().__init__()

    def action(self, checked: bool) -> None:
        pass
