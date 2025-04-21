from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Callable, Type, TypeVar, dataclass_transform

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from qt_helpers.mixins import MenuMixin

T = TypeVar("T", bound=QMenu)


@dataclass_transform()
def menu(name: str | None = None) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        print(f"Decorating {cls.__name__} with menu mixin")

        # First make original class a dataclass if it's not already
        if not is_dataclass(cls):
            cls = dataclass(cls)

        # Create a new class that inherits from both the original class and the mixin
        new_cls = type(
            cls.__name__,
            (cls, MenuMixin),  # Base classes
            {},  # No new attributes/methods
        )

        # Ensure the new class is recognized as a dataclass
        new_cls = dataclass(new_cls)

        original_init = new_cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # Call QMenu's init first
            QMenu.__init__(self)

            # Initialize the mixin
            MenuMixin.__init__(self)

            # Call the original init to set dataclass fields
            if original_init is not QMenu.__init__:
                original_init(self, *args, **kwargs)

            # Add submenus and actions
            for field in fields(self.__class__):
                field_instance = getattr(self, field.name, None)
                if isinstance(field_instance, QMenu):
                    self.addMenu(field_instance)
                elif isinstance(field_instance, QAction):
                    self.addAction(field_instance)

            # Set the menu title if provided
            if name:
                self.setTitle(name)

        # Replace the init method
        new_cls.__init__ = new_init

        return new_cls

    return decorator
