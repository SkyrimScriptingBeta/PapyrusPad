## 🧱 PySide6 Style Guide for AI Assistant

- Target **Qt 6.9.0** via **PySide6** — use the latest available API and syntax.
- Use **QWidget-based UIs only**. Do **not** use `.ui` files or Qt Designer.
- Do **not** use **QtQuick** or QML. Only QWidget and related classes.
- Prefer using the **correct Enums**, e.g.:
  - `Qt.DockWidgetArea.AllDockWidgetAreas`
  - `QDockWidget.DockWidgetFeature.DockWidgetClosable`
- Use `qasync` for **asyncio integration**. All async code should be properly integrated using `qasync.QEventLoop`.
