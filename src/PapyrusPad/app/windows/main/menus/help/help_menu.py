from PySide6.QtWidgets import QMenu
from PapyrusPad.app.windows.main.menus.help.actions.about import AboutAction
from qt_helpers.make import make
from qt_helpers.menu import menu


@menu(name="Help")
class HelpMenu(QMenu):
    about_action: AboutAction = make(AboutAction)
