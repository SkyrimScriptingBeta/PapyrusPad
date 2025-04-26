from assertpy import assert_that

from PapyrusPad.domain.document_type.document_type import DocumentType


class TestDocumentType:
    def test_create_document_type(self) -> None:
        """Test creating a document type with default values."""
        # Arrange & Act
        doc_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py", "pyw"], icon="python-icon")

        # Assert
        assert_that(doc_type.type_id).is_equal_to("python")
        assert_that(doc_type.display_name).is_equal_to("Python")
        assert_that(doc_type.description).is_equal_to("Python source code")
        assert_that(doc_type.extensions).contains(".py")
        assert_that(doc_type.extensions).contains(".pyw")
        assert_that(doc_type.icon).is_equal_to("python-icon")

    def test_type_id_normalization(self) -> None:
        """Test that type_id is normalized to lowercase."""
        # Arrange & Act
        doc_type = DocumentType(type_id="PYTHON", display_name="Python", description="Python source code", extensions=[".py"], icon="python-icon")

        # Assert
        assert_that(doc_type.type_id).is_equal_to("python")

    def test_extensions_normalization(self) -> None:
        """Test that extensions are normalized to lowercase and have dots."""
        # Arrange & Act
        doc_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=["PY", ".PYW", "pyi"], icon="python-icon")

        # Assert
        assert_that(doc_type.extensions).contains(".py")
        assert_that(doc_type.extensions).contains(".pyw")
        assert_that(doc_type.extensions).contains(".pyi")
