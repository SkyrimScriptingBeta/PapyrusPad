# Dependency Injection System

## Overview

The Dependency Injection (DI) system in PapyrusPad provides a clean, type-safe way to manage application dependencies and promote loose coupling between components. Inspired by FastAPI's dependency injection approach, it allows components to request dependencies by type rather than creating or locating them directly.

## Architecture

The DI system follows a three-layer architecture:

```
┌─────────────────┐
│    Container     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dependencies   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Depends      │
└─────────────────┘
```

### Key Components

1. **Container**: A central `DeclarativeContainer` that manages singleton instances of application services.
2. **Dependencies Class**: A static class that provides access to dependencies by name.
3. **Depends Dictionary**: A type-based lookup system that allows components to request dependencies by type.
4. **Depends[T] Pattern**: A syntax for requesting dependencies in function parameters.

## Container

The container is implemented using the `dependency-injector` package and manages singleton instances of application services:

```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    """Container for application dependencies."""
    
    # Core application components
    application = providers.Singleton(Application)
    settings_manager = providers.Singleton(SettingsManager)
    
    # Domain services
    document_collection = providers.Singleton(DocumentCollection)
    dialog_service = providers.Singleton(DialogService)
    filesystem = providers.Singleton(FileSystem)
    
    # UI components
    dock_manager = providers.Singleton(DockManager)
```

Different container configurations are available for different environments:

- **Production Container**: Used in the production application.
- **Development Container**: Used during development, with additional debugging features.
- **Test Container**: Used for testing, with fake implementations of services.

## Dependencies Class

The Dependencies class provides access to dependencies by name:

```python
from dependency_injector.wiring import Provide

class Dependencies:
    """Static access to dependencies."""
    
    application: Application = Provide[Container.application]
    settings_manager: SettingsManager = Provide[Container.settings_manager]
    document_collection: DocumentCollection = Provide[Container.document_collection]
    dialog_service: DialogService = Provide[Container.dialog_service]
    filesystem: FileSystem = Provide[Container.filesystem]
    dock_manager: DockManager = Provide[Container.dock_manager]
```

This class serves as a bridge between the container and the Depends dictionary.

## Depends Dictionary

The Depends dictionary maps types to their implementations:

```python
Depends: dict[type, Any] = {
    Application: Dependencies.application,
    QApplication: Dependencies.application,  # Allow requesting by QApplication type
    SettingsManager: Dependencies.settings_manager,
    IDocumentCollection: Dependencies.document_collection,
    DocumentCollection: Dependencies.document_collection,
    IDialogService: Dependencies.dialog_service,
    DialogService: Dependencies.dialog_service,
    IFileSystem: Dependencies.filesystem,
    FileSystem: Dependencies.filesystem,
    IDockManager: Dependencies.dock_manager,
    DockManager: Dependencies.dock_manager,
}
```

This dictionary allows components to request dependencies by type rather than by name.

## Depends[T] Pattern

The Depends[T] pattern allows components to request dependencies in function parameters:

```python
@action("About", tooltip="Show information about the application")
class ShowAboutAction(QAction, IAction):
    @override
    def action(self, checked: bool, app: QApplication = Depends[QApplication]):
        # Use app dependency
        msg = QMessageBox()
        msg.setText(f"{app.applicationName()} {app.applicationVersion()}")
        msg.setInformativeText("This is a simple text editor.")
        msg.setWindowTitle("About")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
```

This pattern is implemented using a custom parameter resolver that looks up dependencies in the Depends dictionary:

```python
def resolve_dependencies(func: Callable) -> Callable:
    """
    Resolve dependencies for a function.
    
    Args:
        func: The function to resolve dependencies for
        
    Returns:
        A wrapper function that resolves dependencies
    """
    sig = inspect.signature(func)
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a mapping of parameter names to arguments
        bound_args = sig.bind_partial(*args, **kwargs)
        
        # Resolve dependencies for parameters with Depends annotations
        for param_name, param in sig.parameters.items():
            if param_name in bound_args.arguments:
                continue  # Skip parameters that already have values
                
            if param.annotation is inspect.Parameter.empty:
                continue  # Skip parameters without annotations
                
            # Check if the annotation is a Depends[T] type
            if hasattr(param.annotation, "__origin__") and param.annotation.__origin__ is Depends:
                # Get the dependency type
                dep_type = param.annotation.__args__[0]
                
                # Look up the dependency in the Depends dictionary
                if dep_type not in Depends:
                    raise ValueError(f"No dependency registered for type {dep_type.__name__}")
                    
                # Add the dependency to the arguments
                kwargs[param_name] = Depends[dep_type]
        
        return func(*args, **kwargs)
    
    return wrapper
```

The `@action` decorator applies this resolver to the `action` method:

