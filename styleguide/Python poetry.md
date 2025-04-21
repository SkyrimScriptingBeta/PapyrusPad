## 🐍 Python Project Tooling Guide

This project uses **Poetry 2.0+** and **Poe the Poet** for all Python-related dependency and task management.

---

### 📦 Poetry
- Poetry is the **only** tool used for dependency management and running Python commands.
- Always use `poetry run` — never `poetry shell`.
- All scripts and CLI tools are expected to run through the Poetry virtual environment.

#### Example:
```bash
poetry run python some_script.py
poetry run app --dev
```

#### Scripts (pyproject.toml)
```toml
[tool.poetry.scripts]
app = "PapyrusPad.app.__main__:main"
```
- This defines the entrypoint for the application as `poetry run app`

---

### ⚙️ Poe the Poet
- Task runner used via `poe` CLI
- Tasks are defined in `[tool.poe.tasks]` in `pyproject.toml`

#### Common Tasks:
```toml
[tool.poe.tasks]
dev = "poetry run app --dev"
dev-dark = "poetry run app --dev --dark"
dev-debug = "poetry run app --dev --debug"
dev-light = "poetry run app --dev --light"
prod = "poetry run app"
prod-dark = "poetry run app --dark"
prod-light = "poetry run app --light"
exe = "pyinstaller --onefile --windowed --noconfirm --name \"Papyrus Pad\" --icon resources/images/icon.ico src/PapyrusPad/app/__main__.py"
exe-dir = "pyinstaller --onedir --windowed --noconfirm --name \"Papyrus Pad\" --icon resources/images/icon.ico src/PapyrusPad/app/__main__.py"
qrc = "pyside6-rcc -o src/PapyrusPad/app/qrc_resources.py resources/resources.qrc"
```

#### Run a Poe task:
```bash
poe dev
poe prod-dark
poe qrc
```

#### Supported Formats:
```toml
[tool.poe.tasks]
# Shell command
hello = "echo Hello world"

# Python script
start.script = "PapyrusPad.app.__main__:main"

# Shell (explicit)
custom.shell = "some_shell_command --arg1 value"
```

---

### 🛑 Avoid
- Never use `poetry shell`
- Never manually activate virtualenvs
- Never run Python commands outside `poetry run`

---

This setup ensures consistent environments, reproducible builds, and centralized task automation using modern Python tooling.
