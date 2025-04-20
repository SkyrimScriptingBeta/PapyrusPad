"""
Dock Manager Proposal Example

This file demonstrates an encapsulated approach to implementing advanced Qt docking features
using a DockManager class rather than standalone helper functions or mixins.

Features implemented:
- Closeable tabs
- Tabs positioned at the top
- Drag-to-undock functionality
- Title bar management for tabbed widgets
"""

from abc import ABC, abstractmethod
from typing import cast, Callable, Optional, override
from dataclasses import dataclass, field
from enum import Enum, auto
from PySide6.QtWidgets import (
    QMainWindow,
    QDockWidget,
    QTabBar,
    QWidget,
    QTabWidget,
)
from PySide6.QtCore import QEvent, Qt, QObject, QPoint
from PySide6.QtGui import QMouseEvent


@dataclass
class TabDragData:
    """Data for tracking tab drag operations."""

    start_pos: QPoint
    tab_index: int
    tab_text: str


class DockWidgetLocation(Enum):
    """Locations where a dock widget can be placed."""

    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()
    CENTER = auto()  # For tabbed with existing dock


class IDockManager(ABC):
    """
    Abstract base class defining the public interface for a dock manager.

    This interface provides methods for managing dock widgets in a QMainWindow.
    """

    @abstractmethod
    def add_dock_widget(
        self,
        widget: QWidget,
        title: str,
        location: DockWidgetLocation = DockWidgetLocation.RIGHT,
        features: Optional[list[QDockWidget.DockWidgetFeature]] = None,
        tab_with: Optional[QDockWidget] = None,
    ) -> QDockWidget:
        """
        Add a widget as a dock widget to the main window.

        Args:
            widget: The widget to dock
            title: The title for the dock widget
            location: Where to place the dock widget
            features: Features to enable for the dock widget
            tab_with: Existing dock widget to tab with (if any)

        Returns:
            The created dock widget
        """
        ...

    @abstractmethod
    def remove_dock_widget(self, dock: QDockWidget) -> None:
        """
        Remove a dock widget from the main window.

        Args:
            dock: The dock widget to remove
        """
        ...

    @abstractmethod
    def tabify_dock_widgets(self, first: QDockWidget, second: QDockWidget) -> None:
        """
        Tabify two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget to tab with the first
        """
        ...

    @abstractmethod
    def split_dock_widget(
        self, first: QDockWidget, second: QDockWidget, orientation: Qt.Orientation
    ) -> None:
        """
        Split the dock area with two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget
            orientation: The orientation of the split
        """
        ...

    @abstractmethod
    def set_dock_widget_floating(self, dock: QDockWidget, floating: bool) -> None:
        """
        Set whether a dock widget is floating.

        Args:
            dock: The dock widget
            floating: Whether the dock widget should be floating
        """
        ...

    @abstractmethod
    def resize_docks(
        self, docks: list[QDockWidget], sizes: list[int], orientation: Qt.Orientation
    ) -> None:
        """
        Resize a list of dock widgets.

        Args:
            docks: The dock widgets to resize
            sizes: The sizes for each dock widget
            orientation: The orientation of the resize
        """
        ...

    @abstractmethod
    def handle_event_filter(self, watched: QObject, event: QEvent) -> bool:
        """
        Handle event filtering for the main window.

        This method should be called from the main window's eventFilter method.

        Args:
            watched: The object that sent the event
            event: The event to filter

        Returns:
            True if the event was handled and should be filtered out,
            False if the event should be processed normally
        """
        ...


