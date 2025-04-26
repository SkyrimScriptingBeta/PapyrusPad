from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import uuid
from typing import override, TYPE_CHECKING

from PapyrusPad.domain.document.document_interface import IDocument, T
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from qt_helpers.observable import Observable

if TYPE_CHECKING:
    from PapyrusPad.domain.capability.document_capability_provider import DocumentCapabilityProvider


@dataclass
class TextDocument(IDocument):
    """A text document implementation of IDocument."""

    _id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _name: Observable[str] = field(default_factory=lambda: Observable("Untitled"))
    _display_name_observable: Observable[str] = field(default_factory=lambda: Observable("Untitled"))
    _path: Path | None = None
    _content: Observable[str] = field(default_factory=lambda: Observable(""))
    _is_modified: bool = False
    _last_saved: datetime | None = None
    _document_type: Observable[str] = field(default_factory=lambda: Observable("text"))

    def __post_init__(self) -> None:
        self._update_display_name()
        self.content_observable.on_change(self._on_content_changed)
        self.name_observable.on_change(self._on_name_changed)
        self._is_modified = False

    @classmethod
    def create(cls, name: str = "Untitled", content: str = "", path: Path | None = None) -> "TextDocument":
        """
        Create a new TextDocument with the given properties.

        Args:
            name: The name of the document
            content: The content of the document
            path: The path of the document

        Returns:
            A new TextDocument instance
        """
        doc = cls()
        if name != "Untitled":
            doc.name = name
        if content:
            doc.content = content
        if path:
            doc.path = path
        return doc

    @classmethod
    def create_with_id(cls, id: str, name: str = "Untitled", content: str = "", path: Path | None = None) -> "TextDocument":
        """
        Create a new TextDocument with a specific ID (for testing purposes).

        Args:
            id: The ID to use for the document
            name: The name of the document
            content: The content of the document
            path: The path of the document

        Returns:
            A new TextDocument instance with the specified ID
        """
        doc = cls(_id=id)
        if name != "Untitled":
            doc.name = name
        if content:
            doc.content = content
        if path:
            doc.path = path
        return doc

    def _on_content_changed(self, value: str) -> None:
        self.is_modified = True

    def _on_name_changed(self, value: str) -> None:
        self.is_modified = True  # Setting name should mark as modified
        self._update_display_name()

    @property
    @override
    def id(self) -> str:
        return self._id

    @property
    @override
    def name(self) -> str:
        return self._name.get()

    @name.setter
    @override
    def name(self, value: str) -> None:
        self._name.set_if_changed(value)

    @property
    @override
    def name_observable(self) -> Observable[str]:
        return self._name

    @property
    @override
    def path(self) -> Path | None:
        return self._path

    @path.setter
    @override
    def path(self, value: Path | None) -> None:
        self._path = value

    @property
    @override
    def content(self) -> str:
        return self._content.get()

    @content.setter
    @override
    def content(self, value: str) -> None:
        if self._content.get() != value:
            self._content.set(value)
            self.is_modified = True

    @property
    @override
    def content_observable(self) -> Observable[str]:
        return self._content

    @property
    @override
    def is_modified(self) -> bool:
        return self._is_modified

    @is_modified.setter
    @override
    def is_modified(self, value: bool) -> None:
        if value != self._is_modified:
            self._is_modified = value
            self._update_display_name()

    @override
    def mark_saved(self) -> None:
        self.is_modified = False
        self._last_saved = datetime.now()

    @property
    @override
    def last_saved(self) -> datetime | None:
        return self._last_saved

    @property
    @override
    def display_name(self) -> str:
        return self._display_name_observable.get()

    def _update_display_name(self) -> None:
        modified_indicator = "*" if self.is_modified else ""
        text = f"{self.name}{modified_indicator}"
        self._display_name_observable.set_if_changed(text)

    @property
    @override
    def display_name_observable(self) -> Observable[str]:
        return self._display_name_observable

    @property
    @override
    def document_type(self) -> str:
        """Get the document type ID."""
        return self._document_type.get()

    @document_type.setter
    @override
    def document_type(self, value: str) -> None:
        """Set the document type ID."""
        self._document_type.set_if_changed(value)

    @property
    @override
    def document_type_observable(self) -> Observable[str]:
        """Observable for document type changes."""
        return self._document_type

    # Capability provider will be injected at runtime
    _capability_provider = None

    @classmethod
    def set_capability_provider_for_testing(cls, provider: "DocumentCapabilityProvider | None") -> None:
        """
        Set the capability provider for testing purposes.

        This method should only be used in tests.

        Args:
            provider: The capability provider to set
        """
        cls._capability_provider = provider

    @override
    def has_capability(self, capability_id: str) -> bool:
        """
        Check if this document has a specific capability.

        Args:
            capability_id: The ID of the capability to check

        Returns:
            True if the document has the capability, False otherwise
        """
        if self._capability_provider is None:
            return False

        return self._capability_provider.has_capability(self.document_type, capability_id)

    @override
    def get_capability(self, capability_id: str, capability_type: type[T]) -> T | None:
        """
        Get a capability implementation by ID and type.

        Args:
            capability_id: The ID of the capability to get
            capability_type: The expected type of the capability

        Returns:
            The capability implementation, or None if not available
        """
        if self._capability_provider is None:
            return None

        return self._capability_provider.get_capability(self.document_type, capability_id, capability_type)

    @override
    def save(self, filesystem: IFileSystem) -> bool:
        """
        Save the document to its path.

        Args:
            filesystem: The filesystem to use for saving

        Returns:
            True if saved successfully, False otherwise

        Raises:
            ValueError: If the document has no path
        """
        if not self._path:
            raise ValueError("Cannot save document without a path")

        try:
            filesystem.write_text(str(self._path), self.content)
            self.mark_saved()
            return True
        except Exception:
            # Log the error
            # Keep the document marked as modified
            self._is_modified = True
            return False

    @override
    def reload_content(self, filesystem: IFileSystem) -> bool:
        """
        Reload the document's content from its path.

        Args:
            filesystem: The filesystem to use for loading

        Returns:
            True if loaded successfully, False otherwise

        Raises:
            ValueError: If the document has no path
        """
        if not self._path:
            raise ValueError("Cannot reload document without a path")

        try:
            self._content.set(filesystem.read_text(str(self._path)))
            self._is_modified = False
            return True
        except Exception:
            # Log the error
            return False
