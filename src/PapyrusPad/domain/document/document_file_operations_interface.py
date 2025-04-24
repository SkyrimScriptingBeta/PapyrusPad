from abc import ABC, abstractmethod
from pathlib import Path

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection


class IDocumentFileOperations(ABC):
    """Service for handling file operations related to documents."""

    @abstractmethod
    def open_file(self, path: Path, document_collection: IDocumentCollection) -> IDocument:
        """
        Open a file and add it to the document collection.

        If a document with this path is already open, it will be returned.
        Otherwise, a new document will be created, loaded with the file's content,
        and added to the collection.

        Args:
            path: Path to the file to open
            document_collection: The document collection to add the document to

        Returns:
            The document representing the opened file

        Raises:
            FileNotFoundError: If the file does not exist or cannot be read
        """
        ...

    @abstractmethod
    def save_document(self, document: IDocument) -> bool:
        """
        Save a document to its path.

        Args:
            document: The document to save

        Returns:
            True if saved successfully, False otherwise

        Raises:
            ValueError: If the document has no path
        """
        ...

    @abstractmethod
    def save_document_as(self, document: IDocument, path: Path) -> bool:
        """
        Save a document to a new path.

        Args:
            document: The document to save
            path: The path to save the document to

        Returns:
            True if saved successfully, False otherwise
        """
        ...