@dataclass
class DockManager(IDockManager):
    """
    Implementation of the IDockManager interface.

    This class manages advanced docking features for a QMainWindow.
    """

    # Required attributes
    main_window: QMainWindow

    # Optional attributes with defaults
    _drag_state: Optional[TabDragData] = None
    _customized_tab_bars: list[QTabBar] = field(default_factory=lambda: list[QTabBar]())

    def __post_init__(self) -> None:
        """Initialize the dock manager."""
        # Install event filter on main window to catch layout changes
        self.main_window.event = self._wrap_event_method(self.main_window.event)

        # Set up initial configuration
        self._enable_dock_nesting()
        self._set_tabs_position_north()

        # Install event filter on main window
        self.main_window.installEventFilter(self.main_window)

    @override
    def add_dock_widget(
        self,
        widget: QWidget,
        title: str,
        location: DockWidgetLocation = DockWidgetLocation.RIGHT,
        features: Optional[list[QDockWidget.DockWidgetFeature]] = None,
        tab_with: Optional[QDockWidget] = None,
    ) -> QDockWidget:
        """
        Add a widget as a dock widget to the main window.

        Args:
            widget: The widget to dock
            title: The title for the dock widget
            location: Where to place the dock widget
            features: Features to enable for the dock widget
            tab_with: Existing dock widget to tab with (if any)

        Returns:
            The created dock widget
        """
        # Create dock widget
        dock = QDockWidget(title, self.main_window)
        dock.setWidget(widget)

        # Set allowed areas
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # Set features
        qt_features = (
            QDockWidget.DockWidgetFeature.DockWidgetClosable
            | QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        if features:
            qt_features = QDockWidget.DockWidgetFeature.DockWidgetClosable
            for feature in features:
                qt_features |= feature

        dock.setFeatures(qt_features)

        # Add to main window
        qt_location = self._convert_location_to_qt(location)
        self.main_window.addDockWidget(qt_location, dock)

        # Connect signals
        self._connect_dock_signals(dock)

        # Tabify if requested
        if tab_with is not None:
            self.tabify_dock_widgets(tab_with, dock)
            tab_with.raise_()  # Make the first dock active

        # Customize tab bars
        self._customize_all_tab_bars()

        return dock

    @override
    def remove_dock_widget(self, dock: QDockWidget) -> None:
        """
        Remove a dock widget from the main window.

        Args:
            dock: The dock widget to remove
        """
        self.main_window.removeDockWidget(dock)
        dock.deleteLater()

    @override
    def tabify_dock_widgets(self, first: QDockWidget, second: QDockWidget) -> None:
        """
        Tabify two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget to tab with the first
        """
        self.main_window.tabifyDockWidget(first, second)
        self._update_title_bar_for_dock(first)
        self._update_title_bar_for_dock(second)

    @override
    def split_dock_widget(
        self, first: QDockWidget, second: QDockWidget, orientation: Qt.Orientation
    ) -> None:
        """
        Split the dock area with two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget
            orientation: The orientation of the split
        """
        self.main_window.splitDockWidget(first, second, orientation)

    @override
    def set_dock_widget_floating(self, dock: QDockWidget, floating: bool) -> None:
        """
        Set whether a dock widget is floating.

        Args:
            dock: The dock widget
            floating: Whether the dock widget should be floating
        """
        dock.setFloating(floating)
        self._update_title_bar_for_dock(dock)

    @override
    def resize_docks(
        self, docks: list[QDockWidget], sizes: list[int], orientation: Qt.Orientation
    ) -> None:
        """
        Resize a list of dock widgets.

        Args:
            docks: The dock widgets to resize
            sizes: The sizes for each dock widget
            orientation: The orientation of the resize
        """
        self.main_window.resizeDocks(docks, sizes, orientation)  # type: ignore

    def _convert_location_to_qt(
        self, location: DockWidgetLocation
    ) -> Qt.DockWidgetArea:
        """Convert a DockWidgetLocation to a Qt.DockWidgetArea."""
        if location == DockWidgetLocation.LEFT:
            return Qt.DockWidgetArea.LeftDockWidgetArea
        elif location == DockWidgetLocation.RIGHT:
            return Qt.DockWidgetArea.RightDockWidgetArea
        elif location == DockWidgetLocation.TOP:
            return Qt.DockWidgetArea.TopDockWidgetArea
        elif location == DockWidgetLocation.BOTTOM:
            return Qt.DockWidgetArea.BottomDockWidgetArea
        else:
            return Qt.DockWidgetArea.RightDockWidgetArea

    def _enable_dock_nesting(self) -> None:
        """Enable dock nesting in the main window."""
        self.main_window.setDockNestingEnabled(True)

    def _set_tabs_position_north(self) -> None:
        """Set all tab positions to North (top)."""
        self.main_window.setTabPosition(
            Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North
        )

    def _customize_all_tab_bars(self) -> None:
        """Find and customize all tab bars in the main window."""
        for tab_bar in self.main_window.findChildren(QTabBar):
            self._customize_tab_bar(tab_bar)

    def _customize_tab_bar(self, tab_bar: QTabBar) -> bool:
        """
        Apply standard customizations to a tab bar.

        Args:
            tab_bar: The QTabBar to customize

        Returns:
            True if customizations were applied, False if already customized
        """
        if not tab_bar.property("_customized"):
            tab_bar.setTabsClosable(True)
            tab_bar.setMovable(True)
            tab_bar.tabCloseRequested.connect(self._handle_tab_close)
            tab_bar.installEventFilter(self.main_window)
            tab_bar.setProperty("_customized", True)
            self._customized_tab_bars.append(tab_bar)
            return True
        return False

    def _connect_all_dock_signals(self) -> None:
        """Connect signals for all dock widgets in the main window."""
        for dock in self.main_window.findChildren(QDockWidget):
            self._connect_dock_signals(dock)

    def _connect_dock_signals(self, dock: QDockWidget) -> None:
        """
        Connect signals for a dock widget to update its title bar.

        Args:
            dock: The QDockWidget to connect signals for
        """
        # Store dock reference in default parameter to avoid lambda capture issues
        dock.topLevelChanged.connect(
            lambda floating: self._update_title_bar_for_dock(dock)
        )
        dock.dockLocationChanged.connect(
            lambda area: self._update_title_bar_for_dock(dock)
        )

    def _update_title_bar_for_dock(self, dock: QDockWidget) -> None:
        """
        Update the title bar visibility for a dock based on its tabification state.

        Args:
            dock: The QDockWidget to update
        """
        if self._is_dock_tabified(dock):
            current = dock.titleBarWidget()
            # Check if we need to hide the title bar
            if current is None:
                self._hide_dock_title_bar(dock)
            elif current.sizeHint().height() > 0:
                self._hide_dock_title_bar(dock)
        else:
            self._show_dock_title_bar(dock)

    def _update_title_bars_for_tab_group(self, dock: QDockWidget) -> None:
        """
        Update title bars for a dock and all docks tabified with it.

        Args:
            dock: The QDockWidget that is part of the tab group
        """
        tab_group = self.main_window.tabifiedDockWidgets(dock)
        if dock not in tab_group:
            tab_group.append(dock)

        for w in tab_group:
            self._update_title_bar_for_dock(w)

    def _is_dock_tabified(self, dock: QDockWidget) -> bool:
        """
        Check if a dock widget is part of a tab group.

        Args:
            dock: The QDockWidget to check

        Returns:
            True if the dock is tabified with any other dock, False otherwise
        """
        return any(
            other in self.main_window.tabifiedDockWidgets(dock)
            for other in self.main_window.findChildren(QDockWidget)
            if other is not dock
        )

    def _hide_dock_title_bar(self, dock: QDockWidget) -> None:
        """
        Hide the title bar of a dock widget.

        Args:
            dock: The QDockWidget to modify
        """
        hidden = QWidget()
        hidden.setFixedHeight(0)
        dock.setTitleBarWidget(hidden)

    def _show_dock_title_bar(self, dock: QDockWidget) -> None:
        """
        Restore the default title bar of a dock widget.

        Args:
            dock: The QDockWidget to modify
        """
        # Two-step process to handle None correctly
        temp_widget = QWidget()
        dock.setTitleBarWidget(temp_widget)
        # Use None directly - PySide6 handles this correctly at runtime
        dock.setTitleBarWidget(None)  # type: ignore

    def _handle_tab_close(self, index: int) -> None:
        """
        Handle tab close requests.

        Args:
            index: The index of the tab to close
        """
        # Cast sender to QTabBar to access tabText method
        tab_bar = cast(QTabBar, self.main_window.sender())
        tab_text = tab_bar.tabText(index)
        self._remove_dock_by_title(tab_text)

    def _remove_dock_by_title(self, title: str) -> bool:
        """
        Find and remove a dock widget by its title.

        Args:
            title: The title of the dock to remove

        Returns:
            True if the dock was found and removed, False otherwise
        """
        for dock in self.main_window.findChildren(QDockWidget):
            if dock.windowTitle() == title:
                self.remove_dock_widget(dock)
                return True
        return False

    def _undock_tab(self, tab_text: str) -> bool:
        """
        Undock a tab by its text, making it a floating window.

        Args:
            tab_text: The text of the tab to undock

        Returns:
            True if the tab was found and undocked, False otherwise
        """
        for dock in self.main_window.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                siblings = self.main_window.tabifiedDockWidgets(dock)
                self.main_window.removeDockWidget(dock)
                self.main_window.addDockWidget(
                    Qt.DockWidgetArea.RightDockWidgetArea, dock
                )
                self.set_dock_widget_floating(dock, True)
                dock.show()

                # Update title bars for all affected docks
                for d in siblings + [dock]:
                    self._update_title_bar_for_dock(d)

                return True
        return False

    def _handle_tab_drag_event(self, event: QEvent, tab_bar: QTabBar) -> bool:
        """
        Handle mouse events on a tab bar for drag-to-undock functionality.

        Args:
            event: The QEvent to handle
            tab_bar: The QTabBar that received the event

        Returns:
            True if the event was handled, False otherwise
        """
        handled = False

        if event.type() == QEvent.Type.MouseButtonPress:
            mouse_event = cast(QMouseEvent, event)
            tab_index = tab_bar.tabAt(mouse_event.pos())
            if tab_index >= 0:
                tab_text = tab_bar.tabText(tab_index)
                self._drag_state = TabDragData(
                    start_pos=mouse_event.pos(), tab_index=tab_index, tab_text=tab_text
                )
            handled = True

        elif event.type() == QEvent.Type.MouseMove and self._drag_state is not None:
            mouse_event = cast(QMouseEvent, event)
            margin = 50  # Adjust this value to change sensitivity
            padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
            if not padded.contains(mouse_event.pos()):
                self._undock_tab(self._drag_state.tab_text)
                self._drag_state = None  # Reset drag state
            handled = True

        elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
            self._drag_state = None  # Reset drag state
            handled = True

        return handled

    def _wrap_event_method(
        self, original_event_method: Callable[[QEvent], bool]
    ) -> Callable[[QEvent], bool]:
        """
        Wrap the main window's event method to catch layout changes.

        Args:
            original_event_method: The original event method of the main window

        Returns:
            A wrapped event method that customizes tab bars on layout changes
        """

        def wrapped_event(event: QEvent) -> bool:
            if event.type() == QEvent.Type.LayoutRequest:
                self._customize_all_tab_bars()
            return original_event_method(event)

        return wrapped_event

    @override
    def handle_event_filter(self, watched: QObject, event: QEvent) -> bool:
        """
        Handle event filtering for the main window.

        This method should be called from the main window's eventFilter method.

        Args:
            watched: The object that sent the event
            event: The event to filter

        Returns:
            True if the event was handled and should be filtered out,
            False if the event should be processed normally
        """
        if isinstance(watched, QTabBar) and watched in self._customized_tab_bars:
            return self._handle_tab_drag_event(event, watched)

        return False


# class EditorWidget(QWidget):
#     """A simple editor widget for demonstration purposes."""

#     def __init__(self, filename: str) -> None:
#         super().__init__()
#         layout = QVBoxLayout(self)
#         layout.addWidget(QLabel(f"<b>{filename}</b>"))
#         layout.addWidget(QTextEdit(f"// Editing {filename}"))
#         self.setLayout(layout)


# class PanelWidget(QWidget):
#     """A simple panel widget for demonstration purposes."""

#     def __init__(self, title: str) -> None:
#         super().__init__()
#         layout = QVBoxLayout(self)
#         layout.addWidget(QLabel(f"<h3>{title}</h3>"))
#         layout.addWidget(QPushButton(f"{title} Button"))
#         layout.addStretch()
#         self.setLayout(layout)


# class MyIDEWindow(QMainWindow):
#     """
#     An example IDE window that uses the DockManager to implement advanced docking features.

#     This class demonstrates how to use the DockManager to add docking features
#     to a QMainWindow without changing its inheritance hierarchy.
#     """

#     def __init__(self) -> None:
#         super().__init__()
#         self.setWindowTitle("Qt Docking with DockManager")
#         self.resize(1600, 900)

#         # Initialize dock manager
#         self.dock_manager: IDockManager = DockManager(self)

#         # Initialize editor_docks with proper type annotation
#         self.editor_docks: list[QDockWidget] = []

#         # Create dock widgets
#         self.setup_dock_widgets()

#     def setup_dock_widgets(self) -> None:
#         """Create and arrange dock widgets."""
#         # Create panel docks
#         self.left_panel = self.dock_manager.add_dock_widget(
#             PanelWidget("Left Panel"), "Left Panel", DockWidgetLocation.LEFT
#         )

#         self.right_panel = self.dock_manager.add_dock_widget(
#             PanelWidget("Right Panel"), "Right Panel", DockWidgetLocation.RIGHT
#         )

#         self.top_panel = self.dock_manager.add_dock_widget(
#             PanelWidget("Top Panel"), "Top Panel", DockWidgetLocation.TOP
#         )

#         self.bottom_panel = self.dock_manager.add_dock_widget(
#             PanelWidget("Bottom Panel"), "Bottom Panel", DockWidgetLocation.BOTTOM
#         )

#         # Create editor docks
#         first_editor = self.dock_manager.add_dock_widget(
#             EditorWidget("main.cpp"), "main.cpp", DockWidgetLocation.RIGHT
#         )
#         self.editor_docks.append(first_editor)

#         # Split first editor and right panel
#         self.dock_manager.split_dock_widget(
#             first_editor, self.right_panel, Qt.Orientation.Horizontal
#         )

#         # Add more editors as tabs
#         for filename in ["engine.cpp", "ui.cpp"]:
#             dock = self.dock_manager.add_dock_widget(
#                 EditorWidget(filename), filename, tab_with=first_editor
#             )
#             self.editor_docks.append(dock)

#         # Raise first editor to make it the active tab
#         first_editor.raise_()

#         # Resize docks
#         self.dock_manager.resize_docks(
#             [self.left_panel, first_editor, self.right_panel],
#             [200, 1200, 200],
#             Qt.Orientation.Horizontal,
#         )

#         self.dock_manager.resize_docks(
#             [self.top_panel, first_editor, self.bottom_panel],
#             [100, 650, 150],
#             Qt.Orientation.Vertical,
#         )

#     def eventFilter(self, watched: QObject, event: QEvent) -> bool:
#         """Filter events for tab drag detection."""
#         # Delegate to dock manager
#         if self.dock_manager.handle_event_filter(watched, event):
#             return False  # Let the event propagate

#         return super().eventFilter(watched, event)


# def main() -> None:
#     """Run the application."""
#     app = QApplication(sys.argv)
#     app.setFont(QFont("Segoe UI", 9))
#     window = MyIDEWindow()
#     window.show()
#     sys.exit(app.exec())


# if __name__ == "__main__":
#     main()