```python
def action(text: str | None = None, *, shortcut: str | None = None, tooltip: str | None = None, icon: QPixmap | QIcon | QStyle.StandardPixmap | str | None = None):
    """
    Decorator for QAction classes.
    
    Args:
        text: The action text
        shortcut: The action shortcut
        tooltip: The action tooltip
        icon: The action icon
    """
    def decorator(cls):
        # Apply the ActionMixin
        cls = type(cls.__name__, (ActionMixin, cls), {})
        
        # Set class attributes
        if text is not None:
            cls._text = text
        if shortcut is not None:
            cls._shortcut = shortcut
        if tooltip is not None:
            cls._tooltip = tooltip
        if icon is not None:
            cls._icon = icon
            
        # Apply dependency resolution to the action method
        if hasattr(cls, "action"):
            cls.action = resolve_dependencies(cls.action)
            
        return cls
    
    return decorator
```

## Container Setup

The container is set up during application startup:

```python
def setup_container() -> Container:
    """
    Set up the dependency injection container.
    
    Returns:
        The container instance
    """
    # Create the container
    container = Container()
    
    # Configure the container
    container.config.from_dict({
        "application": {
            "name": "PapyrusPad",
            "version": "0.1.0",
        },
        "settings": {
            "theme": "dark",
            "font": "Fira Code",
            "font_size": 12,
        },
    })
    
    # Wire the container
    container.wire(modules=[
        "PapyrusPad.actions",
        "PapyrusPad.widgets",
        "PapyrusPad.windows",
    ])
    
    return container
```

Different container configurations are used for different environments:

```python
def get_container() -> Container:
    """
    Get the dependency injection container.
    
    Returns:
        The container instance
    """
    if os.environ.get("PAPYRUSPAD_ENV") == "test":
        from PapyrusPad.di.container_test import setup_container
    elif os.environ.get("PAPYRUSPAD_ENV") == "dev":
        from PapyrusPad.di.container_dev import setup_container
    else:
        from PapyrusPad.di.container_prod import setup_container
        
    return setup_container()
```

## Testing with Dependency Injection

The DI system is designed to facilitate testing by allowing dependencies to be replaced with test doubles:

```python
@pytest.fixture
def document_collection() -> DocumentCollection:
    """
    Provide a document collection for testing.
    
    Returns:
        A document collection instance
    """
    container = get_container()  # This will be the test container
    return container.document_collection()
```

The test container provides fake implementations of services:

```python
class ContainerTest(Container):
    """Container for testing."""
    
    # Override services with fake implementations
    dialog_service = providers.Singleton(FakeDialogService)
    filesystem = providers.Singleton(MemoryFileSystem)
```

## Singleton Reset

For testing, singleton instances are reset in place rather than recreated to maintain references:

```python
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

This approach ensures that tests are properly isolated while maintaining the integrity of the dependency injection system.

## Benefits

The DI system provides several benefits:

1. **Loose Coupling**: Components depend on interfaces rather than concrete implementations.
2. **Testability**: Dependencies can be easily replaced with test doubles.
3. **Centralized Configuration**: All dependencies are configured in one place.
4. **Type Safety**: Dependencies are requested by type, providing compile-time checking.
5. **Simplified Component Creation**: Components don't need to create or locate their dependencies.

## Best Practices

### Requesting Dependencies

- Always request dependencies by interface rather than concrete implementation when possible.
- Use the Depends[T] pattern for requesting dependencies in function parameters.
- Only request dependencies that are actually needed by the component.

```python
# Good
def action(self, checked: bool, dialog_service: IDialogService = Depends[IDialogService]):
    # Use dialog_service

# Bad
def action(self, checked: bool, dialog_service: DialogService = Depends[DialogService]):
    # Use dialog_service
```

### Registering Dependencies

- Register dependencies in the container using the appropriate provider (usually Singleton).
- Register dependencies by both interface and concrete implementation in the Depends dictionary.
- Use descriptive names for dependencies in the Dependencies class.

```python
# In the container
dialog_service = providers.Singleton(DialogService)

# In the Dependencies class
dialog_service: DialogService = Provide[Container.dialog_service]

# In the Depends dictionary
Depends: dict[type, Any] = {
    IDialogService: Dependencies.dialog_service,
    DialogService: Dependencies.dialog_service,
}
```

### Testing

- Use the test container for testing.
- Reset singleton instances in place rather than recreating them.
- Provide fake implementations of services for testing.
- Use pytest fixtures to access dependencies from the test container.

```python
@pytest.fixture
def dialog_service() -> FakeDialogService:
    container = get_container()
    return container.dialog_service()

def test_dialog_service(dialog_service: FakeDialogService):
    # Use dialog_service
```

## Future Enhancements

Potential future enhancements to the DI system:

1. **Scoped Dependencies**: Support for dependencies with different lifetimes (e.g., request-scoped, session-scoped).
2. **Factory Dependencies**: Support for dependencies that are created on demand.
3. **Conditional Dependencies**: Support for dependencies that are conditionally created based on configuration.
4. **Dependency Graphs**: Visualization of dependency relationships.
5. **Lazy Dependencies**: Support for dependencies that are created only when needed.
