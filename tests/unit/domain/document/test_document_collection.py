from pathlib import Path
from assertpy import assert_that

from PapyrusPad.domain.document.document_collection import DocumentCollection
from PapyrusPad.domain.document.document_interface import IDocument
from PapyrusPad.domain.document.text_document import TextDocument


class TestDocumentCollection:
    """Unit tests for the DocumentCollection class."""

    def test_init_default(self) -> None:
        """Test creating a document collection with default values."""
        collection = DocumentCollection()
        assert_that(collection.list_documents()).is_empty()
        assert collection.get_active() is None

    def test_len(self) -> None:
        """Test the __len__ method for getting document count."""
        collection = DocumentCollection()

        # Empty collection should have length 0
        assert_that(len(collection)).is_equal_to(0)

        # Add documents and check length
        doc1 = TextDocument.create(name="doc1.txt")
        collection.add_or_replace(doc1)
        assert_that(len(collection)).is_equal_to(1)

        doc2 = TextDocument.create(name="doc2.txt")
        collection.add_or_replace(doc2)
        assert_that(len(collection)).is_equal_to(2)

        # Remove a document and check length
        collection.remove(doc1.id)
        assert_that(len(collection)).is_equal_to(1)

        # Remove the last document and check length
        collection.remove(doc2.id)
        assert_that(len(collection)).is_equal_to(0)

    def test_iterator(self) -> None:
        """Test the iterator functionality."""
        collection = DocumentCollection()

        # Empty collection should not have any items to iterate
        assert_that(lambda: next(collection)).raises(StopIteration)

        # Add documents
        doc1 = TextDocument.create(name="doc1.txt")
        doc2 = TextDocument.create(name="doc2.txt")
        doc3 = TextDocument.create(name="doc3.txt")

        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)
        collection.add_or_replace(doc3)

        # Test next() function
        assert_that(next(collection)).is_equal_to(doc1)
        assert_that(next(collection)).is_equal_to(doc2)
        assert_that(next(collection)).is_equal_to(doc3)

        # Should raise StopIteration after all documents
        assert_that(lambda: next(collection)).raises(StopIteration)

        # Test reset of iterator
        iterator = iter(collection)
        assert_that(next(iterator)).is_equal_to(doc1)

        # Test for loop
        docs: list[IDocument] = []
        for doc in collection:
            docs.append(doc)

        assert_that(docs).is_length(3)
        assert_that(docs[0]).is_equal_to(doc1)
        assert_that(docs[1]).is_equal_to(doc2)
        assert_that(docs[2]).is_equal_to(doc3)

    def test_create(self) -> None:
        """Test creating a document."""
        collection = DocumentCollection()
        doc = collection.create(name="test.txt", content="Hello, world!")

        # Check document properties
        assert_that(doc.name).is_equal_to("test.txt")
        assert_that(doc.content).is_equal_to("Hello, world!")

        # Check collection state
        assert_that(collection.list_documents()).is_length(1)
        assert_that(collection.get_document(doc.id)).is_equal_to(doc)
        assert_that(collection.get_active()).is_equal_to(doc)

    def test_add_or_replace(self) -> None:
        """Test adding and replacing documents."""
        collection = DocumentCollection()
        doc1 = TextDocument.create(name="doc1.txt")
        doc2 = TextDocument.create(name="doc2.txt")

        # Add documents
        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)

        # Check collection state
        assert_that(collection.list_documents()).is_length(2)
        assert_that(collection.get_document(doc1.id)).is_equal_to(doc1)
        assert_that(collection.get_document(doc2.id)).is_equal_to(doc2)

        # Replace a document
        # Create a new document with the same ID but different name
        doc1_updated = TextDocument.create_with_id(id=doc1.id, name="doc1_updated.txt")
        collection.add_or_replace(doc1_updated)

        # Check collection state
        assert_that(collection.list_documents()).is_length(2)
        updated_doc = collection.get_document(doc1.id)
        assert updated_doc is not None
        assert_that(updated_doc).is_equal_to(doc1_updated)
        assert_that(updated_doc.name).is_equal_to("doc1_updated.txt")

    def test_remove(self) -> None:
        """Test removing documents."""
        collection = DocumentCollection()
        doc1 = TextDocument.create(name="doc1.txt")
        doc2 = TextDocument.create(name="doc2.txt")

        # Add documents
        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)

        # Remove a document
        result = collection.remove(doc1.id)

        # Check result and collection state
        assert_that(result).is_true()
        assert_that(collection.list_documents()).is_length(1)
        assert collection.get_document(doc1.id) is None
        assert_that(collection.get_document(doc2.id)).is_equal_to(doc2)

        # Try to remove a non-existent document
        result = collection.remove("non-existent-id")

        # Check result
        assert_that(result).is_false()

    def test_set_active(self) -> None:
        """Test setting the active document."""
        collection = DocumentCollection()
        doc1 = TextDocument.create(name="doc1.txt")
        doc2 = TextDocument.create(name="doc2.txt")

        # Add documents
        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)

        # By default, the first document added should be active
        assert_that(collection.get_active()).is_equal_to(doc1)

        # Set doc2 as active
        result = collection.set_active(doc2.id)

        # Check result and collection state
        assert_that(result).is_true()
        assert_that(collection.get_active()).is_equal_to(doc2)

        # Try to set a non-existent document as active
        result = collection.set_active("non-existent-id")

        # Check result
        assert_that(result).is_false()
        # Active document should still be doc2
        assert_that(collection.get_active()).is_equal_to(doc2)

    def test_find_by_path(self) -> None:
        """Test finding a document by path."""
        collection = DocumentCollection()
        path1 = Path("/test/doc1.txt")
        path2 = Path("/test/doc2.txt")
        doc1 = TextDocument.create(name="doc1.txt", path=path1)
        doc2 = TextDocument.create(name="doc2.txt", path=path2)

        # Add documents
        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)

        # Find documents by path
        assert_that(collection.find_by_path(path1)).is_equal_to(doc1)
        assert_that(collection.find_by_path(path2)).is_equal_to(doc2)
        assert collection.find_by_path(Path("/test/non-existent.txt")) is None

    def test_is_path_open(self) -> None:
        """Test checking if a path is open."""
        collection = DocumentCollection()
        path1 = Path("/test/doc1.txt")
        doc1 = TextDocument.create(name="doc1.txt", path=path1)

        # Add document
        collection.add_or_replace(doc1)

        # Check if paths are open
        assert_that(collection.is_path_open(path1)).is_true()
        assert_that(collection.is_path_open(Path("/test/non-existent.txt"))).is_false()

    def test_active_document_after_remove(self) -> None:
        """Test active document behavior after removing documents."""
        collection = DocumentCollection()
        doc1 = TextDocument.create(name="doc1.txt")
        doc2 = TextDocument.create(name="doc2.txt")

        # Add documents
        collection.add_or_replace(doc1)
        collection.add_or_replace(doc2)

        # Set doc2 as active
        collection.set_active(doc2.id)
        assert_that(collection.get_active()).is_equal_to(doc2)

        # Remove active document
        collection.remove(doc2.id)

        # Active document should fall back to doc1
        assert_that(collection.get_active()).is_equal_to(doc1)

        # Remove last document
        collection.remove(doc1.id)

        # No active document
        assert collection.get_active() is None
