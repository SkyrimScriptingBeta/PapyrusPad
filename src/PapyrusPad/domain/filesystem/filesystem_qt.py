from dataclasses import dataclass
from datetime import datetime
from typing import Optional, override

from PySide6.QtCore import QFile, QDir, QIODevice, QTextStream, QFileInfo

from PapyrusPad.domain.filesystem.filesystem_interface import IFileSystem
from PapyrusPad.domain.filesystem.models import FileInfo, DirectoryInfo


@dataclass
class QtFileSystem(IFileSystem):
    """
    Qt implementation of the filesystem interface using QFile and QDir.
    Provides real filesystem operations for production use.
    """

    @override
    def read_text(self, path: str) -> str:
        """
        Read text content from a file using QFile.

        Args:
            path: Path to the file

        Returns:
            The text content of the file

        Raises:
            FileNotFoundError: If the file does not exist or cannot be opened
        """
        file = QFile(path)
        if not file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            raise FileNotFoundError(f"Could not open file: {path}")

        text_stream = QTextStream(file)
        content = text_stream.readAll()
        file.close()
        return content

    @override
    def write_text(self, path: str, content: str) -> None:
        """
        Write text content to a file using QFile.

        Args:
            path: Path to the file
            content: Text content to write

        Raises:
            IOError: If the file cannot be written
        """
        # Ensure parent directory exists
        parent_dir = self.get_parent_directory(path)
        if parent_dir and not self.directory_exists(parent_dir):
            self.create_directory(parent_dir)

        file = QFile(path)
        if not file.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
            raise IOError(f"Could not write to file: {path}")

        # Write content to file
        file.write(content.encode("utf-8"))
        file.close()

    @override
    def file_exists(self, path: str) -> bool:
        """
        Check if a file exists using QFileInfo.

        Args:
            path: Path to the file

        Returns:
            True if the file exists, False otherwise
        """
        file_info = QFileInfo(path)
        return file_info.exists() and file_info.isFile()

    @override
    def delete_file(self, path: str) -> bool:
        """
        Delete a file using QFile.

        Args:
            path: Path to the file

        Returns:
            True if the file was deleted, False if it did not exist
        """
        if not self.file_exists(path):
            return False

        file = QFile(path)
        return file.remove()

    @override
    def get_file_info(self, path: str) -> Optional[FileInfo]:
        """
        Get information about a file using QFileInfo.

        Args:
            path: Path to the file

        Returns:
            FileInfo object if the file exists, None otherwise
        """
        if not self.file_exists(path):
            return None

        file_info = QFileInfo(path)
        name = file_info.fileName()
        extension = file_info.suffix()
        size = file_info.size()
        # Convert QDateTime to Python datetime
        qt_date_time = file_info.lastModified()
        last_modified = datetime.fromtimestamp(qt_date_time.toSecsSinceEpoch())
        is_readonly = not file_info.isWritable()

        return FileInfo(path=path, name=name, extension=extension, size=size, last_modified=last_modified, is_readonly=is_readonly)

    @override
    def list_files(self, dir_path: str) -> list[FileInfo]:
        """
        List all files in a directory using QDir.

        Args:
            dir_path: Path to the directory

        Returns:
            List of FileInfo objects for all files in the directory
        """
        if not self.directory_exists(dir_path):
            return []

        dir = QDir(dir_path)
        file_list = []

        # List all files in the directory
        file_names = dir.entryList(["*"], QDir.Filter.Files)
        for file_name in file_names:
            file_path = self.join_paths(dir_path, file_name)
            file_info = self.get_file_info(file_path)
            if file_info:
                file_list.append(file_info)

        return file_list

    @override
    def list_dirs(self, dir_path: str) -> list[DirectoryInfo]:
        """
        List all subdirectories in a directory using QDir.

        Args:
            dir_path: Path to the directory

        Returns:
            List of DirectoryInfo objects for all subdirectories in the directory
        """
        if not self.directory_exists(dir_path):
            return []

        dir = QDir(dir_path)
        dir_list = []

        # Skip . and .. entries
        # List all subdirectories in the directory
        dir_names = dir.entryList(["*"], QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
        for dir_name in dir_names:
            dir_path_full = self.join_paths(dir_path, dir_name)
            dir_info = self.get_directory_info(dir_path_full)
            if dir_info:
                dir_list.append(dir_info)

        return dir_list

    @override
    def create_directory(self, path: str) -> bool:
        """
        Create a directory using QDir.

        Args:
            path: Path to the directory

        Returns:
            True if the directory was created or already exists, False otherwise
        """
        if self.directory_exists(path):
            return True

        # Create parent directories if needed
        parent_dir = self.get_parent_directory(path)
        if parent_dir and not self.directory_exists(parent_dir):
            if not self.create_directory(parent_dir):
                return False

        dir = QDir()
        return dir.mkpath(path)

    @override
    def directory_exists(self, path: str) -> bool:
        """
        Check if a directory exists using QFileInfo.

        Args:
            path: Path to the directory

        Returns:
            True if the directory exists, False otherwise
        """
        file_info = QFileInfo(path)
        return file_info.exists() and file_info.isDir()

    @override
    def delete_directory(self, path: str, recursive: bool = False) -> bool:
        """
        Delete a directory using QDir.

        Args:
            path: Path to the directory
            recursive: If True, delete all contents recursively

        Returns:
            True if the directory was deleted, False if it did not exist or could not be deleted
        """
        if not self.directory_exists(path):
            return False

        dir = QDir(path)

        if recursive:
            # Remove all files in the directory
            # List all files in the directory
            file_names = dir.entryList(["*"], QDir.Filter.Files)
            for file_name in file_names:
                file_path = self.join_paths(path, file_name)
                if not self.delete_file(file_path):
                    return False

            # Remove all subdirectories
            # List all subdirectories in the directory
            subdir_names = dir.entryList(["*"], QDir.Filter.Dirs | QDir.Filter.NoDotAndDotDot)
            for subdir_name in subdir_names:
                subdir_path = self.join_paths(path, subdir_name)
                if not self.delete_directory(subdir_path, recursive=True):
                    return False

        # Remove the directory itself
        return dir.rmdir(path)

    @override
    def get_directory_info(self, path: str) -> Optional[DirectoryInfo]:
        """
        Get information about a directory using QFileInfo.

        Args:
            path: Path to the directory

        Returns:
            DirectoryInfo object if the directory exists, None otherwise
        """
        if not self.directory_exists(path):
            return None

        file_info = QFileInfo(path)
        name = file_info.fileName() or path  # Use full path for root
        # Convert QDateTime to Python datetime
        qt_date_time = file_info.lastModified()
        last_modified = datetime.fromtimestamp(qt_date_time.toSecsSinceEpoch())

        return DirectoryInfo(path=path, name=name, last_modified=last_modified)

    @override
    def get_parent_directory(self, path: str) -> Optional[str]:
        """
        Get the parent directory of a path using QFileInfo.

        Args:
            path: Path to get the parent of

        Returns:
            Path to the parent directory, or None if there is no parent
        """
        file_info = QFileInfo(path)
        parent_dir = file_info.path()

        # Handle root directory
        if not parent_dir or parent_dir == path:
            return None

        return parent_dir

    @override
    def join_paths(self, *paths: str) -> str:
        """
        Join path components using QDir.

        Args:
            *paths: Path components to join

        Returns:
            Joined path
        """
        if not paths:
            return ""

        result = paths[0]
        for path in paths[1:]:
            result = QDir(result).filePath(path)

        return result

    @override
    def normalize_path(self, path: str) -> str:
        """
        Normalize a path using QDir.

        Args:
            path: Path to normalize

        Returns:
            Normalized path
        """
        # Convert to absolute path and normalize
        return QDir.cleanPath(path)
