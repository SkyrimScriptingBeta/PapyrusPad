from typing import Any
from PySide6.QtCore import QObject


from typing import Any
from PySide6.QtCore import QObject
from qt_helpers.observable_field import ObservableField
from qt_helpers.widget_binding_registry import BINDING_REGISTRY


def bind_fields(bindings: list[tuple[QObject, str, ObservableField[Any]]]) -> None:
    for widget, prop, observable in bindings:
        adapter = BINDING_REGISTRY.get((type(widget), prop))
        if adapter is None:
            raise ValueError(f"No binding registered for {type(widget).__name__}.{prop}")

        lock = False

        # UI → Model
        def update_model(value: Any) -> None:
            nonlocal lock
            if not lock:
                lock = True
                observable.set(value)
                lock = False

        adapter.signal_getter(widget)(update_model)

        # Model → UI
        def update_ui(value: Any) -> None:
            nonlocal lock
            if not lock:
                lock = True
                if adapter:
                    adapter.setter(widget, value)
                lock = False

        observable.bind(update_ui)
