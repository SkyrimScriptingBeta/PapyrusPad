# System Patterns

## Architecture Overview

PapyrusPad follows a component-based architecture with a focus on extensibility through dockable panels. The application is built using Qt/PySide6 and leverages a custom declarative widget system to simplify UI development. It also uses dependency injection to manage application dependencies and promote loose coupling.

## Core Architectural Patterns

### Declarative Widget System

The application uses a custom declarative approach to Qt widgets, inspired by Ruby DSLs and Rails-style conventions:

1. **Widget Decorators**: `@widget`, `@window`, `@menu`, and `@action` decorators are used to define QWidgets, QMainWindow, QMenu, and QAction classes.
2. **Dataclass Integration**: All widget classes are Python dataclasses that implement the appropriate interfaces (IWidget, IAction).
3. **Field-based Widget Declaration**: Widget fields are declared using helper functions like `make()` and `make_widget()`.
4. **Automatic Setup**: The decorators handle initialization and call setup methods automatically, including binding setup.
5. **Dependency Injection**: Components can request dependencies using the `Depends[T]` pattern.

```python
@widget("EditorWidget", classes=["editor"])
class EditorWidget(QWidget, IWidget):
    lbl_title: QLabel = make(QLabel)
    txt_source: QTextEdit = make(QTextEdit)
    
    def setup(self) -> None:
        # Custom setup code
```

### Data Binding System

The application implements a type-safe, registry-based data binding system for synchronizing UI elements with domain models:

1. **Central Registry**: A global registry maps widget types and property names to binding adapters.
2. **Binding Adapters**: Type-safe adapters define how to get signals from and set values on specific widget types.
3. **Observable Fields**: Domain models expose observable fields that notify listeners when values change.
4. **Declarative Binding**: Widgets declare bindings in their `setup_bindings` method using a simple API.
5. **Two-way Binding**: Changes in either the UI or the model are automatically propagated to the other.
6. **Lock Mechanism**: A lock flag prevents infinite update loops between UI and model.

```python
# Registering a binding adapter for QPlainTextEdit
BINDING_REGISTRY[(QPlainTextEdit, "plainText")] = BindingAdapter[QPlainTextEdit, [str]](
    signal_getter=make_signal_getter_for_no_arg("textChanged", lambda w: w.toPlainText()),
    setter=lambda w, val: w.setPlainText(val),
)

# Using the binding in a widget
@override
def setup_bindings(self) -> None:
    bind_fields([(self.txt_source, "plainText", self.document.content_observable)])

# Observable field in a domain model
@dataclass
class TextDocument(IDocument):
    _content: ObservableField[str] = field(default_factory=lambda: ObservableField(""))
    
    @property
    def content(self) -> str:
        return self._content.get()
        
    @content.setter
    def content(self, value: str) -> None:
        if self._content.get() != value:
            self._content.set(value)
            self._is_modified = True
            
    @property
    def content_observable(self) -> ObservableField[str]:
        return self._content
```

### Declarative Menu System

The application extends the declarative approach to menus and actions:

1. **Menu Decorator**: The `@menu` decorator is used to define QMenu classes with automatic child menu and action handling.
2. **Action Decorator**: The `@action` decorator is used to define QAction classes with automatic signal connection.
3. **Field-based Menu Structure**: Menus and actions are declared as fields in their parent classes, creating a hierarchical structure.
4. **Multiple Configuration Styles**: Both decorators support configuration through either decorator parameters or class attributes.

```python
# Menu with decorator parameter
@menu(text="Help")
class HelpMenu(QMenu):
    about_action: AboutAction = make(AboutAction)

# Menu with class attribute
@menu()
class FileMenu(QMenu):
    _text = "File"
    quit_action: QuitAction = make(QuitAction)

# Action with decorator parameters
@action("About", tooltip="Show information about the application", icon=QStyle.StandardPixmap.SP_MessageBoxQuestion)
class AboutAction(QAction, IAction):
    @override
    def action(self, checked: bool):
        # Action implementation

# Action with class attributes
@action()
class QuitAction(QAction, IAction):
    _text = "Quit"
    _shortcut = "Ctrl+Q"
    _tooltip = "Exit the application"
    _icon = QStyle.StandardPixmap.SP_TitleBarCloseButton

    @override
    def action(self, checked: bool) -> None:
        # Action implementation
```

### Dockable Panel System

