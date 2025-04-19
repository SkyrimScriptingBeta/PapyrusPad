from dataclasses import field
from typing import Any, Callable, Generic, Protocol, Type, TypeVar

# Define a generic type variable for any class
T = TypeVar("T", covariant=True)


class Factory(Protocol, Generic[T]):
    """Protocol for factory objects that can create instances."""

    def __call__(self) -> T: ...


def factory[T](class_type: Type[T], *args: Any, **kwargs: Any) -> T:
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
