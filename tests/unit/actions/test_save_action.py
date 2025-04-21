from pathlib import Path
from unittest.mock import Mock
from assertpy import assert_that

from PapyrusPad.actions.save_action import SaveAction
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService
from PapyrusPad.domain.dialog.dialog_interface import DialogType
from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem


class TestSaveAction:
    """Unit tests for the SaveAction class."""

    def test_save_action_with_active_document(self):
        """Test saving an active document with a path."""
        # Arrange
        mock_document = Mock(spec=IDocument)
        mock_document.path = Path("/test/path.txt")
        mock_document.name = "test.txt"
        mock_document.save.return_value = True

        mock_document_collection = Mock(spec=IDocumentCollection)
        mock_document_collection.get_active.return_value = mock_document

        mock_filesystem = Mock(spec=IFileSystem)

        fake_dialog_service = FakeDialogService()

        # Create a SaveAction instance and access its action method directly
        save_action = SaveAction()

        # Act
        save_action.action(False, mock_document_collection, mock_filesystem, fake_dialog_service)

        # Assert
        mock_document.save.assert_called_once_with(mock_filesystem)
        assert_that(fake_dialog_service.shown_messages).is_empty()

    def test_save_action_with_no_active_document(self):
        """Test saving when no document is active."""
        # Arrange
        mock_document_collection = Mock(spec=IDocumentCollection)
        mock_document_collection.get_active.return_value = None

        mock_filesystem = Mock(spec=IFileSystem)

        fake_dialog_service = FakeDialogService()

        # Create a SaveAction instance and access its action method directly
        save_action = SaveAction()

        # Act
        save_action.action(False, mock_document_collection, mock_filesystem, fake_dialog_service)

        # Assert
        assert_that(fake_dialog_service.shown_messages).is_length(1)
        assert_that(fake_dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(fake_dialog_service.shown_messages[0].options.message).is_equal_to("No document is currently active")
        assert_that(fake_dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.WARNING)

    def test_save_action_with_document_no_path(self):
        """Test saving a document with no path."""
        # Arrange
        mock_document = Mock(spec=IDocument)
        mock_document.path = None

        mock_document_collection = Mock(spec=IDocumentCollection)
        mock_document_collection.get_active.return_value = mock_document

        mock_filesystem = Mock(spec=IFileSystem)

        fake_dialog_service = FakeDialogService()

        # Create a SaveAction instance and access its action method directly
        save_action = SaveAction()

        # Act
        save_action.action(False, mock_document_collection, mock_filesystem, fake_dialog_service)

        # Assert
        assert_that(fake_dialog_service.shown_messages).is_length(1)
        assert_that(fake_dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(fake_dialog_service.shown_messages[0].options.message).contains("Save As functionality not yet implemented")
        assert_that(fake_dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.WARNING)
        mock_document.save.assert_not_called()

    def test_save_action_with_save_failure(self):
        """Test saving a document when the save operation fails."""
        # Arrange
        mock_document = Mock(spec=IDocument)
        mock_document.path = Path("/test/path.txt")
        mock_document.name = "test.txt"
        mock_document.save.return_value = False

        mock_document_collection = Mock(spec=IDocumentCollection)
        mock_document_collection.get_active.return_value = mock_document

        mock_filesystem = Mock(spec=IFileSystem)

        fake_dialog_service = FakeDialogService()

        # Create a SaveAction instance and access its action method directly
        save_action = SaveAction()

        # Act
        save_action.action(False, mock_document_collection, mock_filesystem, fake_dialog_service)

        # Assert
        mock_document.save.assert_called_once_with(mock_filesystem)
        assert_that(fake_dialog_service.shown_messages).is_length(1)
        assert_that(fake_dialog_service.shown_messages[0].options.title).is_equal_to("Save Error")
        assert_that(fake_dialog_service.shown_messages[0].options.message).contains("Failed to save document")
        assert_that(fake_dialog_service.shown_messages[0].options.type).is_equal_to(DialogType.ERROR)
