from abc import ABC
from dataclasses import dataclass, field
from typing import Optional, cast, List, TypeVar, override, Any, Callable
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QTabWidget,
    QTextEdit,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTabBar,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import QEvent, Qt, QPoint, QObject

from qt_helpers.signal_typing import as_bool_handler


# Type aliases for better readability
DockList = List[QDockWidget]
T = TypeVar("T")

# Type definition for Qt signal handlers to satisfy Pylance
# This is a workaround for Qt's signal-slot typing issues
SignalHandler = Callable[[Any], None]

# TODO: after we set a widget as floating, from dragging from the tab bar,
# after it becomes floating perform a "click" on the title bar of the widget so we can keep dragging it, if possible


class EditorWidget(QWidget):
    def __init__(self, filename: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{filename}</b>"))
        layout.addWidget(QTextEdit(f"// Editing {filename}"))
        self.setLayout(layout)


class PanelWidget(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h3>{title}</h3>"))
        layout.addWidget(QPushButton(f"{title} Button"))
        layout.addStretch()
        self.setLayout(layout)


class IDockManager(ABC):
    def on_event(self, event: QEvent) -> None: ...
    def on_eventFilter(self, watched: QObject, event: QEvent) -> None: ...
    def dock(
        self,
        widget: QWidget,
        area: Qt.DockWidgetArea,
        title: Optional[str] = None,
        allowed_areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
    ) -> QDockWidget: ...


@dataclass
class DockManager(IDockManager):
    main_window: QMainWindow
    docked_widgets: list[QDockWidget] = field(default_factory=list[QDockWidget])
    _drag_tab_start_pos: QPoint = field(default_factory=QPoint)
    _drag_tab_index: int = -1
    _drag_tab_text: Optional[str] = None

    def __post_init__(self) -> None:
        self.main_window.setDockNestingEnabled(True)
        self.main_window.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)

    @override
    def on_event(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.LayoutRequest:
            self._install_tab_features()

    @override
    def on_eventFilter(self, watched: QObject, event: QEvent) -> None:
        if isinstance(watched, QTabBar):
            tab_bar = watched
            if event.type() == QEvent.Type.MouseButtonPress:
                mouse_event = cast(QMouseEvent, event)
                self._drag_tab_start_pos = mouse_event.pos()
                self._drag_tab_index = tab_bar.tabAt(self._drag_tab_start_pos)
                if self._drag_tab_index >= 0:
                    self._drag_tab_text = tab_bar.tabText(self._drag_tab_index)
            elif event.type() == QEvent.Type.MouseMove and self._drag_tab_text is not None:
                mouse_event = cast(QMouseEvent, event)
                margin = 50
                padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
                if not padded.contains(mouse_event.pos()):
                    self._undock_tab(self._drag_tab_text)
                    self._drag_tab_text = None
            elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
                self._drag_tab_text = None

    def _install_tab_features(self) -> None:
        for tab_bar in self.main_window.findChildren(QTabBar):
            if not tab_bar.property("_customized"):
                tab_bar.setTabsClosable(True)
                tab_bar.setMovable(True)
                tab_bar.tabCloseRequested.connect(self._handle_tab_close)
                tab_bar.installEventFilter(self.main_window)
                tab_bar.setProperty("_customized", True)

    # NOTE: we should handle other close methods to keep docked_widgets in sync
    def _handle_tab_close(self, index: int) -> None:
        tab_bar = self.main_window.sender()
        if isinstance(tab_bar, QTabBar):
            tab_text = tab_bar.tabText(index)
            for dock in self.main_window.findChildren(QDockWidget):
                if dock.windowTitle() == tab_text:
                    self.main_window.removeDockWidget(dock)
                    dock.deleteLater()
                    if dock in self.docked_widgets:
                        self.docked_widgets.remove(dock)
                    break

    # @override
    def _make_dock(
        self,
        widget: QWidget,
        title: Optional[str] = None,
        allowed_areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
    ) -> QDockWidget:
        dock = QDockWidget(title or widget.windowTitle(), self.main_window)
        dock.setWidget(widget)
        dock.setAllowedAreas(allowed_areas)

        dock.setFeatures(features)
        dock.topLevelChanged.connect(as_bool_handler(lambda _: self._update_title_bar_for(dock)))
        dock.dockLocationChanged.connect(as_bool_handler(lambda _: self._update_title_bar_for(dock)))
        self.docked_widgets.append(dock)
        return dock

    @override
    def dock(
        self,
        widget: QWidget,
        area: Qt.DockWidgetArea,
        title: Optional[str] = None,
        allowed_areas: Qt.DockWidgetArea = Qt.DockWidgetArea.AllDockWidgetAreas,
        features: QDockWidget.DockWidgetFeature = QDockWidget.DockWidgetFeature.DockWidgetClosable
        | QDockWidget.DockWidgetFeature.DockWidgetMovable
        | QDockWidget.DockWidgetFeature.DockWidgetFloatable,
    ) -> QDockWidget:
        dock = self._make_dock(widget, title, allowed_areas, features)
        self.main_window.addDockWidget(area, dock)
        return dock

    def _undock_tab(self, tab_text: str) -> None:
        for dock in self.main_window.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                siblings = self.main_window.tabifiedDockWidgets(dock)
                self.main_window.removeDockWidget(dock)
                self.main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                dock.setFloating(True)
                dock.show()

                # Update all previously tabified docks (including the undocked one)
                for d in siblings + [dock]:
                    self._update_title_bar_for(d)
                break

    def _update_title_bar_for(self, dock: QDockWidget) -> None:
        print("Updating title bar for:", dock)
        tab_group = self.main_window.tabifiedDockWidgets(dock)
        if dock not in tab_group:
            tab_group.append(dock)

        for w in tab_group:
            is_tabbified = any(other in self.main_window.tabifiedDockWidgets(w) for other in self.main_window.findChildren(QDockWidget) if other is not w)
            if is_tabbified:
                current = w.titleBarWidget()
                if current is None or current.sizeHint().height() > 0:  # type: ignore
                    hidden = QWidget()
                    hidden.setFixedHeight(0)
                    w.setTitleBarWidget(hidden)
            else:
                w.setTitleBarWidget(None)  # type: ignore


class IDEExampleWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.dock_manager: IDockManager = DockManager(self)

        self.setWindowTitle("Qt Docking — No Lies Edition")
        self.resize(2048, 1152)

        self.left_panel_widget = PanelWidget("Left Panel")
        self.right_panel_widget = PanelWidget("Right Panel")
        self.top_panel_widget = PanelWidget("Top Panel")
        self.bottom_panel_widget = PanelWidget("Bottom Panel")

        top_panel_dock = self.dock_manager.dock(self.top_panel_widget, Qt.DockWidgetArea.TopDockWidgetArea, "Top Panel")
        bottom_panel_dock = self.dock_manager.dock(self.bottom_panel_widget, Qt.DockWidgetArea.BottomDockWidgetArea, "Bottom Panel")
        left_panel_dock = self.dock_manager.dock(self.left_panel_widget, Qt.DockWidgetArea.LeftDockWidgetArea, "Left Panel")

        self.editor_one = EditorWidget("main.cpp")
        self.editor_two = EditorWidget("engine.cpp")
        self.editor_three = EditorWidget("ui.cpp")

        # Add Right
        right_panel_dock = self.dock_manager.dock(self.right_panel_widget, Qt.DockWidgetArea.RightDockWidgetArea, "Right Panel")

        # # SPLIT right Right, with the editor ending up on the left:
        editor_one_dock = self.dock_manager.dock(self.editor_one, Qt.DockWidgetArea.RightDockWidgetArea, "main.cpp")
        self.splitDockWidget(editor_one_dock, right_panel_dock, Qt.Orientation.Horizontal)

        # # Now TABIFY the second and third editor docks to the first one:
        editor_two_dock = self.dock_manager.dock(self.editor_two, Qt.DockWidgetArea.RightDockWidgetArea, "engine.cpp")
        self.tabifyDockWidget(editor_one_dock, editor_two_dock)

        editor_three_dock = self.dock_manager.dock(self.editor_three, Qt.DockWidgetArea.RightDockWidgetArea, "ui.cpp")
        self.tabifyDockWidget(editor_one_dock, editor_three_dock)

        editor_one_dock.raise_()
        # self._update_title_bar_for(editor_one_dock)

        # Type ignore for resizeDocks as it's a Qt API with complex typing
        self.resizeDocks(  # type: ignore
            [left_panel_dock, editor_one_dock, right_panel_dock],
            [200, 1648, 200],
            Qt.Orientation.Horizontal,
        )
        self.resizeDocks(  # type: ignore
            [top_panel_dock, editor_one_dock, bottom_panel_dock],
            [100, 902, 150],
            Qt.Orientation.Vertical,
        )

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self.dock_manager.on_eventFilter(watched, event)
        return super().eventFilter(watched, event)
