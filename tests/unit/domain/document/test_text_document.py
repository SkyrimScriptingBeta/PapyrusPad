from datetime import datetime
from pathlib import Path
from unittest.mock import Mock
import pytest
from assertpy import assert_that

from PapyrusPad.domain.document.text_document import TextDocument
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class TestTextDocument:
    """Unit tests for the TextDocument class."""

    def test_init_default(self) -> None:
        """Test creating a document with default values."""
        doc = TextDocument()
        assert doc.id is not None
        assert_that(doc.name).is_equal_to("Untitled")
        assert doc.path is None
        assert_that(doc.content).is_empty()
        assert_that(doc.is_modified).is_false()
        assert doc.last_saved is None
        assert_that(doc.display_name).is_equal_to("Untitled")

    def test_init_with_values(self) -> None:
        """Test creating a document with specific values."""
        doc = TextDocument.create(name="test.txt", content="Hello, world!", path=Path("/test/test.txt"))
        assert doc.id is not None
        assert_that(doc.name).is_equal_to("test.txt")
        assert_that(doc.path).is_equal_to(Path("/test/test.txt"))
        assert_that(doc.content).is_equal_to("Hello, world!")
        assert_that(doc.is_modified).is_true()  # Setting content marks as modified
        assert doc.last_saved is None
        assert_that(doc.display_name).is_equal_to("test.txt*")  # Has * because it's modified

    def test_name_setter(self) -> None:
        """Test setting the name."""
        doc = TextDocument()
        doc.name = "test.txt"
        assert_that(doc.name).is_equal_to("test.txt")
        assert_that(doc.is_modified).is_true()
        assert_that(doc.display_name).is_equal_to("test.txt*")

    def test_path_setter(self) -> None:
        """Test setting the path."""
        doc = TextDocument()
        doc.path = Path("/test/test.txt")
        assert_that(doc.path).is_equal_to(Path("/test/test.txt"))
        # Setting path should not mark as modified
        assert_that(doc.is_modified).is_false()

    def test_content_setter(self) -> None:
        """Test setting the content."""
        doc = TextDocument()
        doc.content = "Hello, world!"
        assert_that(doc.content).is_equal_to("Hello, world!")
        assert_that(doc.is_modified).is_true()
        assert_that(doc.display_name).is_equal_to("Untitled*")

    def test_content_setter_same_value(self) -> None:
        """Test setting the content to the same value."""
        # Create a document with content
        doc = TextDocument.create(content="Hello, world!")
        # Mark it as saved (not modified)
        doc.mark_saved()
        # Set to same content
        doc.content = "Hello, world!"
        # Should not be modified
        assert_that(doc.is_modified).is_false()

    def test_mark_saved(self) -> None:
        """Test marking a document as saved."""
        doc = TextDocument()
        # Modify the document to ensure it's marked as modified
        doc.content = "Hello, world!"
        assert_that(doc.is_modified).is_true()
        # Mark as saved
        doc.mark_saved()
        # Should not be modified anymore
        assert_that(doc.is_modified).is_false()
        # Should have a last_saved timestamp
        assert_that(doc.last_saved).is_instance_of(datetime)

    def test_display_name(self) -> None:
        """Test the display name property."""
        # Create a document
        doc = TextDocument.create(name="test.txt")
        # Mark it as saved (not modified)
        doc.mark_saved()
        # Check display name without modification indicator
        assert_that(doc.display_name).is_equal_to("test.txt")
        # Modify the document
        doc.content = "New content"
        # Check display name with modification indicator
        assert_that(doc.display_name).is_equal_to("test.txt*")

    def test_save_success(self) -> None:
        """Test saving a document successfully."""
        # Arrange
        doc = TextDocument.create(name="test.txt", path=Path("/test.txt"), content="Hello, world!")
        mock_filesystem = Mock(spec=IFileSystem)

        # Act
        result = doc.save(mock_filesystem)

        # Assert
        assert_that(result).is_true()
        # Use str(doc.path) to get the platform-specific path string
        mock_filesystem.write_text.assert_called_once_with(str(doc.path), "Hello, world!")
        assert_that(doc.is_modified).is_false()
        assert_that(doc.last_saved).is_not_none()

    def test_save_no_path(self) -> None:
        """Test saving a document with no path."""
        # Arrange
        doc = TextDocument.create(name="test.txt", content="Hello, world!")
        mock_filesystem = Mock(spec=IFileSystem)

        # Act & Assert
        with pytest.raises(ValueError):
            doc.save(mock_filesystem)
        mock_filesystem.write_text.assert_not_called()

    def test_save_filesystem_error(self) -> None:
        """Test saving a document when filesystem raises an error."""
        # Arrange
        doc = TextDocument.create(name="test.txt", path=Path("/test.txt"), content="Hello, world!")
        mock_filesystem = Mock(spec=IFileSystem)
        mock_filesystem.write_text.side_effect = Exception("Filesystem error")

        # Act
        result = doc.save(mock_filesystem)

        # Assert
        assert_that(result).is_false()
        mock_filesystem.write_text.assert_called_once()
        # Document should still be marked as modified
        assert_that(doc.is_modified).is_true()

    def test_reload_content_success(self) -> None:
        """Test reloading a document's content successfully."""
        # Arrange
        doc = TextDocument.create(name="test.txt", path=Path("/test.txt"), content="Old content")
        doc.mark_saved()  # Reset modified flag
        doc.content = "Modified content"  # Modify the document
        assert_that(doc.is_modified).is_true()

        mock_filesystem = Mock(spec=IFileSystem)
        mock_filesystem.read_text.return_value = "New content from disk"

        # Act
        result = doc.reload_content(mock_filesystem)

        # Assert
        assert_that(result).is_true()
        # Use str(doc.path) to get the platform-specific path string
        mock_filesystem.read_text.assert_called_once_with(str(doc.path))
        assert_that(doc.content).is_equal_to("New content from disk")
        assert_that(doc.is_modified).is_false()

    def test_reload_content_no_path(self) -> None:
        """Test reloading a document with no path."""
        # Arrange
        doc = TextDocument.create(name="test.txt", content="Hello, world!")
        mock_filesystem = Mock(spec=IFileSystem)

        # Act & Assert
        with pytest.raises(ValueError):
            doc.reload_content(mock_filesystem)
        mock_filesystem.read_text.assert_not_called()

    def test_reload_content_filesystem_error(self) -> None:
        """Test reloading a document when filesystem raises an error."""
        # Arrange
        doc = TextDocument.create(name="test.txt", path=Path("/test.txt"), content="Hello, world!")
        mock_filesystem = Mock(spec=IFileSystem)
        mock_filesystem.read_text.side_effect = Exception("Filesystem error")

        # Act
        result = doc.reload_content(mock_filesystem)

        # Assert
        assert_that(result).is_false()
        mock_filesystem.read_text.assert_called_once()
        # Content should remain unchanged
        assert_that(doc.content).is_equal_to("Hello, world!")
