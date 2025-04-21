from dependency_injector import containers, providers
from dependency_injector.wiring import register_loader_containers

from PapyrusPad.app.application import Application
from qt_helpers.dependency_injection import DIRegistry


# Dependencies
class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)


# Global container
container = Container()
container.wire()
register_loader_containers(container)

DI = DIRegistry(Container)
