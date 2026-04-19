import logging
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from kb_qa.constants import COLLECTION_NAME, EMBED_MODEL, VECTORSTORE_DIR
from kb_qa.loader import Document

log = logging.getLogger(__name__)


def retrieve(
    question: str,
    n_results: int = 5,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    doc_type_filter: str | None = None,
) -> list[Document]:
    """Retrieve relevant document chunks from the vector store."""
    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
    client = chromadb.PersistentClient(path=str(vectorstore_dir))
    collection = client.get_collection(COLLECTION_NAME)

    embedding = model.encode([question], show_progress_bar=False).tolist()[0]

    kwargs: dict = {"query_embeddings": [embedding], "n_results": n_results}
    if doc_type_filter:
        kwargs["where"] = {"type": {"$eq": doc_type_filter}}

    results = collection.query(**kwargs)
    docs: list[Document] = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        docs.append(Document(text=text, metadata=meta))
    return docs


class KbQa:
    """Session-reuse wrapper for retrieve (holds model + collection as instance vars)."""

    def __init__(self, vectorstore_dir: Path = VECTORSTORE_DIR) -> None:
        self._model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
        client = chromadb.PersistentClient(path=str(vectorstore_dir))
        self._collection = client.get_collection(COLLECTION_NAME)

    def retrieve(self, question: str, n_results: int = 5, doc_type_filter: str | None = None) -> list[Document]:
        embedding = self._model.encode([question], show_progress_bar=False).tolist()[0]
        kwargs: dict = {"query_embeddings": [embedding], "n_results": n_results}
        if doc_type_filter:
            kwargs["where"] = {"type": {"$eq": doc_type_filter}}
        results = self._collection.query(**kwargs)
        return [Document(text=t, metadata=m) for t, m in zip(results["documents"][0], results["metadatas"][0])]
