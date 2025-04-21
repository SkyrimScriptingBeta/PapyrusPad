from abc import ABC, abstractmethod
from typing import Optional

from PapyrusPad.domain.filesystem.models import FileInfo, DirectoryInfo


class IFileSystem(ABC):
    """
    Interface for filesystem operations.
    Abstracts file and directory operations to allow for different implementations
    (real filesystem, in-memory, etc.)
    """

    @abstractmethod
    def read_text(self, path: str) -> str:
        """
        Read text content from a file.

        Args:
            path: Path to the file

        Returns:
            The text content of the file

        Raises:
            FileNotFoundError: If the file does not exist
        """
        ...

    @abstractmethod
    def write_text(self, path: str, content: str) -> None:
        """
        Write text content to a file.

        Args:
            path: Path to the file
            content: Text content to write

        Raises:
            IOError: If the file cannot be written
        """
        ...

    @abstractmethod
    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists.

        Args:
            path: Path to the file

        Returns:
            True if the file exists, False otherwise
        """
        ...

    @abstractmethod
    def delete_file(self, path: str) -> bool:
        """
        Delete a file.

        Args:
            path: Path to the file

        Returns:
            True if the file was deleted, False if it did not exist
        """
        ...

    @abstractmethod
    def get_file_info(self, path: str) -> Optional[FileInfo]:
        """
        Get information about a file.

        Args:
            path: Path to the file

        Returns:
            FileInfo object if the file exists, None otherwise
        """
        ...

    @abstractmethod
    def list_files(self, dir_path: str) -> list[FileInfo]:
        """
        List all files in a directory.

        Args:
            dir_path: Path to the directory

        Returns:
            List of FileInfo objects for all files in the directory
        """
        ...

    @abstractmethod
    def list_dirs(self, dir_path: str) -> list[DirectoryInfo]:
        """
        List all subdirectories in a directory.

        Args:
            dir_path: Path to the directory

        Returns:
            List of DirectoryInfo objects for all subdirectories in the directory
        """
        ...

    @abstractmethod
    def create_directory(self, path: str) -> bool:
        """
        Create a directory.

        Args:
            path: Path to the directory

        Returns:
            True if the directory was created or already exists, False otherwise
        """
        ...

    @abstractmethod
    def directory_exists(self, path: str) -> bool:
        """
        Check if a directory exists.

        Args:
            path: Path to the directory

        Returns:
            True if the directory exists, False otherwise
        """
        ...

    @abstractmethod
    def delete_directory(self, path: str, recursive: bool = False) -> bool:
        """
        Delete a directory.

        Args:
            path: Path to the directory
            recursive: If True, delete all contents recursively

        Returns:
            True if the directory was deleted, False if it did not exist or could not be deleted
        """
        ...

    @abstractmethod
    def get_directory_info(self, path: str) -> Optional[DirectoryInfo]:
        """
        Get information about a directory.

        Args:
            path: Path to the directory

        Returns:
            DirectoryInfo object if the directory exists, None otherwise
        """
        ...

    @abstractmethod
    def get_parent_directory(self, path: str) -> Optional[str]:
        """
        Get the parent directory of a path.

        Args:
            path: Path to get the parent of

        Returns:
            Path to the parent directory, or None if there is no parent
        """
        ...

    @abstractmethod
    def join_paths(self, *paths: str) -> str:
        """
        Join path components.

        Args:
            *paths: Path components to join

        Returns:
            Joined path
        """
        ...

    @abstractmethod
    def normalize_path(self, path: str) -> str:
        """
        Normalize a path.

        Args:
            path: Path to normalize

        Returns:
            Normalized path
        """
        ...
