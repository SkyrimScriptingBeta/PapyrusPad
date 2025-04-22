# Import setup_test_dependencies FIRST before any other imports
from PapyrusPad.di.setup import setup_test_dependencies

# Set up test dependencies BEFORE any application code is loaded
setup_test_dependencies()

# Now it's safe to import other modules
import pytest
from PapyrusPad.di.container import get_container
from PapyrusPad.domain.dialog.dialog_fake import FakeDialogService


@pytest.fixture
def dialog_service() -> FakeDialogService:
    """Fixture that provides the fake dialog service from the test container."""
    service = get_container().dialog_service()
    # Ensure we're getting the fake implementation
    assert isinstance(service, FakeDialogService)
    # Reset the service before each test
    service.reset()
    return service


@pytest.fixture
def document_collection():
    """Fixture that provides the document collection from the test container."""
    return get_container().document_collection()


@pytest.fixture
def filesystem():
    """Fixture that provides the filesystem from the test container."""
    return get_container().filesystem()
