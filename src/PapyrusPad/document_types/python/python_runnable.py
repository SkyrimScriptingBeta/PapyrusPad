"""Python runnable capability implementation."""

import subprocess
import sys
import tempfile
from typing import Callable, override, List, Tuple

from PapyrusPad.domain.capability.capability_interface import IRunnable


class PythonRunnable(IRunnable):
    """Python runnable capability."""

    def __init__(self, document_content_provider: Callable[[], str]):
        """
        Initialize the python runnable capability.

        Args:
            document_content_provider: A callable that returns the document content
        """
        self._document_content_provider = document_content_provider

    @property
    @override
    def capability_id(self) -> str:
        """Get the capability ID."""
        return "run"

    @override
    def run(self, args: List[str] | None = None) -> Tuple[int, str, str]:
        """
        Run the python code.

        Args:
            args: Command line arguments to pass to the script

        Returns:
            A tuple of (exit_code, stdout, stderr)
        """
        content = self._document_content_provider()

        # Create a temporary file to run the code
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Build the command
            cmd = [sys.executable, temp_file_path]
            if args:
                cmd.extend(args)

            # Run the process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Get the output
            stdout, stderr = process.communicate()
            exit_code = process.returncode

            return exit_code, stdout, stderr
        except Exception as e:
            return 1, "", f"Error running Python code: {str(e)}"
