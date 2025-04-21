from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import uuid
from typing import override

from PapyrusPad.domain.document.document_interface import IDocument


@dataclass
class TextDocument(IDocument):
    """A text document implementation of IDocument."""

    _id: str = field(default_factory=lambda: str(uuid.uuid4()))
    _name: str = "Untitled"
    _path: Path | None = None
    _content: str = ""
    _is_modified: bool = False
    _last_saved: datetime | None = None

    @property
    @override
    def id(self) -> str:
        return self._id

    @property
    @override
    def name(self) -> str:
        return self._name

    @name.setter
    @override
    def name(self, value: str) -> None:
        self._name = value
        self._is_modified = True

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
        return self._content

    @content.setter
    @override
    def content(self, value: str) -> None:
        if self._content != value:
            self._content = value
            self._is_modified = True

    @property
    @override
    def is_modified(self) -> bool:
        return self._is_modified

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
        return f"{self._name}{modified_indicator}"
