from dataclasses import dataclass
from typing import List, override

from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogResult


@dataclass
class DialogRecord:
    """Record of a dialog that was shown."""

    options: DialogOptions
    result: DialogResult


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

        # Configure default returns
        self.next_message_result = DialogResult.OK
        self.next_question_result = DialogResult.NO

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

    def reset(self):
        """Reset all recorded interactions and default return values."""
        self.shown_messages.clear()
        self.shown_questions.clear()
        self.next_message_result = DialogResult.OK
        self.next_question_result = DialogResult.NO
