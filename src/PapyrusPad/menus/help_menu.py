from PySide6.QtWidgets import QMenu
from PapyrusPad.actions.show_about_action import ShowAboutAction
from qt_helpers.make import make
from qt_helpers.menu import menu


# This is another way to set the menu text, you can pass everything to the decorator
@menu(text="Help")
class HelpMenu(QMenu):
    about_action: ShowAboutAction = make(ShowAboutAction)
