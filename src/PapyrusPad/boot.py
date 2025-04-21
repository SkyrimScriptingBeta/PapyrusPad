from PapyrusPad.di.depends import Depends
from PapyrusPad.domain.document.document_collection_interface import IDocumentCollection


def startup(document_collection: IDocumentCollection = Depends[IDocumentCollection]):
    document_collection.create(name="Untitled")
