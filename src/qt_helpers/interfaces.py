from abc import abstractmethod


class IWidget:
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def setup_layout(self) -> None:
        pass

    @abstractmethod
    def setup_styles(self) -> None:
        pass

    @abstractmethod
    def setup_events(self) -> None:
        pass

    @abstractmethod
    def setup_signals(self) -> None:
        pass
