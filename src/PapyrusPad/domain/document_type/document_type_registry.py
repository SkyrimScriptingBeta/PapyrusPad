from dataclasses import dataclass, field
from typing import Optional
import logging

from .document_type import DocumentType


@dataclass
class DocumentTypeRegistry:
    """
    Registry for document types.

    This registry manages document types and provides lookup by ID or file extension.
    """

    _types: dict[str, DocumentType] = field(default_factory=dict[str, DocumentType])
    _extension_map: dict[str, str] = field(default_factory=dict[str, str])
    _logger: logging.Logger = field(default_factory=lambda: logging.getLogger("DocumentTypeRegistry"))

    def register(self, doc_type: DocumentType) -> bool:
        """
        Register a document type.

        Args:
            doc_type: The document type to register

        Returns:
            True if newly registered, False if already existed
        """
        type_id = doc_type.type_id.lower()

        # Check if already registered
        if type_id in self._types:
            self._logger.info(f"Document type {type_id} already registered")
            return False

        # Register the type
        self._types[type_id] = doc_type

        # Update extension mappings
        for ext in doc_type.extensions:
            ext = ext.lower()
            if ext in self._extension_map and self._extension_map[ext] != type_id:
                self._logger.warning(f"Extension {ext} already mapped to {self._extension_map[ext]}, overriding with {type_id}")
            self._extension_map[ext] = type_id

        self._logger.info(f"Registered document type: {type_id} ({doc_type.display_name})")
        return True

    def get_type(self, type_id: str) -> Optional[DocumentType]:
        """
        Get a document type by ID.

        Args:
            type_id: The ID of the document type to get

        Returns:
            The document type, or None if not found
        """
        return self._types.get(type_id.lower())

    def get_type_for_extension(self, extension: str) -> Optional[DocumentType]:
        """
        Get the document type for a file extension.

        Args:
            extension: The file extension to look up

        Returns:
            The document type, or None if not found
        """
        ext = extension.lower()
        if not ext.startswith("."):
            ext = f".{ext}"

        type_id = self._extension_map.get(ext)
        if type_id:
            return self._types.get(type_id)
        return None

    def get_all_types(self) -> list[DocumentType]:
        """
        Get all registered document types.

        Returns:
            A list of all registered document types
        """
        return list(self._types.values())
