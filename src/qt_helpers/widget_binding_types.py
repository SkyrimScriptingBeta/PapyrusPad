from PySide6.QtCore import QObject
from PySide6.QtWidgets import QLineEdit, QCheckBox, QPlainTextEdit
from typing import Callable, ParamSpec, TypeVar

from qt_helpers.signal_typing import GenericSignalHandler
from qt_helpers.widget_binding_registry import BINDING_REGISTRY, BindingAdapter

from typing import Callable, ParamSpec, TypeVar
from PySide6.QtCore import QObject

P = ParamSpec("P")
TWidget = TypeVar("TWidget", bound=QObject)


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


# Register checkbox binding
BINDING_REGISTRY[(QCheckBox, "checked")] = BindingAdapter[QCheckBox, [bool]](
    signal_getter=make_signal_getter_for("toggled", QCheckBox),
    setter=lambda w, val: w.setChecked(val),
)

# Register line edit binding
BINDING_REGISTRY[(QLineEdit, "text")] = BindingAdapter[QLineEdit, [str]](
    signal_getter=make_signal_getter_for("textChanged", QLineEdit),
    setter=lambda w, val: w.setText(val),
)

BINDING_REGISTRY[(QPlainTextEdit, "plainText")] = BindingAdapter[QPlainTextEdit, [str]](
    signal_getter=make_signal_getter_for_no_arg("textChanged", lambda w: w.toPlainText()),
    setter=lambda w, val: w.setPlainText(val),
)
