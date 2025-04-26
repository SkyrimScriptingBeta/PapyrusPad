"""Markdown preview widget."""

from typing import override
from PySide6.QtWidgets import QTextBrowser, QWidget

from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("markdown_preview", layout="vertical")
class MarkdownPreviewWidget(QWidget, IWidget):
    """Widget for displaying markdown preview."""

    browser: QTextBrowser = make(QTextBrowser)

    def __init__(self, html_content: str = ""):
        """
        Initialize the markdown preview widget.

        Args:
            html_content: The HTML content to display
        """
        super().__init__()
        self._html_content = html_content

    @override
    def setup(self) -> None:
        """Set up the widget."""
        self.setWindowTitle("Markdown Preview")
        self.resize(800, 600)

        # Configure browser
        self.browser.setOpenExternalLinks(True)
        self.browser.setHtml(self._html_content)

    def set_html(self, html: str) -> None:
        """
        Set the HTML content to display.

        Args:
            html: The HTML content
        """
        self._html_content = html
        self.browser.setHtml(html)
