# Data Binding Architecture Proposals for PapyrusPad

This document outlines three different approaches to implementing data binding between the UI and domain models in PapyrusPad. Each approach has its own strengths and weaknesses, and the choice depends on the specific requirements and complexity of the application.

## Background

Currently, PapyrusPad has a one-way data flow from the document model to the UI, but no mechanism to update the document model when the user edits text in the `QPlainTextEdit`. This is why saving works (the file is created) but the content is empty - the document's content property is never updated from the editor.

## Approach 1: Observer Pattern with Property Binding System

This approach creates a generic property binding system that can be used throughout the application.

### Key Components:

#### `Observable` Base Class
```python
class Observable:
    def __init__(self):
        self._observers = {}  # Dict of property_name -> list of observers
        
    def add_observer(self, property_name: str, observer: callable):
        if property_name not in self._observers:
            self._observers[property_name] = []
        self._observers[property_name].append(observer)
        
    def remove_observer(self, property_name: str, observer: callable):
        if property_name in self._observers:
            self._observers[property_name].remove(observer)
            
    def notify_observers(self, property_name: str):
        if property_name in self._observers:
            for observer in self._observers[property_name]:
                observer()
```

#### `ObservableProperty` Descriptor
```python
class ObservableProperty:
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
            if isinstance(instance, Observable):
                instance.notify_observers(self.name)
```

#### Enhanced Document Model
```python
class ObservableDocument(TextDocument, Observable):
    content = ObservableProperty("")
    name = ObservableProperty("Untitled")
    path = ObservableProperty(None)
    is_modified = ObservableProperty(False)
    
    def __init__(self):
        TextDocument.__init__(self)
        Observable.__init__(self)
```

#### Binding Manager
```python
class BindingManager:
    def __init__(self):
        self._bindings = []
        
    def bind_property(self, source_obj, source_prop, target_obj, target_prop=None, transform=None):
        """Bind a property from source to target with optional transformation."""
        if target_prop is None:
            target_prop = source_prop
            
        def update_target():
            value = getattr(source_obj, source_prop)
            if transform:
                value = transform(value)
            setattr(target_obj, target_prop, value)
            
        # Initial update
        update_target()
        
        # Add observer for future updates
        if isinstance(source_obj, Observable):
            source_obj.add_observer(source_prop, update_target)
            
        # Store binding for cleanup
        self._bindings.append((source_obj, source_prop, update_target))
        
        return update_target  # Return the update function for manual updates
        
    def bind_bidirectional(self, obj1, prop1, obj2, prop2=None, transform1to2=None, transform2to1=None):
        """Create a two-way binding between properties."""
        if prop2 is None:
            prop2 = prop1
            
        # Flag to prevent infinite update loops
        updating = False
        
        def update_obj2():
            nonlocal updating
            if updating:
                return
            updating = True
            value = getattr(obj1, prop1)
            if transform1to2:
                value = transform1to2(value)
            setattr(obj2, prop2, value)
            updating = False
            
        def update_obj1():
            nonlocal updating
            if updating:
                return
            updating = True
            value = getattr(obj2, prop2)
            if transform2to1:
                value = transform2to1(value)
            setattr(obj1, prop1, value)
            updating = False
            
        # Initial update
        update_obj2()
        
        # Add observers
        if isinstance(obj1, Observable):
            obj1.add_observer(prop1, update_obj2)
        if isinstance(obj2, Observable):
            obj2.add_observer(prop2, update_obj1)
            
        # Store bindings for cleanup
        self._bindings.append((obj1, prop1, update_obj2))
        self._bindings.append((obj2, prop2, update_obj1))
        
        return (update_obj2, update_obj1)
```

#### Usage Example
```python
# In EditorWidget
def setup(self) -> None:
    self.binding_manager = BindingManager()
    
    # Bind document content to editor text
    self.binding_manager.bind_bidirectional(
        self.document, "content",
        self.txt_source, "plainText"
    )
    
    # Bind document name to label
    self.binding_manager.bind_property(
        self.document, "name",
        self.lbl_title, "text"
    )
```

