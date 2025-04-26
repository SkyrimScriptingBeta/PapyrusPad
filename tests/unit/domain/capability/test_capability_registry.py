from assertpy import assert_that

from PapyrusPad.domain.capability.capability_interface import (
    IPreviewable,
    IRunnable,
)
from PapyrusPad.domain.capability.capability_registry import CapabilityRegistry


class TestCapabilityRegistry:
    def test_register_capability(self) -> None:
        """Test registering a capability."""
        # Arrange
        registry = CapabilityRegistry()

        class TestCapability:
            @property
            def capability_id(self) -> str:
                return "test-capability"

        capability = TestCapability()

        # Act
        result = registry.register(capability)

        # Assert
        assert_that(result).is_true()
        assert_that(registry.has("test-capability")).is_true()
        assert_that(registry.get("test-capability")).is_equal_to(capability)

    def test_register_duplicate_capability(self) -> None:
        """Test registering a capability with the same ID."""
        # Arrange
        registry = CapabilityRegistry()

        class TestCapability1:
            @property
            def capability_id(self) -> str:
                return "test-capability"

        class TestCapability2:
            @property
            def capability_id(self) -> str:
                return "test-capability"

        capability1 = TestCapability1()
        capability2 = TestCapability2()

        # Act
        registry.register(capability1)
        result = registry.register(capability2)

        # Assert
        assert_that(result).is_false()
        assert_that(registry.get("test-capability")).is_equal_to(capability1)

    def test_get_typed(self) -> None:
        """Test getting a capability by ID and type."""
        # Arrange
        registry = CapabilityRegistry()

        class TestPreviewable:
            @property
            def capability_id(self) -> str:
                return "preview"

            def generate_preview(self) -> str:
                return "<html><body>Preview</body></html>"

        class TestRunnable:
            @property
            def capability_id(self) -> str:
                return "run"

            def run(self, args: list[str] | None = None) -> tuple[int, str, str]:
                return (0, "output", "")

        previewable = TestPreviewable()
        runnable = TestRunnable()

        registry.register(previewable)
        registry.register(runnable)

        # Act & Assert
        assert_that(registry.get_typed("preview", IPreviewable)).is_equal_to(previewable)
        assert_that(registry.get_typed("run", IRunnable)).is_equal_to(runnable)
        assert_that(registry.get_typed("preview", IRunnable)).is_none()
        assert_that(registry.get_typed("run", IPreviewable)).is_none()
        assert_that(registry.get_typed("nonexistent", IPreviewable)).is_none()

    def test_has(self) -> None:
        """Test checking if a capability is registered."""
        # Arrange
        registry = CapabilityRegistry()

        class TestCapability:
            @property
            def capability_id(self) -> str:
                return "test-capability"

        capability = TestCapability()

        # Act
        registry.register(capability)

        # Assert
        assert_that(registry.has("test-capability")).is_true()
        assert_that(registry.has("nonexistent")).is_false()

    def test_get_all(self) -> None:
        """Test getting all registered capabilities."""
        # Arrange
        registry = CapabilityRegistry()

        class TestCapability1:
            @property
            def capability_id(self) -> str:
                return "capability1"

        class TestCapability2:
            @property
            def capability_id(self) -> str:
                return "capability2"

        capability1 = TestCapability1()
        capability2 = TestCapability2()

        # Act
        registry.register(capability1)
        registry.register(capability2)
        all_capabilities = registry.get_all()

        # Assert
        assert_that(all_capabilities).contains(capability1)
        assert_that(all_capabilities).contains(capability2)
        assert_that(all_capabilities).is_length(2)
