# System Patterns

## Architecture Overview

PapyrusPal follows a component-based architecture with a focus on extensibility through dockable panels. The application is built using Qt/PySide6 and leverages a custom declarative widget system to simplify UI development.

## Core Architectural Patterns

### Declarative Widget System

The application uses a custom declarative approach to Qt widgets, inspired by Ruby DSLs and Rails-style conventions:

1. **Widget Decorators**: `@widget` and `@window` decorators are used to define QWidgets and QMainWindow classes.
2. **Dataclass Integration**: All widget classes are Python dataclasses that implement the `IWidget` interface.
3. **Field-based Widget Declaration**: Widget fields are declared using helper functions like `make()` and `make_widget()`.
4. **Automatic Setup**: The decorators handle initialization and call setup methods automatically.

```python
@widget("EditorWidget", classes=["editor"])
class EditorWidget(QWidget, IWidget):
    lbl_title: QLabel = make(QLabel)
    txt_source: QTextEdit = make(QTextEdit)
    
    def setup(self) -> None:
        # Custom setup code
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

### Interface-based Design

The application uses interfaces to define contracts and enable loose coupling:

1. **IWidget Interface**: Defines the contract for all widget classes with methods like `setup()`, `setup_layout()`, etc.
2. **IDockManager Interface**: Defines the contract for dock management functionality.
3. **Abstract Base Classes**: Used to define interfaces with the `ABC` module.

```python
class IWidget(ABC):
    @abstractmethod
    def setup(self) -> None: ...
    
    @abstractmethod
    def setup_layout(self) -> None: ...
    
    # Other methods...
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

```python
class MainWindowMixin(SetupFunctionsMixin):
    """Mixin class to provide setup functions for PyQt/PySide main windows."""
    # Implementation...
```

### Decorator Pattern

Used to enhance classes with additional functionality:

1. **@widget**: Enhances QWidget classes with automatic setup and layout.
2. **@window**: Enhances QMainWindow classes with window-specific features.
3. **@dataclass_transform**: Used to maintain type checking with custom decorators.

```python
@dataclass_transform()
def widget(name: str | None = None, classes: list[str] | None = None, layout: str | None = "vertical"):
    # Implementation...
```

### Observer Pattern

Used for event handling and signal connections:

1. **Signal-Slot Connections**: Qt's signal-slot mechanism for event handling.
2. **Event Filtering**: Custom event handling through Qt's event filter system.
3. **File System Watching**: For style sheet hot-reloading during development.

```python
# Observer pattern with signals
dock.topLevelChanged.connect(lambda floating: self._update_title_bar_for(dock))
```

## Component Relationships

### Main Components

1. **MainWindow**: The primary container that hosts the central editor and dockable panels.
2. **EditorWidget**: The central widget that provides the core editing functionality.
3. **DockManager**: Manages the creation and behavior of dockable panels.
4. **Application**: Handles application-level concerns like styling and event loop.

### Data Flow

1. **User Input → Widgets**: User interactions are captured by widgets.
2. **Widgets → Application Logic**: Widgets trigger application logic through signals.
3. **Application Logic → Model**: Changes are applied to the underlying data model.
4. **Model → Widgets**: Updates in the model are reflected back in the UI.

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
