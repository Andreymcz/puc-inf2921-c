"""Tests for kb_qa.ingest and kb_qa.query modules."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from kb_qa.ingest import _doc_id, ingest


def _write_sample_md(directory: Path, filename: str = "sample.md") -> Path:
    """Write a sample markdown file with 2 H2 sections."""
    path = directory / filename
    path.write_text(
        "# Title\n\nPreamble content.\n\n## Section One\n\nContent of section one.\n\n## Section Two\n\nContent of section two.\n",
        encoding="utf-8",
    )
    return path


def _make_mock_collection(existing_ids: list[str] | None = None) -> MagicMock:
    collection = MagicMock()
    collection.get.return_value = {"ids": existing_ids or []}
    return collection


def _make_mock_client(collection: MagicMock) -> MagicMock:
    client = MagicMock()
    client.get_or_create_collection.return_value = collection
    return client


class TestIngestEmptyKnowledgeDir:
    def test_ingest_empty_knowledge(self) -> None:
        """ingest() with an empty dir returns 0 without calling SentenceTransformer."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            with patch("kb_qa.ingest.SentenceTransformer") as mock_st:
                result = ingest(knowledge_dir=tmp_path, vectorstore_dir=tmp_path / "vs")
        assert result == 0
        mock_st.assert_not_called()


class TestIngestReturnsCount:
    def test_ingest_returns_count(self) -> None:
        """ingest() returns the number of newly ingested chunks."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_sample_md(tmp_path)

            collection = _make_mock_collection(existing_ids=[])
            mock_client = _make_mock_client(collection)

            # We'll determine chunk count after loading to build correct mock
            from kb_qa.loader import load_all

            docs = load_all(tmp_path)
            n_chunks = len(docs)
            assert n_chunks > 0

            def fake_encode(texts: list[str], **kwargs: object) -> np.ndarray:
                return np.zeros((len(texts), 384), dtype=np.float32)

            mock_model = MagicMock()
            mock_model.encode.side_effect = fake_encode

            with (
                patch("kb_qa.ingest.SentenceTransformer", return_value=mock_model),
                patch("kb_qa.ingest.chromadb.PersistentClient", return_value=mock_client),
            ):
                result = ingest(
                    knowledge_dir=tmp_path,
                    vectorstore_dir=tmp_path / "vs",
                )

        assert result == n_chunks
        assert collection.add.called


class TestIngestIdempotency:
    def test_ingest_idempotency(self) -> None:
        """ingest() returns 0 when all chunks are already in the collection."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            _write_sample_md(tmp_path)

            from kb_qa.loader import load_all

            docs = load_all(tmp_path)
            all_ids = [_doc_id(d) for d in docs]

            collection = _make_mock_collection(existing_ids=all_ids)
            mock_client = _make_mock_client(collection)

            mock_model = MagicMock()

            with (
                patch("kb_qa.ingest.SentenceTransformer", return_value=mock_model),
                patch("kb_qa.ingest.chromadb.PersistentClient", return_value=mock_client),
            ):
                result = ingest(
                    knowledge_dir=tmp_path,
                    vectorstore_dir=tmp_path / "vs",
                )

        assert result == 0
        collection.add.assert_not_called()


class TestRetrieveWithMock:
    def test_retrieve_with_mock(self) -> None:
        """retrieve() returns a list with one Document when collection.query returns one result."""
        from kb_qa.query import retrieve

        mock_embedding = [0.0] * 384
        mock_model = MagicMock()
        mock_model.encode.return_value = MagicMock(tolist=lambda: [mock_embedding])

        mock_collection = MagicMock()
        mock_collection.query.return_value = {
            "documents": [["Some relevant text about RESQML."]],
            "metadatas": [[{"type": "md", "name": "sample.md", "source": "knowledge/sample.md"}]],
        }

        mock_client = MagicMock()
        mock_client.get_collection.return_value = mock_collection

        with tempfile.TemporaryDirectory() as tmp:
            vs_dir = Path(tmp)
            with (
                patch("kb_qa.query.SentenceTransformer", return_value=mock_model),
                patch("kb_qa.query.chromadb.PersistentClient", return_value=mock_client),
            ):
                docs = retrieve("test question", n_results=1, vectorstore_dir=vs_dir)

        assert len(docs) == 1
        assert docs[0]["text"] == "Some relevant text about RESQML."
        assert docs[0]["metadata"]["type"] == "md"
