from typing import Protocol
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QBoxLayout, QDockWidget, QWidget


class SetupFunctionsProtocol(Protocol):
    """Protocol defining setup methods for Qt components."""

    def setup(self) -> None: ...
    def setup_layout(self) -> None: ...
    def setup_styles(self) -> None: ...
    def setup_events(self) -> None: ...
    def setup_signals(self) -> None: ...


class WidgetProtocol(SetupFunctionsProtocol):
    layout: QBoxLayout | None


class MainWindowProtocol(SetupFunctionsProtocol):
    dock_widgets: list[QDockWidget]

    def make_dock_widget(
        self,
        widget: QWidget,
        areas: Qt.DockWidgetArea,
        features: QDockWidget.DockWidgetFeature,
    ) -> QDockWidget: ...

    def add_dock_widget(
        self,
        widget: QWidget,
        areas: Qt.DockWidgetArea,
        features: QDockWidget.DockWidgetFeature,
    ) -> QDockWidget: ...
