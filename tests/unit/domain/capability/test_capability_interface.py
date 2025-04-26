from assertpy import assert_that
from typing import Any

from PapyrusPad.domain.capability.capability_interface import (
    ICapability,
    IPreviewable,
    IRunnable,
    IFormattable,
    ILintable,
    ICompilable,
)


class TestCapabilityInterfaces:
    def test_capability_protocol(self) -> None:
        """Test that ICapability is a Protocol that can be implemented."""

        class TestCapability:
            @property
            def capability_id(self) -> str:
                return "test-capability"

        # Assert that the class implements the protocol
        capability = TestCapability()
        assert_that(isinstance(capability, ICapability)).is_true()

    def test_previewable_protocol(self) -> None:
        """Test that IPreviewable is a Protocol that can be implemented."""

        class TestPreviewable:
            @property
            def capability_id(self) -> str:
                return "preview"

            def generate_preview(self) -> str:
                return "<html><body>Preview</body></html>"

        # Assert that the class implements the protocol
        previewable = TestPreviewable()
        assert_that(isinstance(previewable, IPreviewable)).is_true()
        assert_that(isinstance(previewable, ICapability)).is_true()
        assert_that(previewable.generate_preview()).is_equal_to("<html><body>Preview</body></html>")

    def test_runnable_protocol(self) -> None:
        """Test that IRunnable is a Protocol that can be implemented."""

        class TestRunnable:
            @property
            def capability_id(self) -> str:
                return "run"

            def run(self, args: list[str] | None = None) -> tuple[int, str, str]:
                return (0, "output", "")

        # Assert that the class implements the protocol
        runnable = TestRunnable()
        assert_that(isinstance(runnable, IRunnable)).is_true()
        assert_that(isinstance(runnable, ICapability)).is_true()
        assert_that(runnable.run()).is_equal_to((0, "output", ""))

    def test_formattable_protocol(self) -> None:
        """Test that IFormattable is a Protocol that can be implemented."""

        class TestFormattable:
            @property
            def capability_id(self) -> str:
                return "format"

            def format_content(self, content: str) -> str:
                return content.strip()

        # Assert that the class implements the protocol
        formattable = TestFormattable()
        assert_that(isinstance(formattable, IFormattable)).is_true()
        assert_that(isinstance(formattable, ICapability)).is_true()
        assert_that(formattable.format_content("  test  ")).is_equal_to("test")

    def test_lintable_protocol(self) -> None:
        """Test that ILintable is a Protocol that can be implemented."""

        class TestLintable:
            @property
            def capability_id(self) -> str:
                return "lint"

            def lint(self) -> list[dict[str, Any]]:
                return [{"line": 1, "column": 1, "message": "Test", "severity": "error"}]

        # Assert that the class implements the protocol
        lintable = TestLintable()
        assert_that(isinstance(lintable, ILintable)).is_true()
        assert_that(isinstance(lintable, ICapability)).is_true()
        assert_that(lintable.lint()).is_equal_to([{"line": 1, "column": 1, "message": "Test", "severity": "error"}])

    def test_compilable_protocol(self) -> None:
        """Test that ICompilable is a Protocol that can be implemented."""

        class TestCompilable:
            @property
            def capability_id(self) -> str:
                return "compile"

            def compile(self, output_path: str | None = None) -> tuple[bool, str]:
                return (True, "")

        # Assert that the class implements the protocol
        compilable = TestCompilable()
        assert_that(isinstance(compilable, ICompilable)).is_true()
        assert_that(isinstance(compilable, ICapability)).is_true()
        assert_that(compilable.compile()).is_equal_to((True, ""))
