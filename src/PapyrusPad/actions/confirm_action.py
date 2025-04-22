from typing import override
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QStyle

from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.dialog.dialog_interface import IDialogService, DialogOptions, DialogType, DialogResult
from qt_helpers.action import action
from qt_helpers.interfaces import IAction


@action("Confirm", tooltip="Confirm an action", icon=QStyle.StandardPixmap.SP_DialogApplyButton)
class ConfirmAction(QAction, IAction):
    """Example action that uses the dialog service to confirm an operation."""

    @override
    def action(
        self,
        checked: bool,
        dialog_service: IDialogService = Depends[IDialogService],
    ) -> None:
        """
        Show a confirmation dialog and perform an action based on the result.

        Args:
            checked: Whether the action is checked (not used)
            dialog_service: The dialog service
        """
        # Show a confirmation dialog
        result = dialog_service.show_question(
            DialogOptions(title="Confirmation", message="Are you sure you want to perform this action?", type=DialogType.QUESTION, detail="This action cannot be undone.")
        )

        # Perform the action if the user confirmed
        if result == DialogResult.YES:
            self._perform_action()
            dialog_service.show_message(DialogOptions(title="Success", message="The action was performed successfully.", type=DialogType.INFO))
        else:
            dialog_service.show_message(DialogOptions(title="Cancelled", message="The action was cancelled.", type=DialogType.INFO))

    def _perform_action(self) -> None:
        """Perform the actual action. This is a placeholder for real functionality."""
        # In a real implementation, this would do something meaningful
        print("Performing the action...")
