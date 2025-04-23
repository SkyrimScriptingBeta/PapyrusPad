from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import uuid
from typing import override, Any

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from qt_helpers.observable_field import ObservableField


@dataclass
class TextDocument(IDocument):
    """A text document implementation of IDocument."""

    _id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _name: Any = field(default_factory=lambda: ObservableField("Untitled"))
    _path: Path | None = None
    _content: Any = field(default_factory=lambda: ObservableField(""))
    _is_modified: bool = False
    _last_saved: datetime | None = None

    def __post_init__(self) -> None:
        """Initialize the document after creation."""
        # Convert string _name to ObservableField if needed
        if isinstance(self._name, str):
            self._name = ObservableField(self._name)

        # Convert string _content to ObservableField if needed
        if isinstance(self._content, str):
            self._content = ObservableField(self._content)

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
        self._name.set(value)
        self._is_modified = True

    @property
    @override
    def name_observable(self) -> ObservableField[str]:
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
            self._is_modified = True

    @property
    @override
    def content_observable(self) -> ObservableField[str]:
        return self._content

    @property
    @override
    def is_modified(self) -> bool:
        return self._is_modified

    @is_modified.setter
    @override
    def is_modified(self, value: bool) -> None:
        self._is_modified = value

    @override
    def mark_saved(self) -> None:
        self._is_modified = False
        self._last_saved = datetime.now()

    @property
    @override
    def last_saved(self) -> datetime | None:
        return self._last_saved

    @property
    @override
    def display_name(self) -> str:
        modified_indicator = "*" if self._is_modified else ""
        return f"{self.name}{modified_indicator}"

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
