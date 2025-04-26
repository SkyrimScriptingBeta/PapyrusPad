"""Python capabilities factory."""

from typing import Callable

from PapyrusPad.domain.capability.capability_interface import IRunnable
from .python_runnable import PythonRunnable


class PythonCapabilities:
    """Factory for python document capabilities."""

    @staticmethod
    def create_runnable(document_content_provider: Callable[[], str]) -> IRunnable:
        """
        Create a python runnable capability.

        Args:
            document_content_provider: A callable that returns the document content

        Returns:
            A python runnable capability
        """
        return PythonRunnable(document_content_provider)
