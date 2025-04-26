from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Generic, Protocol, TypeVar, Dict, List, Iterator, Optional, Tuple, Union, cast, Any, override, runtime_checkable

H = TypeVar("H", contravariant=True)


@runtime_checkable
class SupportsLessThan(Protocol[H]):
    def __lt__(self, other: H) -> bool: ...


T = TypeVar("T", bound="SupportsLessThan[Any]")
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


class IObservableList(Generic[T], ABC):
    """Interface for observable lists with specific event types."""

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items in the list."""
        ...

    @abstractmethod
    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        """Get an item or slice of items from the list."""
        ...

    @abstractmethod
    def __setitem__(self, index: Union[int, slice], value: Union[T, List[T]]) -> None:
        """Set an item or slice of items in the list."""
        ...

    @abstractmethod
    def __delitem__(self, index: Union[int, slice]) -> None:
        """Delete an item or slice of items from the list."""
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the items in the list."""
        ...

    @abstractmethod
    def __contains__(self, item: T) -> bool:
        """Check if an item is in the list."""
        ...

    @abstractmethod
    def append(self, item: T) -> None:
        """Add an item to the end of the list."""
        ...

    @abstractmethod
    def extend(self, items: List[T]) -> None:
        """Extend the list by appending all items from the iterable."""
        ...

    @abstractmethod
    def insert(self, index: int, item: T) -> None:
        """Insert an item at a given position."""
        ...

    @abstractmethod
    def remove(self, item: T) -> None:
        """Remove the first occurrence of an item from the list."""
        ...

    @abstractmethod
    def pop(self, index: int = -1) -> T:
        """Remove and return an item at a given position."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove all items from the list."""
        ...

    @abstractmethod
    def index(self, item: T, start: int = 0, end: Optional[int] = None) -> int:
        """Return the index of the first occurrence of an item."""
        ...

    @abstractmethod
    def count(self, item: T) -> int:
        """Return the number of occurrences of an item in the list."""
        ...

    @abstractmethod
    def sort(self, *, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> None:
        """Sort the list in place."""
        ...

    @abstractmethod
    def reverse(self) -> None:
        """Reverse the list in place."""
        ...

    @abstractmethod
    def copy(self) -> List[T]:
        """Return a shallow copy of the list."""
        ...

    @abstractmethod
    def on_change(self, callback: Callable[[ListChange[T]], None]) -> None:
        """Register for all change events with detailed information."""
        ...

    @abstractmethod
    def on_add(self, callback: Callable[[T, int], None]) -> None:
        """Register for add events with item and index."""
        ...

    @abstractmethod
    def on_remove(self, callback: Callable[[T, int], None]) -> None:
        """Register for remove events with item and index."""
        ...

    @abstractmethod
    def on_clear(self, callback: Callable[[List[T]], None]) -> None:
        """Register for clear events with the cleared items."""
        ...


class ObservableListBase(Generic[T], IObservableList[T]):
    """Base implementation that can work with an external list or create its own."""

    def __init__(self, items: Optional[List[T]] = None):
        """
        Initialize with optional external list reference.

        Args:
            items: Optional external list to observe. If None, creates a new list.
        """
        self._items: list[T] = items if items is not None else []
        self._change_callbacks: List[Callable[[ListChange[T]], None]] = []
        self._add_callbacks: List[Callable[[T, int], None]] = []
        self._remove_callbacks: List[Callable[[T, int], None]] = []
        self._clear_callbacks: List[Callable[[List[T]], None]] = []

    @override
    def __len__(self) -> int:
        """Return the number of items in the list."""
        return len(self._items)

    @override
    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        """Get an item or slice of items from the list."""
        return self._items[index]

    @override
    def __setitem__(self, index: Union[int, slice], value: Union[T, List[T]]) -> None:
        """Set an item or slice of items in the list."""
        if isinstance(index, slice):
            # Remove old items
            old_items = self._items[index]
            if old_items:
                self._notify_remove_items(old_items, index.start)

            # Add new items
            if isinstance(value, list):
                # Explicitly cast to List[T] to help Pylance
                self._items[index] = value
                if value:
                    # Use the explicitly typed value
                    self._notify_add_items(value, index.start)
            else:
                # Handle single item assigned to slice
                single_value: T = cast(T, value)
                items_list: List[T] = [single_value]
                self._items[index] = items_list
                self._notify_add_items(items_list, index.start)
        else:
            # Remove old item
            old_item = self._items[index]
            self._notify_remove(old_item, index)

            # Add new item
            new_value: T = cast(T, value)  # Cast to T since we know it's a single item
            self._items[index] = new_value
            self._notify_add(new_value, index)

    @override
    def __delitem__(self, index: Union[int, slice]) -> None:
        """Delete an item or slice of items from the list."""
        if isinstance(index, slice):
            items = self._items[index]
            if items:
                self._notify_remove_items(items, index.start)
        else:
            item = self._items[index]
            self._notify_remove(item, index)
        del self._items[index]

    @override
    def __iter__(self) -> Iterator[T]:
        """Return an iterator over the items in the list."""
        return iter(self._items)

    @override
    def __contains__(self, item: T) -> bool:
        """Check if an item is in the list."""
        return item in self._items

    @override
    def append(self, item: T) -> None:
        """
        Add an item to the end of the list.

        Args:
            item: The item to add
        """
        self._items.append(item)
        self._notify_add(item, len(self._items) - 1)

    @override
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
        self._notify_add_items(items, start_index)

    @override
    def insert(self, index: int, item: T) -> None:
        """
        Insert an item at a given position.

        Args:
            index: The position to insert the item
            item: The item to insert
        """
        self._items.insert(index, item)
        self._notify_add(item, index)

    @override
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
        self._notify_remove(item, index)

    @override
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
        self._notify_remove(item, index)
        return item

    @override
    def clear(self) -> None:
        """Remove all items from the list."""
        if not self._items:
            return
        items = self._items.copy()
        self._items.clear()
        self._notify_clear(items)

    @override
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

    @override
    def count(self, item: T) -> int:
        """
        Return the number of occurrences of an item in the list.

        Args:
            item: The item to count

        Returns:
            The number of occurrences
        """
        return self._items.count(item)

    @override
    def sort(self, *, key: Optional[Callable[[T], SupportsLessThan[V]]] = lambda x: x, reverse: bool = False) -> None:
        """
        Sort the list in place.

        Args:
            key: A function that takes an item and returns a key for sorting
            reverse: Whether to sort in reverse order
        """
        if key is None:
            if reverse:
                self._items.sort(key=None, reverse=True)
            else:
                self._items.sort(key=None, reverse=False)
        else:
            self._items.sort(key=key, reverse=reverse)

    @override
    def reverse(self) -> None:
        """Reverse the list in place."""
        self._items.reverse()
        # No notification needed as the items themselves haven't changed

    @override
    def copy(self) -> List[T]:
        """
        Return a shallow copy of the list.

        Returns:
            A copy of the list
        """
        return self._items.copy()

    @override
    def on_change(self, callback: Callable[[ListChange[T]], None]) -> None:
        """
        Add a callback to be called when the list changes.

        Args:
            callback: A function that takes a ListChange object
        """
        self._change_callbacks.append(callback)

    @override
    def on_add(self, callback: Callable[[T, int], None]) -> None:
        """
        Register for add events with item and index.

        Args:
            callback: A function that takes an item and its index
        """
        self._add_callbacks.append(callback)

    @override
    def on_remove(self, callback: Callable[[T, int], None]) -> None:
        """
        Register for remove events with item and index.

        Args:
            callback: A function that takes an item and its index
        """
        self._remove_callbacks.append(callback)

    @override
    def on_clear(self, callback: Callable[[List[T]], None]) -> None:
        """
        Register for clear events with the cleared items.

        Args:
            callback: A function that takes a list of cleared items
        """
        self._clear_callbacks.append(callback)

    def _notify_add(self, item: T, index: int) -> None:
        """
        Notify all callbacks of an item being added.

        Args:
            item: The item that was added
            index: The index where the item was added
        """
        # Call specific callbacks
        for callback in self._add_callbacks:
            callback(item, index)

        # Call general change callbacks
        change = ListChange(type=CollectionChangeType.ADD, index=index, item=item)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_add_items(self, items: List[T], start_index: int) -> None:
        """
        Notify all callbacks of multiple items being added.

        Args:
            items: The items that were added
            start_index: The index where the items were added
        """
        # Call specific callbacks for each item
        for i, item in enumerate(items):
            index = start_index + i
            for callback in self._add_callbacks:
                callback(item, index)

        # Call general change callbacks
        change = ListChange(type=CollectionChangeType.ADD, index=start_index, items=items)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_remove(self, item: T, index: int) -> None:
        """
        Notify all callbacks of an item being removed.

        Args:
            item: The item that was removed
            index: The index where the item was removed
        """
        # Call specific callbacks
        for callback in self._remove_callbacks:
            callback(item, index)

        # Call general change callbacks
        change = ListChange(type=CollectionChangeType.REMOVE, index=index, item=item)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_remove_items(self, items: List[T], start_index: int) -> None:
        """
        Notify all callbacks of multiple items being removed.

        Args:
            items: The items that were removed
            start_index: The index where the items were removed
        """
        # Call specific callbacks for each item
        for i, item in enumerate(items):
            index = start_index + i
            for callback in self._remove_callbacks:
                callback(item, index)

        # Call general change callbacks
        change = ListChange(type=CollectionChangeType.REMOVE, index=start_index, items=items)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_clear(self, items: List[T]) -> None:
        """
        Notify all callbacks of the list being cleared.

        Args:
            items: The items that were cleared
        """
        # Call specific callbacks
        for callback in self._clear_callbacks:
            callback(items)

        # Call general change callbacks
        change = ListChange(type=CollectionChangeType.CLEAR, items=items)
        for callback in self._change_callbacks:
            callback(change)


class ObservableList(ObservableListBase[T]):
    """A list that notifies observers when items are added or removed."""

    def __init__(self, initial_items: Optional[List[T]] = None):
        """
        Initialize an ObservableList.

        Args:
            initial_items: Initial items to add to the list
        """
        super().__init__(initial_items)


class IObservableDict(Generic[K, V], ABC):
    """Interface for observable dictionaries with specific event types."""

    @abstractmethod
    def __len__(self) -> int:
        """Return the number of items in the dictionary."""
        ...

    @abstractmethod
    def __getitem__(self, key: K) -> V:
        """Get an item from the dictionary."""
        ...

    @abstractmethod
    def __setitem__(self, key: K, value: V) -> None:
        """Set an item in the dictionary."""
        ...

    @abstractmethod
    def __delitem__(self, key: K) -> None:
        """Delete an item from the dictionary."""
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys in the dictionary."""
        ...

    @abstractmethod
    def __contains__(self, key: K) -> bool:
        """Check if a key is in the dictionary."""
        ...

    @abstractmethod
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Return the value for a key if it exists, otherwise return a default value."""
        ...

    @abstractmethod
    def setdefault(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Return the value for a key if it exists, otherwise set and return the default value."""
        ...

    @abstractmethod
    def pop(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Remove and return the value for a key if it exists, otherwise return a default value."""
        ...

    @abstractmethod
    def popitem(self) -> Tuple[K, V]:
        """Remove and return a (key, value) pair from the dictionary."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove all items from the dictionary."""
        ...

    @abstractmethod
    def update(self, other: Dict[K, V]) -> None:
        """Update the dictionary with the key/value pairs from another dictionary."""
        ...

    @abstractmethod
    def keys(self) -> List[K]:
        """Return a list of all keys in the dictionary."""
        ...

    @abstractmethod
    def values(self) -> List[V]:
        """Return a list of all values in the dictionary."""
        ...

    @abstractmethod
    def items(self) -> List[Tuple[K, V]]:
        """Return a list of all (key, value) pairs in the dictionary."""
        ...

    @abstractmethod
    def copy(self) -> Dict[K, V]:
        """Return a shallow copy of the dictionary."""
        ...

    @abstractmethod
    def on_change(self, callback: Callable[[DictChange[K, V]], None]) -> None:
        """Register for all change events with detailed information."""
        ...

    @abstractmethod
    def on_add(self, callback: Callable[[K, V], None]) -> None:
        """Register for add events with key and value."""
        ...

    @abstractmethod
    def on_remove(self, callback: Callable[[K, V], None]) -> None:
        """Register for remove events with key and value."""
        ...

    @abstractmethod
    def on_update(self, callback: Callable[[K, V], None]) -> None:
        """Register for update events with key and new value."""
        ...

    @abstractmethod
    def on_clear(self, callback: Callable[[Dict[K, V]], None]) -> None:
        """Register for clear events with the cleared items."""
        ...


class ObservableDictBase(Generic[K, V], IObservableDict[K, V]):
    """Base implementation that can work with an external dict or create its own."""

    def __init__(self, items: Optional[Dict[K, V]] = None):
        """
        Initialize with optional external dict reference.

        Args:
            items: Optional external dict to observe. If None, creates a new dict.
        """
        self._items: Dict[K, V] = dict(items) if items is not None else {}
        self._change_callbacks: List[Callable[[DictChange[K, V]], None]] = []
        self._add_callbacks: List[Callable[[K, V], None]] = []
        self._remove_callbacks: List[Callable[[K, V], None]] = []
        self._update_callbacks: List[Callable[[K, V], None]] = []
        self._clear_callbacks: List[Callable[[Dict[K, V]], None]] = []

    @override
    def __len__(self) -> int:
        """Return the number of items in the dictionary."""
        return len(self._items)

    @override
    def __getitem__(self, key: K) -> V:
        """Get an item from the dictionary."""
        return self._items[key]

    @override
    def __setitem__(self, key: K, value: V) -> None:
        """Set an item in the dictionary."""
        if key in self._items:
            self._items[key] = value
            self._notify_update(key, value)
        else:
            self._items[key] = value
            self._notify_add(key, value)

    @override
    def __delitem__(self, key: K) -> None:
        """Delete an item from the dictionary."""
        value = self._items[key]
        del self._items[key]
        self._notify_remove(key, value)

    @override
    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys in the dictionary."""
        return iter(self._items)

    @override
    def __contains__(self, key: K) -> bool:
        """Check if a key is in the dictionary."""
        return key in self._items

    @override
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

    @override
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
            self._notify_add(key, cast(V, default))
            return default
        return self._items[key]

    @override
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
            self._notify_remove(key, value)
            return value
        if default is not None:
            return default
        raise KeyError(key)

    @override
    def popitem(self) -> Tuple[K, V]:
        """
        Remove and return a (key, value) pair from the dictionary.

        Returns:
            A (key, value) pair

        Raises:
            KeyError: If the dictionary is empty
        """
        key, value = self._items.popitem()
        self._notify_remove(key, value)
        return key, value

    @override
    def clear(self) -> None:
        """Remove all items from the dictionary."""
        if not self._items:
            return
        items = self._items.copy()
        self._items.clear()
        self._notify_clear(items)

    @override
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

        # Notify for added items
        if added_items:
            for key, value in added_items.items():
                self._notify_add(key, value)

        # Notify for updated items
        if updated_items:
            for key, value in updated_items.items():
                self._notify_update(key, value)

    @override
    def keys(self) -> List[K]:
        """
        Return a list of all keys in the dictionary.

        Returns:
            A list of keys
        """
        return list(self._items.keys())

    @override
    def values(self) -> List[V]:
        """
        Return a list of all values in the dictionary.

        Returns:
            A list of values
        """
        return list(self._items.values())

    @override
    def items(self) -> List[Tuple[K, V]]:
        """
        Return a list of all (key, value) pairs in the dictionary.

        Returns:
            A list of (key, value) pairs
        """
        return list(self._items.items())

    @override
    def copy(self) -> Dict[K, V]:
        """
        Return a shallow copy of the dictionary.

        Returns:
            A copy of the dictionary
        """
        return self._items.copy()

    @override
    def on_change(self, callback: Callable[[DictChange[K, V]], None]) -> None:
        """
        Add a callback to be called when the dictionary changes.

        Args:
            callback: A function that takes a DictChange object
        """
        self._change_callbacks.append(callback)

    @override
    def on_add(self, callback: Callable[[K, V], None]) -> None:
        """
        Register for add events with key and value.

        Args:
            callback: A function that takes a key and value
        """
        self._add_callbacks.append(callback)

    @override
    def on_remove(self, callback: Callable[[K, V], None]) -> None:
        """
        Register for remove events with key and value.

        Args:
            callback: A function that takes a key and value
        """
        self._remove_callbacks.append(callback)

    @override
    def on_update(self, callback: Callable[[K, V], None]) -> None:
        """
        Register for update events with key and new value.

        Args:
            callback: A function that takes a key and new value
        """
        self._update_callbacks.append(callback)

    @override
    def on_clear(self, callback: Callable[[Dict[K, V]], None]) -> None:
        """
        Register for clear events with the cleared items.

        Args:
            callback: A function that takes a dict of cleared items
        """
        self._clear_callbacks.append(callback)

    def _notify_add(self, key: K, value: V) -> None:
        """
        Notify all callbacks of an item being added.

        Args:
            key: The key that was added
            value: The value that was added
        """
        # Call specific callbacks
        for callback in self._add_callbacks:
            callback(key, value)

        # Create a dictionary with the single item for the items field
        items_dict = {key: value}

        # Call general change callbacks
        change = DictChange(type=CollectionChangeType.ADD, key=key, value=value, items=items_dict)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_remove(self, key: K, value: V) -> None:
        """
        Notify all callbacks of an item being removed.

        Args:
            key: The key that was removed
            value: The value that was removed
        """
        # Call specific callbacks
        for callback in self._remove_callbacks:
            callback(key, value)

        # Create a dictionary with the single item for the items field
        items_dict = {key: value}

        # Call general change callbacks
        change = DictChange(type=CollectionChangeType.REMOVE, key=key, value=value, items=items_dict)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_update(self, key: K, value: V) -> None:
        """
        Notify all callbacks of an item being updated.

        Args:
            key: The key that was updated
            value: The new value
        """
        # Call specific callbacks
        for callback in self._update_callbacks:
            callback(key, value)

        # Create a dictionary with the single item for the items field
        items_dict = {key: value}

        # Call general change callbacks
        change = DictChange(type=CollectionChangeType.UPDATE, key=key, value=value, items=items_dict)
        for callback in self._change_callbacks:
            callback(change)

    def _notify_clear(self, items: Dict[K, V]) -> None:
        """
        Notify all callbacks of the dictionary being cleared.

        Args:
            items: The items that were cleared
        """
        # Call specific callbacks
        for callback in self._clear_callbacks:
            callback(items)

        # Call general change callbacks
        change = DictChange(type=CollectionChangeType.CLEAR, items=items)
        for callback in self._change_callbacks:
            callback(change)


class ObservableDict(ObservableDictBase[K, V]):
    """A dictionary that notifies observers when items are added, removed, or updated."""

    def __init__(self, initial_items: Optional[Dict[K, V]] = None):
        """
        Initialize an ObservableDict.

        Args:
            initial_items: Initial items to add to the dictionary
        """
        super().__init__(initial_items)
