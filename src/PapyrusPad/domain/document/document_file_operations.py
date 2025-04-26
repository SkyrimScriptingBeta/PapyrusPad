from pathlib import Path
from typing import override

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.document.document_file_operations_interface import IDocumentFileOperations
from PapyrusPad.domain.document.text_document import TextDocument
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class DocumentFileOperations(IDocumentFileOperations):
    """Implementation of IDocumentFileOperations that uses IFileSystem."""

    def __init__(self, filesystem: IFileSystem):
        """
        Initialize the document file operations service.

        Args:
            filesystem: The filesystem to use for file operations
        """
        super().__init__()
        self._filesystem = filesystem

    @override
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
        # Check if the file is already open
        existing_doc = document_collection.find_by_path(path)
        if existing_doc:
            # Make it active and return it
            document_collection.active_document_id.set(existing_doc.id)
            return existing_doc

        print(f"Opening file: {path}")

        # Read the file content
        content = self._filesystem.read_text(str(path))

        # Create a new document
        document = TextDocument()
        document.name = path.name
        document.path = path
        document.content = content
        document.mark_saved()  # Mark as saved since we just loaded it

        # Add to collection and make active
        document_collection.add_or_replace(document)
        document_collection.active_document_id.set(document.id)

        print(f"Opened document: {document.name} at {document.path}")

        return document

    @override
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
        if not document.path:
            raise ValueError("Cannot save document without a path")

        try:
            self._filesystem.write_text(str(document.path), document.content)
            document.mark_saved()
            return True
        except Exception:
            # Log the error
            # Keep the document marked as modified
            return False

    @override
    def save_document_as(self, document: IDocument, path: Path) -> bool:
        """
        Save a document to a new path.

        Args:
            document: The document to save
            path: The path to save the document to

        Returns:
            True if saved successfully, False otherwise
        """
        print(f"Saving document as {path}")

        # Update the document's path and name before attempting to save
        document.path = path
        document.name = path.name  # Update the document name to match the filename

        try:
            self._filesystem.write_text(str(path), document.content)
            document.mark_saved()
            return True
        except Exception:
            # Log the error
            # Keep the document marked as modified
            return False
