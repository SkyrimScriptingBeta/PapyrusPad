## 🧙 Qt Helpers Style Guide: Declarative DSL for Widgets, Windows, Menus, and Actions

This guide describes the architecture and usage patterns for projects using `qt_helpers`, a declarative DSL layer built atop PySide6 (Qt 6.9.0). This system is strongly inspired by Ruby DSLs and Rails-style conventions.

---

### ✅ Core Principles
- Use **@widget**, **@window**, **@menu**, and **@action** decorators to define all QWidgets, QMainWindow, QMenu, and QAction classes.
- All widget/window classes must be **dataclasses** and implement the appropriate interfaces (IWidget, IAction).
- **Never** use `__init__` or `__post_init__`. These are handled automatically.
- Field declarations are used to instantiate widgets, menus, and actions.
- Configuration can be set using parameters to decorators or class attributes with underscore prefix.

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
    file_menu: FileMenu = make(FileMenu)
    help_menu: HelpMenu = make(HelpMenu)
```

- Sets object name, classes, window title, icon
- Automatically sets `central_widget` as main content
- Automatically adds QMenu fields to the menu bar
- Calls all setup methods

#### `@menu`
**Import**: `from qt_helpers.menu import menu`

```python
# Using decorator parameter
@menu(text="Help")
class HelpMenu(QMenu):
    about_action: AboutAction = make(AboutAction)

# Using class attribute
@menu()
class FileMenu(QMenu):
    _text = "File"
    quit_action: QuitAction = make(QuitAction)
```

- `text`: Sets the menu title (alternatively, use `_text` class attribute)
- Automatically adds QMenu and QAction fields as menu items
- Supports nested menus through field declarations

#### `@action`
**Import**: `from qt_helpers.action import action`

```python
# Using decorator parameters
@action("About", tooltip="Show information about the application", icon=QStyle.StandardPixmap.SP_MessageBoxQuestion)
class AboutAction(QAction, IAction):
    @override
    def action(self, checked: bool):
        # Action implementation

# Using class attributes
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

- `text`: Sets the action text (alternatively, use `_text` class attribute)
- `shortcut`: Sets the keyboard shortcut (alternatively, use `_shortcut` class attribute)
- `tooltip`: Sets the status tip (alternatively, use `_tooltip` class attribute)
- `icon`: Sets the icon (alternatively, use `_icon` class attribute)
- Automatically connects the `triggered` signal to the `action` method

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

#### `IAction`
**Import**: `from qt_helpers.interfaces import IAction`
```python
class IAction:
    def action(self, checked: bool) -> None: ...
```
This method is required for action classes and is automatically connected to the action's triggered signal.

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
- Menu classes should end in `Menu`
- Action classes should end in `Action`
- Object names: PascalCase, match class name for custom widgets
- QSS classes: lowercase kebab-case
- Class attributes for configuration: use underscore prefix (e.g., `_text`, `_shortcut`)

---

### 🛑 Prohibited Patterns
- ❌ Do not use `__init__` or `__post_init__`
- ❌ Do not imperatively build layouts
- ❌ Do not manually instantiate or set up child widgets
- ❌ Do not subclass QWidget without `@widget` or QMainWindow without `@window`
- ❌ Do not subclass QMenu without `@menu` or QAction without `@action`
- ❌ Do not manually connect action signals; use the `action` method instead

---

### 🔧 Async
- Use `qasync` for asyncio support
- `QEventLoop` from `qasync` should wrap your `asyncio` loops

---

### 📁 File Organization
- Follow a feature-based organization rather than type-based
- Group related components (menus, actions) by feature
- Example structure:
  ```
  src/PapyrusPad/app/
  └── windows/
      └── main/
          ├── main_window.py
          └── menus/
              ├── file/
              │   ├── file_menu.py
              │   └── actions/
              │       ├── new.py
              │       ├── open.py
              │       └── quit.py
              └── help/
                  ├── help_menu.py
                  └── actions/
                      └── about.py
  ```

---

This guide defines the idiomatic, preferred usage patterns for your PySide6 + qt_helpers project. Stick to the declarative Rails-for-Qt vibe and let the magic do the heavy lifting!
