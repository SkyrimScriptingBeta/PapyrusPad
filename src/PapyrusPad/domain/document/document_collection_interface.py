from abc import ABC, abstractmethod
from pathlib import Path

from PapyrusPad.domain.document.document_interface import IDocument


class IDocumentCollection(ABC):
    """Manages all documents open in the editor."""

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
    def get_active(self) -> IDocument | None:
        """Return the currently focused/active document, if any."""
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
    def set_active(self, document_id: str) -> bool:
        """Mark a document as currently active. Returns True if found."""
        ...

    @abstractmethod
    def create(self, name: str = "Untitled", content: str = "") -> IDocument:
        """Create and add a new document with a random ID."""
        ...

    @abstractmethod
    def is_path_open(self, path: Path) -> bool:
        """Check if a document with this path is already open."""
        ...
