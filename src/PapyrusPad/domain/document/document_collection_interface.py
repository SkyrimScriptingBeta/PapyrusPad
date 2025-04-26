from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Iterator

from PapyrusPad.domain.document.document_interface import IDocument
from qt_helpers.observable import Observable


class IDocumentCollection(ABC):
    """Manages all documents open in the editor."""

    @abstractmethod
    def __len__(self) -> int:
        """
        Return the number of documents in the collection.

        This allows using len(collection) to get the document count.
        """
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[IDocument]:
        """
        Return an iterator over the documents in the collection.

        This allows iterating over the collection using for loops and other iteration tools.
        """
        ...

    @abstractmethod
    def __next__(self) -> IDocument:
        """
        Return the next document in the collection.

        This allows using next() on the collection to get the next document.
        Raises StopIteration when there are no more documents.
        """
        ...

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
    def remove(self, document_id: str) -> bool:
        """Close/remove the document. Returns True if found."""
        ...

    @abstractmethod
    def create(self, name: str = "Untitled", content: str = "") -> IDocument:
        """Create and add a new document with a random ID."""
        ...

    @abstractmethod
    def is_path_open(self, path: Path) -> bool:
        """Check if a document with this path is already open."""
        ...

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
