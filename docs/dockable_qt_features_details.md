# Qt Docking Features: Implementation Guide

This document provides a comprehensive guide to implementing advanced docking features in PySide6/PyQt applications, based on the analysis of the `hello_sidebars_etc/app.py` example.

## Table of Contents

1. [Feature Overview](#feature-overview)
2. [Implementation Approaches](#implementation-approaches)
3. [Detailed Feature Explanations](#detailed-feature-explanations)
   - [Closeable Tabs](#closeable-tabs)
   - [Tabs on Top](#tabs-on-top)
   - [Drag to Undock](#drag-to-undock)
   - [Title Bar Management](#title-bar-management)
4. [Implementation Options](#implementation-options)
   - [Helper Functions](#helper-functions)
   - [Mixin Classes](#mixin-classes)
   - [Comprehensive Solution](#comprehensive-solution)
5. [Integration Guide](#integration-guide)
6. [Best Practices](#best-practices)

## Feature Overview

The example application demonstrates several advanced docking features:

1. **Closeable Tabs**: Tabs have close buttons and can be removed from the UI
2. **Tabs on Top**: All tab bars are positioned at the top of their dock areas
3. **Drag to Undock**: Tabs can be dragged away to create floating windows
4. **Title Bar Management**: Title bars are hidden for tabbed widgets to create a cleaner interface

These features enhance the user experience in IDE-like applications by providing intuitive ways to manage multiple docked widgets.

## Implementation Approaches

There are three main approaches to implementing these features:

1. **Helper Functions**: Standalone functions that perform discrete operations on widgets
2. **Mixin Classes**: Classes that can be mixed into a QMainWindow to add specific functionality
3. **Comprehensive Solution**: A complete mixin that implements all features together

The best approach depends on your specific needs:
- Use helper functions for simple operations or when you need maximum flexibility
- Use mixins when you want to add a complete set of features to different window classes
- Use the comprehensive solution when you want all features with minimal integration effort

## Detailed Feature Explanations

### Closeable Tabs

Tabs are made closeable by setting the `tabsClosable` property on QTabBar instances and connecting to the `tabCloseRequested` signal.

**Key implementation details:**
```python
# Find all tab bars in the window
for tab_bar in self.findChildren(QTabBar):
    # Make tabs closeable
    tab_bar.setTabsClosable(True)
    # Connect to close handler
    tab_bar.tabCloseRequested.connect(self._handle_tab_close)

# Handle tab close requests
def _handle_tab_close(self, index: int) -> None:
    tab_bar = self.sender()
    if isinstance(tab_bar, QTabBar):
        tab_text = tab_bar.tabText(index)
        for dock in self.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                self.removeDockWidget(dock)
                dock.deleteLater()
                break
```

**Events to handle:**
- `tabCloseRequested` signal from QTabBar

### Tabs on Top

Tabs are positioned at the top of dock areas using the `setTabPosition` method.

**Key implementation details:**
```python
# Set tab position to North (top) for all dock areas
self.setTabPosition(
    Qt.DockWidgetArea.AllDockWidgetAreas, 
    QTabWidget.TabPosition.North
)
```

**Events to handle:** None (one-time setup)

### Drag to Undock

Tabs can be dragged away from the tab bar to create floating windows. This is implemented using event filtering to track mouse movements.

**Key implementation details:**
```python
# Install event filter on tab bars
for tab_bar in self.findChildren(QTabBar):
    tab_bar.installEventFilter(self)

# Event filter implementation
def eventFilter(self, watched: QObject, event: QEvent) -> bool:
    if isinstance(watched, QTabBar):
        tab_bar = watched
        if event.type() == QEvent.Type.MouseButtonPress:
            # Start tracking potential drag
            mouse_event = cast(QMouseEvent, event)
            self._drag_tab_start_pos = mouse_event.pos()
            self._drag_tab_index = tab_bar.tabAt(self._drag_tab_start_pos)
            if self._drag_tab_index >= 0:
                self._drag_tab_text = tab_bar.tabText(self._drag_tab_index)
        elif (
            event.type() == QEvent.Type.MouseMove
            and self._drag_tab_text is not None
        ):
            # Check if mouse has moved outside tab bar (with margin)
            mouse_event = cast(QMouseEvent, event)
            margin = 50
            padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
            if not padded.contains(mouse_event.pos()):
                self._undock_tab(self._drag_tab_text)
                self._drag_tab_text = None
        elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
            # Cancel drag tracking
            self._drag_tab_text = None
    return super().eventFilter(watched, event)

# Undock implementation
def _undock_tab(self, tab_text: str) -> None:
    for dock in self.findChildren(QDockWidget):
        if dock.windowTitle() == tab_text:
            siblings = self.tabifiedDockWidgets(dock)
            self.removeDockWidget(dock)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
            dock.setFloating(True)
            dock.show()
            # Update title bars
            for d in siblings + [dock]:
                self._update_title_bar_for(d)
            break
```

**Events to handle:**
- `QEvent.Type.MouseButtonPress` - Start tracking potential drag
- `QEvent.Type.MouseMove` - Check if mouse has moved outside tab bar
- `QEvent.Type.MouseButtonRelease` - Cancel drag tracking
- `QEvent.Type.Leave` - Cancel drag tracking when mouse leaves widget

### Title Bar Management

Title bars are hidden for widgets that are part of a tab group to create a cleaner interface.

**Key implementation details:**
```python
def _update_title_bar_for(self, dock: QDockWidget) -> None:
    tab_group = self.tabifiedDockWidgets(dock)
    if dock not in tab_group:
        tab_group.append(dock)

    for w in tab_group:
        if not isinstance(w, QDockWidget):
            continue

        is_tabbified = any(
            other in self.tabifiedDockWidgets(w)
            for other in self.findChildren(QDockWidget)
            if other is not w
        )

        if is_tabbified:
            current = w.titleBarWidget()
            if current is None or current.sizeHint().height() > 0:
                hidden = QWidget()
                hidden.setFixedHeight(0)
                w.setTitleBarWidget(hidden)
        else:
            # Restore normal title bar
            temp_widget = QWidget()
            w.setTitleBarWidget(temp_widget)
            w.setTitleBarWidget(None)
```

**Events to handle:**
- `topLevelChanged` signal from QDockWidget - When dock becomes floating/docked
- `dockLocationChanged` signal from QDockWidget - When dock moves to different area

## Implementation Options

### Helper Functions

Helper functions provide discrete operations that can be used independently:

```python
def customize_tab_bar(tab_bar: QTabBar, close_handler: Callable[[int], None]) -> bool:
    """Apply standard customizations to a tab bar."""
    if not tab_bar.property("_customized"):
        tab_bar.setTabsClosable(True)
        tab_bar.setMovable(True)
        tab_bar.tabCloseRequested.connect(close_handler)
        tab_bar.setProperty("_customized", True)
        return True
    return False

def set_tabs_position_north(main_window: QMainWindow) -> None:
    """Set all tab positions to North (top)."""
    main_window.setTabPosition(
        Qt.DockWidgetArea.AllDockWidgetAreas, 
        QTabWidget.TabPosition.North
    )

def hide_dock_title_bar(dock: QDockWidget) -> None:
    """Hide the title bar of a dock widget."""
    hidden = QWidget()
    hidden.setFixedHeight(0)
    dock.setTitleBarWidget(hidden)

def show_dock_title_bar(dock: QDockWidget) -> None:
    """Restore the default title bar of a dock widget."""
    temp_widget = QWidget()
    dock.setTitleBarWidget(temp_widget)
    dock.setTitleBarWidget(None)

def is_dock_tabified(dock: QDockWidget, main_window: QMainWindow) -> bool:
    """Check if a dock widget is part of a tab group."""
    return any(
        other in main_window.tabifiedDockWidgets(dock)
        for other in main_window.findChildren(QDockWidget)
        if other is not dock
    )

def remove_dock_by_title(main_window: QMainWindow, title: str) -> bool:
    """Find and remove a dock widget by its title."""
    for dock in main_window.findChildren(QDockWidget):
        if dock.windowTitle() == title:
            main_window.removeDockWidget(dock)
            dock.deleteLater()
            return True
    return False
```

### Mixin Classes

Mixin classes provide focused functionality that can be added to a QMainWindow:

```python
class TabFeaturesMixin:
    """Mixin that adds tab customization features to a QMainWindow."""
    
    def setup_tab_features(self) -> None:
        """Set up tab features."""
        self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)
        self._install_tab_features()
    
    def _install_tab_features(self) -> None:
        """Find and customize all tab bars."""
        for tab_bar in self.findChildren(QTabBar):
            if not tab_bar.property("_customized"):
                tab_bar.setTabsClosable(True)
                tab_bar.setMovable(True)
                tab_bar.tabCloseRequested.connect(self._handle_tab_close)
                tab_bar.setProperty("_customized", True)
    
    def _handle_tab_close(self, index: int) -> None:
        """Handle tab close requests."""
        tab_bar = self.sender()
        if isinstance(tab_bar, QTabBar):
            tab_text = tab_bar.tabText(index)
            for dock in self.findChildren(QDockWidget):
                if dock.windowTitle() == tab_text:
                    self.removeDockWidget(dock)
                    dock.deleteLater()
                    break
    
    def event(self, event: QEvent) -> bool:
        """Detect layout changes to find new tab bars."""
        if event.type() == QEvent.Type.LayoutRequest:
            self._install_tab_features()
        return super().event(event)


class TabDragUndockMixin:
    """Mixin that adds drag-to-undock functionality for tabs."""
    
    def __init__(self) -> None:
        self._drag_tab_start_pos = QPoint()
        self._drag_tab_index = -1
        self._drag_tab_text = None
    
    def setup_tab_undocking(self) -> None:
        """Install event filters on all tab bars."""
        for tab_bar in self.findChildren(QTabBar):
            tab_bar.installEventFilter(self)
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Handle tab drag events."""
        if isinstance(watched, QTabBar):
            tab_bar = watched
            if event.type() == QEvent.Type.MouseButtonPress:
                mouse_event = cast(QMouseEvent, event)
                self._drag_tab_start_pos = mouse_event.pos()
                self._drag_tab_index = tab_bar.tabAt(self._drag_tab_start_pos)
                if self._drag_tab_index >= 0:
                    self._drag_tab_text = tab_bar.tabText(self._drag_tab_index)
            elif (
                event.type() == QEvent.Type.MouseMove
                and self._drag_tab_text is not None
            ):
                mouse_event = cast(QMouseEvent, event)
                margin = 50
                padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
                if not padded.contains(mouse_event.pos()):
                    self._undock_tab(self._drag_tab_text)
                    self._drag_tab_text = None
            elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
                self._drag_tab_text = None
        return super().eventFilter(watched, event)
    
    def _undock_tab(self, tab_text: str) -> None:
        """Undock a tab by its text."""
        for dock in self.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                siblings = self.tabifiedDockWidgets(dock)
                self.removeDockWidget(dock)
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                dock.setFloating(True)
                dock.show()
                break


class TitleBarManagerMixin:
    """Mixin that manages dock widget title bars based on tab state."""
    
    def setup_title_bar_management(self) -> None:
        """Connect signals for all dock widgets."""
        for dock in self.findChildren(QDockWidget):
            self._connect_dock_signals(dock)
    
    def _connect_dock_signals(self, dock: QDockWidget) -> None:
        """Connect signals for a dock widget."""
        dock.topLevelChanged.connect(lambda floating: self._update_title_bar_for(dock))
        dock.dockLocationChanged.connect(lambda area: self._update_title_bar_for(dock))
    
    def _update_title_bar_for(self, dock: QDockWidget) -> None:
        """Update title bar visibility based on tabification state."""
        tab_group = self.tabifiedDockWidgets(dock)
        if dock not in tab_group:
            tab_group.append(dock)

        for w in tab_group:
            if not isinstance(w, QDockWidget):
                continue

            is_tabbified = any(
                other in self.tabifiedDockWidgets(w)
                for other in self.findChildren(QDockWidget)
                if other is not w
            )

            if is_tabbified:
                current = w.titleBarWidget()
                if current is None or current.sizeHint().height() > 0:
                    hidden = QWidget()
                    hidden.setFixedHeight(0)
                    w.setTitleBarWidget(hidden)
            else:
                temp_widget = QWidget()
                w.setTitleBarWidget(temp_widget)
                w.setTitleBarWidget(None)
```

### Comprehensive Solution

A comprehensive mixin that implements all features together:

```python
from typing import cast, Optional, List
from PySide6.QtWidgets import QMainWindow, QDockWidget, QTabBar, QWidget
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import QEvent, Qt, QPoint, QObject, QTabWidget


class AdvancedDockingFeaturesMixin:
    """
    A comprehensive mixin that adds advanced docking features to a QMainWindow.
    
    Features:
    - Closeable tabs
    - Tabs positioned at the top
    - Drag-to-undock functionality
    - Automatic title bar management for tabbed widgets
    
    Usage:
    ```python
    class MyMainWindow(QMainWindow, AdvancedDockingFeaturesMixin):
        def __init__(self):
            QMainWindow.__init__(self)
            AdvancedDockingFeaturesMixin.__init__(self)
            
            # Your initialization code
            
            # Set up docking features
            self.setup_docking_features()
    ```
    """
    
    def __init__(self) -> None:
        # Initialize tracking variables for tab dragging
        self._drag_tab_start_pos: QPoint = QPoint()
        self._drag_tab_index: int = -1
        self._drag_tab_text: Optional[str] = None
    
    def setup_docking_features(self) -> None:
        """
        Set up all docking features.
        Call this method after initializing your main window.
        """
        # Enable dock nesting
        self.setDockNestingEnabled(True)
        
        # Set tab position to top
        self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)
        
        # Connect signals for existing dock widgets
        for dock in self.findChildren(QDockWidget):
            self._connect_dock_signals(dock)
        
        # Initial tab feature setup
        self._install_tab_features()
    
    def _connect_dock_signals(self, dock: QDockWidget) -> None:
        """Connect signals for a dock widget."""
        dock.topLevelChanged.connect(lambda floating: self._update_title_bar_for(dock))
        dock.dockLocationChanged.connect(lambda area: self._update_title_bar_for(dock))
    
    def event(self, event: QEvent) -> bool:
        """Detect layout changes to find new tab bars."""
        if event.type() == QEvent.Type.LayoutRequest:
            self._install_tab_features()
        return super().event(event)
    
    def _install_tab_features(self) -> None:
        """Find and customize all tab bars."""
        for tab_bar in self.findChildren(QTabBar):
            if not tab_bar.property("_customized"):
                tab_bar.setTabsClosable(True)
                tab_bar.setMovable(True)
                tab_bar.tabCloseRequested.connect(self._handle_tab_close)
                tab_bar.installEventFilter(self)
                tab_bar.setProperty("_customized", True)
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """Handle tab drag events."""
        if isinstance(watched, QTabBar):
            tab_bar = watched
            if event.type() == QEvent.Type.MouseButtonPress:
                mouse_event = cast(QMouseEvent, event)
                self._drag_tab_start_pos = mouse_event.pos()
                self._drag_tab_index = tab_bar.tabAt(self._drag_tab_start_pos)
                if self._drag_tab_index >= 0:
                    self._drag_tab_text = tab_bar.tabText(self._drag_tab_index)
            elif (
                event.type() == QEvent.Type.MouseMove
                and self._drag_tab_text is not None
            ):
                mouse_event = cast(QMouseEvent, event)
                margin = 50
                padded = tab_bar.rect().adjusted(-margin, -margin, margin, margin)
                if not padded.contains(mouse_event.pos()):
                    self._undock_tab(self._drag_tab_text)
                    self._drag_tab_text = None
            elif event.type() in {QEvent.Type.MouseButtonRelease, QEvent.Type.Leave}:
                self._drag_tab_text = None
        return super().eventFilter(watched, event)
    
    def _handle_tab_close(self, index: int) -> None:
        """Handle tab close requests."""
        tab_bar = self.sender()
        if isinstance(tab_bar, QTabBar):
            tab_text = tab_bar.tabText(index)
            for dock in self.findChildren(QDockWidget):
                if dock.windowTitle() == tab_text:
                    self.removeDockWidget(dock)
                    dock.deleteLater()
                    break
    
    def _undock_tab(self, tab_text: str) -> None:
        """Undock a tab by its text."""
        for dock in self.findChildren(QDockWidget):
            if dock.windowTitle() == tab_text:
                siblings = self.tabifiedDockWidgets(dock)
                self.removeDockWidget(dock)
                self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
                dock.setFloating(True)
                dock.show()
                
                # Update title bars for all affected docks
                for d in siblings + [dock]:
                    self._update_title_bar_for(d)
                break
    
    def _update_title_bar_for(self, dock: QDockWidget) -> None:
        """Update title bar visibility based on tabification state."""
        tab_group = self.tabifiedDockWidgets(dock)
        if dock not in tab_group:
            tab_group.append(dock)

        for w in tab_group:
            if not isinstance(w, QDockWidget):
                continue

            is_tabbified = any(
                other in self.tabifiedDockWidgets(w)
                for other in self.findChildren(QDockWidget)
                if other is not w
            )

            if is_tabbified:
                current = w.titleBarWidget()
                if current is None or current.sizeHint().height() > 0:
                    hidden = QWidget()
                    hidden.setFixedHeight(0)
                    w.setTitleBarWidget(hidden)
            else:
                temp_widget = QWidget()
                w.setTitleBarWidget(temp_widget)
                w.setTitleBarWidget(None)
```

## Integration Guide

### Using Helper Functions

```python
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up tab position
        set_tabs_position_north(self)
        
        # Set up event handling
        self.event_original = self.event
        self.event = self.custom_event
        
        # Initialize dock widgets
        # ...
    
    def custom_event(self, event):
        if event.type() == QEvent.Type.LayoutRequest:
            self.customize_tabs()
        return self.event_original(event)
    
    def customize_tabs(self):
        for tab_bar in self.findChildren(QTabBar):
            customize_tab_bar(tab_bar, self.handle_tab_close)
    
    def handle_tab_close(self, index):
        tab_bar = self.sender()
        if isinstance(tab_bar, QTabBar):
            tab_text = tab_bar.tabText(index)
            remove_dock_by_title(self, tab_text)
```

### Using Mixin Classes

```python
class MyMainWindow(QMainWindow, TabFeaturesMixin, TabDragUndockMixin, TitleBarManagerMixin):
    def __init__(self):
        QMainWindow.__init__(self)
        TabDragUndockMixin.__init__(self)
        
        # Your initialization code
        # ...
        
        # Set up features
        self.setup_tab_features()
        self.setup_tab_undocking()
        self.setup_title_bar_management()
```

### Using Comprehensive Solution

```python
class MyMainWindow(QMainWindow, AdvancedDockingFeaturesMixin):
    def __init__(self):
        QMainWindow.__init__(self)
        AdvancedDockingFeaturesMixin.__init__(self)
        
        # Your initialization code
        # ...
        
        # Set up all docking features with one call
        self.setup_docking_features()
```

## Best Practices

1. **Match dock titles with tab text**: Ensure that dock widget titles match the text displayed in tabs for proper identification.

2. **Handle dock creation consistently**: When creating new dock widgets, apply consistent settings:
   ```python
   def create_dock(self, title, widget):
       dock = QDockWidget(title, self)
       dock.setWidget(widget)
       dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
       dock.setFeatures(
           QDockWidget.DockWidgetFeature.DockWidgetClosable
           | QDockWidget.DockWidgetFeature.DockWidgetMovable
           | QDockWidget.DockWidgetFeature.DockWidgetFloatable
       )
       self._connect_dock_signals(dock)  # If using title bar management
       return dock
   ```

3. **Consider tab bar styling**: You may want to customize the appearance of tab bars:
   ```python
   def style_tab_bar(self, tab_bar):
       tab_bar.setStyleSheet("""
           QTabBar::tab {
               background: #f0f0f0;
               border: 1px solid #c0c0c0;
               padding: 5px;
           }
           QTabBar::tab:selected {
               background: #e0e0e0;
           }
       """)
   ```

4. **Adjust drag sensitivity**: The margin for drag detection (50px in the example) can be adjusted based on your UI needs:
   ```python
   # More sensitive (smaller margin)
   margin = 20
   
   # Less sensitive (larger margin)
   margin = 100
   ```

5. **Consider dock widget lifecycle**: When removing dock widgets, ensure proper cleanup:
   ```python
   def remove_dock(self, dock):
       self.removeDockWidget(dock)
       dock.setParent(None)  # Remove parent relationship
       dock.deleteLater()    # Schedule for deletion
   ```

6. **Handle dynamic dock creation**: When creating docks dynamically, ensure signals are connected:
   ```python
   def add_new_dock(self, title, widget):
       dock = self.create_dock(title, widget)
       self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
       
       # If using the mixin approach
       self._connect_dock_signals(dock)
       
       # Ensure tab features are applied
       self._install_tab_features()
       
       return dock
