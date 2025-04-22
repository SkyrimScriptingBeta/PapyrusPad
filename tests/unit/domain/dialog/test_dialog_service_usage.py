from assertpy import assert_that

from PapyrusPad.domain.dialog.dialog_interface import DialogOptions, DialogType, DialogResult
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService


def test_dialog_service_fixture_usage(dialog_service: FakeDialogService):
    """Test demonstrating how to use the dialog_service fixture."""
    # Arrange
    dialog_service.next_message_result = DialogResult.OK
    dialog_service.next_question_result = DialogResult.YES

    # Act - Show a message
    result = dialog_service.show_message(DialogOptions(title="Information", message="This is a test message", type=DialogType.INFO))

    # Assert
    assert_that(result).is_equal_to(DialogResult.OK)
    assert_that(dialog_service.shown_messages).is_length(1)
    assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Information")
    assert_that(dialog_service.shown_messages[0].options.message).is_equal_to("This is a test message")
    assert_that(dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.INFO)

    # Act - Show a question
    result = dialog_service.show_question(DialogOptions(title="Confirmation", message="Do you want to proceed?", type=DialogType.QUESTION))

    # Assert
    assert_that(result).is_equal_to(DialogResult.YES)
    assert_that(dialog_service.shown_questions).is_length(1)
    assert_that(dialog_service.shown_questions[0].options.title).is_equal_to("Confirmation")
    assert_that(dialog_service.shown_questions[0].options.message).is_equal_to("Do you want to proceed?")
    assert_that(dialog_service.shown_questions[0].options.type).is_equal_to(DialogType.QUESTION)


def test_dialog_service_reset(dialog_service: FakeDialogService):
    """Test that the dialog_service fixture resets between tests."""
    # This test should start with a fresh dialog_service
    # even though the previous test used it

    assert_that(dialog_service.shown_messages).is_empty()
    assert_that(dialog_service.shown_questions).is_empty()

    # Default return values should be reset
    assert_that(dialog_service.next_message_result).is_equal_to(DialogResult.OK)
    assert_that(dialog_service.next_question_result).is_equal_to(DialogResult.NO)
