from dataclasses import field
from typing import (
    Any,
    Callable,
    Generic,
    Protocol,
    Type,
    TypeVar,
    cast,
    runtime_checkable,
)

from PySide6.QtWidgets import QWidget

# Define a type variable for widgets
T = TypeVar("T", bound=QWidget, covariant=True)  # Make T covariant


class WidgetFactory(Protocol, Generic[T]):
    """Protocol for factory objects that can create widgets."""

    def __call__(self) -> T: ...


@runtime_checkable
class FieldWithFactory(Protocol):
    """Protocol for dataclass fields with a default_factory."""

    default_factory: Callable[[], Any]


# Define specific field function that maintains proper typing
def create_widget[T](widget_class: Type[T], *args: Any, **kwargs: Any) -> T:
    """
    Creates a factory for a widget that can be used as a dataclass field default.

    This provides a cleaner syntax for widget creation in dataclasses compared to
    using field(default_factory=lambda: ...) directly.

    Usage:
        central_widget: QLabel = create_widget(QLabel, "Hello World")
        my_button: QPushButton = create_widget(QPushButton, "Click me", clicked=some_callback)

    Returns a widget of type T for type checking, but at runtime returns a dataclass field.
    This type lie is intentional to make the API more ergonomic while maintaining type safety.
    """
    factory_fn: Callable[[], T] = lambda: widget_class(*args, **kwargs)
    # NOTE: This cast is necessary despite Pylance's warning.
    # We're intentionally lying to the type system to make the API more ergonomic.
    # At runtime, this returns a Field, but for type checking, we want it to appear as T.
    return cast(T, field(default_factory=factory_fn))


def with_config[T](
    widget_factory: FieldWithFactory, config_fn: Callable[[T], None]
) -> T:
    """
    Applies additional configuration to a widget after creation.

    Usage:
        combo: QComboBox = with_config(create_widget(QComboBox),
                                     lambda cb: cb.addItems(["One", "Two", "Three"]))

    Returns a widget of type T for type checking, but at runtime returns a dataclass field.
    This type lie is intentional to make the API more ergonomic while maintaining type safety.
    """
    original_factory: Callable[[], Any] = widget_factory.default_factory

    if not callable(original_factory):
        raise TypeError("The default_factory of the Field must be callable.")

    def factory() -> T:
        widget = cast(T, original_factory())
        config_fn(widget)
        return widget

    # NOTE: This cast is necessary despite Pylance's warning.
    # We're intentionally lying to the type system to make the API more ergonomic.
    # At runtime, this returns a Field, but for type checking, we want it to appear as T.
    return cast(T, field(default_factory=factory))
