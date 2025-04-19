from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Type, TypeVar

from PySide6.QtWidgets import QBoxLayout, QWidget

from qt_helpers.setup_functions_mixins import (
    WidgetMixin,
)

T = TypeVar("T", bound=QWidget)

Direction = QBoxLayout.Direction


def widget(
    name: str | None = None,
    classes: list[str] | None = None,
    layout: QBoxLayout.Direction | str | None = QBoxLayout.Direction.TopToBottom,
    *,
    add_widgets_to_layout: bool = True,
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        # First make original class a dataclass if it's not already
        if not is_dataclass(cls):
            cls = dataclass(cls)

        # Create a new class that inherits from both the original class and the mixin
        new_cls = type(
            cls.__name__,
            (cls, WidgetMixin),  # Base classes
            {},  # No new attributes/methods
        )

        # Ensure the new class is recognized as a dataclass
        new_cls = dataclass(new_cls)

        original_init = new_cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # Call QWidget's init first
            QWidget.__init__(self)

            # Initialize the mixin
            WidgetMixin.__init__(self)

            # Call the original init to set dataclass fields
            if original_init is not QWidget.__init__:
                original_init(self, *args, **kwargs)

            # Now setup the widget
            self.setup()
            self.setup_layout()
            self.setup_styles()
            self.setup_events()
            self.setup_signals()

            # Apply additional configurations
            if name:
                self.setObjectName(name)
            if classes:
                self.setProperty("class", f"|{'|'.join(classes)}|")

            # Set up layout if requested
            if layout is not None:
                # Convert string layout names to QBoxLayout.Direction
                layout_direction: QBoxLayout.Direction
                if isinstance(layout, str):
                    # Handle string layout names
                    if layout.lower() == "horizontal":
                        layout_direction = QBoxLayout.Direction.LeftToRight
                    elif layout.lower() == "vertical":
                        layout_direction = QBoxLayout.Direction.TopToBottom
                    else:
                        # Default to vertical for unrecognized strings
                        layout_direction = QBoxLayout.Direction.TopToBottom
                else:
                    # It's already a QBoxLayout.Direction
                    layout_direction = layout

                # Create and set the layout
                self.layout = QBoxLayout(layout_direction)
                self.setLayout(self.layout)

                # Add child widgets to layout if requested
                if add_widgets_to_layout:
                    # Get fields from the dataclass
                    for field in fields(self.__class__):
                        if isinstance(field.type, type) and issubclass(
                            field.type, QWidget
                        ):
                            widget_instance = getattr(self, field.name, None)
                            if widget_instance is not None:
                                self.layout.addWidget(widget_instance)

        # Replace the init method
        new_cls.__init__ = new_init

        return new_cls

    return decorator
