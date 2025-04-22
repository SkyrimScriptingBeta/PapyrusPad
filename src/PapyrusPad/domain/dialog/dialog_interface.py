from abc import ABC, abstractmethod
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class DialogType(Enum):
    """Types of dialogs that can be shown."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    QUESTION = auto()


class DialogResult(Enum):
    """Possible results from dialog interactions."""

    OK = auto()
    CANCEL = auto()
    YES = auto()
    NO = auto()


@dataclass
class DialogOptions:
    """Options for configuring a dialog."""

    title: str
    message: str
    type: DialogType = DialogType.INFO
    detail: Optional[str] = None


class IDialogService(ABC):
    """Interface for dialog services that handle user interactions."""

    @abstractmethod
    def show_message(self, options: DialogOptions) -> DialogResult:
        """
        Show a message dialog with OK button.

        Args:
            options: Configuration options for the dialog

        Returns:
            The result of the dialog interaction
        """
        ...

    @abstractmethod
    def show_question(self, options: DialogOptions) -> DialogResult:
        """
        Show a question dialog with Yes/No buttons.

        Args:
            options: Configuration options for the dialog

        Returns:
            The result of the dialog interaction (YES or NO)
        """
        ...

    @abstractmethod
    def show_file_save_dialog(self, title: str, default_path: str = "", filter: str = "") -> str | None:
        """
        Show a file save dialog.

        Args:
            title: The dialog title
            default_path: Optional default path or filename
            filter: Optional file type filter (e.g., "Text files (*.txt);;All files (*)")

        Returns:
            The selected file path, or None if the dialog was cancelled
        """
        ...
