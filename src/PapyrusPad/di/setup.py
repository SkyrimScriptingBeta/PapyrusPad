from dependency_injector import containers
from dependency_injector.wiring import register_loader_containers

from PapyrusPad.di.container import set_container


def setup_development_dependencies() -> None:
    from PapyrusPad.di.container_dev import DevelopmentContainer

    setup_dependencies(DevelopmentContainer)


def setup_production_dependencies() -> None:
    from PapyrusPad.di.container_prod import ProductionContainer

    setup_dependencies(ProductionContainer)


def setup_test_dependencies() -> None:
    from PapyrusPad.di.container_test import TestContainer

    setup_dependencies(TestContainer)


def setup_dependencies(container_class: type[containers.DeclarativeContainer]) -> None:
    container = container_class()
    container.wire()
    register_loader_containers(container)

    set_container(container_class, container)

    import PapyrusPad.di.depends

    _ = PapyrusPad.di.depends.Depends

    # Initialize document type and capability system
    from PapyrusPad.document_types.registration import setup_document_system

    # Get document collection to provide document content
    document_collection = container.document_collection()

    # Function to get document content by ID
    def get_document_content(doc_id: str) -> str:
        if doc_id == "current":
            # Get the active document
            active_docs = document_collection.list_documents()
            if active_docs:
                return active_docs[0].content
            return ""

        # Get document by ID
        doc = document_collection.get(doc_id)
        if doc:
            return doc.content
        return ""

    # Set up document types and capabilities
    setup_document_system(container.document_type_registry(), container.capability_registry(), container.document_capability_provider(), get_document_content)

    # Set the capability provider for TextDocument
    from PapyrusPad.domain.document.text_document import TextDocument

    TextDocument.set_capability_provider_for_testing(container.document_capability_provider())
