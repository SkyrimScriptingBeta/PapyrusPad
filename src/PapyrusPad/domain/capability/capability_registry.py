from dataclasses import dataclass, field
import logging
from typing import TypeVar, cast

from .capability_interface import ICapability

T = TypeVar("T", bound=ICapability)


@dataclass
class CapabilityRegistry:
    """
    Registry for document capabilities.

    This registry manages capabilities and provides lookup by ID and type.
    """

    _capabilities: dict[str, ICapability] = field(default_factory=dict[str, ICapability])
    _logger: logging.Logger = field(default_factory=lambda: logging.getLogger("CapabilityRegistry"))

    def register(self, capability: ICapability) -> bool:
        """
        Register a capability.

        Args:
            capability: The capability to register

        Returns:
            True if newly registered, False if already existed
        """
        capability_id = capability.capability_id

        # Check if already registered
        if capability_id in self._capabilities:
            self._logger.info(f"Capability {capability_id} already registered")
            return False

        # Register the capability
        self._capabilities[capability_id] = capability

        self._logger.info(f"Registered capability: {capability_id}")
        return True

    def get(self, capability_id: str) -> ICapability | None:
        """
        Get a capability by ID.

        Args:
            capability_id: The ID of the capability to get

        Returns:
            The capability, or None if not found
        """
        return self._capabilities.get(capability_id)

    def get_typed(self, capability_id: str, capability_type: type[T]) -> T | None:
        """
        Get a capability by ID and type.

        Args:
            capability_id: The ID of the capability to get
            capability_type: The expected type of the capability

        Returns:
            The capability, or None if not found or not of the expected type
        """
        capability = self._capabilities.get(capability_id)
        if capability is None:
            return None

        if isinstance(capability, capability_type):
            return cast(T, capability)

        return None

    def has(self, capability_id: str) -> bool:
        """
        Check if a capability is registered.

        Args:
            capability_id: The ID of the capability to check

        Returns:
            True if the capability is registered, False otherwise
        """
        return capability_id in self._capabilities

    def get_all(self) -> list[ICapability]:
        """
        Get all registered capabilities.

        Returns:
            A list of all registered capabilities
        """
        return list(self._capabilities.values())
