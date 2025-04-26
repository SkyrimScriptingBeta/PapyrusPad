from assertpy import assert_that

from PapyrusPad.domain.document_type.document_type import DocumentType
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry


class TestDocumentTypeRegistry:
    def test_register_document_type(self) -> None:
        """Test registering a document type."""
        # Arrange
        registry = DocumentTypeRegistry()
        doc_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py", "pyw"], icon="python-icon")

        # Act
        result = registry.register(doc_type)

        # Assert
        assert_that(result).is_true()
        assert_that(registry.get_type("python")).is_equal_to(doc_type)

    def test_register_duplicate_document_type(self) -> None:
        """Test registering a document type with the same ID."""
        # Arrange
        registry = DocumentTypeRegistry()
        doc_type1 = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py"], icon="python-icon")
        doc_type2 = DocumentType(type_id="python", display_name="Python 2", description="Python source code 2", extensions=[".pyw"], icon="python-icon-2")

        # Act
        registry.register(doc_type1)
        result = registry.register(doc_type2)

        # Assert
        assert_that(result).is_false()
        assert_that(registry.get_type("python")).is_equal_to(doc_type1)

    def test_get_type_case_insensitive(self) -> None:
        """Test getting a document type with case-insensitive ID."""
        # Arrange
        registry = DocumentTypeRegistry()
        doc_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py"], icon="python-icon")
        registry.register(doc_type)

        # Act & Assert
        assert_that(registry.get_type("PYTHON")).is_equal_to(doc_type)
        assert_that(registry.get_type("Python")).is_equal_to(doc_type)
        assert_that(registry.get_type("python")).is_equal_to(doc_type)

    def test_get_type_for_extension(self) -> None:
        """Test getting a document type by extension."""
        # Arrange
        registry = DocumentTypeRegistry()
        python_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py", ".pyw"], icon="python-icon")
        markdown_type = DocumentType(type_id="markdown", display_name="Markdown", description="Markdown document", extensions=[".md", ".markdown"], icon="markdown-icon")
        registry.register(python_type)
        registry.register(markdown_type)

        # Act & Assert
        assert_that(registry.get_type_for_extension(".py")).is_equal_to(python_type)
        assert_that(registry.get_type_for_extension("py")).is_equal_to(python_type)
        assert_that(registry.get_type_for_extension(".PY")).is_equal_to(python_type)
        assert_that(registry.get_type_for_extension(".pyw")).is_equal_to(python_type)
        assert_that(registry.get_type_for_extension(".md")).is_equal_to(markdown_type)
        assert_that(registry.get_type_for_extension(".markdown")).is_equal_to(markdown_type)
        assert_that(registry.get_type_for_extension(".txt")).is_none()

    def test_extension_conflict(self) -> None:
        """Test handling extension conflicts."""
        # Arrange
        registry = DocumentTypeRegistry()
        python_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py"], icon="python-icon")
        custom_type = DocumentType(type_id="custom", display_name="Custom", description="Custom type", extensions=[".py"], icon="custom-icon")  # Same extension as Python

        # Act
        registry.register(python_type)
        registry.register(custom_type)

        # Assert - the last registered type wins for the extension
        assert_that(registry.get_type_for_extension(".py")).is_equal_to(custom_type)

    def test_get_all_types(self) -> None:
        """Test getting all registered document types."""
        # Arrange
        registry = DocumentTypeRegistry()
        python_type = DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py"], icon="python-icon")
        markdown_type = DocumentType(type_id="markdown", display_name="Markdown", description="Markdown document", extensions=[".md"], icon="markdown-icon")

        # Act
        registry.register(python_type)
        registry.register(markdown_type)
        all_types = registry.get_all_types()

        # Assert
        assert_that(all_types).contains(python_type)
        assert_that(all_types).contains(markdown_type)
        assert_that(all_types).is_length(2)
