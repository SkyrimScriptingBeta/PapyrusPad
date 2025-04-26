"""Text document type implementation."""

from PapyrusPad.domain.document_type.document_type import DocumentType


class TextType:
    """Text document type provider."""

    @staticmethod
    def create() -> DocumentType:
        """
        Create a text document type.

        Returns:
            A text document type
        """
        return DocumentType(type_id="text", display_name="Text", description="Plain text document", extensions=[".txt", ".text"], icon="text-icon")
