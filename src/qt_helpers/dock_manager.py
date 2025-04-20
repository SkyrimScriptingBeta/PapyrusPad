"""
Dock Manager

This module provides a reusable DockManager class that encapsulates advanced Qt docking features
for QMainWindow applications. It handles tab management, drag-to-undock functionality, and
title bar management for tabbed widgets.

Features:
- Closeable tabs
- Tabs positioned at the top
- Drag-to-undock functionality
- Title bar management for tabbed widgets
- Strongly typed interface
"""

import logging
from dataclasses import dataclass
from enum import Enum, auto
from typing import cast, List, Optional, TypeVar, Protocol, override

from PySide6.QtCore import QEvent, QObject, QPoint, Qt, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QDockWidget,
    QMainWindow,
    QTabBar,
    QTabWidget,
    QWidget,
)

# Type variable for generic methods
T = TypeVar("T")


class DockWidgetLocation(Enum):
    """Locations where a dock widget can be placed."""

    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()
    CENTER = auto()  # For tabbed with existing dock


@dataclass
class TabDragState:
    """Data for tracking tab drag operations."""

    start_pos: QPoint
    tab_index: int
    tab_text: str


class IDockManager(Protocol):
    """
    Protocol defining the public interface for a dock manager.

    This interface provides methods for managing dock widgets in a QMainWindow.
    """

    def add_dock_widget(
        self,
        widget: QWidget,
        title: str,
        location: DockWidgetLocation = DockWidgetLocation.RIGHT,
        features: Optional[List[QDockWidget.DockWidgetFeature]] = None,
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

    def remove_dock_widget(self, dock: QDockWidget) -> None:
        """
        Remove a dock widget from the main window.

        Args:
            dock: The dock widget to remove
        """
        ...

    def tabify_dock_widgets(self, first: QDockWidget, second: QDockWidget) -> None:
        """
        Tabify two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget to tab with the first
        """
        ...

    def split_dock_widget(self, first: QDockWidget, second: QDockWidget, orientation: Qt.Orientation) -> None:
        """
        Split the dock area with two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget
            orientation: The orientation of the split
        """
        ...

    def set_dock_widget_floating(self, dock: QDockWidget, floating: bool) -> None:
        """
        Set whether a dock widget is floating.

        Args:
            dock: The dock widget
            floating: Whether the dock widget should be floating
        """
        ...

    def resize_docks(self, docks: List[QDockWidget], sizes: List[int], orientation: Qt.Orientation) -> None:
        """
        Resize a list of dock widgets.

        Args:
            docks: The dock widgets to resize
            sizes: The sizes for each dock widget
            orientation: The orientation of the resize
        """
        ...

    def raise_dock_widget(self, dock: QDockWidget) -> None:
        """
        Raise a dock widget to the top of its tab stack.

        Args:
            dock: The dock widget to raise
        """
        ...

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

    def customize_tab_bars(self) -> None:
        """
        Find and customize all tab bars in the main window.

        This ensures that tabs are closable, movable, and have the correct event filters.
        """
        ...


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("DockManager")


class DockManager(QObject):
    """
    Implementation of the IDockManager interface.

    This class manages advanced docking features for a QMainWindow.
    """

    # Signal emitted when a dock widget is added
    dock_added = Signal(QDockWidget)

    # Signal emitted when a dock widget is removed
    dock_removed = Signal(QDockWidget)

    def __init__(self, main_window: QMainWindow) -> None:
        """
        Initialize the dock manager.

        Args:
            main_window: The main window to manage docks for
        """
        super().__init__(main_window)
        self._main_window = main_window
        self._drag_state: Optional[TabDragState] = None
        self._customized_tab_bars: List[QTabBar] = []

        logger.debug("Initializing DockManager")

        # Configure the main window
        self._main_window.setDockNestingEnabled(True)
        self._set_tabs_position_north()

        # Install event filter on the main window
        self._main_window.installEventFilter(self)
        logger.debug("Event filter installed on main window")

    def add_dock_widget(
        self,
        widget: QWidget,
        title: str,
        location: DockWidgetLocation = DockWidgetLocation.RIGHT,
        features: Optional[List[QDockWidget.DockWidgetFeature]] = None,
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
        dock = QDockWidget(title, self._main_window)
        dock.setWidget(widget)

        # Set allowed areas
        dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)

        # Set features
        default_features = QDockWidget.DockWidgetFeature.DockWidgetClosable | QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable

        if features:
            qt_features = QDockWidget.DockWidgetFeature(0)
            for feature in features:
                qt_features |= feature
        else:
            qt_features = default_features

        dock.setFeatures(qt_features)

        # Add to main window
        qt_location = self._convert_location_to_qt(location)
        self._main_window.addDockWidget(qt_location, dock)

        # Connect signals
        dock.topLevelChanged.connect(lambda floating: self._handle_dock_top_level_changed(dock, floating))  # type: ignore
        dock.dockLocationChanged.connect(lambda area: self._handle_dock_location_changed(dock, area))  # type: ignore

        # Install event filter on the dock widget
        dock.installEventFilter(self)
        logger.debug(f"Event filter installed on dock '{dock.windowTitle()}'")

        # Tabify if requested
        if tab_with is not None:
            self.tabify_dock_widgets(tab_with, dock)

        # Customize tab bars
        self._customize_all_tab_bars()

        # Emit signal
        self.dock_added.emit(dock)

        return dock

    def remove_dock_widget(self, dock: QDockWidget) -> None:
        """
        Remove a dock widget from the main window.

        Args:
            dock: The dock widget to remove
        """
        # Get tab group before removal
        tab_group = self._main_window.tabifiedDockWidgets(dock)

        # Remove the dock
        self._main_window.removeDockWidget(dock)

        # Update title bars for remaining docks in the tab group
        for other_dock in tab_group:
            self._update_title_bars_for_tab_group(other_dock)

        # Emit signal
        self.dock_removed.emit(dock)

        # Schedule the dock for deletion
        dock.deleteLater()

    def tabify_dock_widgets(self, first: QDockWidget, second: QDockWidget) -> None:
        """
        Tabify two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget to tab with the first
        """
        self._main_window.tabifyDockWidget(first, second)
        self._update_title_bars_for_tab_group(first)

    def split_dock_widget(self, first: QDockWidget, second: QDockWidget, orientation: Qt.Orientation) -> None:
        """
        Split the dock area with two dock widgets.

        Args:
            first: The first dock widget
            second: The second dock widget
            orientation: The orientation of the split
        """
        self._main_window.splitDockWidget(first, second, orientation)

    def set_dock_widget_floating(self, dock: QDockWidget, floating: bool) -> None:
        """
        Set whether a dock widget is floating.

        Args:
            dock: The dock widget
            floating: Whether the dock widget should be floating
        """
        logger.debug(f"Setting dock '{dock.windowTitle()}' floating: {floating}")
        dock.setFloating(floating)
        self._update_title_bars_for_tab_group(dock)

    def resize_docks(self, docks: List[QDockWidget], sizes: List[int], orientation: Qt.Orientation) -> None:
        """
        Resize a list of dock widgets.

        Args:
            docks: The dock widgets to resize
            sizes: The sizes for each dock widget
            orientation: The orientation of the resize
        """
        self._main_window.resizeDocks(docks, sizes, orientation)  # type: ignore

    def raise_dock_widget(self, dock: QDockWidget) -> None:
        """
        Raise a dock widget to the top of its tab stack.

        Args:
            dock: The dock widget to raise
        """
        dock.raise_()

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
        # We now handle all event filtering directly in the eventFilter method
        # This method is kept for backward compatibility
        return False  # Let the event propagate

    def customize_tab_bars(self) -> None:
        """
        Find and customize all tab bars in the main window.

        This ensures that tabs are closable, movable, and have the correct event filters.
        """
        self._customize_all_tab_bars()

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
        Filter events for the main window and tab bars.

        Args:
            watched: The object that sent the event
            event: The event to filter

        Returns:
            True if the event was handled and should be filtered out,
            False if the event should be processed normally
        """
        # Log dock widget events (for debugging only)
        if isinstance(watched, QDockWidget) and event.type() in {
            QEvent.Type.DragEnter,
            QEvent.Type.DragLeave,
            QEvent.Type.DragMove,
            QEvent.Type.Drop,
        }:
            logger.debug(f"Dock event: {watched.windowTitle()} - {event.type().name}")

        # Handle layout changes to customize tab bars
        if watched is self._main_window and event.type() == QEvent.Type.LayoutRequest:
            logger.debug("Layout request event received")
            self._customize_all_tab_bars()
            # Don't return True here, let the event continue to propagate

        # Handle tab bar events for drag detection
        if isinstance(watched, QTabBar) and watched in self._customized_tab_bars:
            tab_bar = watched
            if event.type() == QEvent.Type.MouseButtonPress:
                mouse_event = cast(QMouseEvent, event)
                tab_index = tab_bar.tabAt(mouse_event.pos())
                if tab_index >= 0:
                    self._drag_state = TabDragState(
                        start_pos=mouse_event.pos(),
                        tab_index=tab_index,
                        tab_text=tab_bar.tabText(tab_index),
                    )
                # Don't return True, let the event continue to propagate
            elif event.type() == QEvent.Type.MouseMove and self._drag_state is not None:
                mouse_event = cast(QMouseEvent, event)
                margin = 50  # Adjust this value to change sensitivity
                padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
                if not padded.contains(mouse_event.pos()):
                    self._undock_tab(self._drag_state.tab_text)
                    self._drag_state = None
                    # Don't return True here either
            elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
                self._drag_state = None
                # Don't return True, let the event continue to propagate

        # Always call the parent class's eventFilter to ensure proper event propagation
        return super().eventFilter(watched, event)

    def _convert_location_to_qt(self, location: DockWidgetLocation) -> Qt.DockWidgetArea:
        """
        Convert a DockWidgetLocation to a Qt.DockWidgetArea.

        Args:
            location: The location to convert

        Returns:
            The corresponding Qt dock widget area
        """
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

    def _set_tabs_position_north(self) -> None:
        """Set all tab positions to North (top)."""
        self._main_window.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)

    def _customize_all_tab_bars(self) -> None:
        """Find and customize all tab bars in the main window."""
        for tab_bar in self._main_window.findChildren(QTabBar):
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
            tab_bar.installEventFilter(self)
            tab_bar.setProperty("_customized", True)

            # Track the tab bar and remove it when destroyed
            tab_bar.destroyed.connect(lambda: self._remove_tab_bar(tab_bar))
            self._customized_tab_bars.append(tab_bar)
            return True
        return False

    def _remove_tab_bar(self, tab_bar: QTabBar) -> None:
        """
        Remove a tab bar from the tracked list when it's destroyed.

        Args:
            tab_bar: The tab bar to remove
        """
        if tab_bar in self._customized_tab_bars:
            self._customized_tab_bars.remove(tab_bar)

    def _handle_tab_close(self, index: int) -> None:
        """
        Handle tab close requests.

        Args:
            index: The index of the tab to close
        """
        tab_bar = self.sender()
        if not isinstance(tab_bar, QTabBar):
            return

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
        for dock in self._main_window.findChildren(QDockWidget):
            if dock.windowTitle() == title:
                self.remove_dock_widget(dock)
                return True
        return False

    # Remove the _handle_tab_drag_event method as we've integrated its functionality directly into eventFilter

    def _undock_tab(self, tab_text: str) -> bool:
        """
        Undock a tab by its text, making it a floating window.

        Args:
            tab_text: The text of the tab to undock

        Returns:
            True if the tab was found and undocked, False otherwise
        """
        for dock in self._main_window.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                # Get siblings before removal
                siblings = self._main_window.tabifiedDockWidgets(dock)

                # Remove and re-add the dock
                self._main_window.removeDockWidget(dock)
                self._main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

                # Make it floating
                dock.setFloating(True)
                dock.show()

                # Update title bars for all affected docks (including the undocked one)
                for d in siblings + [dock]:
                    self._update_title_bar_for_dock(d)

                return True
        return False

    def _handle_dock_top_level_changed(self, dock: QDockWidget, floating: bool) -> None:
        """
        Handle the topLevelChanged signal from a dock widget.

        Args:
            dock: The dock widget that changed
            floating: Whether the dock is now floating
        """
        logger.debug(f"Dock '{dock.windowTitle()}' topLevelChanged: floating={floating}")
        self._update_title_bars_for_tab_group(dock)

    def _handle_dock_location_changed(self, dock: QDockWidget, area: Qt.DockWidgetArea) -> None:
        """
        Handle the dockLocationChanged signal from a dock widget.

        Args:
            dock: The dock widget that changed
            area: The new dock area
        """
        logger.debug(f"Dock '{dock.windowTitle()}' dockLocationChanged: area={area}")
        self._update_title_bars_for_tab_group(dock)

    def _is_dock_tabified(self, dock: QDockWidget) -> bool:
        """
        Check if a dock widget is part of a tab group.

        Args:
            dock: The QDockWidget to check

        Returns:
            True if the dock is tabified with any other dock, False otherwise
        """
        tabified_docks = self._main_window.tabifiedDockWidgets(dock)
        is_tabified = any(other in tabified_docks for other in self._main_window.findChildren(QDockWidget) if other is not dock)
        logger.debug(f"Dock '{dock.windowTitle()}' is tabified: {is_tabified}")
        return is_tabified

    def _update_title_bar_for_dock(self, dock: QDockWidget) -> None:
        """
        Update the title bar visibility for a dock based on its tabification state.

        Args:
            dock: The QDockWidget to update
        """
        logger.debug(f"Updating title bar for dock '{dock.windowTitle()}'")
        logger.debug(f"  - isFloating: {dock.isFloating()}")
        logger.debug(f"  - isVisible: {dock.isVisible()}")
        logger.debug(f"  - features: {dock.features()}")
        logger.debug(f"  - allowedAreas: {dock.allowedAreas()}")

        # Check if the dock is tabified with any other dock
        is_tabified = any(other in self._main_window.tabifiedDockWidgets(dock) for other in self._main_window.findChildren(QDockWidget) if other is not dock)
        logger.debug(f"Dock '{dock.windowTitle()}' is tabified: {is_tabified}")

        if is_tabified:
            # If the dock is tabified, hide the title bar
            logger.debug(f"  - Hiding title bar (tabified)")
            self._hide_dock_title_bar(dock)
        else:
            # Otherwise, show the title bar
            logger.debug(f"  - Showing title bar (normal)")
            self._show_dock_title_bar(dock)

    def _update_title_bars_for_tab_group(self, dock: QDockWidget) -> None:
        """
        Update title bars for a dock and all docks tabified with it.

        Args:
            dock: The QDockWidget that is part of the tab group
        """
        logger.debug(f"Updating title bars for tab group of dock '{dock.windowTitle()}'")
        tab_group = self._main_window.tabifiedDockWidgets(dock)
        logger.debug(f"  - Tab group size: {len(tab_group)}")

        if dock not in tab_group:
            tab_group.append(dock)
            logger.debug(f"  - Added dock to tab group, new size: {len(tab_group)}")

        for other_dock in tab_group:
            logger.debug(f"  - Updating title bar for dock in group: '{other_dock.windowTitle()}'")
            self._update_title_bar_for_dock(other_dock)

    def _hide_dock_title_bar(self, dock: QDockWidget) -> None:
        """
        Hide the title bar of a dock widget.

        Args:
            dock: The QDockWidget to modify
        """
        logger.debug(f"Hiding title bar for dock '{dock.windowTitle()}'")
        hidden = QWidget()
        hidden.setFixedHeight(0)
        dock.setTitleBarWidget(hidden)

    def _show_dock_title_bar(self, dock: QDockWidget) -> None:
        """
        Restore the default title bar of a dock widget.

        Args:
            dock: The QDockWidget to modify
        """
        logger.debug(f"Showing title bar for dock '{dock.windowTitle()}'")
        # First set a temporary widget
        temp_widget = QWidget()
        dock.setTitleBarWidget(temp_widget)

        # Then restore the default title bar
        # In Qt, passing None to setTitleBarWidget restores the default title bar
        # This is a valid Qt API call even though Pylance doesn't recognize it
        # We need to use type: ignore because Pylance doesn't understand this Qt behavior
        dock.setTitleBarWidget(None)  # type: ignore
