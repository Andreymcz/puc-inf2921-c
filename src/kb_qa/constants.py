from pathlib import Path

KNOWLEDGE_DIR: Path = Path(__file__).parent.parent.parent / "knowledge"
VECTORSTORE_DIR: Path = KNOWLEDGE_DIR / "vectorstore"
COLLECTION_NAME: str = "kb-qa-docs"
EMBED_MODEL: str = "nomic-ai/nomic-embed-text-v1"
DOCUMENT_TYPES: frozenset[str] = frozenset({"md", "pdf"})
EMBED_BATCH_SIZE: int = 256