### Pros:
- Generic and reusable across the entire application
- Supports one-way and two-way binding
- Supports property transformation
- Minimal changes to existing models
- Easy to test with mock observers

### Cons:
- More complex implementation
- Requires careful handling of circular updates
- May need special handling for Qt signals

## Approach 2: MVVM with ViewModels and Commands

This approach follows the Model-View-ViewModel pattern, which is popular in WPF and other UI frameworks.

### Key Components:

#### `ViewModel` Base Class
```python
class ViewModel:
    def __init__(self):
        self._property_changed_handlers = {}
        
    def on_property_changed(self, property_name: str, handler: callable):
        if property_name not in self._property_changed_handlers:
            self._property_changed_handlers[property_name] = []
        self._property_changed_handlers[property_name].append(handler)
        
    def notify_property_changed(self, property_name: str):
        if property_name in self._property_changed_handlers:
            for handler in self._property_changed_handlers[property_name]:
                handler()
```

#### `Command` Class
```python
class Command:
    def __init__(self, execute_func, can_execute_func=None):
        self.execute = execute_func
        self._can_execute = can_execute_func or (lambda: True)
        self._can_execute_changed_handlers = []
        
    def can_execute(self):
        return self._can_execute()
        
    def on_can_execute_changed(self, handler):
        self._can_execute_changed_handlers.append(handler)
        
    def notify_can_execute_changed(self):
        for handler in self._can_execute_changed_handlers:
            handler()
```

#### Document ViewModel
```python
class DocumentViewModel(ViewModel):
    def __init__(self, document: IDocument):
        super().__init__()
        self._document = document
        self._text = document.content
        
        # Commands
        self.save_command = Command(
            execute_func=self.save,
            can_execute_func=lambda: self.is_modified
        )
        
    @property
    def text(self):
        return self._text
        
    @text.setter
    def text(self, value):
        if self._text != value:
            self._text = value
            self._document.content = value
            self.notify_property_changed("text")
            self.notify_property_changed("is_modified")
            self.save_command.notify_can_execute_changed()
            
    @property
    def title(self):
        return self._document.name
        
    @property
    def is_modified(self):
        return self._document.is_modified
        
    def save(self):
        # Logic to save the document
        pass
```

#### View Binding
```python
class ViewBinder:
    def __init__(self):
        self._bindings = []
        
    def bind_text_edit(self, view_model, property_name, text_edit):
        """Bind a text edit to a view model property."""
        # Update text edit when view model changes
        def update_text_edit():
            text_edit.setPlainText(getattr(view_model, property_name))
            
        view_model.on_property_changed(property_name, update_text_edit)
        
        # Update view model when text edit changes
        def on_text_changed():
            setattr(view_model, property_name, text_edit.toPlainText())
            
        text_edit.textChanged.connect(on_text_changed)
        
        # Initial update
        update_text_edit()
        
        self._bindings.append((view_model, property_name, update_text_edit))
        
    def bind_command(self, command, button):
        """Bind a command to a button."""
        def update_enabled():
            button.setEnabled(command.can_execute())
            
        command.on_can_execute_changed(update_enabled)
        button.clicked.connect(command.execute)
        
        # Initial update
        update_enabled()
```

#### Usage Example
```python
# In EditorWidget
def setup(self) -> None:
    self.view_model = DocumentViewModel(self.document)
    self.view_binder = ViewBinder()
    
    # Bind text edit to view model
    self.view_binder.bind_text_edit(
        self.view_model, "text", self.txt_source
    )
    
    # Bind save button to save command
    self.view_binder.bind_command(
        self.view_model.save_command, self.btn_save
    )
```

### Pros:
- Clear separation of concerns
- Commands provide a clean way to handle user actions
- ViewModels can be tested independently of the UI
- Supports complex UI logic and validation

### Cons:
- More verbose than other approaches
- Requires creating ViewModels for each model
- May be overkill for simple bindings

## Approach 3: Reactive Programming with Observables

