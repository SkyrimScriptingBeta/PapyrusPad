## 💉 Dependency Injection Style Guide

This guide describes the dependency injection approach used in PapyrusPad, which is inspired by FastAPI's dependency injection system but adapted for a Qt application.

---

### ✅ Core Principles

- Use the `Depends[T]` pattern to request dependencies in function parameters
- Register dependencies in the central container
- Keep the dependency injection system simple and transparent
- Prefer constructor injection where possible

---

### 🧩 Dependency Injection System

The application uses a three-layer dependency injection system:

1. **Container**: A central `dependency_injector.containers.DeclarativeContainer` that manages singleton instances
2. **Dependencies Class**: A static class that provides access to dependencies by name
3. **Depends Dictionary**: A type-based lookup system that allows components to request dependencies by type

```python
# Layer 1: Container
class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)

# Layer 2: Dependencies class
class Dependencies:
    application: Application = Provide[Container.application]

# Layer 3: Depends dictionary
Depends: dict[type, Any] = {
    Application: Dependencies.application,
    QApplication: Dependencies.application,
}
```

---

### 🔌 Using Dependencies

Dependencies can be requested in function parameters using the `Depends[T]` pattern:

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

---

### 🧠 Registering Dependencies

To register a new dependency:

1. Add it to the `Container` class
2. Add it to the `Dependencies` class
3. Add it to the `Depends` dictionary if it should be accessible by type

```python
# 1. Add to Container
class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)
    settings_manager = providers.Singleton(SettingsManager)

# 2. Add to Dependencies class
class Dependencies:
    application: Application = Provide[Container.application]
    settings_manager: SettingsManager = Provide[Container.settings_manager]

# 3. Add to Depends dictionary
Depends: dict[type, Any] = {
    Application: Dependencies.application,
    QApplication: Dependencies.application,
    SettingsManager: Dependencies.settings_manager,
}
```

---

### 🛑 Prohibited Patterns

- ❌ Do not use `dependency_injector.wiring.inject` directly; use the `Depends[T]` pattern instead
- ❌ Do not create multiple containers; use a single container for the entire application
- ❌ Do not use circular dependencies
- ❌ Do not use dependencies in constructors; use them in methods instead

---

### 🧪 Testing

We've implemented a robust approach for testing with dependency injection:

1. **Reset Singletons In Place**: Instead of creating new instances or replacing the container, we reset the existing singleton instances between tests.
2. **Autouse Fixture**: We use an autouse fixture to reset all services before each test.
3. **Service-specific Reset Methods**: Each service that needs to be reset between tests implements a `reset()` method.

```python
# Autouse fixture to reset all services before each test
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

This approach ensures that:
1. The same instance is used throughout the tests, but with a clean state for each test
2. The dependency injection system's references remain intact
3. Tests are properly isolated from each other

For services that need to be mocked, you can still use the traditional approach:

```python
def test_about_action(monkeypatch):
    # Create mock application
    mock_app = Mock(spec=QApplication)
    mock_app.applicationName.return_value = "Test App"
    mock_app.applicationVersion.return_value = "1.0.0"
    
    # Get the container
    container = get_container()
    
    # Store the original application
    original_app = container.application()
    
    # Replace the application with the mock
    monkeypatch.setattr(container, "application", lambda: mock_app)
    
    try:
        # Create action and trigger it
        action = ShowAboutAction()
        action.trigger()
        
        # Assert mock was called
        mock_app.applicationName.assert_called_once()
        mock_app.applicationVersion.assert_called_once()
    finally:
        # Restore the original application
        monkeypatch.setattr(container, "application", lambda: original_app)
```

---

This guide defines the idiomatic, preferred usage patterns for dependency injection in PapyrusPad. Stick to these patterns to ensure a consistent and maintainable codebase.
