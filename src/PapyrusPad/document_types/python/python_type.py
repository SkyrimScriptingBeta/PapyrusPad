"""Python document type implementation."""

from PapyrusPad.domain.document_type.document_type import DocumentType


class PythonType:
    """Python document type provider."""

    @staticmethod
    def create() -> DocumentType:
        """
        Create a python document type.

        Returns:
            A python document type
        """
        return DocumentType(type_id="python", display_name="Python", description="Python source code", extensions=[".py", ".pyw", ".pyi"], icon="python-icon")