This approach uses reactive programming principles, similar to RxPy or ReactiveX.

### Key Components:

#### `Observable` and `Observer` Interfaces
```python
class IObservable:
    def subscribe(self, observer):
        pass
        
    def unsubscribe(self, observer):
        pass
        
class IObserver:
    def on_next(self, value):
        pass
        
    def on_error(self, error):
        pass
        
    def on_completed(self):
        pass
```

#### `Subject` Implementation
```python
class Subject(IObservable):
    def __init__(self):
        self._observers = []
        
    def subscribe(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
        return observer
        
    def unsubscribe(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
            
    def notify(self, value):
        for observer in self._observers:
            observer.on_next(value)
            
    def notify_error(self, error):
        for observer in self._observers:
            observer.on_error(error)
            
    def notify_completed(self):
        for observer in self._observers:
            observer.on_completed()
```

#### `BehaviorSubject` Implementation
```python
class BehaviorSubject(Subject):
    def __init__(self, initial_value=None):
        super().__init__()
        self._value = initial_value
        
    @property
    def value(self):
        return self._value
        
    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.notify(new_value)
        
    def subscribe(self, observer):
        observer = super().subscribe(observer)
        observer.on_next(self._value)
        return observer
```

#### Reactive Document Model
```python
class ReactiveDocument:
    def __init__(self, document: IDocument):
        self._document = document
        
        # Create subjects for each property
        self.content = BehaviorSubject(document.content)
        self.name = BehaviorSubject(document.name)
        self.is_modified = BehaviorSubject(document.is_modified)
        
        # Update document when subjects change
        self.content.subscribe(Observer(
            on_next=lambda value: setattr(document, "content", value)
        ))
        
        self.name.subscribe(Observer(
            on_next=lambda value: setattr(document, "name", value)
        ))
```

#### `Observer` Implementation
```python
class Observer(IObserver):
    def __init__(self, on_next=None, on_error=None, on_completed=None):
        self._on_next = on_next or (lambda x: None)
        self._on_error = on_error or (lambda e: None)
        self._on_completed = on_completed or (lambda: None)
        
    def on_next(self, value):
        self._on_next(value)
        
    def on_error(self, error):
        self._on_error(error)
        
    def on_completed(self):
        self._on_completed()
```

#### UI Binding
```python
class ReactiveBinding:
    @staticmethod
    def bind_text_edit(subject, text_edit):
        """Bind a text edit to a subject."""
        # Update text edit when subject changes
        subject.subscribe(Observer(
            on_next=lambda value: text_edit.setPlainText(value)
        ))
        
        # Update subject when text edit changes
        def on_text_changed():
            if subject.value != text_edit.toPlainText():
                subject.value = text_edit.toPlainText()
                
        text_edit.textChanged.connect(on_text_changed)
```

#### Usage Example
```python
# In EditorWidget
def setup(self) -> None:
    self.reactive_document = ReactiveDocument(self.document)
    
    # Bind text edit to content subject
    ReactiveBinding.bind_text_edit(
        self.reactive_document.content, self.txt_source
    )
    
    # Bind label to name subject
    self.reactive_document.name.subscribe(Observer(
        on_next=lambda value: self.lbl_title.setText(value)
    ))
```

### Pros:
- Powerful and flexible reactive programming model
- Supports complex transformations and combinations of observables
- Good for handling asynchronous events
- Well-suited for complex UI interactions

### Cons:
- Steeper learning curve
- More complex than other approaches
- May be overkill for simple bindings
- Requires careful handling of subscriptions to avoid memory leaks

## Recommendation

For PapyrusPad, starting with **Approach 1: Observer Pattern with Property Binding System** is recommended for these reasons:

1. It provides a good balance of flexibility and simplicity
2. It can be incrementally adopted without rewriting existing code
3. It's easy to test with mock observers
4. It scales well as the application grows
5. It's familiar to developers with experience in other UI frameworks

As the application grows, consider moving to Approach 2 (MVVM) for more complex views that require validation and commands, or Approach 3 (Reactive) for views with complex event handling.
