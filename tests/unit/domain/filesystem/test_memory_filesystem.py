import pytest
from datetime import datetime

from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


class TestMemoryFileSystem:
    """
    Unit tests for the MemoryFileSystem implementation.
    """

    def test_init(self) -> None:
        """Test that the filesystem is initialized with a root directory."""
        fs = MemoryFileSystem()
        assert fs.directory_exists("/")
        dir_info = fs.get_directory_info("/")
        assert dir_info is not None
        assert dir_info.name == "/"

    def test_write_and_read_text(self) -> None:
        """Test writing and reading text from a file."""
        fs = MemoryFileSystem()
        content = "Hello, world!"
        fs.write_text("/test.txt", content)

        # Check that the file exists
        assert fs.file_exists("/test.txt")

        # Check that we can read the content
        assert fs.read_text("/test.txt") == content

        # Check file info
        file_info = fs.get_file_info("/test.txt")
        assert file_info is not None
        assert file_info.name == "test.txt"
        assert file_info.extension == "txt"
        assert file_info.size == len(content)
        assert isinstance(file_info.last_modified, datetime)

    def test_write_to_nonexistent_directory(self) -> None:
        """Test writing to a file in a directory that doesn't exist yet."""
        fs = MemoryFileSystem()
        content = "Hello, world!"
        fs.write_text("/dir1/dir2/test.txt", content)

        # Check that the directories were created
        assert fs.directory_exists("/dir1")
        assert fs.directory_exists("/dir1/dir2")

        # Check that the file exists
        assert fs.file_exists("/dir1/dir2/test.txt")

        # Check that we can read the content
        assert fs.read_text("/dir1/dir2/test.txt") == content

    def test_read_nonexistent_file(self) -> None:
        """Test reading a file that doesn't exist."""
        fs = MemoryFileSystem()
        with pytest.raises(FileNotFoundError):
            fs.read_text("/nonexistent.txt")

    def test_delete_file(self) -> None:
        """Test deleting a file."""
        fs = MemoryFileSystem()
        fs.write_text("/test.txt", "Hello, world!")

        # Check that the file exists
        assert fs.file_exists("/test.txt")

        # Delete the file
        assert fs.delete_file("/test.txt") is True

        # Check that the file no longer exists
        assert not fs.file_exists("/test.txt")

        # Try to delete a file that doesn't exist
        assert fs.delete_file("/nonexistent.txt") is False

    def test_list_files(self) -> None:
        """Test listing files in a directory."""
        fs = MemoryFileSystem()
        fs.write_text("/dir/file1.txt", "File 1")
        fs.write_text("/dir/file2.txt", "File 2")
        fs.write_text("/dir/subdir/file3.txt", "File 3")

        # List files in /dir
        files = fs.list_files("/dir")
        assert len(files) == 2
        assert any(f.name == "file1.txt" for f in files)
        assert any(f.name == "file2.txt" for f in files)

        # List files in /dir/subdir
        files = fs.list_files("/dir/subdir")
        assert len(files) == 1
        assert files[0].name == "file3.txt"

        # List files in a directory that doesn't exist
        files = fs.list_files("/nonexistent")
        assert len(files) == 0

    def test_list_dirs(self) -> None:
        """Test listing subdirectories in a directory."""
        fs = MemoryFileSystem()
        fs.create_directory("/dir/subdir1")
        fs.create_directory("/dir/subdir2")
        fs.create_directory("/dir/subdir1/subsubdir")

        # List directories in /dir
        dirs = fs.list_dirs("/dir")
        assert len(dirs) == 2
        assert any(d.name == "subdir1" for d in dirs)
        assert any(d.name == "subdir2" for d in dirs)

        # List directories in /dir/subdir1
        dirs = fs.list_dirs("/dir/subdir1")
        assert len(dirs) == 1
        assert dirs[0].name == "subsubdir"

        # List directories in a directory that doesn't exist
        dirs = fs.list_dirs("/nonexistent")
        assert len(dirs) == 0

    def test_create_directory(self) -> None:
        """Test creating a directory."""
        fs = MemoryFileSystem()

        # Create a directory
        assert fs.create_directory("/dir") is True
        assert fs.directory_exists("/dir")

        # Create a nested directory
        assert fs.create_directory("/dir/subdir") is True
        assert fs.directory_exists("/dir/subdir")

        # Create a directory that already exists
        assert fs.create_directory("/dir") is True

        # Create a deeply nested directory
        assert fs.create_directory("/a/b/c/d") is True
        assert fs.directory_exists("/a")
        assert fs.directory_exists("/a/b")
        assert fs.directory_exists("/a/b/c")
        assert fs.directory_exists("/a/b/c/d")

    def test_delete_directory(self) -> None:
        """Test deleting a directory."""
        fs = MemoryFileSystem()
        fs.create_directory("/dir/subdir")
        fs.write_text("/dir/file.txt", "Hello")

        # Try to delete a non-empty directory without recursive flag
        assert fs.delete_directory("/dir") is False
        assert fs.directory_exists("/dir")

        # Delete a non-empty directory with recursive flag
        assert fs.delete_directory("/dir", recursive=True) is True
        assert not fs.directory_exists("/dir")
        assert not fs.file_exists("/dir/file.txt")
        assert not fs.directory_exists("/dir/subdir")

        # Delete an empty directory
        fs.create_directory("/empty")
        assert fs.delete_directory("/empty") is True
        assert not fs.directory_exists("/empty")

        # Try to delete a directory that doesn't exist
        assert fs.delete_directory("/nonexistent") is False

    def test_get_parent_directory(self) -> None:
        """Test getting the parent directory of a path."""
        fs = MemoryFileSystem()

        # Get parent of a file
        assert fs.get_parent_directory("/dir/file.txt") == "/dir"

        # Get parent of a directory
        assert fs.get_parent_directory("/dir/subdir") == "/dir"

        # Get parent of a root-level file
        assert fs.get_parent_directory("/file.txt") == "/"

        # Get parent of root
        assert fs.get_parent_directory("/") is None

    def test_join_paths(self) -> None:
        """Test joining path components."""
        fs = MemoryFileSystem()

        # Join simple paths
        assert fs.join_paths("dir", "file.txt") == "dir/file.txt"

        # Join with leading slash
        assert fs.join_paths("/dir", "file.txt") == "/dir/file.txt"

        # Join multiple components
        assert fs.join_paths("/dir", "subdir", "file.txt") == "/dir/subdir/file.txt"

        # Join with empty components
        assert fs.join_paths("/dir", "", "file.txt") == "/dir/file.txt"

    def test_normalize_path(self) -> None:
        """Test normalizing paths."""
        fs = MemoryFileSystem()

        # Normalize simple path
        assert fs.normalize_path("/dir/file.txt") == "/dir/file.txt"

        # Normalize path with double slashes
        assert fs.normalize_path("/dir//file.txt") == "/dir/file.txt"

        # Normalize path with trailing slash
        assert fs.normalize_path("/dir/") == "/dir"

        # Normalize path with . and ..
        assert fs.normalize_path("/dir/./file.txt") == "/dir/file.txt"
        assert fs.normalize_path("/dir/../file.txt") == "/file.txt"

        # Normalize Windows-style path
        assert fs.normalize_path("C:\\dir\\file.txt") == "C:/dir/file.txt"
