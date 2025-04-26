"""Document type and capability registration."""

from typing import Callable

from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry
from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider

from .text.text_type import TextType
from .markdown.markdown_type import MarkdownType
from .python.python_type import PythonType
from .markdown.markdown_capabilities import MarkdownCapabilities
from .python.python_capabilities import PythonCapabilities


def register_document_types(registry: DocumentTypeRegistry) -> None:
    """
    Register all document types.

    Args:
        registry: The document type registry
    """
    # Register text document type
    registry.register(TextType.create())

    # Register markdown document type
    registry.register(MarkdownType.create())

    # Register python document type
    registry.register(PythonType.create())


def register_capabilities(capability_registry: CapabilityRegistry, capability_provider: DocumentCapabilityProvider, document_content_provider: Callable[[str], str]) -> None:
    """
    Register all capabilities.

    Args:
        capability_registry: The capability registry
        capability_provider: The document capability provider
        document_content_provider: A function that takes a document ID and returns its content
    """
    # Register markdown preview capability
    markdown_preview = MarkdownCapabilities.create_preview(lambda: document_content_provider("current"))
    capability_registry.register(markdown_preview)
    capability_provider.register_capability_for_type("markdown", markdown_preview.capability_id)

    # Register python runnable capability
    python_runnable = PythonCapabilities.create_runnable(lambda: document_content_provider("current"))
    capability_registry.register(python_runnable)
    capability_provider.register_capability_for_type("python", python_runnable.capability_id)


def setup_document_system(
    type_registry: DocumentTypeRegistry, capability_registry: CapabilityRegistry, capability_provider: DocumentCapabilityProvider, document_content_provider: Callable[[str], str]
) -> None:
    """
    Set up the document system by registering all document types and capabilities.

    Args:
        type_registry: The document type registry
        capability_registry: The capability registry
        capability_provider: The document capability provider
        document_content_provider: A function that takes a document ID and returns its content
    """
    register_document_types(type_registry)
    register_capabilities(capability_registry, capability_provider, document_content_provider)
