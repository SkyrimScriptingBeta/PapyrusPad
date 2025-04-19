from typing import cast, TYPE_CHECKING, Type, Callable, Any


def type_hint_only(mixin_cls: type) -> Callable[[Type[Any]], Type[Any]]:
    def decorator(cls: Type[Any]) -> Type[Any]:
        if TYPE_CHECKING:
            # Pretend we're adding mixin, just for Pylance
            return cast(Type[Any], cls)
        return cls

    return decorator
