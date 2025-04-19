from dataclasses import dataclass, is_dataclass
from typing import Any, Callable, Type, TypeVar

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QBoxLayout, QMainWindow

from qt_helpers.setup_functions_mixins import MainWindowMixin

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

        # Create a new class that inherits from both the original class and the mixin
        new_cls = type(
            cls.__name__,
            (cls, MainWindowMixin),  # Base classes
            {},  # No new attributes/methods
        )

        # Ensure the new class is recognized as a dataclass
        new_cls = dataclass(new_cls)

        original_init = new_cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # Call QMainWindow's init first
            QMainWindow.__init__(self)

            # Initialize the mixin
            MainWindowMixin.__init__(self)

            # Call the original init to set dataclass fields
            # Use super() to avoid direct method calling issues
            if original_init is not QMainWindow.__init__:
                original_init(self, *args, **kwargs)

            # Now setup the window
            # We know these methods exist because of our mixin
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
            if title:
                self.setWindowTitle(title)
            if icon:
                self.setWindowIcon(QPixmap(icon))

            # Set central widget if available
            if hasattr(self, "central_widget") and self.central_widget is not None:
                self.setCentralWidget(self.central_widget)

        # Replace the init method
        new_cls.__init__ = new_init

        return new_cls

    return decorator
