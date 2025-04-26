from assertpy import assert_that
from unittest.mock import Mock

from PapyrusPad.domain.capability.capability_interface import IRunnable
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider
from PapyrusPad.domain.document.text_document import TextDocument


class TestDocumentCapabilityIntegration:
    def test_document_with_capability_provider(self) -> None:
        """Test document with capability provider."""
        # Arrange
        doc = TextDocument()
        doc.document_type = "python"

        # Create mock capability provider
        provider = Mock(spec=DocumentCapabilityProvider)
        provider.has_capability.return_value = True

        # Create mock runnable capability
        mock_runnable = Mock(spec=IRunnable)
        provider.get_capability.return_value = mock_runnable

        # Inject capability provider
        TextDocument.set_capability_provider_for_testing(provider)

        try:
            # Act & Assert
            assert_that(doc.has_capability("run")).is_true()
            assert_that(doc.get_capability("run", IRunnable)).is_equal_to(mock_runnable)

            # Verify provider was called with correct arguments
            provider.has_capability.assert_called_with("python", "run")
            provider.get_capability.assert_called_with("python", "run", IRunnable)
        finally:
            # Clean up
            TextDocument.set_capability_provider_for_testing(None)

    def test_document_without_capability_provider(self) -> None:
        """Test document without capability provider."""
        # Arrange
        doc = TextDocument()
        doc.document_type = "python"

        # Ensure no capability provider
        TextDocument.set_capability_provider_for_testing(None)

        # Act & Assert
        assert_that(doc.has_capability("run")).is_false()
        assert_that(doc.get_capability("run", IRunnable)).is_none()

    def test_document_with_provider_but_no_capability(self) -> None:
        """Test document with provider but no capability."""
        # Arrange
        doc = TextDocument()
        doc.document_type = "text"

        # Create mock capability provider
        provider = Mock(spec=DocumentCapabilityProvider)
        provider.has_capability.return_value = False
        provider.get_capability.return_value = None

        # Inject capability provider
        TextDocument.set_capability_provider_for_testing(provider)

        try:
            # Act & Assert
            assert_that(doc.has_capability("run")).is_false()
            assert_that(doc.get_capability("run", IRunnable)).is_none()

            # Verify provider was called with correct arguments
            provider.has_capability.assert_called_with("text", "run")
        finally:
            # Clean up
            TextDocument.set_capability_provider_for_testing(None)
