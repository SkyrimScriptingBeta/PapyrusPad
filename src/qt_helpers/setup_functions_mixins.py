from dataclasses import dataclass
from typing import cast
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QBoxLayout, QDockWidget, QMainWindow, QWidget


@dataclass
class SetupFunctionsMixin:
    """
    Mixin class to provide setup functions for a PyQt/PySide application.
    """

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
    """
    Mixin class to provide setup functions for a PyQt/PySide widgets.
    """

    layout: QBoxLayout | None

    def __init__(self):
        super().__init__()
        self.layout = None


class MainWindowMixin(SetupFunctionsMixin):
    """
    Mixin class to provide setup functions for a PyQt/PySide main windows.
    """

    central_widget: QWidget | None

    dock_widgets: list[QDockWidget]

    def __init__(self):
        super().__init__()
        self.central_widget = None
        self.dock_widgets = []

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
    ) -> QDockWidget:
        dock_widget = QDockWidget(title or widget.windowTitle(), self._as_main_window())
        dock_widget.setWidget(widget)
        dock_widget.setAllowedAreas(areas)
        dock_widget.setFeatures(features)
        self.dock_widgets.append(dock_widget)
        return dock_widget

    def add_dock_widget(
        self,
        widget: QWidget,
        areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
        title: str = "",
    ) -> QDockWidget:
        dock_widget = self.make_dock_widget(widget, areas, features, title)
        self._as_main_window().addDockWidget(areas, dock_widget)
        return dock_widget

    def _as_main_window(self) -> QMainWindow:
        return cast(QMainWindow, self)
