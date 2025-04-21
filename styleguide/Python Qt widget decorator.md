## 🧙 Qt Helpers Style Guide: Declarative DSL for Widgets and Windows

This guide describes the architecture and usage patterns for projects using `qt_helpers`, a declarative DSL layer built atop PySide6 (Qt 6.9.0). This system is strongly inspired by Ruby DSLs and Rails-style conventions.

---

### ✅ Core Principles
- Use **@widget** and **@window** decorators to define all QWidgets and QMainWindow classes.
- All widget/window classes must be **dataclasses** and implement **IWidget**.
- **Never** use `__init__` or `__post_init__`. These are handled automatically.
- Field declarations are used to instantiate widgets.
- Object names and QSS classes are set using parameters to decorators or `make_widget()`.

---

### 🧩 Decorators

#### `@widget`
**Import**: `from qt_helpers.widget import widget`

```python
@widget("EditorWidget", classes=["editor"], layout="vertical")
class EditorWidget(QWidget, IWidget):
    # fields defined here using make/make_widget
```

- `name`: Sets `setObjectName()` (PascalCase, match class name if custom)
- `classes`: Sets QSS `"class"` property
- `layout`: Can be "horizontal", "vertical", or `QBoxLayout.Direction`
- Automatically adds child widgets to layout in declaration order
- Calls `setup()`, `setup_layout()`, `setup_styles()`, `setup_events()`, `setup_signals()`

#### `@window`
**Import**: `from qt_helpers.window import window`

```python
@window("MainWindow", classes=["window"], title="My App")
class MainWindow(QMainWindow, IWidget):
    central_widget: EditorWidget = make(EditorWidget)
```

- Sets object name, classes, window title, icon
- Automatically sets `central_widget` as main content
- Calls all setup methods

---

### 🧱 Field Helpers

#### `make()`
**Import**: `from qt_helpers.make import make`
```python
label: QLabel = make(QLabel, "Label text")
```
- Use for any custom widget or basic construction with args

#### `make_later()`
**Import**: `from qt_helpers.make import make_later`
```python
label: QLabel = make_later(QLabel)
```
- Use when a field must be set later

#### `make_widget()`
**Import**: `from qt_helpers.make_widget import make_widget`
```python
label: QLabel = make_widget(QLabel, "MyLabel", "Label text")
button: QPushButton = make_widget(QPushButton, ("BtnSave", ["primary"]), "Save")
```
- Use for basic Qt widgets (not custom ones)
- Sets object name and QSS classes

---

### 🔌 Interfaces

#### `IWidget`
**Import**: `from qt_helpers.interfaces import IWidget`
```python
class IWidget:
    def setup(self) -> None: ...
    def setup_layout(self) -> None: ...
    def setup_styles(self) -> None: ...
    def setup_events(self) -> None: ...
    def setup_signals(self) -> None: ...
```
These methods are optional, but called automatically if defined.

---

### 🎨 Styling with QSS (SCSS-backed)
- SCSS files live in `resources/styles/`
- Main file is `main.scss`, which imports partials like `_app.scss`
- New style files can be added and imported from `main.scss`
- QSS is generated automatically; no manual compilation required
- Use `setObjectName` and `setProperty("class", ...)` for styling hooks

---

### 📦 Resources
- QRC file: `resources/resources.qrc`
- After changes, run: `poetry run poe qrc`

---

### 🧠 Naming Conventions
- Widget classes must end in `Widget`
- Main window classes must end in `Window`
- Object names: PascalCase, match class name for custom widgets
- QSS classes: lowercase kebab-case

---

### 🛑 Prohibited Patterns
- ❌ Do not use `__init__` or `__post_init__`
- ❌ Do not imperatively build layouts
- ❌ Do not manually instantiate or set up child widgets
- ❌ Do not subclass QWidget without `@widget` or QMainWindow without `@window`

---

### 🔧 Async
- Use `qasync` for asyncio support
- `QEventLoop` from `qasync` should wrap your `asyncio` loops

---

This guide defines the idiomatic, preferred usage patterns for your PySide6 + qt_helpers project. Stick to the declarative Rails-for-Qt vibe and let the magic do the heavy lifting!
