from pathlib import Path
from assertpy import assert_that

from PapyrusPad.actions.save_action import SaveAction
from PapyrusPad.di.container import get_container
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.dialog.dialog_interface import DialogType


class TestSaveAction:
    """Unit tests for the SaveAction class."""

    def test_save_action_with_active_document(self, dialog_service: FakeDialogService):
        """Test saving an active document with a path."""
        # Arrange
        # Get components from the container
        document_collection = get_container().document_collection()

        # Create a document with a path
        document = document_collection.create(name="test.txt")
        document.path = Path("/test/path.txt")
        document_collection.set_active(document.id)

        # Create a SaveAction instance
        save_action = SaveAction()

        # Act - explicitly pass the dialog service
        save_action.action(False, dialog_service=dialog_service)

        # Assert
        assert not document.is_modified  # Document should be marked as saved
        assert_that(dialog_service.shown_messages).is_empty()

    def test_save_action_with_no_active_document(self, dialog_service: FakeDialogService):
        """Test saving when no document is active."""
        # Arrange
        # Get components from the container
        document_collection = get_container().document_collection()

        # Ensure no document is active
        # First, create a document and make it active
        temp_doc = document_collection.create(name="temp.txt")
        document_collection.set_active(temp_doc.id)
        # Then remove it to leave no active document
        document_collection.remove(temp_doc.id)

        # Create a SaveAction instance
        save_action = SaveAction()

        # Act - explicitly pass the dialog service
        save_action.action(False, dialog_service=dialog_service)

        # Assert
        assert_that(dialog_service.shown_messages).is_length(1)
        assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(dialog_service.shown_messages[0].options.message).is_equal_to("No document is currently active")
        assert_that(dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.WARNING)

    def test_save_action_with_document_no_path(self, dialog_service: FakeDialogService):
        """Test saving a document with no path."""
        # Arrange
        # Get components from the container
        document_collection = get_container().document_collection()

        # Create a document without a path and mark it as modified
        document = document_collection.create(name="untitled.txt")
        document.content = "Some content to make it modified"  # This will mark it as modified
        document.path = None
        document_collection.set_active(document.id)

        # Create a SaveAction instance
        save_action = SaveAction()

        # Act - explicitly pass the dialog service
        save_action.action(False, dialog_service=dialog_service)

        # Assert
        assert_that(dialog_service.shown_messages).is_length(1)
        assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(dialog_service.shown_messages[0].options.message).contains("Save As functionality not yet implemented")
        assert_that(dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.WARNING)
        assert document.is_modified  # Document should still be marked as modified

    def test_save_action_with_save_failure(self, dialog_service: FakeDialogService):
        """Test saving a document when the save operation fails."""
        # Arrange
        # Get components from the container
        document_collection = get_container().document_collection()

        # Create a document that will fail to save and mark it as modified
        document = document_collection.create(name="test.txt")
        document.content = "Some content to make it modified"  # This will mark it as modified
        document.path = Path("/invalid/path/that/does/not/exist.txt")  # Use an invalid path to make save fail
        document_collection.set_active(document.id)

        # Create a SaveAction instance
        save_action = SaveAction()

        # Act - explicitly pass the dialog service
        save_action.action(False, dialog_service=dialog_service)

        # Assert
        assert document.is_modified  # Document should still be marked as modified
        assert_that(dialog_service.shown_messages).is_length(1)
        assert_that(dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(dialog_service.shown_messages[0].options.message).contains("Failed to save document")
        assert_that(dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.ERROR)
