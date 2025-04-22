from dataclasses import dataclass, is_dataclass
from typing import Any, Callable, Type, TypeVar, dataclass_transform

from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QStyle

from qt_helpers.mixins import ActionMixin
from qt_helpers.signal_typing import as_bool_handler

T = TypeVar("T", bound=QAction)


@dataclass_transform()
def action(
    text: str | None = None, *, shortcut: str | None = None, tooltip: str | None = None, icon: QPixmap | QIcon | QStyle.StandardPixmap | str | None = None
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        print(f"Decorating {cls.__name__} with action mixin")

        # First make original class a dataclass if it's not already
        if not is_dataclass(cls):
            cls = dataclass(cls)

        # Create a new class that inherits from both the original class and the mixin
        new_cls = type(
            cls.__name__,
            (cls, ActionMixin),  # Base classes
            {},  # No new attributes/methods
        )

        # Ensure the new class is recognized as a dataclass
        new_cls = dataclass(new_cls)

        original_init = new_cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            # Call QAction's init first
            QAction.__init__(self, parent=None)

            # Initialize the mixin
            ActionMixin.__init__(self)

            # Call the original init to set dataclass fields
            if original_init is not QAction.__init__:
                original_init(self, *args, **kwargs)

            # Apply additional configurations
            if self._text:
                self.setText(self._text)
            elif text:
                self.setText(text)
                self._text = text

            if self._shortcut:
                self.setShortcut(self._shortcut)
            elif shortcut:
                self.setShortcut(shortcut)
                self._shortcut = shortcut

            if self._tooltip:
                self.setStatusTip(self._tooltip)
            elif tooltip:
                self.setStatusTip(tooltip)
                self._tooltip = tooltip

            # if self._icon:
            #     if isinstance(self._icon, str):
            #         self.setIcon(QIcon(self._icon))
            #     elif isinstance(self._icon, (QPixmap, QIcon)):
            #         self.setIcon(self._icon)
            #     else:
            #         self.setIcon(app.style().standardIcon(self._icon))
            # elif icon:
            #     if isinstance(icon, str):
            #         self.setIcon(QIcon(icon))
            #     elif isinstance(icon, (QPixmap, QIcon)):
            #         self.setIcon(icon)
            #     else:
            #         self.setIcon(app.style().standardIcon(icon))
            #     self._icon = icon

            self.triggered.connect(as_bool_handler(lambda checked: self.action(checked)))

        # Replace the init method
        new_cls.__init__ = new_init

        return new_cls

    return decorator
