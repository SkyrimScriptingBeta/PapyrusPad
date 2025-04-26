"""Header widget for displaying document information."""

from typing import override
from PySide6.QtWidgets import QLabel, QSizePolicy, QWidget

from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("header_widget", layout="horizontal")
class HeaderWidget(QWidget, IWidget):
    """Widget for displaying document header information."""

    # Left side - document title
    lbl_title: QLabel = make(QLabel)

    # Right side - document type
    lbl_document_type: QLabel = make(QLabel)

    _title: str = ""
    _document_type: str = ""

    def __init__(self):
        """Initialize the header widget."""
        super().__init__()

    # Spacer to push document type to the right
    spacer: QWidget = make(QWidget)

    @override
    def setup(self) -> None:
        """Set up the widget."""
        # Set up labels
        self.lbl_title.setText(self._title)
        self.lbl_document_type.setText(f"Type: {self._document_type}")

        # Configure spacer
        self.spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def set_title(self, title: str) -> None:
        """
        Set the document title.

        Args:
            title: The document title
        """
        self._title = title
        self.lbl_title.setText(title)

    def set_document_type(self, document_type: str) -> None:
        """
        Set the document type.

        Args:
            document_type: The document type
        """
        self._document_type = document_type
        self.lbl_document_type.setText(f"Type: {document_type}")
