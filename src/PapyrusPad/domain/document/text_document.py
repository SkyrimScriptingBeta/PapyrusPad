from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import uuid
from typing import override

from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from qt_helpers.observable_field import ObservableField


@dataclass
class TextDocument(IDocument):
    """A text document implementation of IDocument."""

    _id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _name: ObservableField[str] = field(default_factory=lambda: ObservableField("Untitled"))
    _display_name_observable: ObservableField[str] = field(default_factory=lambda: ObservableField("Untitled"))
    _path: Path | None = None
    _content: ObservableField[str] = field(default_factory=lambda: ObservableField(""))
    _is_modified: bool = False
    _last_saved: datetime | None = None

    def __post_init__(self) -> None:
        print("START __post_init")
        self._update_display_name()
        self.content_observable.bind(self._on_content_changed)
        self.name_observable.bind(self._on_name_changed)
        self._is_modified = False
        print("END __post_init")

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
        print("--> Content changed")
        self.is_modified = True

    def _on_name_changed(self, value: str) -> None:
        print("--> Name changed")
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
        print("A")
        if self._content.get() != value:
            print("B")
            self._content.set(value)
            self.is_modified = True

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
        print("-----------> Updating display name")
        modified_indicator = "*" if self.is_modified else ""
        text = f"{self.name}{modified_indicator}"
        print(f"Setting display name to: {text}")
        self._display_name_observable.set_if_changed(text)
        print(f"SET - Display name updated to: {text}")

    @property
    @override
    def display_name_observable(self) -> ObservableField[str]:
        return self._display_name_observable

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
