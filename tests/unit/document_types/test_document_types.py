from assertpy import assert_that

from PapyrusPad.document_types.text.text_type import TextType
from PapyrusPad.document_types.markdown.markdown_type import MarkdownType
from PapyrusPad.document_types.python.python_type import PythonType


class TestDocumentTypes:
    def test_text_type(self) -> None:
        """Test text document type."""
        # Arrange & Act
        doc_type = TextType.create()

        # Assert
        assert_that(doc_type.type_id).is_equal_to("text")
        assert_that(doc_type.display_name).is_equal_to("Text")
        assert_that(doc_type.description).is_equal_to("Plain text document")
        assert_that(doc_type.extensions).contains(".txt")
        assert_that(doc_type.extensions).contains(".text")
        assert_that(doc_type.icon).is_equal_to("text-icon")

    def test_markdown_type(self) -> None:
        """Test markdown document type."""
        # Arrange & Act
        doc_type = MarkdownType.create()

        # Assert
        assert_that(doc_type.type_id).is_equal_to("markdown")
        assert_that(doc_type.display_name).is_equal_to("Markdown")
        assert_that(doc_type.description).is_equal_to("Markdown document")
        assert_that(doc_type.extensions).contains(".md")
        assert_that(doc_type.extensions).contains(".markdown")
        assert_that(doc_type.icon).is_equal_to("markdown-icon")

    def test_python_type(self) -> None:
        """Test python document type."""
        # Arrange & Act
        doc_type = PythonType.create()

        # Assert
        assert_that(doc_type.type_id).is_equal_to("python")
        assert_that(doc_type.display_name).is_equal_to("Python")
        assert_that(doc_type.description).is_equal_to("Python source code")
        assert_that(doc_type.extensions).contains(".py")
        assert_that(doc_type.extensions).contains(".pyw")
        assert_that(doc_type.extensions).contains(".pyi")
        assert_that(doc_type.icon).is_equal_to("python-icon")
