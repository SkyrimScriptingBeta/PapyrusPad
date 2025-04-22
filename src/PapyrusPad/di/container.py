container_class: type | None = None


def set_container_class(container: type) -> None:
    """Set the container class to be used for dependency injection.

    Args:
        container (type): The container class to be used.
    """
    global container_class
    container_class = container
    print(f"Container class set to {container_class.__name__}")


def get_container_class() -> type:
    """Get the container class.

    Returns:
        type: The container class.
    """
    if container_class is None:
        raise RuntimeError("Container class not set. Call set_container_class() first.")
    return container_class
