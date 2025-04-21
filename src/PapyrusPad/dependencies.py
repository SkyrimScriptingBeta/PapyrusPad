from dependency_injector import containers, providers

import PapyrusPad
from PapyrusPad.app.application import Application


class Container(containers.DeclarativeContainer):
    application = providers.Singleton(Application)


container = Container()
container.wire(packages=[PapyrusPad], modules=["PapyrusPad.actions.show_about_action"])
