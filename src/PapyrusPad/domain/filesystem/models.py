from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class FileInfo:
    """
    Immutable value object representing file information.
    """

    path: str
    name: str
    extension: str
    size: int
    last_modified: datetime
    is_readonly: bool = False


@dataclass(frozen=True)
class DirectoryInfo:
    """
    Immutable value object representing directory information.
    """

    path: str
    name: str
    last_modified: datetime
