from assertpy import assert_that
from unittest.mock import Mock

from PapyrusPad.document_types.markdown.markdown_capabilities import MarkdownCapabilities
from PapyrusPad.document_types.python.python_capabilities import PythonCapabilities
from PapyrusPad.domain.capability.capability_interface import IPreviewable, IRunnable


class TestCapabilities:
    def test_markdown_preview_capability(self) -> None:
        """Test markdown preview capability."""
        # Arrange
        content_provider = Mock(return_value="# Heading\n\nSome text")

        # Act
        capability = MarkdownCapabilities.create_preview(content_provider)

        # Assert
        assert_that(capability.capability_id).is_equal_to("preview")
        assert_that(capability).is_instance_of(IPreviewable)

        # Test preview generation
        preview = capability.generate_preview()
        assert_that(preview).contains("<h1>Heading</h1>")
        assert_that(preview).contains("<p>Some text</p>")
        content_provider.assert_called_once()

    def test_python_runnable_capability(self) -> None:
        """Test python runnable capability."""
        # Arrange
        content_provider = Mock(return_value="print('Hello, World!')")

        # Act
        capability = PythonCapabilities.create_runnable(content_provider)

        # Assert
        assert_that(capability.capability_id).is_equal_to("run")
        assert_that(capability).is_instance_of(IRunnable)

        # Test running the code
        exit_code, stdout, stderr = capability.run()
        assert_that(exit_code).is_equal_to(0)
        assert_that(stdout.strip()).is_equal_to("Hello, World!")
        assert_that(stderr).is_empty()
        content_provider.assert_called_once()

    def test_python_runnable_with_error(self) -> None:
        """Test python runnable capability with syntax error."""
        # Arrange
        content_provider = Mock(return_value="print('Incomplete string")

        # Act
        capability = PythonCapabilities.create_runnable(content_provider)

        # Assert
        exit_code, stdout, stderr = capability.run()
        assert_that(exit_code).is_not_equal_to(0)
        assert_that(stdout).is_empty()
        assert_that(stderr).contains("SyntaxError")
        content_provider.assert_called_once()

    def test_python_runnable_with_args(self) -> None:
        """Test python runnable capability with command line arguments."""
        # Arrange
        content_provider = Mock(return_value="import sys\nprint(sys.argv[1:])")

        # Act
        capability = PythonCapabilities.create_runnable(content_provider)

        # Assert
        exit_code, stdout, stderr = capability.run(["arg1", "arg2"])
        assert_that(exit_code).is_equal_to(0)
        assert_that(stdout.strip()).is_equal_to("['arg1', 'arg2']")
        assert_that(stderr).is_empty()
        content_provider.assert_called_once()
