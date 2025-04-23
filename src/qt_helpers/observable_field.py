from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


@dataclass
class ObservableField(Generic[T]):
    _value: T
    _callbacks: list[Callable[[T], None]] = field(default_factory=list[Callable[[T], None]])

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        if value != self._value:
            self._value = value
            print(f"ObservableField set to {value} - {self}")
            for callback in self._callbacks:
                callback(value)

    def bind(self, callback: Callable[[T], None]) -> None:
        self._callbacks.append(callback)
        callback(self._value)  # trigger immediately with current value
