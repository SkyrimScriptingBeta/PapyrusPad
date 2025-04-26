"""Widget for displaying capability buttons."""

from dataclasses import field
from typing import Callable, override
from PySide6.QtWidgets import QPushButton, QWidget

from qt_helpers.interfaces import IWidget
from qt_helpers.widget import widget


@widget("capability_buttons", layout="horizontal")
class CapabilityButtonsWidget(QWidget, IWidget):
    """Widget for displaying capability buttons."""

    _capabilities: list[str] = field(default_factory=list)
    _on_button_click: Callable[[str], None] | None = None
    _buttons: list[QPushButton] = field(default_factory=list)

    @override
    def setup_layout(self) -> None:
        self._create_buttons()

    def _create_buttons(self) -> None:
        print("Creating buttons")

        # Clear existing buttons
        for button in self._buttons:
            if button.parent() == self:
                button.deleteLater()
        self._buttons = []

        # Create new buttons
        for capability in self._capabilities:
            button = QPushButton(capability.capitalize(), self)
            button.clicked.connect(lambda checked=False, cap=capability: self._handle_button_click(cap))
            self._buttons.append(button)
            layout = self.layout()
            if layout is not None:
                layout.addWidget(button)

    def _handle_button_click(self, capability: str) -> None:
        """
        Handle button click.

        Args:
            capability: The capability name
        """
        if self._on_button_click:
            self._on_button_click(capability)

    def set_on_button_click(self, callback: Callable[[str], None]) -> None:
        """
        Set the button click callback.

        Args:
            callback: The callback function
        """
        self._on_button_click = callback

    def update_capabilities(self, capabilities: list[str]) -> None:
        """
        Update the capability buttons.

        Args:
            capabilities: List of capability names
        """
        self._capabilities = capabilities
        self._create_buttons()
