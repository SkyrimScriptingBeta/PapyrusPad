from typing import override
from assertpy import assert_that

from PapyrusPad.actions.confirm_action import ConfirmAction
from PapyrusPad.domain.dialog.dialog_interface import DialogResult
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService


# Create a testable subclass of ConfirmAction that tracks if _perform_action was called
class TestableConfirmAction(ConfirmAction):
    """A subclass of ConfirmAction that tracks if _perform_action was called."""

    def __init__(self):
        super().__init__()
        self.action_performed = False

    @override
    def _perform_action(self) -> None:
        """Override to track if the action was performed."""
        self.action_performed = True
        # Call the parent implementation to maintain behavior
        super()._perform_action()


class TestConfirmAction:
    """Unit tests for the ConfirmAction class."""

    def test_confirm_action_when_user_confirms(self, dialog_service: FakeDialogService):
        """Test the confirm action when the user confirms the action."""
        # Arrange
        action = TestableConfirmAction()
        dialog_service.next_question_result = DialogResult.YES

        # Act - dependencies will be resolved from the container
        action.action(False, dialog_service=dialog_service)

        # Assert
        assert action.action_performed  # Check if the action was performed

        # Verify dialog interactions
        assert_that(dialog_service.shown_questions).is_length(1)
        assert_that(dialog_service.shown_questions[0].options.title).is_equal_to("Confirmation")
        assert_that(dialog_service.shown_questions[0].options.message).contains("Are you sure")

        assert_that(dialog_service.shown_messages).is_length(1)
        assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Success")
        assert_that(dialog_service.shown_messages[0].options.message).contains("performed successfully")

    def test_confirm_action_when_user_cancels(self, dialog_service: FakeDialogService):
        """Test the confirm action when the user cancels the action."""
        # Arrange
        action = TestableConfirmAction()
        dialog_service.next_question_result = DialogResult.NO

        # Act - dependencies will be resolved from the container
        action.action(False, dialog_service=dialog_service)

        # Assert
        assert not action.action_performed  # Check that the action was not performed

        # Verify dialog interactions
        assert_that(dialog_service.shown_questions).is_length(1)
        assert_that(dialog_service.shown_questions[0].options.title).is_equal_to("Confirmation")

        assert_that(dialog_service.shown_messages).is_length(1)
        assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Cancelled")
        assert_that(dialog_service.shown_messages[0].options.message).contains("cancelled")
