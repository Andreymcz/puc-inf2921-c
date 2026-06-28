"""Document loaders for the kb-qa RAG pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypedDict

logger = logging.getLogger(__name__)

_CHUNK_MAX_CHARS = 2000
_PDF_CHUNK_WORDS = 512
_PDF_OVERLAP_WORDS = 64
_TXT_CHUNK_LINES = 30
_TXT_OVERLAP_LINES = 6


class Document(TypedDict):
    text: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class LoaderConfig:
    base: str
    pattern: str
    fn: Callable[[Path], list[Document]]


def load_md_chunks(path: Path) -> list[Document]:
    """Split a Markdown file into chunks by H2 headings."""
    content = path.read_text(encoding="utf-8")
    source = str(path)
    name = path.stem

    parts = content.split("\n## ")
    if len(parts) == 1:
        # No H2 headings — single chunk
        return [
            Document(
                text=content[:_CHUNK_MAX_CHARS],
                metadata={"type": "md", "source": source, "name": name},
            )
        ]

    chunks: list[Document] = []
    # First part is content before the first ## (may be empty or have a title)
    preamble = parts[0].strip()
    if preamble:
        chunks.append(
            Document(
                text=preamble[:_CHUNK_MAX_CHARS],
                metadata={"type": "md", "source": source, "name": name},
            )
        )
    for section in parts[1:]:
        lines = section.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1] if len(lines) > 1 else ""
        text = f"## {heading}\n{body}"
        chunks.append(
            Document(
                text=text[:_CHUNK_MAX_CHARS],
                metadata={"type": "md", "source": source, "name": name},
            )
        )
    return chunks


def load_pdf_chunks(path: Path) -> list[Document]:
    """Split a PDF file into fixed-size word chunks with overlap."""
    import fitz  # type: ignore[import-untyped]

    source = str(path)
    name = path.stem

    doc = fitz.open(str(path))
    full_text = "\n".join(page.get_text() for page in doc)
    doc.close()

    words = full_text.split()
    if not words:
        return []

    chunks: list[Document] = []
    step = _PDF_CHUNK_WORDS - _PDF_OVERLAP_WORDS
    for i in range(0, len(words), step):
        chunk_words = words[i : i + _PDF_CHUNK_WORDS]
        text = " ".join(chunk_words)
        chunks.append(
            Document(
                text=text,
                metadata={"type": "pdf", "source": source, "name": name},
            )
        )
        if i + _PDF_CHUNK_WORDS >= len(words):
            break
    return chunks


def load_txt_chunks(path: Path) -> list[Document]:
    """Split a plain-text file into overlapping line windows.

    Unlike the Markdown loader (which splits on H2 headings), plain-text files
    such as chat exports have no structural headings, so a sliding window of
    lines with overlap keeps nearby messages together for retrieval while
    preserving each line's leading date/sender prefix.
    """
    source = str(path)
    name = path.stem
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    if not lines:
        return []

    chunks: list[Document] = []
    step = _TXT_CHUNK_LINES - _TXT_OVERLAP_LINES
    for i in range(0, len(lines), step):
        window = lines[i : i + _TXT_CHUNK_LINES]
        text = "\n".join(window).strip()
        if text:
            chunks.append(
                Document(
                    text=text[:_CHUNK_MAX_CHARS],
                    metadata={
                        "type": "txt",
                        "source": source,
                        "name": name,
                        "lines": f"{i + 1}-{i + len(window)}",
                    },
                )
            )
        if i + _TXT_CHUNK_LINES >= len(lines):
            break
    return chunks


LOADER_REGISTRY: list[LoaderConfig] = [
    LoaderConfig(".", "**/*.md", load_md_chunks),
    LoaderConfig(".", "**/*.pdf", load_pdf_chunks),
    LoaderConfig(".", "**/*.txt", load_txt_chunks),
]


def load_all(knowledge_dir: Path) -> list[Document]:
    """Load all documents from knowledge_dir using LOADER_REGISTRY."""
    documents: list[Document] = []
    for config in LOADER_REGISTRY:
        for file_path in knowledge_dir.rglob(config.pattern.split("/")[-1]):
            if "vectorstore" in file_path.parts:
                continue
            try:
                docs = config.fn(file_path)
                documents.extend(docs)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Failed to load %s: %s", file_path, exc)
    return documents
