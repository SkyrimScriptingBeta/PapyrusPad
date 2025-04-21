These features are DESIRED features and are not guaranteed to be implemented.

Pretty much nothing is implemented yet except just setting up a Qt/PySide6 project.

# PapyrusPal

**PapyrusPal** is a lightweight, modern, and script-focused IDE for writing and managing Bethesda's Papyrus scripts, aimed primarily at **Skyrim** and **Fallout 4** modders. Think *Notepad.exe* with a hidden arsenal of power: toggleable, dockable panels that reveal a full development suite.

## ✨ Features

- **Minimal UI by Default**: Starts as a clean, fast-loading editor using a custom `QPlainTextEdit`
- **Dockable IDE Panels**: Toggle project explorer, compiler output, LSP inspector, etc.
- **Syntax Highlighting**: Native Papyrus highlighting baked into the editor
- **Autocomplete & IntelliSense**: Powered by Language Server Protocol (LSP)

## 🧠 Language Server Support

PapyrusPal uses a **MIT-built LSP server** based on the excellent [Joel Day Papyrus Extension for VS Code](https://github.com/joelday/papyrus-lang).

- Integrates tightly with the official **Creation Kit compiler** and Papyrus metadata
- Provides function signatures, definitions, symbol lookup, and tooltips

## 🛠 Compilation & Tooling

- Interfaces with the **Bethesda Creation Kit compiler** for compiling `.psc` files
- Support for build targets, batch compiling, and clickable compile errors

## 🧩 Integration With Modding Tools

PapyrusPal integrates with the following key modding tools and formats:

- **Champollion** (MIT): For decompiling `.pex` to `.psc`
- **bsarch** (MPL): For browsing and managing `.bsa` archives
- **usvfs**: Virtual filesystem support for modding setups (e.g., MO2-like behavior)
- **MO2 & Vortex Support**:
  - Reads mod orders, config paths, and staging directories
  - Autoload your current modding profile for context-aware scripting

## 📁 Project-Aware Environment

- Smart detection of mod structure (scripts, sources, includes)
- Automatic linking to dependencies and Papyrus native types

## 🧪 Future Features

- Built-in Papyrus documentation browser
- Snippets for common modding patterns (OnInit, OnUpdate, utility scripts)
- Linting and static analysis
- Context-aware suggestions (AI-assisted long-term goal)

## 🔧 Tech Stack

- **Frontend**: Python with PySide6 (Qt6)
- **Backend**: LSP integration, filesystem tools, compiler interface
- **Language Tools**:
  - Papyrus compiler (Bethesda CK)
  - LSP from Joel Day’s MIT repo
  - Champollion (PEX decompiling)
  - bsarch (BSA archive handling)
  - usvfs (Virtual filesystem)

## 📜 License

PapyrusPal is open source (license TBD) and integrates the following open-source tools:

- Joel Day Papyrus LSP – MIT
- Champollion – MIT
- bsarch – MPL 2.0
- usvfs – Various open licenses

---

**PapyrusPal**: A total Swiss Army knife for Papyrus scripting — lean, extensible, and tuned for serious modders.
