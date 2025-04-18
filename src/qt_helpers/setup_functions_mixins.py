from dataclasses import dataclass
from PySide6.QtWidgets import QBoxLayout, QWidget


@dataclass
class SetupFunctionsMixin:
    """
    Mixin class to provide setup functions for a PyQt/PySide application.
    """

    def setup(self) -> None:
        pass

    def setup_styles(self) -> None:
        pass

    def setup_events(self) -> None:
        pass

    def setup_signals(self) -> None:
        pass


class WidgetSetupFunctionsMixin(SetupFunctionsMixin):
    """
    Mixin class to provide setup functions for a PyQt/PySide widgets.
    """

    layout: QBoxLayout | None

    def __init__(self):
        super().__init__()
        self.layout = None


class MainWindowSetupFunctionsMixin(SetupFunctionsMixin):
    """
    Mixin class to provide setup functions for a PyQt/PySide main windows.
    """

    central_widget: QWidget | None

    # TODO: some docking stuff

    def __init__(self):
        super().__init__()
        self.central_widget = None
