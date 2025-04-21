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

### 🧪 Testing (Future)

In the future, we will add support for testing with dependency injection:

1. Create a test container that overrides dependencies with mocks
2. Use a context manager to temporarily replace the global container with the test container
3. Reset the container after each test

```python
# Example (future implementation)
def test_about_action():
    # Create mock application
    mock_app = Mock(spec=QApplication)
    mock_app.applicationName.return_value = "Test App"
    mock_app.applicationVersion.return_value = "1.0.0"
    
    # Create test container
    test_container = Container()
    test_container.application.override(mock_app)
    
    # Use test container
    with use_test_container(test_container):
        # Create action and trigger it
        action = ShowAboutAction()
        action.trigger()
        
        # Assert mock was called
        mock_app.applicationName.assert_called_once()
        mock_app.applicationVersion.assert_called_once()
```

---

This guide defines the idiomatic, preferred usage patterns for dependency injection in PapyrusPad. Stick to these patterns to ensure a consistent and maintainable codebase.
