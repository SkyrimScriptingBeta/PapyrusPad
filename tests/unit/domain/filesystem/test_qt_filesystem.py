from pathlib import Path
from assertpy import assert_that

from PapyrusPad.domain.filesystem.filesystem_qt import QtFileSystem


class TestQtFileSystem:
    """Unit tests for the QtFileSystem class."""

    def test_write_and_read_text(self, temp_dir: Path):
        """Test writing and reading text from a file."""
        # Arrange
        filesystem = QtFileSystem()
        test_file = temp_dir / "test.txt"
        content = "Hello, world!"

        # Act
        filesystem.write_text(str(test_file), content)
        result = filesystem.read_text(str(test_file))

        # Assert
        assert_that(result).is_equal_to(content)

    def test_file_exists(self, temp_dir: Path):
        """Test checking if a file exists."""
        # Arrange
        filesystem = QtFileSystem()
        test_file = temp_dir / "test.txt"

        # Act - Create the file
        filesystem.write_text(str(test_file), "content")

        # Assert
        assert_that(filesystem.file_exists(str(test_file))).is_true()
        assert_that(filesystem.file_exists(str(temp_dir / "nonexistent.txt"))).is_false()

    def test_delete_file(self, temp_dir: Path):
        """Test deleting a file."""
        # Arrange
        filesystem = QtFileSystem()
        test_file = temp_dir / "test.txt"
        filesystem.write_text(str(test_file), "content")

        # Act
        result = filesystem.delete_file(str(test_file))

        # Assert
        assert_that(result).is_true()
        assert_that(filesystem.file_exists(str(test_file))).is_false()

    def test_delete_nonexistent_file(self, temp_dir: Path):
        """Test deleting a file that doesn't exist."""
        # Arrange
        filesystem = QtFileSystem()
        test_file = temp_dir / "nonexistent.txt"

        # Act
        result = filesystem.delete_file(str(test_file))

        # Assert
        assert_that(result).is_false()

    def test_get_file_info(self, temp_dir: Path):
        """Test getting information about a file."""
        # Arrange
        filesystem = QtFileSystem()
        test_file = temp_dir / "test.txt"
        content = "Hello, world!"
        filesystem.write_text(str(test_file), content)

        # Act
        file_info = filesystem.get_file_info(str(test_file))

        # Assert
        assert file_info is not None  # None check uses standard assertion
        assert_that(file_info.path).is_equal_to(str(test_file))
        assert_that(file_info.name).is_equal_to("test.txt")
        assert_that(file_info.extension).is_equal_to("txt")
        assert_that(file_info.size).is_equal_to(len(content))

    def test_list_files(self, temp_dir: Path):
        """Test listing files in a directory."""
        # Arrange
        filesystem = QtFileSystem()
        file1 = temp_dir / "file1.txt"
        file2 = temp_dir / "file2.txt"
        filesystem.write_text(str(file1), "content1")
        filesystem.write_text(str(file2), "content2")

        # Act
        files = filesystem.list_files(str(temp_dir))

        # Assert
        assert_that(files).is_length(2)
        file_names = [f.name for f in files]
        assert_that(file_names).contains("file1.txt")
        assert_that(file_names).contains("file2.txt")

    def test_create_directory(self, temp_dir: Path):
        """Test creating a directory."""
        # Arrange
        filesystem = QtFileSystem()
        test_dir = temp_dir / "test_dir"

        # Act
        result = filesystem.create_directory(str(test_dir))

        # Assert
        assert_that(result).is_true()
        assert_that(filesystem.directory_exists(str(test_dir))).is_true()

    def test_create_nested_directory(self, temp_dir: Path):
        """Test creating a nested directory."""
        # Arrange
        filesystem = QtFileSystem()
        test_dir = temp_dir / "parent" / "child" / "grandchild"

        # Act
        result = filesystem.create_directory(str(test_dir))

        # Assert
        assert_that(result).is_true()
        assert_that(filesystem.directory_exists(str(test_dir))).is_true()
        assert_that(filesystem.directory_exists(str(temp_dir / "parent"))).is_true()
        assert_that(filesystem.directory_exists(str(temp_dir / "parent" / "child"))).is_true()

    def test_directory_exists(self, temp_dir: Path):
        """Test checking if a directory exists."""
        # Arrange
        filesystem = QtFileSystem()
        test_dir = temp_dir / "test_dir"
        filesystem.create_directory(str(test_dir))

        # Act & Assert
        assert_that(filesystem.directory_exists(str(test_dir))).is_true()
        assert_that(filesystem.directory_exists(str(temp_dir / "nonexistent"))).is_false()

    def test_delete_directory(self, temp_dir: Path):
        """Test deleting a directory."""
        # Arrange
        filesystem = QtFileSystem()
        test_dir = temp_dir / "test_dir"
        filesystem.create_directory(str(test_dir))

        # Act
        result = filesystem.delete_directory(str(test_dir))

        # Assert
        assert_that(result).is_true()
        assert_that(filesystem.directory_exists(str(test_dir))).is_false()

    def test_delete_directory_recursive(self, temp_dir: Path):
        """Test deleting a directory recursively."""
        # Arrange
        filesystem = QtFileSystem()
        parent_dir = temp_dir / "parent"
        child_dir = parent_dir / "child"
        file_path = child_dir / "test.txt"

        filesystem.create_directory(str(child_dir))
        filesystem.write_text(str(file_path), "content")

        # Act
        result = filesystem.delete_directory(str(parent_dir), recursive=True)

        # Assert
        assert_that(result).is_true()
        assert_that(filesystem.directory_exists(str(parent_dir))).is_false()

    def test_get_directory_info(self, temp_dir: Path):
        """Test getting information about a directory."""
        # Arrange
        filesystem = QtFileSystem()
        test_dir = temp_dir / "test_dir"
        filesystem.create_directory(str(test_dir))

        # Act
        dir_info = filesystem.get_directory_info(str(test_dir))

        # Assert
        assert dir_info is not None  # None check uses standard assertion
        assert_that(dir_info.path).is_equal_to(str(test_dir))
        assert_that(dir_info.name).is_equal_to("test_dir")

    def test_list_dirs(self, temp_dir: Path):
        """Test listing subdirectories in a directory."""
        # Arrange
        filesystem = QtFileSystem()
        dir1 = temp_dir / "dir1"
        dir2 = temp_dir / "dir2"
        filesystem.create_directory(str(dir1))
        filesystem.create_directory(str(dir2))

        # Act
        dirs = filesystem.list_dirs(str(temp_dir))

        # Assert
        assert_that(dirs).is_length(2)
        dir_names = [d.name for d in dirs]
        assert_that(dir_names).contains("dir1")
        assert_that(dir_names).contains("dir2")

    def test_get_parent_directory(self, temp_dir: Path):
        """Test getting the parent directory of a path."""
        # Arrange
        filesystem = QtFileSystem()
        child_dir = temp_dir / "child"

        # Act
        parent = filesystem.get_parent_directory(str(child_dir))

        # Assert - Normalize path separators for cross-platform compatibility
        assert parent is not None  # None check uses standard assertion
        assert_that(Path(parent)).is_equal_to(temp_dir)

    def test_join_paths(self):
        """Test joining path components."""
        # Arrange
        filesystem = QtFileSystem()

        # Act
        result = filesystem.join_paths("parent", "child", "file.txt")

        # Assert
        assert_that(result).contains("parent")
        assert_that(result).contains("child")
        assert_that(result).contains("file.txt")

    def test_normalize_path(self):
        """Test normalizing a path."""
        # Arrange
        filesystem = QtFileSystem()

        # Act
        result = filesystem.normalize_path("parent/./child/../child/file.txt")

        # Assert
        assert_that(result).is_equal_to("parent/child/file.txt")
