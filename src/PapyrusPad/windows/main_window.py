from typing import override
from PySide6.QtCore import QEvent, QObject
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDockWidget, QMainWindow

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

    editor_dock_by_document_id: dict[str, QDockWidget | None] = make(dict[str, QDockWidget | None])

    file_menu: FileMenu = make(FileMenu)
    help_menu: HelpMenu = make(HelpMenu)

    @override
    def setup(self, document_collection: IDocumentCollection = Depends[IDocumentCollection]):
        self.resize(1024, 1024)
        self.dock_manager = get_dock_manager(self)
        self.dock_manager.on_tab_close(self._on_tab_close)

        # Add editor for all of the editor documents
        for document in document_collection.list_documents():
            self._add_editor_for_document(document)

        # If there is only one document, hide its draggable docking title bar
        self._update_titlebar_visibility()

        # Listen for document added events
        document_collection.add_document_added_listener(self._on_document_added)
        document_collection.active_document_id.bind(self._on_active_document_changed)

    def _add_editor_for_document(self, document: IDocument) -> None:
        dock_widget = self.dock_manager.dock(EditorWidget(document), Qt.DockWidgetArea.RightDockWidgetArea)
        self.editor_dock_by_document_id[document.id] = dock_widget
        if len(self.dock_manager.get_docked_widgets()) > 1:
            print(f"TABBIFYING dock widget: {dock_widget.windowTitle()}")
            self.tabifyDockWidget(self.dock_manager.get_docked_widgets()[0], dock_widget)

    def _update_titlebar_visibility(self) -> None:
        """Update the visibility of the titlebar based on the number of docked widgets."""
        docked_widgets = self.dock_manager.get_docked_widgets()
        if len(docked_widgets) == 1:
            if dock_widget := docked_widgets[0]:
                self.dock_manager.hide_titlebar(dock_widget)

    def _on_document_added(self, document: IDocument) -> None:
        self._add_editor_for_document(document)
        self._update_titlebar_visibility()

    def _on_active_document_changed(self, document_id: str | None) -> None:
        if document_id is None:
            return

        # Show the editor for the active document and hide others
        editor_dock = self.editor_dock_by_document_id[document_id]

        # Update the titlebar visibility
        self._update_titlebar_visibility()

        # Need to switch the active tabbified dock widget to the active document
        if editor_dock is not None:
            editor_dock.show()
            editor_dock.raise_

    def _on_tab_close(self, index: int, document_collection: IDocumentCollection = Depends[IDocumentCollection]) -> None:
        if index < 0 or index >= len(document_collection.list_documents()):
            return

        # document = document_collection.get

    @override
    def event(self, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().event(event)

    @override
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        self.dock_manager.on_event(event)
        return super().eventFilter(obj, event)
