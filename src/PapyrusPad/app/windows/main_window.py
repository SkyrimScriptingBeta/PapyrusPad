from typing import override
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QKeySequence, QAction

from PapyrusPad.app.widgets.editor_widget import EditorWidget
from qt_helpers.dock_manager import IDockManager, get_dock_manager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make, make_later
from qt_helpers.window import window


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    dock_manager: IDockManager = make_later(IDockManager)
    central_widget: EditorWidget = make(EditorWidget, text="Untitled")

    @override
    def setup(self):
        self.resize(1024, 1024)
        self.dock_manager = get_dock_manager(self)
        self._create_menus()

    def _create_menus(self) -> None:
        """Create the menu bar and menu items."""
        # Create menu bar
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")

        # File > Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.setStatusTip("Open a file")
        open_action.triggered.connect(self._on_file_open)
        file_menu.addAction(open_action)

        # File > Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self._on_file_save)
        file_menu.addAction(save_action)

        # Separator
        file_menu.addSeparator()

        # File > Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menu_bar.addMenu("&View")

        # View > Toggle Project Explorer (placeholder)
        toggle_project_explorer_action = QAction("Toggle &Project Explorer", self)
        toggle_project_explorer_action.setStatusTip("Show or hide the project explorer")
        toggle_project_explorer_action.triggered.connect(self._on_toggle_project_explorer)
        view_menu.addAction(toggle_project_explorer_action)

        # View > Toggle Output Panel (placeholder)
        toggle_output_panel_action = QAction("Toggle &Output Panel", self)
        toggle_output_panel_action.setStatusTip("Show or hide the output panel")
        toggle_output_panel_action.triggered.connect(self._on_toggle_output_panel)
        view_menu.addAction(toggle_output_panel_action)

        # About menu
        about_menu = menu_bar.addMenu("&About")

        # About > About PapyrusPal
        about_action = QAction("About &PapyrusPal", self)
        about_action.setStatusTip("Show information about PapyrusPal")
        about_action.triggered.connect(self._on_about)
        about_menu.addAction(about_action)

    def _on_file_open(self) -> None:
        """Handle File > Open action."""
        print("File > Open triggered")
        # TODO: Implement file open functionality

    def _on_file_save(self) -> None:
        """Handle File > Save action."""
        print("File > Save triggered")
        # TODO: Implement file save functionality

    def _on_toggle_project_explorer(self) -> None:
        """Handle View > Toggle Project Explorer action."""
        print("View > Toggle Project Explorer triggered")
        # TODO: Implement toggle project explorer functionality

    def _on_toggle_output_panel(self) -> None:
        """Handle View > Toggle Output Panel action."""
        print("View > Toggle Output Panel triggered")
        # TODO: Implement toggle output panel functionality

    def _on_about(self) -> None:
        """Handle About > About PapyrusPal action."""
        print("About > About PapyrusPal triggered")
        # TODO: Implement about dialog

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self.dock_manager.on_eventFilter(watched, event)
        return super().eventFilter(watched, event)
