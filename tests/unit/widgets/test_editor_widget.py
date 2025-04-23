from assertpy import assert_that

from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection
from PapyrusPad.widgets.editor_widget import EditorWidget


class TestEditorWidget:
    """Unit tests for the EditorWidget class."""

    def test_editor_updates_document_when_text_changes(self, document_collection: IDocumentCollection):
        """Test that changes to the editor text update the document content."""
        # Arrange
        document = document_collection.create(name="Test Document", content="")
        editor = EditorWidget(document=document)

        # Act
        editor.txt_source.setPlainText("New content")

        # Assert
        assert_that(document.content).is_equal_to("New content")
        assert_that(document.is_modified).is_true()

    def test_document_updates_editor_when_content_changes(self, document_collection: IDocumentCollection):
        """Test that changes to the document content update the editor text.

        This test is expected to fail with the current implementation because
        there is no binding from document to editor.
        """
        # Arrange
        document = document_collection.create(name="Test Document", content="")
        editor = EditorWidget(document=document)

        # Act
        document.content = "Updated content"

        # Assert - This should fail with the current implementation
        assert_that(editor.txt_source.toPlainText()).is_equal_to("Updated content")
