# Import setup_test_dependencies FIRST before any other imports
from PapyrusPad.di.setup import setup_test_dependencies

# Set up test dependencies BEFORE any application code is loaded
setup_test_dependencies()

# Now it's safe to import other modules
import pytest
import tempfile
from pathlib import Path
from PapyrusPad.di.container import get_container
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService


@pytest.fixture(autouse=True)
def reset_all_services():
    """Reset all services before each test."""
    # Get the container
    container = get_container()

    # Reset the dialog service
    dialog_service = container.dialog_service()
    if hasattr(dialog_service, "reset"):
        dialog_service.reset()

    # Reset the document collection
    document_collection = container.document_collection()
    for doc in document_collection.list_documents():
        document_collection.remove(doc.id)

    # Yield to allow the test to run
    yield


@pytest.fixture
def dialog_service() -> FakeDialogService:
    """Fixture that provides the fake dialog service from the test container."""
    # Get the container
    container = get_container()

    # Get the existing singleton instance
    service = container.dialog_service()

    # Ensure we're getting the fake implementation
    assert isinstance(service, FakeDialogService)

    # Reset the service state
    service.reset()

    return service


@pytest.fixture
def document_collection():
    """Fixture that provides the document collection from the test container."""
    # Get the container
    container = get_container()

    # Get the existing singleton instance
    collection = container.document_collection()

    # Reset the collection by removing all documents
    for doc in collection.list_documents():
        collection.remove(doc.id)

    return collection


@pytest.fixture
def temp_dir():
    """Fixture that provides a temporary directory that is automatically cleaned up."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
    # The temporary directory is automatically cleaned up when the context manager exits


@pytest.fixture
def filesystem():
    """Fixture that provides the filesystem from the test container."""
    # Get the container
    container = get_container()

    # Get the existing singleton instance
    return container.filesystem()
