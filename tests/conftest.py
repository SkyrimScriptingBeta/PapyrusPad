import pytest
import contextlib
from PapyrusPad.di.container_registry import ContainerRegistry
from PapyrusPad.di.container_test import TestContainer


@contextlib.contextmanager
def use_test_container():
    """Context manager for using the test container.

    This temporarily replaces the active container with a test container,
    and restores the original container when done.

    Yields:
        TestContainer: The test container instance.
    """
    # Create test container
    test_container = TestContainer()

    # Store original container
    original_container = ContainerRegistry.get_container()

    try:
        # Set the test container as the active container
        ContainerRegistry.set_container(test_container)

        # Yield the test container for use in tests
        yield test_container

    finally:
        # Restore the original container
        ContainerRegistry.set_container(original_container)


@pytest.fixture
def test_di():
    """Fixture for using the test container in tests.

    This sets up a test container for the duration of the test,
    and restores the original container when done.

    Yields:
        TestContainer: The test container instance.
    """
    with use_test_container() as container:
        yield container
