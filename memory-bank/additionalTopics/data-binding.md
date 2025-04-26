# Data Binding System

## Overview

The Data Binding System provides a type-safe, registry-based approach to synchronizing UI elements with domain models. It enables automatic propagation of changes between the UI and the underlying data, reducing boilerplate code and improving maintainability.

## Architecture

The Data Binding System follows a registry-based architecture with adapters for different widget types:

```
┌─────────────────┐     ┌─────────────────┐
│  Binding Registry │◄────│  Binding Adapter │
└────────┬────────┘     └────────┬────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Widget Property │     │ Observable Field │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   bind_fields()   │
            └─────────────────┘
```

### Key Components

1. **Binding Registry**: A global registry that maps widget types and property names to binding adapters.
2. **Binding Adapter**: Type-safe adapters that define how to get signals from and set values on specific widget types.
3. **Observable Field**: Domain model properties that notify listeners when values change.
4. **bind_fields()**: A function that establishes bindings between widget properties and observable fields.
5. **Lock Mechanism**: A flag that prevents infinite update loops between UI and model.

## Binding Registry

The binding registry is a central dictionary that maps tuples of widget types and property names to binding adapters:

```python
BINDING_REGISTRY: Dict[Tuple[Type, str], BindingAdapter] = {}
```

This registry is populated with adapters for common widget types and properties:

```python
# Register binding adapter for QLineEdit.text
BINDING_REGISTRY[(QLineEdit, "text")] = BindingAdapter[QLineEdit, str](
    signal_getter=lambda w: w.textChanged,
    setter=lambda w, val: w.setText(val),
)

# Register binding adapter for QPlainTextEdit.plainText
BINDING_REGISTRY[(QPlainTextEdit, "plainText")] = BindingAdapter[QPlainTextEdit, str](
    signal_getter=make_signal_getter_for_no_arg("textChanged", lambda w: w.toPlainText()),
    setter=lambda w, val: w.setPlainText(val),
)

# Register binding adapter for QCheckBox.checked
BINDING_REGISTRY[(QCheckBox, "checked")] = BindingAdapter[QCheckBox, bool](
    signal_getter=lambda w: w.stateChanged,
    setter=lambda w, val: w.setChecked(val),
    signal_converter=lambda state: state == Qt.CheckState.Checked,
)
```

## Binding Adapter

The `BindingAdapter` class defines how to get signals from and set values on specific widget types:

```python
@dataclass
class BindingAdapter(Generic[W, T]):
    """
    Adapter for binding a widget property to an observable field.
    
    Args:
        signal_getter: Function that returns the signal to connect to
        setter: Function that sets the value on the widget
        signal_converter: Optional function to convert the signal parameter to the expected type
    """
    signal_getter: Callable[[W], SignalInstance]
    setter: Callable[[W, T], None]
    signal_converter: Callable[[Any], T] = lambda x: x
```

The adapter provides three key functions:

1. **signal_getter**: Returns the signal to connect to for detecting changes in the widget.
2. **setter**: Sets the value on the widget when the observable field changes.
3. **signal_converter**: Converts the signal parameter to the expected type (optional).

## Observable Field

The `Observable` class provides a generic container for values that can notify listeners when the value changes:

```python
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
```

Domain models expose observable fields for properties that need to be bound to UI elements:

```python
@dataclass
class TextDocument(IDocument):
    _content: Observable[str] = field(default_factory=lambda: Observable(""))
    
    @property
    def content(self) -> str:
        return self._content.get()
        
    @content.setter
    def content(self, value: str) -> None:
        if self._content.get() != value:
            self._content.set(value)
            self._is_modified = True
            
    @property
    def content_observable(self) -> Observable[str]:
        return self._content
```

## Binding Establishment

The `bind_fields()` function establishes bindings between widget properties and observable fields:

