from dataclasses import dataclass, field
from pathlib import Path
from typing import override, Callable, List

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.text_document import TextDocument


def _empty_document_list() -> list[IDocument]:
    return []


def _empty_listener_list() -> List[Callable[[IDocument], None]]:
    return []


@dataclass
class DocumentCollection(IDocumentCollection):
    """Implementation of IDocumentCollection that manages documents in memory."""

    _documents: list[IDocument] = field(default_factory=_empty_document_list)
    _active_document_id: str | None = None
    _document_added_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)
    _active_document_changed_listeners: List[Callable[[IDocument], None]] = field(default_factory=_empty_listener_list)

    @override
    def __len__(self) -> int:
        """
        Return the number of documents in the collection.

        This allows using len(collection) to get the document count.
        """
        return len(self._documents)

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
    def get_active(self) -> IDocument | None:
        """Return the currently focused/active document, if any."""
        if not self._active_document_id:
            return None
        return self.get_document(self._active_document_id)

    @override
    def add_or_replace(self, document: IDocument) -> None:
        """Add a new document or replace one with same ID."""
        # Remove existing document with same ID if it exists
        self._documents = [doc for doc in self._documents if doc.id != document.id]
        # Add the new document
        self._documents.append(document)
        # If there's no active document, make this one active
        if not self._active_document_id:
            self._active_document_id = document.id

        # Notify listeners that a document was added
        for listener in self._document_added_listeners:
            listener(document)

    @override
    def remove(self, document_id: str) -> bool:
        """Close/remove the document. Returns True if found."""
        original_length = len(self._documents)
        self._documents = [doc for doc in self._documents if doc.id != document_id]

        # If we removed the active document, update the active document
        if self._active_document_id == document_id:
            self._active_document_id = self._documents[0].id if self._documents else None

        # Return True if we removed a document
        return len(self._documents) < original_length

    @override
    def set_active(self, document_id: str) -> bool:
        """Mark a document as currently active. Returns True if found."""
        document = self.get_document(document_id)
        if not document:
            return False
        self._active_document_id = document_id

        # Notify listeners that the active document changed
        for listener in self._active_document_changed_listeners:
            listener(document)

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
    def add_active_document_changed_listener(self, listener: Callable[[IDocument], None]) -> None:
        """
        Add a listener that will be called when the active document changes.

        Args:
            listener: A function that takes an IDocument parameter
        """
        self._active_document_changed_listeners.append(listener)
