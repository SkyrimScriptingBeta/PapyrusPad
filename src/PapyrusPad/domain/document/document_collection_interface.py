from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Iterator, List, Union, Optional, Any, override

from PapyrusPad.domain.document.document_interface import IDocument
from qt_helpers.observable import Observable, IObservableList, ListChange


class IDocumentCollection(IObservableList[IDocument], ABC):
    """Manages all documents open in the editor."""

    @property
    @abstractmethod
    def active_document_id(self) -> Observable[str | None]:
        """
        Get the observable field for the active document ID.

        This allows binding to changes in the active document.
        """
        ...

    @property
    @abstractmethod
    def active_document(self) -> IDocument | None:
        """
        Get the currently active document, if any.

        This is a convenience property that returns the document with the active ID.
        """
        ...

    @abstractmethod
    def get_document_by_index(self, index: int) -> IDocument | None:
        """
        Get the document at the specified index.

        Args:
            index: The index of the document to get (0-based)

        Returns:
            The document at the specified index, or None if the index is out of range
        """
        ...

    @abstractmethod
    def get_document_id_by_index(self, index: int) -> str | None:
        """
        Get the ID of the document at the specified index.

        Args:
            index: The index of the document to get (0-based)

        Returns:
            The ID of the document at the specified index, or None if the index is out of range
        """
        ...

    @abstractmethod
    def remove_at_index(self, index: int) -> bool:
        """
        Remove the document at the specified index.

        Args:
            index: The index of the document to remove (0-based)

        Returns:
            True if a document was removed, False if the index was out of range
        """
        ...

    @abstractmethod
    def list_documents(self) -> list[IDocument]:
        """All open documents, in open-tab order."""
        ...

    @abstractmethod
    def get_document(self, document_id: str) -> IDocument | None:
        """Lookup by unique ID."""
        ...

    @abstractmethod
    def find_by_path(self, path: Path) -> IDocument | None:
        """Find document with a given file path."""
        ...

    @abstractmethod
    def add_or_replace(self, document: IDocument) -> None:
        """Add a new document or replace one with same ID."""
        ...

    @abstractmethod
    def remove_by_id(self, document_id: str) -> bool:
        """Close/remove the document by ID. Returns True if found."""
        ...

    @abstractmethod
    def create(self, name: str = "Untitled", content: str = "") -> IDocument:
        """Create and add a new document with a random ID."""
        ...

    @abstractmethod
    def is_path_open(self, path: Path) -> bool:
        """Check if a document with this path is already open."""
        ...

    # Legacy event methods - these will be deprecated in favor of the observable list pattern
    @abstractmethod
    def add_document_added_listener(self, listener: Callable[[IDocument], None]) -> None:
        """
        Add a listener that will be called when a document is added to the collection.

        Args:
            listener: A function that takes an IDocument parameter
        """
        ...

    @abstractmethod
    def add_removing_document_listener(self, listener: Callable[[IDocument], None]) -> None:
        """
        Add a listener that will be called BEFORE a document is removed from the collection.

        This allows performing cleanup or saving operations before the document is removed.

        Args:
            listener: A function that takes an IDocument parameter (the document about to be removed)
        """
        ...

    @abstractmethod
    def add_removed_document_listener(self, listener: Callable[[str], None]) -> None:
        """
        Add a listener that will be called AFTER a document is removed from the collection.

        Since the document might already be destroyed, this listener receives the document ID
        rather than the document itself.

        Args:
            listener: A function that takes a str parameter (the ID of the removed document)
        """
        ...

    # IObservableList methods that need to be implemented
    @abstractmethod
    @override
    def __len__(self) -> int:
        """Return the number of documents in the collection."""
        ...

    @abstractmethod
    @override
    def __getitem__(self, index: Union[int, slice]) -> Union[IDocument, List[IDocument]]:
        """Get a document or slice of documents from the collection."""
        ...

    @abstractmethod
    @override
    def __setitem__(self, index: Union[int, slice], value: Union[IDocument, List[IDocument]]) -> None:
        """Set a document or slice of documents in the collection."""
        ...

    @abstractmethod
    @override
    def __delitem__(self, index: Union[int, slice]) -> None:
        """Delete a document or slice of documents from the collection."""
        ...

    @abstractmethod
    @override
    def __iter__(self) -> Iterator[IDocument]:
        """Return an iterator over the documents in the collection."""
        ...

    @abstractmethod
    @override
    def __contains__(self, item: IDocument) -> bool:
        """Check if a document is in the collection."""
        ...

    @abstractmethod
    @override
    def append(self, item: IDocument) -> None:
        """Add a document to the end of the collection."""
        ...

    @abstractmethod
    @override
    def extend(self, items: List[IDocument]) -> None:
        """Extend the collection by appending all documents from the iterable."""
        ...

    @abstractmethod
    @override
    def insert(self, index: int, item: IDocument) -> None:
        """Insert a document at a given position."""
        ...

    @abstractmethod
    @override
    def remove(self, item: IDocument) -> None:
        """Remove the first occurrence of a document from the collection."""
        ...

    @abstractmethod
    @override
    def pop(self, index: int = -1) -> IDocument:
        """Remove and return a document at a given position."""
        ...

    @abstractmethod
    @override
    def clear(self) -> None:
        """Remove all documents from the collection."""
        ...

    @abstractmethod
    @override
    def index(self, item: IDocument, start: int = 0, end: Optional[int] = None) -> int:
        """Return the index of the first occurrence of a document."""
        ...

    @abstractmethod
    @override
    def count(self, item: IDocument) -> int:
        """Return the number of occurrences of a document in the collection."""
        ...

    @abstractmethod
    @override
    def sort(self, *, key: Optional[Callable[[IDocument], Any]] = None, reverse: bool = False) -> None:
        """Sort the collection in place."""
        ...

    @abstractmethod
    @override
    def reverse(self) -> None:
        """Reverse the collection in place."""
        ...

    @abstractmethod
    @override
    def copy(self) -> List[IDocument]:
        """Return a shallow copy of the collection."""
        ...

    @abstractmethod
    @override
    def on_change(self, callback: Callable[[ListChange[IDocument]], None]) -> None:
        """Register for all change events with detailed information."""
        ...

    @abstractmethod
    @override
    def on_add(self, callback: Callable[[IDocument, int], None]) -> None:
        """Register for add events with document and index."""
        ...

    @abstractmethod
    @override
    def on_remove(self, callback: Callable[[IDocument, int], None]) -> None:
        """Register for remove events with document and index."""
        ...

    @abstractmethod
    @override
    def on_clear(self, callback: Callable[[List[IDocument]], None]) -> None:
        """Register for clear events with the cleared documents."""
        ...
