# Observable Collections System

## Overview

The Observable Collections system provides a robust, type-safe way to create collections (lists and dictionaries) that notify observers when their contents change. This system is a core part of PapyrusPad's reactive architecture, enabling UI components to automatically update when underlying data changes.

## Architecture

The Observable Collections system follows a layered architecture with interfaces, base implementations, and concrete classes:

```
┌─────────────────┐     ┌─────────────────┐
│ IObservableList │     │ IObservableDict │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│ObservableListBase│     │ObservableDictBase│
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  ObservableList │     │  ObservableDict │
└─────────────────┘     └─────────────────┘
```

### Key Components

1. **Interfaces**: `IObservableList` and `IObservableDict` define the contracts for observable collections.
2. **Base Classes**: `ObservableListBase` and `ObservableDictBase` provide concrete implementations that can be extended.
3. **Concrete Classes**: `ObservableList` and `ObservableDict` are ready-to-use implementations.
4. **Change Objects**: `ListChange` and `DictChange` encapsulate information about collection changes.
5. **Change Type Enum**: `CollectionChangeType` defines the types of changes (ADD, REMOVE, UPDATE, CLEAR).

## Observable List

### Interface

`IObservableList[T]` defines the contract for observable lists:

- Standard list operations (`__len__`, `__getitem__`, `__setitem__`, etc.)
- Collection modification methods (`append`, `extend`, `insert`, `remove`, etc.)
- Event registration methods:
  - `on_change`: Register for all change events with detailed information
  - `on_add`: Register for add events with item and index
  - `on_remove`: Register for remove events with item and index
  - `on_clear`: Register for clear events with the cleared items

### Base Implementation

`ObservableListBase[T]` provides a concrete implementation of `IObservableList[T]`:

- Manages a list of items and callbacks
- Implements all list operations with appropriate notifications
- Provides helper methods for notifying observers

### Concrete Implementation

`ObservableList[T]` extends `ObservableListBase[T]` and provides a ready-to-use observable list.

### Usage Example

```python
# Create an observable list
items = ObservableList[str](["apple", "banana", "cherry"])

# Register for change events
items.on_change(lambda change: print(f"Change: {change.type}, Item: {change.item}"))
items.on_add(lambda item, index: print(f"Added {item} at index {index}"))
items.on_remove(lambda item, index: print(f"Removed {item} from index {index}"))
items.on_clear(lambda items: print(f"Cleared {len(items)} items"))

# Modify the list
items.append("date")  # Triggers on_add and on_change
items.remove("banana")  # Triggers on_remove and on_change
items.clear()  # Triggers on_clear and on_change
```

## Observable Dictionary

### Interface

`IObservableDict[K, V]` defines the contract for observable dictionaries:

- Standard dictionary operations (`__len__`, `__getitem__`, `__setitem__`, etc.)
- Collection modification methods (`get`, `setdefault`, `pop`, `update`, etc.)
- Event registration methods:
  - `on_change`: Register for all change events with detailed information
  - `on_add`: Register for add events with key and value
  - `on_remove`: Register for remove events with key and value
  - `on_update`: Register for update events with key and new value
  - `on_clear`: Register for clear events with the cleared items

### Base Implementation

`ObservableDictBase[K, V]` provides a concrete implementation of `IObservableDict[K, V]`:

- Manages a dictionary of items and callbacks
- Implements all dictionary operations with appropriate notifications
- Provides helper methods for notifying observers

### Concrete Implementation

`ObservableDict[K, V]` extends `ObservableDictBase[K, V]` and provides a ready-to-use observable dictionary.

### Usage Example

```python
# Create an observable dictionary
items = ObservableDict[str, int]({"apple": 1, "banana": 2, "cherry": 3})

# Register for change events
items.on_change(lambda change: print(f"Change: {change.type}, Key: {change.key}, Value: {change.value}"))
items.on_add(lambda key, value: print(f"Added {key}: {value}"))
items.on_remove(lambda key, value: print(f"Removed {key}: {value}"))
items.on_update(lambda key, value: print(f"Updated {key} to {value}"))
items.on_clear(lambda items: print(f"Cleared {len(items)} items"))

# Modify the dictionary
items["date"] = 4  # Triggers on_add and on_change
items["apple"] = 5  # Triggers on_update and on_change
del items["banana"]  # Triggers on_remove and on_change
items.clear()  # Triggers on_clear and on_change
```

## Integration with DocumentCollection

The `DocumentCollection` class has been updated to implement `IObservableList[IDocument]` and extend `ObservableListBase[IDocument]`. This provides several benefits:

1. **Type Safety**: The collection is now explicitly typed as a list of `IDocument` objects.
2. **Event Notifications**: Changes to the collection automatically trigger notifications to observers.
3. **Standard List Interface**: The collection now provides a standard list interface with all expected methods.
4. **Backward Compatibility**: The class maintains backward compatibility with existing code through bridge methods.

### Example Usage

```python
# Create a document collection
collection = DocumentCollection()

# Register for change events
collection.on_add(lambda doc, index: print(f"Added document {doc.name} at index {index}"))
collection.on_remove(lambda doc, index: print(f"Removed document {doc.name} from index {index}"))

# Add a document
doc = TextDocument()
doc.name = "New Document"
collection.append(doc)  # Triggers on_add

# Remove a document
collection.remove(doc)  # Triggers on_remove
```

## Type Checking Challenges

During implementation, we encountered some type checking challenges:

1. **Generic Type Erasure**: Python's runtime doesn't maintain information about generic type parameters, which can lead to type checking issues.
2. **Union Types**: Working with `T | list[T]` parameters can be challenging for type checkers.
3. **Optional Parameters**: Methods like `sort()` with optional parameters can cause type checking issues.

These challenges were addressed through:

1. **Explicit Type Casting**: Using `cast()` to provide type hints to the type checker.
2. **Type Annotations**: Adding explicit type annotations to variables and parameters.
3. **Type Ignore Comments**: Using `# type: ignore` comments in specific cases where the type checker is too restrictive.

## Benefits of the New System

The new Observable Collections system provides several benefits:

1. **Type Safety**: Strong typing throughout the system improves code quality and IDE support.
2. **Code Reuse**: Common collection functionality is now in base classes, reducing duplication.
3. **Flexibility**: It's now easier to create new observable collections by extending the base classes.
4. **Cleaner API**: The event system is more consistent and easier to use.
5. **Better Testability**: The system is designed with testing in mind, with clear interfaces and behaviors.

## Future Enhancements

Potential future enhancements to the Observable Collections system:

1. **Filtered Views**: Create filtered views of collections that update automatically.
2. **Sorted Views**: Create sorted views of collections that update automatically.
3. **Mapped Collections**: Create collections that transform items from another collection.
4. **Batch Operations**: Support for batching multiple operations with a single notification.
5. **Undo/Redo Support**: Track changes to enable undo/redo functionality.
