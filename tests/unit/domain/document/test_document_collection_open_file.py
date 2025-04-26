from pathlib import Path
import pytest
from assertpy import assert_that

from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class TestDocumentFileOperations:
    """Unit tests for the DocumentFileOperations class."""

    def test_open_file_new(self, document_collection: DocumentCollection, filesystem: IFileSystem) -> None:
        """Test opening a file that is not already open."""
        # Arrange
        file_path = Path("/test/test.txt")
        document_file_operations = DocumentFileOperations(filesystem)

        # Set up the file in the filesystem
        filesystem.write_text(str(file_path), "File content")

        # Act
        document = document_file_operations.open_file(file_path, document_collection)

        # Assert
        assert_that(document.name).is_equal_to("test.txt")
        assert_that(document.path).is_equal_to(file_path)
        assert_that(document.content).is_equal_to("File content")
        assert_that(document.is_modified).is_false()
        assert_that(document.last_saved).is_not_none()
        assert_that(document_collection.active_document).is_equal_to(document)

    def test_open_file_already_open(self, document_collection: DocumentCollection, filesystem: IFileSystem) -> None:
        """Test opening a file that is already open."""
        # Arrange
        file_path = Path("/test/test.txt")
        document_file_operations = DocumentFileOperations(filesystem)

        # Set up the files in the filesystem
        filesystem.write_text(str(file_path), "File content")
        filesystem.write_text("/test/other.txt", "Other content")

        # First open the file
        first_document = document_file_operations.open_file(file_path, document_collection)

        # Open another file to make it active
        other_document = document_file_operations.open_file(Path("/test/other.txt"), document_collection)
        assert_that(document_collection.active_document).is_equal_to(other_document)

        # Act - open the first file again
        document = document_file_operations.open_file(file_path, document_collection)

        # Assert
        # Should return the same document
        assert_that(document).is_equal_to(first_document)
        # Should make it active
        assert_that(document_collection.active_document).is_equal_to(first_document)

    def test_open_file_error(self, document_collection: DocumentCollection, filesystem: IFileSystem) -> None:
        """Test opening a file that cannot be read."""
        # Arrange
        file_path = Path("/nonexistent/file.txt")
        document_file_operations = DocumentFileOperations(filesystem)

        # Make sure the file doesn't exist
        if filesystem.file_exists(str(file_path)):
            filesystem.delete_file(str(file_path))

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            document_file_operations.open_file(file_path, document_collection)

        # Should not have added a document
        assert_that(document_collection.list_documents()).is_empty()