The application implements a dockable panel system that allows for a flexible, user-configurable interface:

1. **DockManager**: A central manager class that handles dock widget creation, tabification, and event handling.
2. **Tab Management**: Custom tab behavior including closeable tabs, drag-to-undock functionality, and title bar management.
3. **Event Filtering**: Uses Qt's event filtering system to intercept mouse events for custom tab behavior.

```python
# Adding a dockable panel
dock = dock_manager.dock(
    widget=my_widget,
    area=Qt.DockWidgetArea.RightDockWidgetArea,
    title="My Panel"
)
```

### Dependency Injection System

The application uses a dependency injection system to manage dependencies and promote loose coupling:

1. **Container**: A central container manages singleton instances of application services.
2. **Dependencies Class**: A static class provides access to dependencies by name.
3. **Depends Dictionary**: A type-based lookup system allows components to request dependencies by type.
4. **FastAPI-inspired Syntax**: Components can request dependencies using a syntax similar to FastAPI's `Depends()`.
5. **Singleton Reset**: For testing, singleton instances are reset in place rather than recreated to maintain references.

```python
def action(self, checked: bool, app: QApplication = Depends[QApplication]):
    # Use app dependency
```

```python
# Resetting a singleton for testing
@pytest.fixture(autouse=True)
def reset_all_services():
    """Reset all services before each test."""
    container = get_container()
    
    # Reset the dialog service
    dialog_service = container.dialog_service()
    if hasattr(dialog_service, "reset"):
        dialog_service.reset()
    
    # Reset the document collection
    document_collection = container.document_collection()
    for doc in document_collection.list_documents():
        document_collection.remove(doc.id)
    
    yield
```

### Interface-based Design

The application uses interfaces to define contracts and enable loose coupling:

1. **IWidget Interface**: Defines the contract for all widget classes with methods like `setup()`, `setup_layout()`, etc.
2. **IAction Interface**: Defines the contract for action classes with the `action()` method.
3. **IDockManager Interface**: Defines the contract for dock management functionality.
4. **Abstract Base Classes**: Used to define interfaces with the `ABC` module.

```python
class IWidget(ABC):
    @abstractmethod
    def setup(self) -> None: ...
    
    @abstractmethod
    def setup_layout(self) -> None: ...
    
    # Other methods...

class IAction(ABC):
    @abstractmethod
    def action(self, checked: bool) -> None:
        """Defines the default action behavior for QAction instances."""
        pass
```

## Design Patterns

### Factory Pattern

Used extensively through helper functions that create widgets:

1. **make()**: Creates any object for use in dataclass fields.
2. **make_widget()**: Creates Qt widgets with name and class properties.
3. **make_later()**: Creates fields that will be initialized later.

```python
# Factory pattern in action
label: QLabel = make_widget(QLabel, "MyLabel", "Hello World")
```

### Mixin Pattern

Used to add functionality to classes without deep inheritance hierarchies:

1. **SetupFunctionsMixin**: Provides setup methods for widgets.
2. **WidgetMixin**: Adds widget-specific functionality.
3. **MainWindowMixin**: Adds main window-specific functionality.
4. **MenuMixin**: Adds menu-specific functionality.
5. **ActionMixin**: Adds action-specific functionality.

```python
class MainWindowMixin(SetupFunctionsMixin):
    """Mixin class to provide setup functions for PyQt/PySide main windows."""
    # Implementation...

class MenuMixin:
    _text: str | None = None
    
    def __init__(self):
        super().__init__()

class ActionMixin:
    _text: str | None = None
    _shortcut: str | None = None
    _tooltip: str | None = None
    _icon: str | QPixmap | QIcon | QStyle.StandardPixmap | None = None
    
    def __init__(self):
        super().__init__()
        
    def action(self, checked: bool) -> None:
        pass
```

### Decorator Pattern

Used to enhance classes with additional functionality:

1. **@widget**: Enhances QWidget classes with automatic setup and layout.
2. **@window**: Enhances QMainWindow classes with window-specific features and automatic menu loading.
3. **@menu**: Enhances QMenu classes with automatic action and submenu loading.
4. **@action**: Enhances QAction classes with automatic signal connection.
5. **@dataclass_transform**: Used to maintain type checking with custom decorators.

