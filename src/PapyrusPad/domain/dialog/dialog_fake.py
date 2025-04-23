from dataclasses import dataclass
from typing import List, override

from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogResult


@dataclass
class DialogRecord:
    """Record of a dialog that was shown."""

    options: DialogOptions
    result: DialogResult


@dataclass
class FileDialogRecord:
    """Record of a file dialog that was shown."""

    title: str
    default_path: str
    filter: str
    result: str | None


class FakeDialogService(IDialogService):
    """
    Fake implementation of the dialog service for testing.

    This implementation doesn't show any actual dialogs but records
    all interactions and returns pre-configured results.
    """

    def __init__(self):
        super().__init__()
        self.shown_messages: List[DialogRecord] = []
        self.shown_questions: List[DialogRecord] = []
        self.shown_file_save_dialogs: List[FileDialogRecord] = []
        self.shown_file_open_dialogs: List[FileDialogRecord] = []

        # Configure default returns
        self.next_message_result = DialogResult.OK
        self.next_question_result = DialogResult.NO
        self.next_file_save_dialog_result: str | None = None
        self.next_file_open_dialog_result: str | None = None

    @override
    def show_message(self, options: DialogOptions) -> DialogResult:
        """
        Record a message dialog interaction without showing an actual dialog.

        Args:
            options: Configuration options for the dialog

        Returns:
            The pre-configured result (default: DialogResult.OK)
        """
        record = DialogRecord(options=options, result=self.next_message_result)
        self.shown_messages.append(record)
        return self.next_message_result

    @override
    def show_question(self, options: DialogOptions) -> DialogResult:
        """
        Record a question dialog interaction without showing an actual dialog.

        Args:
            options: Configuration options for the dialog

        Returns:
            The pre-configured result (default: DialogResult.NO)
        """
        record = DialogRecord(options=options, result=self.next_question_result)
        self.shown_questions.append(record)
        return self.next_question_result

    @override
    def show_file_save_dialog(self, title: str, default_path: str = "", filter: str = "") -> str | None:
        """
        Record a file save dialog interaction without showing an actual dialog.

        Args:
            title: The dialog title
            default_path: Optional default path or filename
            filter: Optional file type filter

        Returns:
            The pre-configured result (default: None)
        """
        record = FileDialogRecord(title=title, default_path=default_path, filter=filter, result=self.next_file_save_dialog_result)
        self.shown_file_save_dialogs.append(record)
        return self.next_file_save_dialog_result

    @override
    def show_file_open_dialog(self, title: str, default_path: str = "", filter: str = "") -> str | None:
        """
        Record a file open dialog interaction without showing an actual dialog.

        Args:
            title: The dialog title
            default_path: Optional default path or directory
            filter: Optional file type filter

        Returns:
            The pre-configured result (default: None)
        """
        record = FileDialogRecord(title=title, default_path=default_path, filter=filter, result=self.next_file_open_dialog_result)
        self.shown_file_open_dialogs.append(record)
        return self.next_file_open_dialog_result

    def reset(self):
        """Reset all recorded interactions and default return values."""
        self.shown_messages.clear()
        self.shown_questions.clear()
        self.shown_file_save_dialogs.clear()
        self.shown_file_open_dialogs.clear()
        self.next_message_result = DialogResult.OK
        self.next_question_result = DialogResult.NO
        self.next_file_save_dialog_result = None
        self.next_file_open_dialog_result = None
