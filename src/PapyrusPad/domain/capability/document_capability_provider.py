from dataclasses import dataclass, field
from typing import TypeVar

from PapyrusPad.domain.document_type.document_type_registry import DocumentTypeRegistry
from .capability_interface import ICapability
from .capability_registry import CapabilityRegistry

T = TypeVar("T", bound=ICapability)


@dataclass
class DocumentCapabilityProvider:
    """
    Provider for document capabilities based on document type.

    This provider uses the document type registry and capability registry
    to determine which capabilities are available for a given document type.
    """

    _document_type_registry: DocumentTypeRegistry
    _capability_registry: CapabilityRegistry
    _type_capabilities: dict[str, list[str]] = field(default_factory=dict[str, list[str]])

    def register_capability_for_type(self, type_id: str, capability_id: str) -> None:
        """
        Register a capability for a document type.

        Args:
            type_id: The document type ID
            capability_id: The capability ID
        """
        if type_id not in self._type_capabilities:
            self._type_capabilities[type_id] = []

        if capability_id not in self._type_capabilities[type_id]:
            self._type_capabilities[type_id].append(capability_id)

    def has_capability(self, type_id: str, capability_id: str) -> bool:
        """
        Check if a document type has a specific capability.

        Args:
            type_id: The document type ID
            capability_id: The capability ID

        Returns:
            True if the document type has the capability, False otherwise
        """
        if type_id not in self._type_capabilities:
            return False

        return capability_id in self._type_capabilities[type_id]

    def get_capability(self, type_id: str, capability_id: str, capability_type: type[T]) -> T | None:
        """
        Get a capability for a document type.

        Args:
            type_id: The document type ID
            capability_id: The capability ID
            capability_type: The expected type of the capability

        Returns:
            The capability, or None if not available
        """
        if not self.has_capability(type_id, capability_id):
            return None

        return self._capability_registry.get_typed(capability_id, capability_type)

    def get_capabilities_for_type(self, type_id: str) -> list[str]:
        """
        Get all capability IDs for a document type.

        Args:
            type_id: The document type ID

        Returns:
            A list of capability IDs
        """
        if type_id not in self._type_capabilities:
            return []

        return self._type_capabilities[type_id].copy()
