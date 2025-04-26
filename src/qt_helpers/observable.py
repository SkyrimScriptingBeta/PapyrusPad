from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Generic, TypeVar, Dict, List, Iterator, Optional, Tuple, Union, cast, Any

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


@dataclass
class Observable(Generic[T]):
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

    def on_change(self, callback: Callable[[T], None]) -> None:
        self._callbacks.append(callback)


class CollectionChangeType(Enum):
    """Type of change that occurred in a collection."""

    ADD = auto()
    REMOVE = auto()
    CLEAR = auto()
    UPDATE = auto()  # For dictionaries, when a value is updated


@dataclass
class ListChange(Generic[T]):
    """Information about a change to an ObservableList."""

    type: CollectionChangeType
    index: Optional[int] = None  # Index where the change occurred, if applicable
    item: Optional[T] = None  # Item that was added or removed, if applicable
    items: Optional[List[T]] = None  # Multiple items that were added or removed, if applicable


@dataclass
class DictChange(Generic[K, V]):
    """Information about a change to an ObservableDict."""

    type: CollectionChangeType
    key: Optional[K] = None  # Key where the change occurred, if applicable
    value: Optional[V] = None  # Value that was added, removed, or updated, if applicable
    items: Optional[Dict[K, V]] = None  # Multiple items that were added, removed, or updated, if applicable


