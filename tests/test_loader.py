"""Tests for kb_qa.loader."""

from pathlib import Path

import pytest

from kb_qa.loader import load_all, load_md_chunks


def test_load_md_chunks_two_sections(tmp_path: Path) -> None:
    md_file = tmp_path / "sample.md"
    md_file.write_text(
        "# Title\n\n## Section One\nContent of section one.\n\n## Section Two\nContent of section two.\n",
        encoding="utf-8",
    )
    docs = load_md_chunks(md_file)
    assert len(docs) == 3  # preamble + 2 sections
    # Filter to only H2 sections
    section_docs = [d for d in docs if d["text"].startswith("## ")]
    assert len(section_docs) == 2
    for doc in section_docs:
        assert doc["metadata"]["type"] == "md"
        assert doc["metadata"]["source"] == str(md_file)


def test_load_md_chunks_no_headings(tmp_path: Path) -> None:
    md_file = tmp_path / "flat.md"
    md_file.write_text("Just some plain text without any headings.", encoding="utf-8")
    docs = load_md_chunks(md_file)
    assert len(docs) == 1
    assert docs[0]["metadata"]["type"] == "md"
    assert docs[0]["metadata"]["source"] == str(md_file)


def test_load_all_empty(tmp_path: Path) -> None:
    docs = load_all(tmp_path)
    assert docs == []


def test_load_all_skips_vectorstore(tmp_path: Path) -> None:
    vectorstore_dir = tmp_path / "vectorstore"
    vectorstore_dir.mkdir()
    hidden_md = vectorstore_dir / "hidden.md"
    hidden_md.write_text("## Should be skipped\nThis file should not be loaded.", encoding="utf-8")

    visible_md = tmp_path / "visible.md"
    visible_md.write_text("## Visible\nThis should be loaded.", encoding="utf-8")

    docs = load_all(tmp_path)
    sources = [d["metadata"]["source"] for d in docs]
    assert str(hidden_md) not in sources
    assert str(visible_md) in sources
