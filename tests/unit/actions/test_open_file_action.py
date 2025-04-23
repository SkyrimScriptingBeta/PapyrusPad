from pathlib import Path
from unittest.mock import Mock
from assertpy import assert_that

from PapyrusPad.actions.open_file_action import OpenFileAction
from PapyrusPad.domain.dialog.dialog_interface import DialogType
from PapyrusPad.domain.document.document_interface import IDocument


class TestOpenFileAction:
    """Unit tests for the OpenFileAction class."""

    def test_action_user_cancels(self) -> None:
        """Test the action when the user cancels the file dialog."""
        # Arrange
        action = OpenFileAction()

        # Create mocks
        mock_dialog_service = Mock()
        mock_document_collection = Mock()
        mock_filesystem = Mock()

        # Configure the dialog service to return None (user cancelled)
        mock_dialog_service.show_file_open_dialog.return_value = None

        # Act
        action.action(False, document_collection=mock_document_collection, filesystem=mock_filesystem, dialog_service=mock_dialog_service)

        # Assert
        mock_dialog_service.show_file_open_dialog.assert_called_once()
        mock_document_collection.open_file.assert_not_called()
        mock_dialog_service.show_message.assert_not_called()

    def test_action_success(self) -> None:
        """Test the action when the file is opened successfully."""
        # Arrange
        action = OpenFileAction()

        # Create mocks
        mock_dialog_service = Mock()
        mock_document_collection = Mock()
        mock_filesystem = Mock()

        # Configure the dialog service to return a file path
        mock_dialog_service.show_file_open_dialog.return_value = "/test/test.txt"

        # Configure the document collection to return a mock document
        mock_document = Mock(spec=IDocument)
        mock_document_collection.open_file.return_value = mock_document

        # Act
        action.action(False, document_collection=mock_document_collection, filesystem=mock_filesystem, dialog_service=mock_dialog_service)

        # Assert
        mock_dialog_service.show_file_open_dialog.assert_called_once()
        mock_document_collection.open_file.assert_called_once_with(Path("/test/test.txt"), mock_filesystem)
        mock_dialog_service.show_message.assert_not_called()

    def test_action_file_not_found(self) -> None:
        """Test the action when the file is not found."""
        # Arrange
        action = OpenFileAction()

        # Create mocks
        mock_dialog_service = Mock()
        mock_document_collection = Mock()
        mock_filesystem = Mock()

        # Configure the dialog service to return a file path
        mock_dialog_service.show_file_open_dialog.return_value = "/test/test.txt"

        # Configure the document collection to raise a FileNotFoundError
        mock_document_collection.open_file.side_effect = FileNotFoundError("File not found")

        # Act
        action.action(False, document_collection=mock_document_collection, filesystem=mock_filesystem, dialog_service=mock_dialog_service)

        # Assert
        mock_dialog_service.show_file_open_dialog.assert_called_once()
        mock_document_collection.open_file.assert_called_once_with(Path("/test/test.txt"), mock_filesystem)
        mock_dialog_service.show_message.assert_called_once()

        # Check that the error message was shown
        args, _ = mock_dialog_service.show_message.call_args
        options = args[0]
        assert_that(options.title).is_equal_to("Open Error")
        assert_that(options.message).contains("Could not open file")
        assert_that(options.type).is_equal_to(DialogType.ERROR)

    def test_action_other_error(self) -> None:
        """Test the action when another error occurs."""
        # Arrange
        action = OpenFileAction()

        # Create mocks
        mock_dialog_service = Mock()
        mock_document_collection = Mock()
        mock_filesystem = Mock()

        # Configure the dialog service to return a file path
        mock_dialog_service.show_file_open_dialog.return_value = "/test/test.txt"

        # Configure the document collection to raise an exception
        mock_document_collection.open_file.side_effect = Exception("Some error")

        # Act
        action.action(False, document_collection=mock_document_collection, filesystem=mock_filesystem, dialog_service=mock_dialog_service)

        # Assert
        mock_dialog_service.show_file_open_dialog.assert_called_once()
        mock_document_collection.open_file.assert_called_once_with(Path("/test/test.txt"), mock_filesystem)
        mock_dialog_service.show_message.assert_called_once()

        # Check that the error message was shown
        args, _ = mock_dialog_service.show_message.call_args
        options = args[0]
        assert_that(options.title).is_equal_to("Open Error")
        assert_that(options.message).contains("Error opening file")
        assert_that(options.detail).is_equal_to("Some error")
        assert_that(options.type).is_equal_to(DialogType.ERROR)
