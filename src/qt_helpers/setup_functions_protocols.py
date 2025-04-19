from typing import Protocol
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDockWidget, QWidget


class SetupFunctionsProtocol(Protocol):
    """Protocol defining setup methods for Qt components."""

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


class WidgetProtocol(SetupFunctionsProtocol):
    pass


class MainWindowProtocol(SetupFunctionsProtocol):
    dock_widgets: list[QDockWidget]

    def setup_dock_widgets(self) -> None:
        pass

    def make_dock_widget(
        self,
        widget: QWidget,
        areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
        title: str = "",
    ) -> QDockWidget: ...

    def add_dock_widget(
        self,
        widget: QWidget,
        areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
        title: str = "",
    ) -> QDockWidget: ...
