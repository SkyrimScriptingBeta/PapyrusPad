# Updated Data Binding Approaches for PapyrusPad

This document outlines refined approaches to implementing data binding between the UI and domain models in PapyrusPad, focusing on a more declarative and fluent API style that aligns with the existing codebase patterns.

## Fluent Binding API

The most promising approach is a fluent binding API that uses method chaining for a clean, readable syntax:

```python
self.bind(self.txt_source).to(self.document, "content")
```

This approach is intuitive, explicit, and aligns well with the declarative style of the existing codebase.

### Implementation

```python
class Binder:
    def __init__(self, widget, property_name=None):
        self.widget = widget
        self.widget_property = property_name
        self.signal_name = None
        self._bindings = []
    
    def with_signal(self, signal_name):
        """Specify which signal to use for change notification."""
        self.signal_name = signal_name
        return self
    
    def to(self, model, property_name):
        """Create a two-way binding between the widget and model property."""
        # Get the appropriate signal based on widget type
        signal = self._get_signal()
        
        # Set up UI → Model binding
        def update_model():
            value = self._get_widget_value()
            setattr(model, property_name, value)
        
        signal.connect(update_model)
        
        # Set up Model → UI binding
        if isinstance(model, Observable):
            def update_ui(value):
                # Temporarily disconnect to prevent loops
                signal.disconnect(update_model)
                self._set_widget_value(value)
                signal.connect(update_model)
            
            model.observe(property_name).subscribe(update_ui)
        
        # Initial update
        self._set_widget_value(getattr(model, property_name))
        
        return self
    
    def _get_signal(self):
        """Get the appropriate signal for the widget."""
        if self.signal_name:
            return getattr(self.widget, self.signal_name)
        
        if isinstance(self.widget, QPlainTextEdit):
            return self.widget.textChanged
        elif isinstance(self.widget, QLineEdit):
            return self.widget.textEdited
        # Add more widget types as needed
    
    def _get_widget_value(self):
        """Get the current value from the widget."""
        if isinstance(self.widget, QPlainTextEdit):
            return self.widget.toPlainText()
        elif isinstance(self.widget, QLineEdit):
            return self.widget.text()
        # Add more widget types as needed
    
    def _set_widget_value(self, value):
        """Set a value on the widget."""
        if isinstance(self.widget, QPlainTextEdit):
            self.widget.setPlainText(str(value))
        elif isinstance(self.widget, QLineEdit):
            self.widget.setText(str(value))
        # Add more widget types as needed
```

### Usage Examples

```python
# Basic binding
self.bind(self.txt_source).to(self.document, "content")

# Binding with a specific signal
self.bind(self.txt_source).with_signal("textEdited").to(self.document, "content")

# Binding a specific widget property
self.bind(self.lbl_title, "text").to(self.document, "name")
```

## Domain Model Change Notification

For two-way binding to work, domain models need to notify observers when their properties change. Several approaches are possible:

### 1. Hybrid Observable Pattern

This approach combines a lightweight Observable mixin with property descriptors:

```python
class Observable:
    def __init__(self):
        self._observers = {}
    
    def observe(self, property_name):
        """Create an observable for a property."""
        return PropertyObservable(self, property_name)
    
    def add_observer(self, property_name, callback):
        if property_name not in self._observers:
            self._observers[property_name] = []
        self._observers[property_name].append(callback)
        return callback  # Return for easy removal
    
    def remove_observer(self, property_name, callback):
        if property_name in self._observers:
            self._observers[property_name].remove(callback)
    
    def notify_observers(self, property_name, value):
        if property_name in self._observers:
            for callback in self._observers[property_name]:
                callback(value)

class PropertyObservable:
    """Represents an observable property that can be subscribed to."""
    def __init__(self, observable, property_name):
        self.observable = observable
        self.property_name = property_name
    
    def subscribe(self, callback):
        """Subscribe to changes in this property."""
        return self.observable.add_observer(self.property_name, callback)

class ObservableProperty:
    """A property descriptor that automatically notifies observers."""
    def __init__(self, initial_value=None):
        self.name = None
        self.initial_value = initial_value
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(f"_{self.name}", self.initial_value)
    
    def __set__(self, instance, value):
        old_value = instance.__dict__.get(f"_{self.name}", self.initial_value)
        if old_value != value:
            instance.__dict__[f"_{self.name}"] = value
            if hasattr(instance, "notify_observers"):
                instance.notify_observers(self.name, value)
```

