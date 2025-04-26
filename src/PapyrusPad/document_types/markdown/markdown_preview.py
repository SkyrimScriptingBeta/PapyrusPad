"""Markdown preview capability implementation."""

import markdown
from pygments.formatters import HtmlFormatter
from typing import Callable, override

from PapyrusPad.domain.capability.capability_interface import IPreviewable


class MarkdownPreview(IPreviewable):
    """Markdown preview capability."""

    def __init__(self, document_content_provider: Callable[[], str]):
        """
        Initialize the markdown preview capability.

        Args:
            document_content_provider: A callable that returns the document content
        """
        self._document_content_provider = document_content_provider

    @property
    @override
    def capability_id(self) -> str:
        """Get the capability ID."""
        return "preview"

    @override
    def generate_preview(self) -> str:
        """
        Generate a preview of the markdown content.

        Returns:
            HTML content for preview
        """
        content = self._document_content_provider()

        # Generate CSS for code highlighting
        css: str = HtmlFormatter().get_style_defs(".codehilite")

        # Convert markdown to HTML with extensions
        html = markdown.markdown(
            content,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.codehilite",
            ],
        )

        # Wrap in HTML document with CSS
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; }}
                {css}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
