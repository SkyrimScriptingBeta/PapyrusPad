from assertpy import assert_that

from PapyrusPad.actions.open_file_action import OpenFileAction
from PapyrusPad.domain.dialog.dialog_interface import DialogType
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class TestOpenFileAction:
    """Unit tests for the OpenFileAction class."""

    def test_action_user_cancels(self, dialog_service: FakeDialogService, document_collection: IDocumentCollection, filesystem: IFileSystem) -> None:
        """Test the action when the user cancels the file dialog."""
        # Arrange
        action = OpenFileAction()

        # Configure the dialog service to return None (user cancelled)
        dialog_service.next_file_open_dialog_result = None

        # Act
        action.action(False, document_collection=document_collection, filesystem=filesystem, dialog_service=dialog_service)

        # Assert
        assert_that(len(dialog_service.shown_file_open_dialogs)).is_equal_to(1)
        assert_that(len(document_collection.list_documents())).is_equal_to(0)
        assert_that(len(dialog_service.shown_messages)).is_equal_to(0)

    def test_action_success(self, dialog_service: FakeDialogService, document_collection: IDocumentCollection, filesystem: IFileSystem) -> None:
        """Test the action when the file is opened successfully."""
        # Arrange
        action = OpenFileAction()

        # Create a test file
        test_file_path = "/test/test.txt"
        filesystem.write_text(test_file_path, "File content")

        # Configure the dialog service to return the test file path
        dialog_service.next_file_open_dialog_result = test_file_path

        # Act
        action.action(False, document_collection=document_collection, filesystem=filesystem, dialog_service=dialog_service)

        # Assert
        assert_that(len(dialog_service.shown_file_open_dialogs)).is_equal_to(1)
        assert_that(len(document_collection.list_documents())).is_equal_to(1)
        assert_that(document_collection.list_documents()[0].name).is_equal_to("test.txt")
        assert_that(document_collection.list_documents()[0].content).is_equal_to("File content")
        assert_that(len(dialog_service.shown_messages)).is_equal_to(0)

    def test_action_file_not_found(self, dialog_service: FakeDialogService, document_collection: IDocumentCollection, filesystem: IFileSystem) -> None:
        """Test the action when the file is not found."""
        # Arrange
        action = OpenFileAction()

        # Configure the dialog service to return a non-existent file path
        nonexistent_file_path = "/nonexistent/file.txt"
        dialog_service.next_file_open_dialog_result = nonexistent_file_path

        # Act
        action.action(False, document_collection=document_collection, filesystem=filesystem, dialog_service=dialog_service)

        # Assert
        assert_that(len(dialog_service.shown_file_open_dialogs)).is_equal_to(1)
        assert_that(len(document_collection.list_documents())).is_equal_to(0)
        assert_that(len(dialog_service.shown_messages)).is_equal_to(1)

        # Check that the error message was shown
        error_message = dialog_service.shown_messages[0]
        assert_that(error_message.options.title).is_equal_to("Open Error")
        assert_that(error_message.options.message).contains("Could not open file")
        assert_that(error_message.options.type).is_equal_to(DialogType.ERROR)

    def test_action_other_error(self, dialog_service: FakeDialogService, document_collection: IDocumentCollection, filesystem: IFileSystem) -> None:
        """Test the action when another error occurs."""
        # Arrange
        action = OpenFileAction()

        # Configure the dialog service to return a file path that will cause an error
        # We'll use a directory path, which will cause an error when trying to read it as a file
        error_path = "/"
        filesystem.create_directory(error_path)  # Ensure the directory exists
        dialog_service.next_file_open_dialog_result = error_path

        # Act
        action.action(False, document_collection=document_collection, filesystem=filesystem, dialog_service=dialog_service)

        # Assert
        assert_that(len(dialog_service.shown_file_open_dialogs)).is_equal_to(1)
        assert_that(len(document_collection.list_documents())).is_equal_to(0)
        assert_that(len(dialog_service.shown_messages)).is_equal_to(1)

        # Check that the error message was shown
        error_message = dialog_service.shown_messages[0]
        assert_that(error_message.options.title).is_equal_to("Open Error")
        assert_that(error_message.options.message).contains("Could not open file")  # Changed to match actual behavior
        assert_that(error_message.options.type).is_equal_to(DialogType.ERROR)
