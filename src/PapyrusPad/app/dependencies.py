from typing import Any
from PySide6.QtWidgets import QApplication
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, register_loader_containers

from PapyrusPad.app.application import Application


# Dependencies
class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)


# Global container
container = Container()
container.wire()
register_loader_containers(container)


# Lookup by dependency name
class Dependencies:
    application: Application = Provide[Container.application]


# Lookup by type
Depends: dict[type, Any] = {
    Application: Dependencies.application,
    QApplication: Dependencies.application,
}
