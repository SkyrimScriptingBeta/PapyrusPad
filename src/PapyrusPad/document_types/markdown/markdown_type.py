"""Markdown document type implementation."""

from PapyrusPad.domain.document_type.document_type import DocumentType


class MarkdownType:
    """Markdown document type provider."""

    @staticmethod
    def create() -> DocumentType:
        """
        Create a markdown document type.

        Returns:
            A markdown document type
        """
        return DocumentType(type_id="markdown", display_name="Markdown", description="Markdown document", extensions=[".md", ".markdown"], icon="markdown-icon")
