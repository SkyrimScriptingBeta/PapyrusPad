from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")


@runtime_checkable
class ICapability(Protocol):
    """Base interface for all capabilities."""

    @property
    @abstractmethod
    def capability_id(self) -> str:
        """Get the unique identifier for this capability."""
        ...


@runtime_checkable
class IPreviewable(ICapability, Protocol):
    """Interface for document types that can be previewed."""

    @abstractmethod
    def generate_preview(self) -> str:
        """
        Generate a preview of the document content.

        Returns:
            HTML content for preview
        """
        ...


@runtime_checkable
class IRunnable(ICapability, Protocol):
    """Interface for document types that can be run/executed."""

    @abstractmethod
    def run(self, args: list[str] | None = None) -> tuple[int, str, str]:
        """
        Run the document content.

        Args:
            args: Optional command line arguments

        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        ...


@runtime_checkable
class IFormattable(ICapability, Protocol):
    """Interface for document types that can be formatted."""

    @abstractmethod
    def format_content(self, content: str) -> str:
        """
        Format the document content.

        Args:
            content: The content to format

        Returns:
            The formatted content
        """
        ...


@runtime_checkable
class ILintable(ICapability, Protocol):
    """Interface for document types that can be linted."""

    @abstractmethod
    def lint(self) -> list[dict[str, Any]]:
        """
        Lint the document content.

        Returns:
            A list of lint issues, each as a dictionary with at least 'line', 'column', 'message', and 'severity' keys
        """
        ...


@runtime_checkable
class ICompilable(ICapability, Protocol):
    """Interface for document types that can be compiled."""

    @abstractmethod
    def compile(self, output_path: str | None = None) -> tuple[bool, str]:
        """
        Compile the document content.

        Args:
            output_path: Optional path to write the compiled output

        Returns:
            Tuple of (success, error_message)
        """
        ...
