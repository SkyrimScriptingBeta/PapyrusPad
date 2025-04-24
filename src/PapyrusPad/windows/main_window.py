from typing import override
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QMainWindow

from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.menus.file_menu import FileMenu
from PapyrusPad.menus.help_menu import HelpMenu
from PapyrusPad.widgets.editor_widget import EditorWidget
from qt_helpers.dock_manager import IDockManager, get_dock_manager
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make, make_later
from qt_helpers.window import window

# TODO IDockWidget and DockWidget which wrap QDockWidget and IDockManager


@window("main_window", title="PapyrusPad")
class MainWindow(QMainWindow, IWidget):
    dock_manager: IDockManager = make_later(IDockManager)

    file_menu: FileMenu = make(FileMenu)
    help_menu: HelpMenu = make(HelpMenu)

    @override
    def setup(self, document_collection: IDocumentCollection = Depends[IDocumentCollection]):
        self.resize(1024, 1024)
        self.dock_manager = get_dock_manager(self)

        # Add editor for all of the editor documents
        for document in document_collection.list_documents():
            self._add_editor_for_document(document)

        # If there is only one document, hide its draggable docking title bar
        self._update_titlebar_visibility()

        # Listen for document added events
        document_collection.add_document_added_listener(self._on_document_added)

    def _add_editor_for_document(self, document: IDocument) -> None:
        self.dock_manager.dock(EditorWidget(document), Qt.DockWidgetArea.RightDockWidgetArea)

    def _update_titlebar_visibility(self) -> None:
        """Update the visibility of the titlebar based on the number of docked widgets."""
        docked_widgets = self.dock_manager.get_docked_widgets()
        if len(docked_widgets) == 1:
            if dock_widget := docked_widgets[0]:
                self.dock_manager.hide_titlebar(dock_widget)

    def _on_document_added(self, document: IDocument) -> None:
        self._add_editor_for_document(document)
        self._update_titlebar_visibility()
