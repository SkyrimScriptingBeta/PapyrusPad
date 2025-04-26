from assertpy import assert_that
from unittest.mock import Mock

from PapyrusPad.domain.capability.capability_interface import (
    IRunnable,
)
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider
from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry


class TestDocumentCapabilityProvider:
    def test_register_capability_for_type(self) -> None:
        """Test registering a capability for a document type."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Act
        provider.register_capability_for_type("python", "run")

        # Assert
        assert_that(provider.has_capability("python", "run")).is_true()
        assert_that(provider.has_capability("python", "preview")).is_false()
        assert_that(provider.has_capability("markdown", "run")).is_false()

    def test_register_multiple_capabilities(self) -> None:
        """Test registering multiple capabilities for a document type."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Act
        provider.register_capability_for_type("python", "run")
        provider.register_capability_for_type("python", "lint")
        provider.register_capability_for_type("markdown", "preview")

        # Assert
        assert_that(provider.has_capability("python", "run")).is_true()
        assert_that(provider.has_capability("python", "lint")).is_true()
        assert_that(provider.has_capability("python", "preview")).is_false()
        assert_that(provider.has_capability("markdown", "preview")).is_true()
        assert_that(provider.has_capability("markdown", "run")).is_false()

    def test_get_capability(self) -> None:
        """Test getting a capability for a document type."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Mock capability
        mock_runnable = Mock()
        capability_registry.get_typed.return_value = mock_runnable

        # Act
        provider.register_capability_for_type("python", "run")
        result = provider.get_capability("python", "run", IRunnable)

        # Assert
        assert_that(result).is_equal_to(mock_runnable)
        capability_registry.get_typed.assert_called_once_with("run", IRunnable)

    def test_get_capability_not_registered(self) -> None:
        """Test getting a capability that is not registered for a document type."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Act
        result = provider.get_capability("python", "run", IRunnable)

        # Assert
        assert_that(result).is_none()
        capability_registry.get_typed.assert_not_called()

    def test_get_capabilities_for_type(self) -> None:
        """Test getting all capabilities for a document type."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Act
        provider.register_capability_for_type("python", "run")
        provider.register_capability_for_type("python", "lint")
        capabilities = provider.get_capabilities_for_type("python")

        # Assert
        assert_that(capabilities).contains("run")
        assert_that(capabilities).contains("lint")
        assert_that(capabilities).is_length(2)

    def test_get_capabilities_for_nonexistent_type(self) -> None:
        """Test getting capabilities for a document type that doesn't exist."""
        # Arrange
        doc_type_registry = Mock(spec=DocumentTypeRegistry)
        capability_registry = Mock(spec=CapabilityRegistry)
        provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)

        # Act
        capabilities = provider.get_capabilities_for_type("nonexistent")

        # Assert
        assert_that(capabilities).is_empty()
