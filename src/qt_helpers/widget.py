from dataclasses import dataclass, fields
from typing import Callable, Type, TypeVar, cast

from PySide6.QtWidgets import QBoxLayout, QWidget

from qt_helpers.setup_functions_mixins import (
    WidgetSetupFunctionsMixin,
)

T = TypeVar("T", bound=QWidget)

Direction = QBoxLayout.Direction


def widget(
    name: str | None = None,
    classes: list[str] | None = None,
    layout: QBoxLayout.Direction | None = QBoxLayout.Direction.TopToBottom,
    *,
    # title: str | None = None,
    add_widgets_to_layout: bool = True,
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        # Create a new class that inherits from both the original class and the mixin
        # We use type() to dynamically create a new class
        new_cls = type(
            cls.__name__,
            (cls, WidgetSetupFunctionsMixin),  # Base classes
            {},  # No new attributes/methods
        )

        def new_post_init(self: T) -> None:
            derived_from = cls.__bases__[0]
            derived_from.__init__(self)

            # Cast for type safety, but without requiring inheritance
            self_typed = cast(WidgetSetupFunctionsMixin, self)

            # Call lifecycle methods
            self_typed.setup()
            self_typed.setup_styles()
            self_typed.setup_events()
            self_typed.setup_signals()

            # Apply additional configurations
            if name:
                self.setObjectName(name)
            if classes:
                self.setProperty("class", f"|{'|'.join(classes)}|")
            if layout is not None:
                self_typed.layout = QBoxLayout(layout)
                self.setLayout(self_typed.layout)
                if add_widgets_to_layout:
                    for field in fields(new_cls):
                        if isinstance(field.type, type) and issubclass(
                            field.type, QWidget
                        ):
                            widget_instance = getattr(self, field.name)
                            if widget_instance is not None:
                                self_typed.layout.addWidget(widget_instance)

        new_cls.__post_init__ = new_post_init  # type: ignore[attr-defined]

        return dataclass(new_cls)  # type: ignore[no-untyped-call]

    return decorator
