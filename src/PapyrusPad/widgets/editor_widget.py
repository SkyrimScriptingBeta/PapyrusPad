"""Editor widget for PapyrusPad."""

from typing import override
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QWidget

from PapyrusPad.domain.capability.capability_interface import IPreviewable, IRunnable
from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.widgets.capability_buttons_widget import CapabilityButtonsWidget
from PapyrusPad.widgets.header_widget import HeaderWidget
from PapyrusPad.widgets.markdown_preview_widget import MarkdownPreviewWidget
from PapyrusPad.widgets.syntax_highlighter import MarkdownHighlighter, PythonHighlighter
from qt_helpers.bind_fields import bind_fields
from qt_helpers.interfaces import IWidget
from qt_helpers.make import make
from qt_helpers.widget import widget


@widget("editor", layout="vertical")
class EditorWidget(QWidget, IWidget):
    """Editor widget for editing documents."""

    document: IDocument

    # Header section
    header: HeaderWidget = make(HeaderWidget)

    # Capabilities label
    lbl_capabilities: QLabel = make(QLabel)

    # Editor section
    txt_source: QPlainTextEdit = make(QPlainTextEdit)

    # Capability buttons
    capability_buttons: CapabilityButtonsWidget = make(CapabilityButtonsWidget)

    def __init__(self, document: IDocument):
        """Initialize the editor widget."""
        super().__init__()
        self.document = document
        self._highlighter = None

    @override
    def setup(self) -> None:
        """Set up the widget."""
        # Set up header
        self.header.set_title(self.document.name)
        self.header.set_document_type(self.document.document_type)

        # Set up capabilities label
        capabilities = self._get_capability_names()
        self.lbl_capabilities.setText(f"Capabilities: {', '.join(capabilities) if capabilities else 'None'}")

        # Set up editor
        self.txt_source.setPlainText(self.document.content)

        # Apply syntax highlighting based on document type
        self._apply_syntax_highlighting()

        # Set up capability buttons
        self.capability_buttons.update_capabilities(self._get_capability_names())
        self.capability_buttons.set_on_button_click(self._on_capability_button_clicked)

    @override
    def setup_bindings(self) -> None:
        """Set up data bindings."""
        bind_fields([(self.txt_source, "plainText", self.document.content_observable)])
        bind_fields([(self, "windowTitle", self.document.display_name_observable)])

        # Bind document title
        def update_title(title: str) -> None:
            self.header.set_title(title)

        self.document.display_name_observable.on_change(update_title)

        # Bind document type
        def update_document_type(type_id: str) -> None:
            self.header.set_document_type(type_id)
            # Re-apply syntax highlighting when document type changes
            self._apply_syntax_highlighting()
            # Update capability buttons
            self._update_capability_buttons()

        self.document.document_type_observable.on_change(update_document_type)

    def _get_capability_names(self) -> list[str]:
        """Get the names of all capabilities for the current document."""
        if not hasattr(self.document, "get_capability"):
            return []

        # This is a simplified approach - in a real implementation, you would
        # get the capability IDs from the document capability provider
        capabilities = []
        if self.document.has_capability("preview"):
            capabilities.append("preview")
        if self.document.has_capability("run"):
            capabilities.append("run")
        return capabilities

    def _update_capability_buttons(self) -> None:
        """Update capability buttons when document type changes."""
        capabilities = self._get_capability_names()
        self.capability_buttons.update_capabilities(capabilities)
        self.lbl_capabilities.setText(f"Capabilities: {', '.join(capabilities) if capabilities else 'None'}")

    def _on_capability_button_clicked(self, capability_id: str) -> None:
        """Handle capability button clicks."""
        if capability_id == "preview" and self.document.has_capability("preview"):
            preview_capability = self.document.get_capability("preview", IPreviewable)
            if preview_capability:
                html = preview_capability.generate_preview()
                preview_widget = MarkdownPreviewWidget(html)
                preview_widget.show()

        elif capability_id == "run" and self.document.has_capability("run"):
            run_capability = self.document.get_capability("run", IRunnable)
            if run_capability:
                exit_code, stdout, stderr = run_capability.run()
                # In a real implementation, you would show the output in a better way
                print(f"Exit code: {exit_code}")
                print(f"Output: {stdout}")
                if stderr:
                    print(f"Error: {stderr}")

    def _apply_syntax_highlighting(self) -> None:
        """Apply syntax highlighting based on document type."""
        if self.document.document_type == "markdown":
            self._highlighter = MarkdownHighlighter(self.txt_source.document())
        elif self.document.document_type == "python":
            self._highlighter = PythonHighlighter(self.txt_source.document())