```python
@dataclass_transform()
def widget(name: str | None = None, classes: list[str] | None = None, layout: str | None = "vertical"):
    # Implementation...

@dataclass_transform()
def menu(text: str | None = None):
    # Implementation...

@dataclass_transform()
def action(text: str | None = None, *, shortcut: str | None = None, tooltip: str | None = None, icon: QPixmap | QIcon | QStyle.StandardPixmap | str | None = None):
    # Implementation...
```

### Observer Pattern

Used for event handling and signal connections:

1. **Signal-Slot Connections**: Qt's signal-slot mechanism for event handling.
2. **Event Filtering**: Custom event handling through Qt's event filter system.
3. **File System Watching**: For style sheet hot-reloading during development.
4. **Observable Fields**: Generic observable value containers that notify listeners when values change.

```python
# Observer pattern with signals
dock.topLevelChanged.connect(lambda floating: self._update_title_bar_for(dock))

# Observer pattern with observable fields
@dataclass
class ObservableField(Generic[T]):
    _value: T
    _callbacks: list[Callable[[T], None]] = field(default_factory=list[Callable[[T], None]])

    def get(self) -> T:
        return self._value

    def set(self, value: T) -> None:
        if value != self._value:
            self._value = value
            for callback in self._callbacks:
                callback(value)

    def bind(self, callback: Callable[[T], None]) -> None:
        self._callbacks.append(callback)
        callback(self._value)  # trigger immediately with current value
```

## File Organization

The application follows a domain-driven, feature-based organization:

```
src/PapyrusPad/
├── __main__.py          # Application entry point
├── main.py              # Main application setup
├── qrc_resources.py     # Compiled resources
├── actions/             # Action classes
│   ├── quit_action.py
│   └── show_about_action.py
├── app/                 # Core application components
│   ├── application.py   # QApplication subclass
│   └── dependencies.py  # Dependency injection setup
├── domain/              # Domain models and business logic
├── menus/               # Menu classes
│   ├── file_menu.py
│   ├── help_menu.py
│   └── view_menu.py
├── services/            # Application services
├── widgets/             # Widget components
│   └── editor_widget.py
└── windows/             # Window components
    └── main_window.py
```

## Component Relationships

### Main Components

1. **MainWindow**: The primary container that hosts the central editor, menus, and dockable panels.
2. **EditorWidget**: The central widget that provides the core editing functionality.
3. **Menus**: Hierarchical menu structure with File, Help, etc.
4. **Actions**: Encapsulated action handlers for menu items.
5. **DockManager**: Manages the creation and behavior of dockable panels.
6. **Application**: Handles application-level concerns like styling and event loop.
7. **Dependencies**: Manages application dependencies and wiring.
8. **Binding Registry**: Central registry for widget binding adapters.
9. **Observable Fields**: Domain model properties that notify listeners when values change.

### Data Flow

1. **User Input → Widgets**: User interactions are captured by widgets.
2. **Widgets → Model**: Changes in widgets are automatically propagated to the model through bindings.
3. **Model → Widgets**: Changes in the model are automatically propagated to widgets through bindings.
4. **Model → Application Logic**: Application logic operates on the model.
5. **Application Logic → Model**: Application logic updates the model, which triggers UI updates through bindings.

## Critical Implementation Paths

### Application Startup

1. Load fonts and resources
2. Initialize the main window
3. Set up the central editor widget
4. Configure the dock manager
5. Apply styles
6. Show the window and start the event loop

### Dockable Panel Creation

1. Create the panel widget
2. Create a dock widget through the dock manager
3. Add the dock widget to the main window
4. Connect signals for title bar management
5. Update tab features

### Style Management

1. In development mode: Watch SCSS files for changes
2. Compile SCSS to QSS
3. Apply the stylesheet to the application
4. In production mode: Load pre-compiled QSS from resources

## Future Architecture Considerations

1. **Plugin System**: A formal plugin architecture to allow for extensibility.
2. **Language Server Protocol Integration**: Full LSP client implementation for Papyrus.
3. **Virtual File System**: Integration with mod managers' virtual file systems.
4. **Compiler Integration**: Direct integration with the Papyrus compiler.
5. **Project Management**: Formal project structure and management.
6. **Menu Extension System**: Allow plugins to extend the menu system.
7. **Enhanced Data Binding**: Extend the data binding system to support validation, transformation, and more complex binding scenarios.
8. **Testing Framework**: Comprehensive testing strategy with proper test isolation. We've already implemented a robust approach for resetting singleton instances between tests, which will serve as the foundation for our testing framework.
