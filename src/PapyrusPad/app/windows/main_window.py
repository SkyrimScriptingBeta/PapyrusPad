from dataclasses import field
from typing import List, override
from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QDockWidget, QLabel, QMainWindow, QVBoxLayout, QWidget

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.dock_manager import DockManager, DockWidgetLocation, IDockManager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make_later
from qt_helpers.make_widget import make_widget
from qt_helpers.window import window


class PanelWidget(QWidget):
    """A simple panel widget similar to the one in ide_window_example.py."""

    def __init__(self, title: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h3>{title}</h3>"))
        layout.addStretch()
        self.setLayout(layout)


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    # Create editor widgets
    editor_main: EditorWidget = make_widget(EditorWidget, ["editor"], "main.cpp")
    editor_engine: EditorWidget = make_widget(EditorWidget, ["editor"], "engine.cpp")
    editor_ui: EditorWidget = make_widget(EditorWidget, ["editor"], "ui.cpp")

    # Create panel widgets
    left_panel: QWidget = make_widget(PanelWidget, [], "Left Panel")
    right_panel: QWidget = make_widget(PanelWidget, [], "Right Panel")
    top_panel: QWidget = make_widget(PanelWidget, [], "Top Panel")
    bottom_panel: QWidget = make_widget(PanelWidget, [], "Bottom Panel")

    dock_manager: IDockManager = make_later(DockManager)
    editor_docks: List[QDockWidget] = field(default_factory=lambda: [])

    @override
    def setup(self):
        self.resize(2048, 1152)
        self.dock_manager = DockManager(self)

        # Add panel docks
        top_dock = self.dock_manager.add_dock_widget(self.top_panel, "Top Panel", DockWidgetLocation.TOP)
        bottom_dock = self.dock_manager.add_dock_widget(self.bottom_panel, "Bottom Panel", DockWidgetLocation.BOTTOM)
        left_dock = self.dock_manager.add_dock_widget(self.left_panel, "Left Panel", DockWidgetLocation.LEFT)

        # Add main editor dock
        main_editor_dock = self.dock_manager.add_dock_widget(self.editor_main, "main.cpp", DockWidgetLocation.RIGHT)
        self.editor_docks.append(main_editor_dock)

        # Add right panel dock
        right_dock = self.dock_manager.add_dock_widget(self.right_panel, "Right Panel", DockWidgetLocation.RIGHT)

        # Split the main editor and right panel
        self.dock_manager.split_dock_widget(main_editor_dock, right_dock, Qt.Orientation.Horizontal)

        # Add engine and ui editor docks and tabify them with the main editor
        engine_dock = self.dock_manager.add_dock_widget(self.editor_engine, "engine.cpp", DockWidgetLocation.RIGHT)
        ui_dock = self.dock_manager.add_dock_widget(self.editor_ui, "ui.cpp", DockWidgetLocation.RIGHT)

        # Tabify the editor docks
        self.dock_manager.tabify_dock_widgets(main_editor_dock, engine_dock)
        self.dock_manager.tabify_dock_widgets(main_editor_dock, ui_dock)

        # Add the engine and ui docks to our list
        self.editor_docks.append(engine_dock)
        self.editor_docks.append(ui_dock)

        # Raise the main editor dock to the top of the tab stack
        self.dock_manager.raise_dock_widget(main_editor_dock)

        # Resize the docks to match the original example
        self.dock_manager.resize_docks(
            [left_dock, main_editor_dock, right_dock],
            [200, 1648, 200],
            Qt.Orientation.Horizontal,
        )
        self.dock_manager.resize_docks(
            [top_dock, main_editor_dock, bottom_dock],
            [100, 902, 150],
            Qt.Orientation.Vertical,
        )

    @override
    def event(self, event: QEvent) -> bool:
        """
        Handle events for the main window.

        This is called before eventFilter and is used to catch layout changes
        to customize tab bars, similar to the original example.

        Args:
            event: The event to handle

        Returns:
            True if the event was handled, False otherwise
        """
        if event.type() == QEvent.Type.LayoutRequest:
            # This is similar to the _install_tab_features method in the original example
            # It ensures tab bars are customized immediately after layout changes
            self.dock_manager.customize_tab_bars()

        # Always call the parent class's event method
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        """
        Filter events for objects being watched by this window.

        Args:
            watched: The object that sent the event
            event: The event to filter

        Returns:
            True if the event was handled and should be filtered out,
            False if the event should be processed normally
        """
        # Let the dock manager handle the event, but don't filter it out
        # This ensures that Qt's native drag-and-drop functionality works properly
        self.dock_manager.handle_event_filter(watched, event)

        # Always let the parent class handle the event
        return super().eventFilter(watched, event)
