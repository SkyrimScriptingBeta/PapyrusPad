from dataclasses import field
from typing import Any, Callable, ParamSpec, TypeVar

T = TypeVar("T", covariant=True)
P = ParamSpec("P")


def make(class_type: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
    """
    Creates a factory for any object that can be used as a dataclass field default.

    This provides a cleaner syntax for object creation in dataclasses compared to
    using field(default_factory=lambda: ...) directly.

    Usage:
        # For widgets:
        central_widget: QLabel = factory(QLabel, "Hello World")
        my_button: QPushButton = factory(QPushButton, "Click me", clicked=some_callback)

        # For other types:
        items: list[str] = factory(list, ["item1", "item2"])
        counter: dict[str, int] = factory(dict, [("apples", 5), ("oranges", 10)])

    Returns an object of type T for type checking, but at runtime returns a dataclass field.

    This type lie is intentional to make the API more ergonomic while maintaining type safety.
    """

    factory_fn: Callable[[], T] = lambda: class_type(*args, **kwargs)
    return field(default_factory=factory_fn)


def make_later[T](class_type: type[T], *args: Any, **kwargs: Any) -> T:
    """
    Creates a factory for any dataclass field which you must initialize later.

    This is useful for fields that require a parent or other dependencies to be set first.

    Returns an object of type T for type checking, but at runtime returns a dataclass field.

    This type lie is intentional to make the API more ergonomic while maintaining type safety.
    """

    return field(init=False)
