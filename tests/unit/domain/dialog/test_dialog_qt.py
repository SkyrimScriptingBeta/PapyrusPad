from unittest.mock import patch, MagicMock
from assertpy import assert_that
from PySide6.QtWidgets import QMessageBox

from PapyrusPad.domain.dialog.dialog_interface import DialogOptions, DialogType, DialogResult
from PapyrusPad.domain.dialog.dialog_qt import QtDialogService


class TestQtDialogService:
    """Unit tests for the QtDialogService class."""

    @patch("PapyrusPad.domain.dialog.dialog_qt.QMessageBox")
    def test_show_message_creates_correct_messagebox(self, mock_qmessagebox):
        """Test that show_message creates a QMessageBox with the correct properties."""
        # Arrange
        mock_box_instance = MagicMock()
        mock_qmessagebox.return_value = mock_box_instance

        service = QtDialogService()
        options = DialogOptions(title="Test Title", message="Test Message", type=DialogType.WARNING, detail="Additional details")

        # Act
        result = service.show_message(options)

        # Assert
        mock_qmessagebox.assert_called_once()
        mock_box_instance.setText.assert_called_once_with("Test Message")
        mock_box_instance.setWindowTitle.assert_called_once_with("Test Title")
        mock_box_instance.setInformativeText.assert_called_once_with("Additional details")
        mock_box_instance.setIcon.assert_called_once_with(QMessageBox.Icon.Warning)
        mock_box_instance.setStandardButtons.assert_called_once_with(QMessageBox.StandardButton.Ok)
        mock_box_instance.exec.assert_called_once()
        assert_that(result).is_equal_to(DialogResult.OK)

    @patch("PapyrusPad.domain.dialog.dialog_qt.QMessageBox")
    def test_show_question_returns_yes_when_user_clicks_yes(self, mock_qmessagebox):
        """Test that show_question returns YES when the user clicks Yes."""
        # Arrange
        mock_box_instance = MagicMock()
        mock_qmessagebox.return_value = mock_box_instance
        # Simulate user clicking "Yes"
        mock_box_instance.exec.return_value = QMessageBox.StandardButton.Yes

        service = QtDialogService()
        options = DialogOptions(title="Confirm", message="Are you sure?", type=DialogType.QUESTION)

        # Act
        result = service.show_question(options)

        # Assert
        assert_that(result).is_equal_to(DialogResult.YES)
        mock_box_instance.setStandardButtons.assert_called_once_with(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        mock_box_instance.setDefaultButton.assert_called_once_with(QMessageBox.StandardButton.No)

    @patch("PapyrusPad.domain.dialog.dialog_qt.QMessageBox")
    def test_show_question_returns_no_when_user_clicks_no(self, mock_qmessagebox):
        """Test that show_question returns NO when the user clicks No."""
        # Arrange
        mock_box_instance = MagicMock()
        mock_qmessagebox.return_value = mock_box_instance
        # Simulate user clicking "No"
        mock_box_instance.exec.return_value = QMessageBox.StandardButton.No

        service = QtDialogService()
        options = DialogOptions(title="Confirm", message="Are you sure?", type=DialogType.QUESTION)

        # Act
        result = service.show_question(options)

        # Assert
        assert_that(result).is_equal_to(DialogResult.NO)