```python
def bind_fields(bindings: List[Tuple[Any, str, Observable]]) -> None:
    """
    Bind widget properties to observable fields.
    
    Args:
        bindings: List of tuples (widget, property_name, observable_field)
    """
    for widget, property_name, observable in bindings:
        widget_type = type(widget)
        
        # Find the binding adapter
        adapter_key = (widget_type, property_name)
        if adapter_key not in BINDING_REGISTRY:
            raise ValueError(f"No binding adapter registered for {widget_type.__name__}.{property_name}")
        
        adapter = BINDING_REGISTRY[adapter_key]
        
        # Create a lock to prevent infinite update loops
        lock = False
        
        # Define the widget-to-model update function
        def update_model(value):
            nonlocal lock
            if lock:
                return
            lock = True
            try:
                converted_value = adapter.signal_converter(value)
                observable.set(converted_value)
            finally:
                lock = False
        
        # Define the model-to-widget update function
        def update_widget(value):
            nonlocal lock
            if lock:
                return
            lock = True
            try:
                adapter.setter(widget, value)
            finally:
                lock = False
        
        # Connect the signal
        signal = adapter.signal_getter(widget)
        signal.connect(update_model)
        
        # Register for observable changes
        observable.on_change(update_widget)
        
        # Initial update
        update_widget(observable.get())
```

This function:

1. Looks up the appropriate binding adapter for the widget type and property name.
2. Creates a lock to prevent infinite update loops.
3. Defines functions for updating the model when the widget changes and updating the widget when the model changes.
4. Connects the widget's signal to the update_model function.
5. Registers the update_widget function with the observable field.
6. Performs an initial update to synchronize the widget with the current model value.

## Usage in Widgets

Widgets declare bindings in their `setup_bindings` method:

```python
@widget("EditorWidget", classes=["editor"])
class EditorWidget(QWidget, IWidget):
    txt_source: QPlainTextEdit = make(QPlainTextEdit)
    
    def __init__(self, document: IDocument):
        self.document = document
    
    @override
    def setup_bindings(self) -> None:
        bind_fields([
            (self.txt_source, "plainText", self.document.content_observable)
        ])
```

The `@widget` decorator automatically calls the `setup_bindings` method during initialization.

## Helper Functions

The system includes helper functions for creating signal getters:

```python
def make_signal_getter_for_no_arg(signal_name: str, value_getter: Callable[[W], T]) -> Callable[[W], SignalInstance]:
    """
    Create a signal getter for signals that don't pass the new value as an argument.
    
    Args:
        signal_name: Name of the signal
        value_getter: Function to get the current value from the widget
        
    Returns:
        A function that returns a signal that emits the current value
    """
    def signal_getter(widget: W) -> SignalInstance:
        signal = getattr(widget, signal_name)
        
        # Create a new signal that emits the current value
        new_signal = Signal(T)
        
        # Connect the original signal to the new signal
        signal.connect(lambda: new_signal.emit(value_getter(widget)))
        
        return new_signal
    
    return signal_getter
```

This function is useful for signals that don't pass the new value as an argument, such as `QPlainTextEdit.textChanged`.

## Benefits

The Data Binding System provides several benefits:

1. **Type Safety**: The binding adapters ensure type compatibility between widget properties and observable fields.
2. **Reduced Boilerplate**: No need to manually connect signals and update widgets.
3. **Centralized Binding Logic**: All binding logic is centralized in the registry and adapters.
4. **Automatic Synchronization**: Changes in either the UI or the model are automatically propagated to the other.
5. **Prevention of Infinite Loops**: The lock mechanism prevents infinite update loops.

## Future Enhancements

Potential future enhancements to the Data Binding System:

1. **Validation**: Add support for validation rules and error display.
2. **Transformation**: Add support for transforming values between the UI and the model.
3. **Conditional Binding**: Enable or disable bindings based on conditions.
4. **Binding Groups**: Group related bindings for collective operations.
5. **Two-way vs. One-way Binding**: Support for one-way binding in addition to two-way binding.
