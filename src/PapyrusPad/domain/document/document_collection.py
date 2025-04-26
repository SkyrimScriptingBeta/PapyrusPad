from dataclasses import dataclass, field
from pathlib import Path
from typing import override, Callable, List, Iterator

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.text_document import TextDocument
from qt_helpers.observable_field import Observable


def _empty_document_list() -> list[IDocument]:
    return []


def _empty_listener_list() -> List[Callable[[IDocument], None]]:
    return []


def _empty_id_listener_list() -> List[Callable[[str], None]]:
    return []


@dataclass
class DocumentCollection(IDocumentCollection):
    """Implementation of IDocumentCollection that manages documents in memory."""

    _documents: list[IDocument] = field(default_factory=_empty_document_list)
    _active_document_id_field: Observable[str | None] = field(default_factory=lambda: Observable(None))
    _document_added_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)
    _removing_document_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)
    _removed_document_listeners: List[Callable[[str], None]] = field(default_factory=_empty_id_listener_list)
    _current_index: int = field(default=0, init=False)

    @override
    def __len__(self) -> int:
        """
        Return the number of documents in the collection.

        This allows using len(collection) to get the document count.
        """
        return len(self._documents)

    @override
    def __iter__(self) -> Iterator[IDocument]:
        """
        Return an iterator over the documents in the collection.

        This allows iterating over the collection using for loops and other iteration tools.
        """
        self._current_index = 0
        return self

    @override
    def __next__(self) -> IDocument:
        """
        Return the next document in the collection.

        This allows using next() on the collection to get the next document.
        Raises StopIteration when there are no more documents.
        """
        if self._current_index >= len(self._documents):
            raise StopIteration
        document = self._documents[self._current_index]
        self._current_index += 1
        return document

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
        if index < 0 or index >= len(self._documents):
            return None
        return self._documents[index]

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
        return self.remove(document_id)

    @override
    def list_documents(self) -> list[IDocument]:
        """All open documents, in open-tab order."""
        return self._documents.copy()

    @override
    def get_document(self, document_id: str) -> IDocument | None:
        """Lookup by unique ID."""
        for doc in self._documents:
            if doc.id == document_id:
                return doc
        return None

    @override
    def find_by_path(self, path: Path) -> IDocument | None:
        """Find document with a given file path."""
        for doc in self._documents:
            if doc.path == path:
                return doc
        return None

    @override
    def add_or_replace(self, document: IDocument) -> None:
        """Add a new document or replace one with same ID."""
        # Remove existing document with same ID if it exists
        self._documents = [doc for doc in self._documents if doc.id != document.id]
        # Add the new document
        self._documents.append(document)
        # If there's no active document, make this one active
        if not self._active_document_id_field.get():
            self._active_document_id_field.set(document.id)

        # Notify listeners that a document was added
        for listener in self._document_added_listeners:
            listener(document)

    @override
    def remove(self, document_id: str) -> bool:
        """Close/remove the document. Returns True if found."""
        # Find the document
        document = self.get_document(document_id)
        if not document:
            return False

        # Notify listeners that a document is about to be removed
        for listener in self._removing_document_listeners:
            listener(document)

        # Remove the document
        original_length = len(self._documents)
        self._documents = [doc for doc in self._documents if doc.id != document_id]

        # If we removed the active document, update the active document
        if self._active_document_id_field.get() == document_id:
            # Set to the first document if available, otherwise None
            new_active_id = self._documents[0].id if self._documents else None
            self._active_document_id_field.set(new_active_id)

        # Notify listeners that a document was removed
        for listener in self._removed_document_listeners:
            listener(document_id)

        # Return True if we removed a document
        return len(self._documents) < original_length

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
