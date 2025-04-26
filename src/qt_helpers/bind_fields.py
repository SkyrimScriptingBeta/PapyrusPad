from typing import Any
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLabel, QLineEdit, QCheckBox, QPlainTextEdit, QWidget
from typing import Callable, ParamSpec, TypeVar

from qt_helpers.signal_typing import GenericSignalHandler

from typing import Callable, ParamSpec, TypeVar
from PySide6.QtCore import QObject
from PySide6.QtCore import QObject


from typing import Any
from PySide6.QtCore import QObject
from qt_helpers.observable import Observable

from typing import Callable, Any, ParamSpec
from PySide6.QtCore import QObject

from typing import Callable, Generic, ParamSpec, TypeVar, Any
from PySide6.QtCore import QObject

from qt_helpers.signal_typing import GenericSignalHandler
from typing import Any

P = ParamSpec("P")
TWidget = TypeVar("TWidget", bound=QObject)


class BindingAdapter(Generic[TWidget, P]):
    def __init__(  # type: ignore
        self,
        signal_getter: Callable[[TWidget], Callable[[GenericSignalHandler[P]], None]] | None = None,
        setter: Callable[[TWidget, Any], None] | None = None,
    ) -> None:
        self.signal_getter = signal_getter
        self.setter = setter


BINDING_REGISTRY: dict[tuple[type[QObject], str], BindingAdapter[Any, Any]] = {}


def bind_fields(bindings: list[tuple[QObject, str, Observable[Any]]]) -> None:
    for widget, prop, observable in bindings:
        adapter = None
        widget_type = type(widget)

        # Walk the parent inheritance tree
        for cls in widget_type.mro():
            adapter = BINDING_REGISTRY.get((cls, prop))
            if adapter:
                break

        if adapter is None:
            raise ValueError(f"No binding registered for {widget_type.__name__}.{prop}")

        lock = False

        # UI → Model
        def update_model(value: Any) -> None:
            nonlocal lock
            if not lock:
                lock = True
                observable.set(value)
                lock = False

        if adapter.signal_getter:
            adapter.signal_getter(widget)(update_model)

        # Model → UI
        def update_ui(value: Any) -> None:
            nonlocal lock
            if not lock:
                lock = True
                if adapter and adapter.setter:
                    adapter.setter(widget, value)
                lock = False

        observable.on_change(update_ui)

        # Call the update_ui function once to initialize the UI with the current value
        update_ui(observable.get())


def make_signal_getter_for(signal_name: str, _widget_type: type[TWidget]) -> Callable[[TWidget], Callable[[GenericSignalHandler[P]], None]]:  # For type checking purposes
    def getter(widget: TWidget) -> Callable[[GenericSignalHandler[P]], None]:
        signal = getattr(widget, signal_name)

        def connect_wrapper(handler: GenericSignalHandler[P]) -> None:
            signal.connect(handler)

        return connect_wrapper

    return getter


def make_signal_getter_for_no_arg[TWidget](signal_name: str, getter: Callable[[TWidget], str]) -> Callable[[TWidget], Callable[[Callable[[str], None]], None]]:
    def signal_getter(widget: TWidget) -> Callable[[Callable[[str], None]], None]:
        signal = getattr(widget, signal_name)

        def connect_wrapper(handler: Callable[[str], None]) -> None:
            def on_signal() -> None:
                handler(getter(widget))  # pull value manually

            signal.connect(on_signal)

        return connect_wrapper

    return signal_getter


BINDING_REGISTRY[(QCheckBox, "checked")] = BindingAdapter[QCheckBox, [bool]](
    signal_getter=make_signal_getter_for("toggled", QCheckBox),
    setter=lambda w, val: w.setChecked(val),
)

BINDING_REGISTRY[(QLineEdit, "text")] = BindingAdapter[QLineEdit, [str]](
    signal_getter=make_signal_getter_for("textChanged", QLineEdit),
    setter=lambda w, val: w.setText(val),
)

BINDING_REGISTRY[(QPlainTextEdit, "plainText")] = BindingAdapter[QPlainTextEdit, [str]](
    signal_getter=make_signal_getter_for_no_arg("textChanged", lambda w: w.toPlainText()),
    setter=lambda w, val: w.setPlainText(val),
)

BINDING_REGISTRY[(QWidget, "windowTitle")] = BindingAdapter[QWidget, [str]](
    setter=lambda w, val: w.setWindowTitle(val),
)

BINDING_REGISTRY[(QLabel, "text")] = BindingAdapter[QLabel, [str]](
    setter=lambda w, val: w.setText(val),
)
