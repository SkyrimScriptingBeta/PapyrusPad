from dataclasses import dataclass


@dataclass
class DocumentType:
    """
    Represents a document type with its associated metadata.

    Document types are used to categorize documents and determine
    what capabilities are available for them.
    """

    type_id: str  # Case-insensitive identifier
    display_name: str
    description: str
    extensions: list[str]
    icon: str = ""

    def __post_init__(self) -> None:
        """
        Normalize type_id and extensions to lowercase for case-insensitive comparison.
        """
        # Normalize type_id to lowercase
        self.type_id = self.type_id.lower()

        # Normalize extensions to lowercase
        self.extensions = [ext.lower() for ext in self.extensions]

        # Ensure extensions start with a dot
        self.extensions = [ext if ext.startswith(".") else f".{ext}" for ext in self.extensions]
