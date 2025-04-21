from dataclasses import dataclass, field
from datetime import datetime
import os
import posixpath
from typing import Dict, Optional
from typing import override

from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.filesystem.models import FileInfo, DirectoryInfo


@dataclass
class MemoryFileSystem(IFileSystem):
    """
    In-memory implementation of IFileSystem.
    Useful for testing and for operations that don't need to persist to disk.
    """

    _files: Dict[str, str] = field(default_factory=dict)
    _file_info: Dict[str, FileInfo] = field(default_factory=dict)
    _dir_info: Dict[str, DirectoryInfo] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """
        Initialize the root directory.
        """
        # Create root directory
        self._dir_info["/"] = DirectoryInfo(path="/", name="/", last_modified=datetime.now())

    @override
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
        norm_path = self.normalize_path(path)
        if not self.file_exists(norm_path):
            raise FileNotFoundError(f"File not found: {norm_path}")
        return self._files[norm_path]

    @override
    def write_text(self, path: str, content: str) -> None:
        """
        Write text content to a file.

        Args:
            path: Path to the file
            content: Text content to write

        Raises:
            IOError: If the file cannot be written
        """
        norm_path = self.normalize_path(path)

        # Ensure parent directory exists
        parent_dir = self.get_parent_directory(norm_path)
        if parent_dir and not self.directory_exists(parent_dir):
            self.create_directory(parent_dir)

        # Update or create file
        self._files[norm_path] = content

        # Update file info
        file_name = os.path.basename(norm_path)
        _, extension = os.path.splitext(file_name)
        extension = extension[1:] if extension else ""  # Remove leading dot

        self._file_info[norm_path] = FileInfo(path=norm_path, name=file_name, extension=extension, size=len(content), last_modified=datetime.now(), is_readonly=False)

    @override
    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists.

        Args:
            path: Path to the file

        Returns:
            True if the file exists, False otherwise
        """
        norm_path = self.normalize_path(path)
        return norm_path in self._files

    @override
    def delete_file(self, path: str) -> bool:
        """
        Delete a file.

        Args:
            path: Path to the file

        Returns:
            True if the file was deleted, False if it did not exist
        """
        norm_path = self.normalize_path(path)
        if not self.file_exists(norm_path):
            return False

        del self._files[norm_path]
        del self._file_info[norm_path]
        return True

    @override
    def get_file_info(self, path: str) -> Optional[FileInfo]:
        """
        Get information about a file.

        Args:
            path: Path to the file

        Returns:
            FileInfo object if the file exists, None otherwise
        """
        norm_path = self.normalize_path(path)
        return self._file_info.get(norm_path)

    @override
    def list_files(self, dir_path: str) -> list[FileInfo]:
        """
        List all files in a directory.

        Args:
            dir_path: Path to the directory

        Returns:
            List of FileInfo objects for all files in the directory
        """
        norm_dir = self.normalize_path(dir_path)
        if not self.directory_exists(norm_dir):
            return []

        result = []
        for path, info in self._file_info.items():
            parent_dir = self.get_parent_directory(path)
            if parent_dir == norm_dir:
                result.append(info)

        return result

    @override
    def list_dirs(self, dir_path: str) -> list[DirectoryInfo]:
        """
        List all subdirectories in a directory.

        Args:
            dir_path: Path to the directory

        Returns:
            List of DirectoryInfo objects for all subdirectories in the directory
        """
        norm_dir = self.normalize_path(dir_path)
        if not self.directory_exists(norm_dir):
            return []

        result = []
        for path, info in self._dir_info.items():
            if path == norm_dir:
                continue  # Skip the directory itself

            parent_dir = self.get_parent_directory(path)
            if parent_dir == norm_dir:
                result.append(info)

        return result

    @override
    def create_directory(self, path: str) -> bool:
        """
        Create a directory.

        Args:
            path: Path to the directory

        Returns:
            True if the directory was created or already exists, False otherwise
        """
        norm_path = self.normalize_path(path)

        # Already exists
        if self.directory_exists(norm_path):
            return True

        # Create parent directories if needed
        parent_dir = self.get_parent_directory(norm_path)
        if parent_dir and not self.directory_exists(parent_dir):
            self.create_directory(parent_dir)

        # Create directory info
        dir_name = os.path.basename(norm_path)
        self._dir_info[norm_path] = DirectoryInfo(path=norm_path, name=dir_name or norm_path, last_modified=datetime.now())  # Use full path for root

        return True

    @override
    def directory_exists(self, path: str) -> bool:
        """
        Check if a directory exists.

        Args:
            path: Path to the directory

        Returns:
            True if the directory exists, False otherwise
        """
        norm_path = self.normalize_path(path)
        return norm_path in self._dir_info

    @override
    def delete_directory(self, path: str, recursive: bool = False) -> bool:
        """
        Delete a directory.

        Args:
            path: Path to the directory
            recursive: If True, delete all contents recursively

        Returns:
            True if the directory was deleted, False if it did not exist or could not be deleted
        """
        norm_path = self.normalize_path(path)
        if not self.directory_exists(norm_path):
            return False

        # Check if directory is empty or recursive delete is requested
        has_files = any(self.get_parent_directory(file_path) == norm_path for file_path in self._files.keys())
        has_dirs = any(self.get_parent_directory(dir_path) == norm_path for dir_path in self._dir_info.keys() if dir_path != norm_path)

        if (has_files or has_dirs) and not recursive:
            return False

        # Delete all files in directory
        if recursive:
            for file_path in list(self._files.keys()):
                if file_path.startswith(norm_path + "/"):
                    del self._files[file_path]
                    del self._file_info[file_path]

            # Delete all subdirectories
            for dir_path in list(self._dir_info.keys()):
                if dir_path != norm_path and dir_path.startswith(norm_path + "/"):
                    del self._dir_info[dir_path]

        # Delete the directory itself
        del self._dir_info[norm_path]
        return True

    @override
    def get_directory_info(self, path: str) -> Optional[DirectoryInfo]:
        """
        Get information about a directory.

        Args:
            path: Path to the directory

        Returns:
            DirectoryInfo object if the directory exists, None otherwise
        """
        norm_path = self.normalize_path(path)
        return self._dir_info.get(norm_path)

    @override
    def get_parent_directory(self, path: str) -> Optional[str]:
        """
        Get the parent directory of a path.

        Args:
            path: Path to get the parent of

        Returns:
            Path to the parent directory, or None if there is no parent
        """
        norm_path = self.normalize_path(path)
        if norm_path == "/":
            return None

        parent_dir = posixpath.dirname(norm_path)
        return parent_dir if parent_dir else "/"

    @override
    def join_paths(self, *paths: str) -> str:
        """
        Join path components.

        Args:
            *paths: Path components to join

        Returns:
            Joined path
        """
        # Use posixpath for consistent behavior in memory filesystem
        return posixpath.join(*paths)

    @override
    def normalize_path(self, path: str) -> str:
        """
        Normalize a path.

        Args:
            path: Path to normalize

        Returns:
            Normalized path
        """
        # Use posixpath for consistent behavior in memory filesystem
        # Convert Windows backslashes to forward slashes
        norm_path = path.replace("\\", "/")
        # Remove trailing slash except for root
        if norm_path != "/" and norm_path.endswith("/"):
            norm_path = norm_path[:-1]
        return posixpath.normpath(norm_path)
