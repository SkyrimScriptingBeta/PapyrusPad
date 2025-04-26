# Project Progress

## Current Status

PapyrusPad is in the early stages of development. The project has established its foundational architecture and basic UI framework, but most of the Papyrus-specific functionality is yet to be implemented.

## What Works

### Core Application Framework

- ✅ Basic Qt/PySide6 application structure
- ✅ Custom declarative widget system
- ✅ Window, widget, menu, and action decorators
- ✅ Factory functions for widget creation
- ✅ Type-safe data binding system
- ✅ Application startup and shutdown flow
- ✅ Dark/light mode support via command-line arguments
- ✅ Domain-driven file organization
- ✅ Dependency injection system
- ✅ Observable collections system with interfaces and base classes

### UI Components

- ✅ Main window with central editor widget
- ✅ Menu bar with File and Help menus
- ✅ Menu actions with icons, shortcuts, and tooltips
- ✅ Basic docking system implementation
- ✅ Tab management (closeable tabs, drag-to-undock)
- ✅ Title bar management for tabbed widgets
- ✅ Basic editor widget with QPlainTextEdit
- ✅ Two-way data binding between UI and domain models

### Development Infrastructure

- ✅ Poetry-based dependency management
- ✅ SCSS/Sass styling with hot-reloading in development
- ✅ Resource compilation (icons, fonts)
- ✅ PyInstaller packaging configuration
- ✅ Debug mode with debugpy support

### Domain Models

- ✅ Document model with observable properties
- ✅ Document collection with observable list behavior
- ✅ File system abstraction with memory and Qt implementations
- ✅ Dialog service abstraction with fake and Qt implementations

## What's In Progress

### Editor Enhancements

- ✅ Replacing QTextEdit with QPlainTextEdit for better performance
- 🔄 Custom text editor with line numbers and syntax highlighting
- 🔄 Editor configuration options (tab size, font, etc.)

### Docking System

- 🔄 Refining the dock manager implementation
- 🔄 Saving and restoring dock layouts
- 🔄 Default panel configurations

### Observable Collections

- ✅ Interface-based design for observable collections
- ✅ Base implementations for observable lists and dictionaries
- ✅ Integration with DocumentCollection
- 🔄 Additional collection types (filtered views, sorted views, etc.)

## What's Left to Build

### Papyrus Language Support

- ❌ Papyrus syntax highlighting
- ❌ Papyrus LSP client integration
- ❌ Autocomplete and IntelliSense
- ❌ Error checking and diagnostics
- ❌ Function signatures and tooltips
- ❌ Go to definition and references

### Compilation Support

- ❌ Integration with Creation Kit compiler
- ❌ Compilation error parsing and display
- ❌ Clickable error navigation
- ❌ Batch compilation support
- ❌ Build targets and configurations

### Project Management

- ❌ Project structure detection
- ❌ Script dependency analysis
- ❌ Project explorer panel
- ❌ File creation templates
- ❌ Project settings

### Modding Tool Integration

- ❌ Mod Organizer 2 integration
- ❌ Vortex integration
- ❌ BSA archive browsing
- ❌ PEX decompilation with Champollion
- ❌ Virtual filesystem support

### Additional Features

- ❌ Papyrus documentation browser
- ❌ Snippets for common patterns
- ❌ Linting and static analysis
- ❌ Settings panel and configuration
- ❌ Recent files and projects
- ❌ Session management

## Known Issues

- The current editor widget is a placeholder and lacks Papyrus-specific features
- Dock manager needs refinement for better tab management
- No persistent settings or configuration yet
- No project management capabilities
- Type checking challenges with generic types in observable collections

## Next Steps

1. **Immediate Focus**: Replace the basic QTextEdit with a custom QPlainTextEdit-based editor with syntax highlighting
2. **Short-term Goals**:
   - Implement Papyrus syntax highlighting
   - Begin LSP client integration
   - Create project explorer panel
3. **Medium-term Goals**:
   - Complete LSP integration
   - Add compilation support
   - Implement basic project management
4. **Long-term Goals**:
   - Modding tool integration
   - Advanced features like snippets and documentation
   - Packaging and distribution

## Evolution of Project Decisions

### Initial Approach

The project started with a focus on creating a minimal, fast-loading editor with the ability to expand functionality through dockable panels. This approach remains central to the design.

### Architectural Refinements

- **Declarative Widget System**: Evolved to simplify UI development with decorators and factory functions
- **Declarative Menu System**: Extended the declarative approach to menus and actions
- **Data Binding System**: Implemented a type-safe, registry-based data binding system for UI-to-model synchronization
- **Domain-driven File Organization**: Implemented a domain-driven file structure that organizes code by domain concepts
- **Dependency Injection**: Implemented a FastAPI-inspired dependency injection system
- **Docking System**: Enhanced to provide a more modern tab-based interface
- **Styling**: Moved to SCSS for better maintainability
- **Observable Collections**: Refactored to use interfaces and base classes for better type safety, code reuse, and flexibility

### Future Direction Considerations

- **Plugin Architecture**: Considering a formal plugin system for extensibility
- **Enhanced Data Binding**: Extending the data binding system to support validation, transformation, and more complex binding scenarios
- **Performance Optimization**: May need to optimize editor performance for large scripts
- **Distribution Strategy**: Evaluating options for distribution and updates
- **Observable Collections Extensions**: Considering extensions like filtered views, sorted views, mapped collections, batch operations, and undo/redo support
