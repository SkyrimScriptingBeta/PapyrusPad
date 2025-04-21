# Technical Context

## Core Technologies

### Python

- **Version**: 3.13
- **Role**: Primary programming language for the entire application
- **Key Features Used**:
  - Type hints and strict type checking
  - Dataclasses for model representation
  - Modern syntax (union types with `|`, pattern matching, etc.)
  - Abstract base classes for interface definitions

### Qt/PySide6

- **Version**: PySide6 6.9.0 (Qt 6.9.0)
- **Role**: GUI framework providing widgets, layouts, and event handling
- **Key Components Used**:
  - QWidget-based UI (no QtQuick/QML)
  - QDockWidget for dockable panels
  - QTabBar for tab management
  - QPlainTextEdit for the code editor
  - QFileSystemWatcher for file monitoring
  - Event filtering system for custom behaviors

### Language Server Protocol (LSP)

- **Source**: Joel Day's MIT-licensed Papyrus LSP implementation
- **Role**: Provides language intelligence features like autocomplete and error checking
- **Integration**: Via pylspclient library

## Development Tools

### Poetry

- **Role**: Dependency management and packaging
- **Key Features Used**:
  - Virtual environment management
  - Dependency resolution
  - Script execution via poethepoet

### PyInstaller

- **Role**: Application packaging for distribution
- **Configuration**: Both onefile and onedir options available

### SCSS/Sass

- **Role**: Stylesheet preprocessing for UI styling
- **Library**: libsass for Python
- **Workflow**: SCSS files are compiled to QSS (Qt's CSS-like styling language)

## Dependencies

### Primary Dependencies

- **pyside6**: Qt bindings for Python
- **qasync**: Asyncio integration with Qt's event loop
- **pylspclient**: Client library for Language Server Protocol
- **dependency-injector**: Dependency injection container
- **libsass**: SCSS/Sass compiler

### Development Dependencies

- **debugpy**: Remote debugging support
- **poethepoet**: Task runner for Poetry
- **pyinstaller**: Application packaging

## Development Environment

### IDE Support

- **Type Checking**: Strict mode with pyright
- **Linting**: Configured for high standards of code quality
- **Formatting**: Black with 180 character line length

### Build System

- **Task Runner**: Poethepoet for development tasks
- **Resource Compilation**: pyside6-rcc for Qt resources
- **Packaging**: PyInstaller for executable creation

## External Integrations

### Planned Integrations

- **Creation Kit Compiler**: For compiling Papyrus scripts
- **Champollion**: For decompiling PEX to PSC
- **bsarch**: For BSA archive handling
- **usvfs**: For virtual filesystem support
- **Mod Organizer 2 & Vortex**: For mod management integration

## Technical Constraints

### Platform Support

- **Primary**: Windows (with dark mode support)
- **Secondary**: Potentially macOS and Linux

### Performance Considerations

- **Startup Time**: Must be fast-loading for quick script edits
- **Memory Usage**: Should be lightweight compared to full IDEs
- **Responsiveness**: UI must remain responsive during compilation or LSP operations

## Technical Decisions

### Declarative Widget System

- **Decision**: Create a custom declarative system for Qt widgets
- **Rationale**: Simplify widget creation and reduce boilerplate
- **Implementation**: Decorators and factory functions

### Docking System

- **Decision**: Implement custom docking behavior on top of Qt's docking system
- **Rationale**: Provide a more modern and user-friendly docking experience
- **Implementation**: Event filtering and signal connections

### Styling Approach

- **Decision**: Use SCSS for styling with hot-reloading in development
- **Rationale**: More maintainable styling with variables and nesting
- **Implementation**: File watching and compilation to QSS

### Async Support

- **Decision**: Use qasync for asyncio integration
- **Rationale**: Allow for non-blocking operations while maintaining UI responsiveness
- **Implementation**: QEventLoop from qasync wrapping asyncio loops

## Development Setup

### Required Tools

- Python 3.13
- Poetry for dependency management
- Qt resources compiler (pyside6-rcc)

### Development Workflow

1. Clone repository
2. Install dependencies with Poetry
3. Run development server with hot-reloading
4. Compile resources when changed
5. Package with PyInstaller when ready for distribution

### Environment Variables

- **QT_QPA_PLATFORM**: Controls dark/light mode on Windows
- Debug flags available via command-line arguments

## Deployment Strategy

### Packaging

- **Windows**: Single executable with embedded Python and dependencies
- **Distribution**: Direct download and potentially through mod manager extensions

### Updates

- **Strategy**: Manual updates initially, potential for auto-update system later
- **Versioning**: Semantic versioning (major.minor.patch)
