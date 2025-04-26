from assertpy import assert_that
from unittest.mock import Mock

from PapyrusPad.domain.document.text_document import TextDocument


class TestDocumentTypeSupport:
    def test_document_type_property(self) -> None:
        """Test the document_type property."""
        # Arrange
        doc = TextDocument()

        # Act & Assert
        assert_that(doc.document_type).is_equal_to("text")  # Default type

        # Change the type
        doc.document_type = "python"
        assert_that(doc.document_type).is_equal_to("python")

    def test_document_type_observable(self) -> None:
        """Test the document_type_observable property."""
        # Arrange
        doc = TextDocument()
        mock_callback = Mock()

        # Act
        doc.document_type_observable.on_change(mock_callback)
        doc.document_type = "python"

        # Assert
        mock_callback.assert_called_once_with("python")

    def test_has_capability(self) -> None:
        """Test the has_capability method."""
        # Arrange
        doc = TextDocument()

        # Act & Assert
        assert_that(doc.has_capability("compile")).is_false()  # Text documents don't have compile capability

    def test_get_capability(self) -> None:
        """Test the get_capability method."""
        # Arrange
        doc = TextDocument()

        # Act & Assert
        assert_that(doc.get_capability("compile", Mock)).is_none()  # Text documents don't have compile capability
