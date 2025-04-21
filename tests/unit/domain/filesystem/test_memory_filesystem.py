import pytest
from datetime import datetime
from assertpy import assert_that

from PapyrusPad.domain.filesystem.filesystem_memory import MemoryFileSystem


class TestMemoryFileSystem:
    """
    Unit tests for the MemoryFileSystem implementation.
    """

    def test_init(self) -> None:
        """Test that the filesystem is initialized with a root directory."""
        fs = MemoryFileSystem()
        assert_that(fs.directory_exists("/")).is_true()
        dir_info = fs.get_directory_info("/")
        assert dir_info is not None
        assert_that(dir_info.name).is_equal_to("/")

    def test_write_and_read_text(self) -> None:
        """Test writing and reading text from a file."""
        fs = MemoryFileSystem()
        content = "Hello, world!"
        fs.write_text("/test.txt", content)

        # Check that the file exists
        assert_that(fs.file_exists("/test.txt")).is_true()

        # Check that we can read the content
        assert_that(fs.read_text("/test.txt")).is_equal_to(content)

        # Check file info
        file_info = fs.get_file_info("/test.txt")
        assert file_info is not None
        assert_that(file_info.name).is_equal_to("test.txt")
        assert_that(file_info.extension).is_equal_to("txt")
        assert_that(file_info.size).is_equal_to(len(content))
        assert_that(file_info.last_modified).is_instance_of(datetime)

    def test_write_to_nonexistent_directory(self) -> None:
        """Test writing to a file in a directory that doesn't exist yet."""
        fs = MemoryFileSystem()
        content = "Hello, world!"
        fs.write_text("/dir1/dir2/test.txt", content)

        # Check that the directories were created
        assert_that(fs.directory_exists("/dir1")).is_true()
        assert_that(fs.directory_exists("/dir1/dir2")).is_true()

        # Check that the file exists
        assert_that(fs.file_exists("/dir1/dir2/test.txt")).is_true()

        # Check that we can read the content
        assert_that(fs.read_text("/dir1/dir2/test.txt")).is_equal_to(content)

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
        assert_that(fs.file_exists("/test.txt")).is_true()

        # Delete the file
        assert_that(fs.delete_file("/test.txt")).is_true()

        # Check that the file no longer exists
        assert_that(fs.file_exists("/test.txt")).is_false()

        # Try to delete a file that doesn't exist
        assert_that(fs.delete_file("/nonexistent.txt")).is_false()

    def test_list_files(self) -> None:
        """Test listing files in a directory."""
        fs = MemoryFileSystem()
        fs.write_text("/dir/file1.txt", "File 1")
        fs.write_text("/dir/file2.txt", "File 2")
        fs.write_text("/dir/subdir/file3.txt", "File 3")

        # List files in /dir
        files = fs.list_files("/dir")
        assert_that(files).is_length(2)
        assert_that(files).extracting("name").contains("file1.txt", "file2.txt")

        # List files in /dir/subdir
        files = fs.list_files("/dir/subdir")
        assert_that(files).is_length(1)
        assert_that(files[0].name).is_equal_to("file3.txt")

        # List files in a directory that doesn't exist
        files = fs.list_files("/nonexistent")
        assert_that(files).is_empty()

    def test_list_dirs(self) -> None:
        """Test listing subdirectories in a directory."""
        fs = MemoryFileSystem()
        fs.create_directory("/dir/subdir1")
        fs.create_directory("/dir/subdir2")
        fs.create_directory("/dir/subdir1/subsubdir")

        # List directories in /dir
        dirs = fs.list_dirs("/dir")
        assert_that(dirs).is_length(2)
        assert_that(dirs).extracting("name").contains("subdir1", "subdir2")

        # List directories in /dir/subdir1
        dirs = fs.list_dirs("/dir/subdir1")
        assert_that(dirs).is_length(1)
        assert_that(dirs[0].name).is_equal_to("subsubdir")

        # List directories in a directory that doesn't exist
        dirs = fs.list_dirs("/nonexistent")
        assert_that(dirs).is_empty()

    def test_create_directory(self) -> None:
        """Test creating a directory."""
        fs = MemoryFileSystem()

        # Create a directory
        assert_that(fs.create_directory("/dir")).is_true()
        assert_that(fs.directory_exists("/dir")).is_true()

        # Create a nested directory
        assert_that(fs.create_directory("/dir/subdir")).is_true()
        assert_that(fs.directory_exists("/dir/subdir")).is_true()

        # Create a directory that already exists
        assert_that(fs.create_directory("/dir")).is_true()

        # Create a deeply nested directory
        assert_that(fs.create_directory("/a/b/c/d")).is_true()
        assert_that(fs.directory_exists("/a")).is_true()
        assert_that(fs.directory_exists("/a/b")).is_true()
        assert_that(fs.directory_exists("/a/b/c")).is_true()
        assert_that(fs.directory_exists("/a/b/c/d")).is_true()

    def test_delete_directory(self) -> None:
        """Test deleting a directory."""
        fs = MemoryFileSystem()
        fs.create_directory("/dir/subdir")
        fs.write_text("/dir/file.txt", "Hello")

        # Try to delete a non-empty directory without recursive flag
        assert_that(fs.delete_directory("/dir")).is_false()
        assert_that(fs.directory_exists("/dir")).is_true()

        # Delete a non-empty directory with recursive flag
        assert_that(fs.delete_directory("/dir", recursive=True)).is_true()
        assert_that(fs.directory_exists("/dir")).is_false()
        assert_that(fs.file_exists("/dir/file.txt")).is_false()
        assert_that(fs.directory_exists("/dir/subdir")).is_false()

        # Delete an empty directory
        fs.create_directory("/empty")
        assert_that(fs.delete_directory("/empty")).is_true()
        assert_that(fs.directory_exists("/empty")).is_false()

        # Try to delete a directory that doesn't exist
        assert_that(fs.delete_directory("/nonexistent")).is_false()

    def test_get_parent_directory(self) -> None:
        """Test getting the parent directory of a path."""
        fs = MemoryFileSystem()

        # Get parent of a file
        assert_that(fs.get_parent_directory("/dir/file.txt")).is_equal_to("/dir")

        # Get parent of a directory
        assert_that(fs.get_parent_directory("/dir/subdir")).is_equal_to("/dir")

        # Get parent of a root-level file
        assert_that(fs.get_parent_directory("/file.txt")).is_equal_to("/")

        # Get parent of root
        assert_that(fs.get_parent_directory("/")).is_none()

    def test_join_paths(self) -> None:
        """Test joining path components."""
        fs = MemoryFileSystem()

        # Join simple paths
        assert_that(fs.join_paths("dir", "file.txt")).is_equal_to("dir/file.txt")

        # Join with leading slash
        assert_that(fs.join_paths("/dir", "file.txt")).is_equal_to("/dir/file.txt")

        # Join multiple components
        assert_that(fs.join_paths("/dir", "subdir", "file.txt")).is_equal_to("/dir/subdir/file.txt")

        # Join with empty components
        assert_that(fs.join_paths("/dir", "", "file.txt")).is_equal_to("/dir/file.txt")

    def test_normalize_path(self) -> None:
        """Test normalizing paths."""
        fs = MemoryFileSystem()

        # Normalize simple path
        assert_that(fs.normalize_path("/dir/file.txt")).is_equal_to("/dir/file.txt")

        # Normalize path with double slashes
        assert_that(fs.normalize_path("/dir//file.txt")).is_equal_to("/dir/file.txt")

        # Normalize path with trailing slash
        assert_that(fs.normalize_path("/dir/")).is_equal_to("/dir")

        # Normalize path with . and ..
        assert_that(fs.normalize_path("/dir/./file.txt")).is_equal_to("/dir/file.txt")
        assert_that(fs.normalize_path("/dir/../file.txt")).is_equal_to("/file.txt")

        # Normalize Windows-style path
        assert_that(fs.normalize_path("C:\\dir\\file.txt")).is_equal_to("C:/dir/file.txt")
