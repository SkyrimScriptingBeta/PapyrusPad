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
        self._value = value
        for callback in self._callbacks:
            callback(value)

    def set_if_changed(self, value: T) -> None:
        if self._value != value:
            self._value = value
            for callback in self._callbacks:
                callback(value)

    def bind(self, callback: Callable[[T], None]) -> None:
        self._callbacks.append(callback)
