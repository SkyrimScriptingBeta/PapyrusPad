"""Markdown capabilities factory."""

from typing import Callable

from PapyrusPad.domain.capability.capability_interface import IPreviewable
from .markdown_preview import MarkdownPreview


class MarkdownCapabilities:
    """Factory for markdown document capabilities."""

    @staticmethod
    def create_preview(document_content_provider: Callable[[], str]) -> IPreviewable:
        """
        Create a markdown preview capability.

        Args:
            document_content_provider: A callable that returns the document content

        Returns:
            A markdown preview capability
        """
        return MarkdownPreview(document_content_provider)
