from dataclasses import dataclass, is_dataclass
from typing import Callable, Type, TypeVar, cast

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QBoxLayout, QMainWindow

from qt_helpers.setup_functions_mixins import MainWindowSetupFunctionsMixin

T = TypeVar("T", bound=QMainWindow)

Direction = QBoxLayout.Direction


def window(
    name: str | None = None,
    classes: list[str] | None = None,
    *,
    title: str | None = None,
    icon: str | None = None,
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        # First make original class a dataclass if it's not already
        if not is_dataclass(cls):
            cls = dataclass(cls)

        # Store original __init__ methods
        original_init = cls.__init__
        mixin_init = MainWindowSetupFunctionsMixin.__init__

        # Create a new class that inherits from both the original class and the mixin
        # We use type() to dynamically create a new class
        new_cls = type(
            cls.__name__,
            (cls, MainWindowSetupFunctionsMixin),  # Base classes
            {},  # No new attributes/methods
        )

        # Store original post_init if it exists
        original_post_init = getattr(new_cls, "__post_init__", None)

        def new_post_init(self: T) -> None:
            # Properly initialize QMainWindow first
            QMainWindow.__init__(self)

            # Initialize the mixin with its default values
            mixin_init(self)  # This will set central_widget=None by default

            # Now call the original class's __init__ to populate any dataclass fields
            # Pass args/kwargs to support custom initialization parameters
            original_init(self, *args, **kwargs)

            # Cast for type safety, but without requiring inheritance
            self_typed = cast(MainWindowSetupFunctionsMixin, self)

            # Run original post_init if it exists
            if original_post_init is not None:
                original_post_init(self)

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
            if title:
                self.setWindowTitle(title)
            if icon:
                self.setWindowIcon(QPixmap(icon))
            if self_typed.central_widget is not None:
                self.setCentralWidget(self_typed.central_widget)

        new_cls.__post_init__ = new_post_init

        return new_cls

    return decorator
