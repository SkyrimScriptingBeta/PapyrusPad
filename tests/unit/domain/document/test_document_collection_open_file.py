from pathlib import Path
from unittest.mock import Mock
import pytest
from assertpy import assert_that

from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class TestDocumentCollectionOpenFile:
    """Unit tests for the open_file method of DocumentCollection."""

    def test_open_file_new(self) -> None:
        """Test opening a file that is not already open."""
        # Arrange
        collection = DocumentCollection()
        mock_filesystem = Mock(spec=IFileSystem)
        mock_filesystem.read_text.return_value = "File content"
        file_path = Path("/test/test.txt")

        # Act
        document = collection.open_file(file_path, mock_filesystem)

        # Assert
        mock_filesystem.read_text.assert_called_once_with(str(file_path))
        assert_that(document.name).is_equal_to("test.txt")
        assert_that(document.path).is_equal_to(file_path)
        assert_that(document.content).is_equal_to("File content")
        assert_that(document.is_modified).is_false()
        assert_that(document.last_saved).is_not_none()
        assert_that(collection.get_active()).is_equal_to(document)

    def test_open_file_already_open(self) -> None:
        """Test opening a file that is already open."""
        # Arrange
        collection = DocumentCollection()
        mock_filesystem = Mock(spec=IFileSystem)
        file_path = Path("/test/test.txt")

        # First open the file
        mock_filesystem.read_text.return_value = "File content"
        first_document = collection.open_file(file_path, mock_filesystem)

        # Open another file to make it active
        mock_filesystem.read_text.return_value = "Other content"
        other_document = collection.open_file(Path("/test/other.txt"), mock_filesystem)
        assert_that(collection.get_active()).is_equal_to(other_document)

        # Reset the mock
        mock_filesystem.reset_mock()

        # Act - open the first file again
        document = collection.open_file(file_path, mock_filesystem)

        # Assert
        # Should not read the file again
        mock_filesystem.read_text.assert_not_called()
        # Should return the same document
        assert_that(document).is_equal_to(first_document)
        # Should make it active
        assert_that(collection.get_active()).is_equal_to(first_document)

    def test_open_file_error(self) -> None:
        """Test opening a file that cannot be read."""
        # Arrange
        collection = DocumentCollection()
        mock_filesystem = Mock(spec=IFileSystem)
        mock_filesystem.read_text.side_effect = FileNotFoundError("File not found")
        file_path = Path("/test/test.txt")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            collection.open_file(file_path, mock_filesystem)

        # Should not have added a document
        assert_that(collection.list_documents()).is_empty()
