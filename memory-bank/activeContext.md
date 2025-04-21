# Active Context

## Current Work Focus

The current focus of the PapyrusPad project is establishing the foundational architecture and UI framework. This includes:

1. **Core Application Structure**: Setting up the basic Qt/PySide6 application with a main window and central editor widget.
2. **Declarative Widget System**: Developing a custom declarative approach to Qt widgets using decorators and factory functions.
3. **Docking System**: Implementing a flexible docking system for panels with modern tab management.
4. **Development Infrastructure**: Establishing the development workflow with Poetry, SCSS styling, and resource compilation.

## Recent Changes

### Architecture and Framework

- Implemented the `@widget` and `@window` decorators for declarative UI definition
- Created factory functions (`make()`, `make_widget()`, `make_later()`) for widget creation
- Set up the main window with a central editor widget
- Implemented a dock manager for handling dockable panels
- Added support for dark/light mode via command-line arguments

### UI Components

- Created a basic editor widget (currently using QTextEdit)
- Implemented tab management with closeable tabs and drag-to-undock functionality
- Added title bar management for tabbed widgets
- Set up SCSS styling with hot-reloading in development mode

### Development Tools

- Configured Poetry for dependency management
- Set up PyInstaller for application packaging
- Added debugpy support for remote debugging
- Configured resource compilation for icons and fonts

## Next Steps

### Immediate Tasks

1. **Editor Enhancement**: Replace the basic QTextEdit with a custom QPlainTextEdit-based editor with:
   - Line numbers
   - Syntax highlighting
   - Code folding
   - Editor configuration options

2. **Docking System Refinement**:
   - Improve tab management
   - Add support for saving and restoring dock layouts
   - Create default panel configurations

3. **Papyrus Language Support**:
   - Implement Papyrus syntax highlighting
   - Begin LSP client integration for language intelligence

### Upcoming Considerations

1. **Project Management**:
   - Detect and manage Papyrus project structures
   - Create a project explorer panel
   - Implement file creation templates

2. **Compilation Support**:
   - Integrate with the Creation Kit compiler
   - Parse and display compilation errors
   - Implement clickable error navigation

## Active Decisions and Considerations

### Architecture Decisions

1. **Declarative UI Approach**: The decision to use a declarative approach with decorators and dataclasses has proven effective for simplifying UI development. This pattern will continue to be refined and expanded.

2. **Docking System**: The custom docking behavior built on top of Qt's docking system provides a more modern and user-friendly experience. Further refinements will focus on stability and user experience.

3. **Styling with SCSS**: Using SCSS for styling with hot-reloading in development has improved the styling workflow. This approach will be maintained and expanded with more comprehensive styling.

### Technical Considerations

1. **Editor Performance**: As we move to implement a custom editor, performance will be a key consideration, especially for large Papyrus scripts.

2. **LSP Integration**: The integration with the Papyrus LSP will require careful design to ensure responsiveness and reliability.

3. **Modding Tool Integration**: Planning for integration with mod managers (MO2, Vortex) needs to begin early to ensure a smooth experience.

### Open Questions

1. **Plugin Architecture**: Should we implement a formal plugin system for extensibility, and if so, what should the architecture look like?

2. **Project Structure**: What is the optimal project structure for Papyrus scripts, and how should we detect and manage it?

3. **Distribution Strategy**: What is the best approach for distributing the application to users?

## Important Patterns and Preferences

### Code Organization

- **Module Structure**: Maintain clear separation between UI components, application logic, and utilities.
- **Interface-based Design**: Continue using interfaces (ABC) to define contracts and enable loose coupling.
- **Typing**: Maintain strict typing throughout the codebase.

### UI Design

- **Minimal by Default**: Keep the default UI clean and minimal, with advanced features available through dockable panels.
- **Progressive Disclosure**: Organize features to reveal complexity progressively as needed.
- **Consistent Styling**: Maintain consistent styling across all components.

### Development Workflow

- **Test-Driven Development**: Consider implementing a testing strategy for critical components.
- **Documentation**: Document code and architecture decisions as they are made.
- **Incremental Development**: Focus on getting core features working well before adding advanced functionality.

## Learnings and Project Insights

### Successful Approaches

- The declarative widget system has significantly reduced boilerplate and simplified UI development.
- The docking system provides a flexible and user-friendly way to organize the interface.
- Using SCSS for styling has improved maintainability and development workflow.

### Challenges

- Qt's docking system requires significant customization to achieve a modern user experience.
- Balancing simplicity and power in the editor interface requires careful design.
- Integrating with external tools (compiler, LSP) will require robust error handling and user feedback.

### Future Opportunities

- The declarative widget system could potentially be extracted as a separate library for other Qt projects.
- The editor component could be enhanced with Papyrus-specific features beyond what general-purpose editors provide.
- Integration with mod managers could provide a seamless workflow for modders.