### 2. Qt-Style Signals in Domain Models

Alternatively, we could use Qt's signal mechanism:

```python
from PySide6.QtCore import QObject, Signal

class Document(QObject, IDocument):
    content_changed = Signal(str)  # Signal with new content
    name_changed = Signal(str)     # Signal with new name
    
    @property
    def content(self) -> str:
        return self._content
    
    @content.setter
    def content(self, value: str) -> None:
        if self._content != value:
            self._content = value
            self._is_modified = True
            self.content_changed.emit(value)
```

### 3. Custom Observer Pattern

A simpler approach without property descriptors:

```python
class Observable:
    def __init__(self):
        self._observers = {}  # property_name -> list of callbacks
    
    def add_observer(self, property_name: str, callback: callable):
        if property_name not in self._observers:
            self._observers[property_name] = []
        self._observers[property_name].append(callback)
    
    def remove_observer(self, property_name: str, callback: callable):
        if property_name in self._observers:
            self._observers[property_name].remove(callback)
    
    def notify_observers(self, property_name: str, value):
        if property_name in self._observers:
            for callback in self._observers[property_name]:
                callback(value)

class ObservableDocument(TextDocument, Observable):
    def __init__(self, *args, **kwargs):
        TextDocument.__init__(self, *args, **kwargs)
        Observable.__init__(self)
    
    @property
    def content(self) -> str:
        return self._content
    
    @content.setter
    def content(self, value: str) -> None:
        if self._content != value:
            self._content = value
            self._is_modified = True
            self.notify_observers("content", value)
```

## Integration with Existing Code

To integrate with the existing widget decorator system:

```python
@dataclass_transform()
def bindable_widget(name=None, classes=None, layout=None, **kwargs):
    def decorator(cls):
        # Apply the regular widget decorator first
        cls = widget(name, classes, layout, **kwargs)(cls)
        
        # Get the original init
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            # Call the original init
            original_init(self, *args, **kwargs)
            
            # Initialize the binding mixin if needed
            if isinstance(self, BindableMixin) and not hasattr(self, '_all_bindings'):
                BindableMixin.__init__(self)
            
            # Call setup_bindings if it exists
            if hasattr(self, 'setup_bindings') and callable(self.setup_bindings):
                self.setup_bindings()
        
        # Replace the init method
        cls.__init__ = new_init
        
        return cls
    
    return decorator
```

## Complete Example

Here's how everything would work together:

```python
class Document(TextDocument, Observable):
    content = ObservableProperty("")
    name = ObservableProperty("Untitled")
    
    def __init__(self):
        TextDocument.__init__(self)
        Observable.__init__(self)

@bindable_widget("editor")
class EditorWidget(QWidget, IWidget, BindableMixin):
    document: Document

    lbl_title: QLabel = make(QLabel)
    txt_source: QPlainTextEdit = make(QPlainTextEdit)
    
    def setup_bindings(self):
        self.bind(self.txt_source).to(self.document, "content")
        self.bind(self.lbl_title, "text").to(self.document, "name")
```

## Advantages of This Approach

1. **Fluent API**: The binding API is intuitive and chainable
2. **Two-Way by Default**: Bindings work in both directions
3. **Automatic Signal Selection**: Appropriate signals are selected based on widget type
4. **Extensible**: Easy to add support for new widget types
5. **Declarative**: Aligns with the existing declarative style of the codebase
6. **Testable**: Each component can be tested independently

## Next Steps for Experimentation

1. Implement a basic version of the `Observable` mixin and `ObservableProperty` descriptor
2. Create a simple `BindableMixin` with the `bind` method
3. Test with a simple example like binding a text edit to a document's content
4. Gradually add support for more widget types and properties
5. Integrate with the existing widget decorator system