class ObservableList(Generic[T]):
    """A list that notifies observers when items are added or removed."""

    def __init__(self, initial_items: Optional[List[T]] = None):
        """
        Initialize an ObservableList.

        Args:
            initial_items: Initial items to add to the list
        """
        self._items: List[T] = list(initial_items) if initial_items is not None else []
        self._callbacks: List[Callable[[ListChange[T]], None]] = []

    def __len__(self) -> int:
        """Return the number of items in the list."""
        return len(self._items)

    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        """Get an item or slice of items from the list."""
        return self._items[index]

    def __setitem__(self, index: Union[int, slice], value: Union[T, List[T]]) -> None:
        """Set an item or slice of items in the list."""
        if isinstance(index, slice):
            # Remove old items
            old_items = self._items[index]
            if old_items:
                self._notify(CollectionChangeType.REMOVE, index=index.start, items=old_items)

            # Add new items
            if isinstance(value, list):
                self._items[index] = value
                if value:
                    self._notify(CollectionChangeType.ADD, index=index.start, items=value)
            else:
                # Handle single item assigned to slice
                items_list = [cast(T, value)]
                self._items[index] = items_list
                self._notify(CollectionChangeType.ADD, index=index.start, items=items_list)
        else:
            # Remove old item
            old_item = self._items[index]
            self._notify(CollectionChangeType.REMOVE, index=index, item=old_item)

            # Add new item
            self._items[index] = cast(T, value)  # Cast to T since we know it's a single item
            self._notify(CollectionChangeType.ADD, index=index, item=cast(T, value))

    def __delitem__(self, index: Union[int, slice]) -> None:
        """Delete an item or slice of items from the list."""
        if isinstance(index, slice):
            items = self._items[index]
            if items:
                self._notify(CollectionChangeType.REMOVE, index=index.start, items=items)
        else:
            item = self._items[index]
            self._notify(CollectionChangeType.REMOVE, index=index, item=item)
        del self._items[index]

    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the items in the list."""
        return iter(self._items)

    def __contains__(self, item: T) -> bool:
        """Check if an item is in the list."""
        return item in self._items

    def append(self, item: T) -> None:
        """
        Add an item to the end of the list.

        Args:
            item: The item to add
        """
        self._items.append(item)
        self._notify(CollectionChangeType.ADD, index=len(self._items) - 1, item=item)

    def extend(self, items: List[T]) -> None:
        """
        Extend the list by appending all items from the iterable.

        Args:
            items: The items to add
        """
        if not items:
            return
        start_index = len(self._items)
        self._items.extend(items)
        self._notify(CollectionChangeType.ADD, index=start_index, items=items)

    def insert(self, index: int, item: T) -> None:
        """
        Insert an item at a given position.

        Args:
            index: The position to insert the item
            item: The item to insert
        """
        self._items.insert(index, item)
        self._notify(CollectionChangeType.ADD, index=index, item=item)

    def remove(self, item: T) -> None:
        """
        Remove the first occurrence of an item from the list.

        Args:
            item: The item to remove

        Raises:
            ValueError: If the item is not in the list
        """
        index = self._items.index(item)
        self._items.remove(item)
        self._notify(CollectionChangeType.REMOVE, index=index, item=item)

    def pop(self, index: int = -1) -> T:
        """
        Remove and return an item at a given position.

        Args:
            index: The position to remove the item from (default is -1, which is the last item)

        Returns:
            The removed item
        """
        item = self._items[index]
        self._items.pop(index)
        self._notify(CollectionChangeType.REMOVE, index=index, item=item)
        return item

    def clear(self) -> None:
        """Remove all items from the list."""
        if not self._items:
            return
        items = self._items.copy()
        self._items.clear()
        self._notify(CollectionChangeType.CLEAR, items=items)

    def index(self, item: T, start: int = 0, end: Optional[int] = None) -> int:
        """
        Return the index of the first occurrence of an item.

        Args:
            item: The item to find
            start: The start index to search from
            end: The end index to search to

        Returns:
            The index of the item

        Raises:
            ValueError: If the item is not in the list
        """
        if end is None:
            return self._items.index(item, start)
        return self._items.index(item, start, end)

    def count(self, item: T) -> int:
        """
        Return the number of occurrences of an item in the list.

        Args:
            item: The item to count

        Returns:
            The number of occurrences
        """
        return self._items.count(item)

    def sort(self, *, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
        """
        Sort the list in place.

        Args:
            key: A function that takes an item and returns a key for sorting
            reverse: Whether to sort in reverse order
        """
        self._items.sort(key=key, reverse=reverse)
        # No notification needed as the items themselves haven't changed

    def reverse(self) -> None:
        """Reverse the list in place."""
        self._items.reverse()
        # No notification needed as the items themselves haven't changed

    def copy(self) -> List[T]:
        """
        Return a shallow copy of the list.

        Returns:
            A copy of the list
        """
        return self._items.copy()

    def on_change(self, callback: Callable[[ListChange[T]], None]) -> None:
        """
        Add a callback to be called when the list changes.

        Args:
            callback: A function that takes a ListChange object
        """
        self._callbacks.append(callback)

    def _notify(self, change_type: CollectionChangeType, index: Optional[int] = None, item: Optional[T] = None, items: Optional[List[T]] = None) -> None:
        """
        Notify all callbacks of a change to the list.

        Args:
            change_type: The type of change that occurred
            index: The index where the change occurred, if applicable
            item: The item that was added or removed, if applicable
            items: Multiple items that were added or removed, if applicable
        """
        change = ListChange(type=change_type, index=index, item=item, items=items)
        for callback in self._callbacks:
            callback(change)


class ObservableDict(Generic[K, V]):
    """A dictionary that notifies observers when items are added, removed, or updated."""

    def __init__(self, initial_items: Optional[Dict[K, V]] = None):
        """
        Initialize an ObservableDict.

        Args:
            initial_items: Initial items to add to the dictionary
        """
        self._items: Dict[K, V] = dict(initial_items) if initial_items is not None else {}
        self._callbacks: List[Callable[[DictChange[K, V]], None]] = []

    def __len__(self) -> int:
        """Return the number of items in the dictionary."""
        return len(self._items)

    def __getitem__(self, key: K) -> V:
        """Get an item from the dictionary."""
        return self._items[key]

    def __setitem__(self, key: K, value: V) -> None:
        """Set an item in the dictionary."""
        if key in self._items:
            # We don't need to use old_value, but we could if we wanted to
            # old_value = self._items[key]
            self._items[key] = value
            self._notify(CollectionChangeType.UPDATE, key=key, value=value)
        else:
            self._items[key] = value
            self._notify(CollectionChangeType.ADD, key=key, value=value)

    def __delitem__(self, key: K) -> None:
        """Delete an item from the dictionary."""
        value = self._items[key]
        del self._items[key]
        self._notify(CollectionChangeType.REMOVE, key=key, value=value)

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys in the dictionary."""
        return iter(self._items)

    def __contains__(self, key: K) -> bool:
        """Check if a key is in the dictionary."""
        return key in self._items

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Return the value for a key if it exists, otherwise return a default value.

        Args:
            key: The key to look up
            default: The default value to return if the key is not found

        Returns:
            The value for the key, or the default value
        """
        return self._items.get(key, default)

    def setdefault(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Return the value for a key if it exists, otherwise set and return the default value.

        Args:
            key: The key to look up
            default: The default value to set and return if the key is not found

        Returns:
            The value for the key, or the default value
        """
        if key not in self._items:
            self._items[key] = cast(V, default)  # Cast to V since we know it's a value
            self._notify(CollectionChangeType.ADD, key=key, value=cast(V, default))
            return default
        return self._items[key]

    def pop(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """
        Remove and return the value for a key if it exists, otherwise return a default value.

        Args:
            key: The key to look up
            default: The default value to return if the key is not found

        Returns:
            The value for the key, or the default value

        Raises:
            KeyError: If the key is not found and no default value is provided
        """
        if key in self._items:
            value = self._items.pop(key)
            self._notify(CollectionChangeType.REMOVE, key=key, value=value)
            return value
        if default is not None:
            return default
        raise KeyError(key)

    def popitem(self) -> Tuple[K, V]:
        """
        Remove and return a (key, value) pair from the dictionary.

        Returns:
            A (key, value) pair

        Raises:
            KeyError: If the dictionary is empty
        """
        key, value = self._items.popitem()
        self._notify(CollectionChangeType.REMOVE, key=key, value=value)
        return key, value

    def clear(self) -> None:
        """Remove all items from the dictionary."""
        if not self._items:
            return
        items = self._items.copy()
        self._items.clear()
        self._notify(CollectionChangeType.CLEAR, items=items)

    def update(self, other: Dict[K, V]) -> None:
        """
        Update the dictionary with the key/value pairs from another dictionary.

        Args:
            other: Another dictionary to update from
        """
        if not other:
            return
        added_items: Dict[K, V] = {}
        updated_items: Dict[K, V] = {}
        for key, value in other.items():
            if key in self._items:
                updated_items[key] = value
            else:
                added_items[key] = value
        self._items.update(other)
        if added_items:
            self._notify(CollectionChangeType.ADD, items=added_items)
        if updated_items:
            self._notify(CollectionChangeType.UPDATE, items=updated_items)

    def keys(self) -> List[K]:
        """
        Return a list of all keys in the dictionary.

        Returns:
            A list of keys
        """
        return list(self._items.keys())

    def values(self) -> List[V]:
        """
        Return a list of all values in the dictionary.

        Returns:
            A list of values
        """
        return list(self._items.values())

    def items(self) -> List[Tuple[K, V]]:
        """
        Return a list of all (key, value) pairs in the dictionary.

        Returns:
            A list of (key, value) pairs
        """
        return list(self._items.items())

    def copy(self) -> Dict[K, V]:
        """
        Return a shallow copy of the dictionary.

        Returns:
            A copy of the dictionary
        """
        return self._items.copy()

    def on_change(self, callback: Callable[[DictChange[K, V]], None]) -> None:
        """
        Add a callback to be called when the dictionary changes.

        Args:
            callback: A function that takes a DictChange object
        """
        self._callbacks.append(callback)

    def _notify(self, change_type: CollectionChangeType, key: Optional[K] = None, value: Optional[V] = None, items: Optional[Dict[K, V]] = None) -> None:
        """
        Notify all callbacks of a change to the dictionary.

        Args:
            change_type: The type of change that occurred
            key: The key where the change occurred, if applicable
            value: The value that was added, removed, or updated, if applicable
            items: Multiple items that were added, removed, or updated, if applicable
        """
        change = DictChange(type=change_type, key=key, value=value, items=items)
        for callback in self._callbacks:
            callback(change)
