from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Protocol, Type, TypeVar, runtime_checkable

from PySide6.QtWidgets import QBoxLayout, QWidget

from qt_helpers.setup_functions_mixins import (
    WidgetSetupFunctionsMixin,
)

T = TypeVar("T", bound=QWidget)

Direction = QBoxLayout.Direction


@runtime_checkable
class WidgetWithMixin(Protocol):
    """Protocol representing a QWidget with mixin capabilities"""

    setup: Callable[[], None]
    setup_styles: Callable[[], None]
    setup_events: Callable[[], None]
    setup_signals: Callable[[], None]
    layout: QBoxLayout | None


def widget(
    name: str | None = None,
    classes: list[str] | None = None,
    layout: QBoxLayout.Direction | None = QBoxLayout.Direction.TopToBottom,
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
            (cls, WidgetSetupFunctionsMixin),  # Base classes
            {},  # No new attributes/methods
        )

        original_init = new_cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # Call QWidget's init first
            QWidget.__init__(self)

            # Initialize the mixin
            WidgetSetupFunctionsMixin.__init__(self)

            # Call the original init to set dataclass fields
            if original_init is not QWidget.__init__:
                original_init(self, *args, **kwargs)

            # Now setup the widget
            self.setup()
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
                self.layout = QBoxLayout(layout)
                self.setLayout(self.layout)

                # Add child widgets to layout if requested
                if add_widgets_to_layout:
                    print(f"Adding widgets to layout for {self.__class__.__name__}")
                    for field in fields(new_cls):
                        print(f"Field: {field.name}, Type: {field.type}")
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
