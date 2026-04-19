import hashlib
import logging
from pathlib import Path

import chromadb
import click
from sentence_transformers import SentenceTransformer

from kb_qa.constants import (
    COLLECTION_NAME,
    EMBED_BATCH_SIZE,
    EMBED_MODEL,
    KNOWLEDGE_DIR,
    VECTORSTORE_DIR,
)
from kb_qa.loader import load_all

log = logging.getLogger(__name__)


def ingest(
    knowledge_dir: Path = KNOWLEDGE_DIR,
    vectorstore_dir: Path = VECTORSTORE_DIR,
    force: bool = False,
    batch_size: int = EMBED_BATCH_SIZE,
) -> int:
    """Ingest documents from knowledge_dir into ChromaDB. Returns count of newly added chunks."""
    docs = load_all(knowledge_dir)
    if not docs:
        log.info("No documents found in %s", knowledge_dir)
        return 0

    model = SentenceTransformer(EMBED_MODEL, trust_remote_code=True)
    vectorstore_dir.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(vectorstore_dir))
    collection = client.get_or_create_collection(
        COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    existing_ids: set[str] = set(collection.get(include=[])["ids"])

    new_docs = [d for d in docs if _doc_id(d) not in existing_ids] if not force else docs
    if not new_docs:
        log.info("All %d chunks already ingested (use --force to reingest)", len(docs))
        return 0

    ids = [_doc_id(d) for d in new_docs]
    texts = [d["text"] for d in new_docs]
    metadatas = [d["metadata"] for d in new_docs]

    batches = range(0, len(new_docs), batch_size)
    with click.progressbar(batches, label="Ingesting chunks", length=len(batches)) as bar:
        for i in bar:
            batch_ids = ids[i : i + batch_size]
            batch_texts = texts[i : i + batch_size]
            batch_meta = metadatas[i : i + batch_size]
            embeddings = model.encode(batch_texts, show_progress_bar=False).tolist()
            collection.add(
                ids=batch_ids,
                embeddings=embeddings,
                documents=batch_texts,
                metadatas=batch_meta,
            )

    log.info("Ingested %d new chunks", len(new_docs))
    return len(new_docs)


def _doc_id(doc: dict) -> str:
    text = doc["text"]
    source = doc["metadata"].get("source", "")
    return hashlib.md5(f"{source}::{text[:200]}".encode()).hexdigest()
