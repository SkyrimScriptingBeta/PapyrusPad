from assertpy import assert_that
from unittest.mock import Mock

from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider
from PapyrusPad.document_types.registration import (
    register_document_types,
    register_capabilities,
    setup_document_system,
)


class TestRegistration:
    def test_register_document_types(self) -> None:
        """Test registering document types."""
        # Arrange
        registry = DocumentTypeRegistry()

        # Act
        register_document_types(registry)

        # Assert
        assert_that(registry.get_type("text")).is_not_none()
        assert_that(registry.get_type("markdown")).is_not_none()
        assert_that(registry.get_type("python")).is_not_none()

        # Check extensions
        txt_type = registry.get_type_for_extension(".txt")
        assert txt_type is not None  # Type assertion for Pylance
        assert_that(txt_type).is_not_none()
        assert_that(txt_type.type_id).is_equal_to("text")

        md_type = registry.get_type_for_extension(".md")
        assert md_type is not None  # Type assertion for Pylance
        assert_that(md_type).is_not_none()
        assert_that(md_type.type_id).is_equal_to("markdown")

        py_type = registry.get_type_for_extension(".py")
        assert py_type is not None  # Type assertion for Pylance
        assert_that(py_type).is_not_none()
        assert_that(py_type.type_id).is_equal_to("python")

    def test_register_capabilities(self) -> None:
        """Test registering capabilities."""
        # Arrange
        capability_registry = CapabilityRegistry()
        doc_type_registry = DocumentTypeRegistry()
        capability_provider = DocumentCapabilityProvider(doc_type_registry, capability_registry)
        document_content_provider = Mock()
        document_content_provider.return_value = "# Test content"

        # Act
        register_capabilities(capability_registry, capability_provider, document_content_provider)

        # Assert
        assert_that(capability_registry.has("preview")).is_true()
        assert_that(capability_registry.has("run")).is_true()

        assert_that(capability_provider.has_capability("markdown", "preview")).is_true()
        assert_that(capability_provider.has_capability("python", "run")).is_true()

        # Check that capabilities are not registered for wrong types
        assert_that(capability_provider.has_capability("text", "preview")).is_false()
        assert_that(capability_provider.has_capability("markdown", "run")).is_false()

    def test_setup_document_system(self) -> None:
        """Test setting up the document system."""
        # Arrange
        type_registry = DocumentTypeRegistry()
        capability_registry = CapabilityRegistry()
        capability_provider = DocumentCapabilityProvider(type_registry, capability_registry)
        document_content_provider = Mock()
        document_content_provider.return_value = "# Test content"

        # Act
        setup_document_system(type_registry, capability_registry, capability_provider, document_content_provider)

        # Assert - document types
        assert_that(type_registry.get_type("text")).is_not_none()
        assert_that(type_registry.get_type("markdown")).is_not_none()
        assert_that(type_registry.get_type("python")).is_not_none()

        # Assert - capabilities
        assert_that(capability_registry.has("preview")).is_true()
        assert_that(capability_registry.has("run")).is_true()

        # Assert - capability provider
        assert_that(capability_provider.has_capability("markdown", "preview")).is_true()
        assert_that(capability_provider.has_capability("python", "run")).is_true()
