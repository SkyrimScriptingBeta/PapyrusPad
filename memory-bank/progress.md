# Project Progress

## Current Status

PapyrusPad is in the early stages of development. The project has established its foundational architecture and basic UI framework, but most of the Papyrus-specific functionality is yet to be implemented.

## What Works

### Core Application Framework

- ✅ Basic Qt/PySide6 application structure
- ✅ Custom declarative widget system
- ✅ Window and widget decorators
- ✅ Factory functions for widget creation
- ✅ Application startup and shutdown flow
- ✅ Dark/light mode support via command-line arguments

### UI Components

- ✅ Main window with central editor widget
- ✅ Basic docking system implementation
- ✅ Tab management (closeable tabs, drag-to-undock)
- ✅ Title bar management for tabbed widgets
- ✅ Basic editor widget structure (currently just a QTextEdit)

### Development Infrastructure

- ✅ Poetry-based dependency management
- ✅ SCSS/Sass styling with hot-reloading in development
- ✅ Resource compilation (icons, fonts)
- ✅ PyInstaller packaging configuration
- ✅ Debug mode with debugpy support

## What's In Progress

### Editor Enhancements

- 🔄 Replacing QTextEdit with QPlainTextEdit for better performance
- 🔄 Custom text editor with line numbers and syntax highlighting
- 🔄 Editor configuration options (tab size, font, etc.)

### Docking System

- 🔄 Refining the dock manager implementation
- 🔄 Saving and restoring dock layouts
- 🔄 Default panel configurations

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
- **Docking System**: Enhanced to provide a more modern tab-based interface
- **Styling**: Moved to SCSS for better maintainability

### Future Direction Considerations

- **Plugin Architecture**: Considering a formal plugin system for extensibility
- **Performance Optimization**: May need to optimize editor performance for large scripts
- **Distribution Strategy**: Evaluating options for distribution and updates
