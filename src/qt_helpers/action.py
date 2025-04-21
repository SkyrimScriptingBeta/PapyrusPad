from dataclasses import dataclass, is_dataclass
from typing import Any, Callable, Type, TypeVar, dataclass_transform

from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QStyle

from PapyrusPad.app.app_instance import app

T = TypeVar("T", bound=QAction)


@dataclass_transform()
def action(
    text: str | None = None, *, shortcut: str | None = None, tooltip: str | None = None, icon: QPixmap | QIcon | QStyle.StandardPixmap | str | None = None
) -> Callable[[Type[T]], Type[T]]:
    def decorator(cls: Type[T]) -> Type[T]:
        if not is_dataclass(cls):
            cls = dataclass(cls)

        original_init = cls.__init__

        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            QAction.__init__(self, parent=None)
            if original_init is not QAction.__init__:
                original_init(self, *args, **kwargs)

            if text:
                self.setText(text)
            if shortcut:
                self.setShortcut(shortcut)
            if tooltip:
                self.setStatusTip(tooltip)
            if icon:
                if isinstance(icon, str):
                    self.setIcon(QIcon(icon))
                elif isinstance(icon, QPixmap) or isinstance(icon, QIcon):
                    self.setIcon(icon)
                else:
                    self.setIcon(app.style().standardIcon(icon))

            # Connect default action method if defined
            if hasattr(self, "action") and callable(getattr(self, "action")):
                self.triggered.connect(self.action)

        cls.__init__ = new_init
        return cls

    return decorator
