from pathlib import Path
import pytest
from assertpy import assert_that

from PapyrusPad.domain.document.document_file_operations import DocumentFileOperations
from PapyrusPad.domain.document.text_document import TextDocument
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


@pytest.fixture
def document_type_registry() -> DocumentTypeRegistry:
    """Create a document type registry for testing."""
    return DocumentTypeRegistry()


class TestDocumentFileOperations:
    """Unit tests for the DocumentFileOperations class."""

    def test_save_document_as_updates_name(self, filesystem: IFileSystem, document_type_registry: DocumentTypeRegistry) -> None:
        """Test that save_document_as updates the document name to match the filename."""
        # Arrange
        document = TextDocument()
        document.name = "old_name.txt"
        document.content = "Document content"
        document_file_operations = DocumentFileOperations(filesystem, document_type_registry)

        # Act
        new_path = Path("/test/new_name.txt")
        success = document_file_operations.save_document_as(document, new_path)

        # Assert
        assert_that(success).is_true()
        assert_that(document.path).is_equal_to(new_path)
        assert_that(document.name).is_equal_to("new_name.txt")  # Name should be updated to match filename
        assert_that(document.is_modified).is_false()  # Document should be marked as saved
        assert_that(document.last_saved).is_not_none()  # Last saved timestamp should be set

        # Verify the file was written to the filesystem
        assert_that(filesystem.file_exists(str(new_path))).is_true()
        assert_that(filesystem.read_text(str(new_path))).is_equal_to("Document content")
