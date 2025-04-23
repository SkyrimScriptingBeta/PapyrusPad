from typing import Callable, Any, ParamSpec
from PySide6.QtCore import QObject

from typing import Callable, Generic, ParamSpec, TypeVar, Any
from PySide6.QtCore import QObject

from qt_helpers.signal_typing import GenericSignalHandler

P = ParamSpec("P")
TWidget = TypeVar("TWidget", bound=QObject)


class BindingAdapter(Generic[TWidget, P]):
    def __init__(  # type: ignore
        self,
        signal_getter: Callable[[TWidget], Callable[[GenericSignalHandler[P]], None]],
        setter: Callable[[TWidget, Any], None],
    ) -> None:
        self.signal_getter = signal_getter
        self.setter = setter


from typing import Any

BINDING_REGISTRY: dict[tuple[type[QObject], str], BindingAdapter[Any, Any]] = {}
