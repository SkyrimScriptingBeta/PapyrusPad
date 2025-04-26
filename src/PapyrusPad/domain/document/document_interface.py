from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from qt_helpers.observable_field import Observable


class IDocument(ABC):
    """Represents a document open in the editor."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for this document (not the file path)."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name for UI (e.g., filename or 'Untitled')."""
        ...

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None: ...

    @property
    @abstractmethod
    def name_observable(self) -> Observable[str]: ...

    @property
    @abstractmethod
    def path(self) -> Path | None:
        """Path on disk, or None if unsaved."""
        ...

    @path.setter
    @abstractmethod
    def path(self, value: Path | None) -> None: ...

    @property
    @abstractmethod
    def content(self) -> str:
        """Current text content of the document."""
        ...

    @content.setter
    @abstractmethod
    def content(self, value: str) -> None: ...

    @property
    @abstractmethod
    def content_observable(self) -> Observable[str]: ...

    @property
    @abstractmethod
    def is_modified(self) -> bool:
        """True if modified since last save."""
        ...

    @is_modified.setter
    @abstractmethod
    def is_modified(self, value: bool) -> None:
        """Set modified state."""
        ...

    @abstractmethod
    def mark_saved(self) -> None:
        """Reset modified state and update last_saved timestamp."""
        ...

    @property
    @abstractmethod
    def last_saved(self) -> datetime | None:
        """Time of last save. None if never saved."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Name for tab or sidebar display, may include '*' if modified."""
        ...

    @property
    @abstractmethod
    def display_name_observable(self) -> Observable[str]:
        """Observable for display name."""
        ...

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...
