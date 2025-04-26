from dataclasses import dataclass, field
from pathlib import Path
from typing import override, Callable, List, Union

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.text_document import TextDocument
from qt_helpers.observable import Observable, ObservableListBase


def _empty_listener_list() -> List[Callable[[IDocument], None]]:
    return []


def _empty_id_listener_list() -> List[Callable[[str], None]]:
    return []


@dataclass
class DocumentCollection(ObservableListBase[IDocument], IDocumentCollection):
    """Implementation of IDocumentCollection that manages documents in memory."""

    _active_document_id_field: Observable[str | None] = field(default_factory=lambda: Observable(None))
    _document_added_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)
    _removing_document_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)
    _removed_document_listeners: List[Callable[[str], None]] = field(default_factory=_empty_id_listener_list)
    _current_index: int = field(default=0, init=False)

    def __init__(self):
        """Initialize an empty document collection."""
        super().__init__([])
        self._active_document_id_field = Observable[str | None](None)
        self._document_added_listeners = []
        self._removing_document_listeners = []
        self._removed_document_listeners = []
        self._current_index = 0

        # Connect the observable list events to the legacy listeners
        self.on_add(self._handle_document_added)
        self.on_remove(self._handle_document_removed)
        self.on_clear(self._handle_documents_cleared)

    def _handle_document_added(self, document: IDocument, index: int) -> None:
        """Handle a document being added to the collection."""
        for listener in self._document_added_listeners:
            listener(document)

    def _handle_document_removed(self, document: IDocument, index: int) -> None:
        """Handle a document being removed from the collection."""
        # We don't call the removing listeners here because they need to be called
        # before the document is removed, and this is called after the document is removed.
        # The removing listeners are called in the remove_by_id method.
        for listener in self._removed_document_listeners:
            listener(document.id)

    def _handle_documents_cleared(self, documents: List[IDocument]) -> None:
        """Handle all documents being cleared from the collection."""
        # Call removing listeners for each document
        for document in documents:
            for listener in self._removing_document_listeners:
                listener(document)

        # Call removed listeners for each document
        for document in documents:
            for listener in self._removed_document_listeners:
                listener(document.id)

    @property
    @override
    def active_document_id(self) -> Observable[str | None]:
        """
        Get the observable field for the active document ID.

        This allows binding to changes in the active document.
        """
        return self._active_document_id_field

    @property
    @override
    def active_document(self) -> IDocument | None:
        """
        Get the currently active document, if any.

        This is a convenience property that returns the document with the active ID.
        """
        active_id = self._active_document_id_field.get()
        if not active_id:
            return None
        return self.get_document(active_id)

    @override
    def get_document_by_index(self, index: int) -> IDocument | None:
        """
        Get the document at the specified index.

        Args:
            index: The index of the document to get (0-based)

        Returns:
            The document at the specified index, or None if the index is out of range
        """
        if index < 0 or index >= len(self._items):
            return None
        return self._items[index]

    @override
    def get_document_id_by_index(self, index: int) -> str | None:
        """
        Get the ID of the document at the specified index.

        Args:
            index: The index of the document to get (0-based)

        Returns:
            The ID of the document at the specified index, or None if the index is out of range
        """
        document = self.get_document_by_index(index)
        if not document:
            return None
        return document.id

    @override
    def remove_at_index(self, index: int) -> bool:
        """
        Remove the document at the specified index.

        Args:
            index: The index of the document to remove (0-based)

        Returns:
            True if a document was removed, False if the index was out of range
        """
        document_id = self.get_document_id_by_index(index)
        if not document_id:
            return False
        return self.remove_by_id(document_id)

    @override
    def list_documents(self) -> list[IDocument]:
        """All open documents, in open-tab order."""
        return self._items.copy()

    @override
    def get_document(self, document_id: str) -> IDocument | None:
        """Lookup by unique ID."""
        for doc in self._items:
            if doc.id == document_id:
                return doc
        return None

    @override
    def find_by_path(self, path: Path) -> IDocument | None:
        """Find document with a given file path."""
        for doc in self._items:
            if doc.path == path:
                return doc
        return None

    @override
    def add_or_replace(self, document: IDocument) -> None:
        """Add a new document or replace one with same ID."""
        # Remove existing document with same ID if it exists
        existing_doc = self.get_document(document.id)
        if existing_doc:
            # Remove the existing document
            index = self._items.index(existing_doc)
            self._items[index] = document

            # Manually call the document added listener since __setitem__ doesn't trigger it
            for listener in self._document_added_listeners:
                listener(document)
        else:
            self.append(document)

        # If there's no active document, make this one active
        if not self._active_document_id_field.get():
            self._active_document_id_field.set(document.id)

    @override
    def remove_by_id(self, document_id: str) -> bool:
        """Close/remove the document by ID. Returns True if found."""
        # Find the document
        document = self.get_document(document_id)
        if not document:
            return False

        # Notify listeners that a document is about to be removed
        for listener in self._removing_document_listeners:
            listener(document)

        # Remove the document
        try:
            super().remove(document)  # Use the base class remove method
        except ValueError:
            return False

        # If we removed the active document, update the active document
        if self._active_document_id_field.get() == document_id:
            # Set to the first document if available, otherwise None
            new_active_id = self._items[0].id if self._items else None
            self._active_document_id_field.set(new_active_id)

        return True

    @override
    def create(self, name: str = "Untitled", content: str = "") -> IDocument:
        """Create and add a new document with a random ID."""
        document = TextDocument()
        document.name = name
        document.content = content
        self.add_or_replace(document)
        return document

    @override
    def is_path_open(self, path: Path) -> bool:
        """Check if a document with this path is already open."""
        return self.find_by_path(path) is not None

    @override
    def add_document_added_listener(self, listener: Callable[[IDocument], None]) -> None:
        """
        Add a listener that will be called when a document is added to the collection.

        Args:
            listener: A function that takes an IDocument parameter
        """
        self._document_added_listeners.append(listener)

    @override
    def add_removing_document_listener(self, listener: Callable[[IDocument], None]) -> None:
        """
        Add a listener that will be called BEFORE a document is removed from the collection.

        This allows performing cleanup or saving operations before the document is removed.

        Args:
            listener: A function that takes an IDocument parameter (the document about to be removed)
        """
        self._removing_document_listeners.append(listener)

    @override
    def add_removed_document_listener(self, listener: Callable[[str], None]) -> None:
        """
        Add a listener that will be called AFTER a document is removed from the collection.

        Since the document might already be destroyed, this listener receives the document ID
        rather than the document itself.

        Args:
            listener: A function that takes a str parameter (the ID of the removed document)
        """
        self._removed_document_listeners.append(listener)

    # IObservableList methods implementation
    def __next__(self) -> IDocument:
        """
        Return the next document in the collection.

        This allows using next() on the collection to get the next document.
        Raises StopIteration when there are no more documents.
        """
        if self._current_index >= len(self._items):
            raise StopIteration
        document = self._items[self._current_index]
        self._current_index += 1
        return document

    # Compatibility method for the old API
    def remove(self, item: Union[IDocument, str]) -> bool:
        """
        Remove a document from the collection.

        This is a compatibility method that supports both the old API (remove by ID)
        and the new API (remove by document object).

        Args:
            item: The document or document ID to remove

        Returns:
            True if the document was removed, False otherwise
        """
        if isinstance(item, str):
            # Old API: remove by ID
            return self.remove_by_id(item)
        else:
            # New API: remove by document object
            try:
                super().remove(item)  # Use the base class remove method
                return True
            except ValueError:
                return False
