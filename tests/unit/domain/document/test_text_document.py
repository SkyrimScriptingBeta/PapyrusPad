from datetime import datetime
from pathlib import Path
from assertpy import assert_that

from PapyrusPad.domain.document.text_document import TextDocument


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
        doc = TextDocument(_name="test.txt", _content="Hello, world!", _path=Path("/test/test.txt"))
        assert doc.id is not None
        assert_that(doc.name).is_equal_to("test.txt")
        assert_that(doc.path).is_equal_to(Path("/test/test.txt"))
        assert_that(doc.content).is_equal_to("Hello, world!")
        assert_that(doc.is_modified).is_false()
        assert doc.last_saved is None
        assert_that(doc.display_name).is_equal_to("test.txt")

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
        doc = TextDocument(_content="Hello, world!")
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
        doc = TextDocument(_name="test.txt")
        # Mark it as saved (not modified)
        doc.mark_saved()
        # Check display name without modification indicator
        assert_that(doc.display_name).is_equal_to("test.txt")
        # Modify the document
        doc.content = "New content"
        # Check display name with modification indicator
        assert_that(doc.display_name).is_equal_to("test.txt*")
