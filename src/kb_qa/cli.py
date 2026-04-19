from pathlib import Path

import click

from kb_qa.constants import KNOWLEDGE_DIR, VECTORSTORE_DIR


@click.group()
def cli() -> None:
    """kb-qa: generic RAG knowledge base CLI."""


@cli.command()
@click.option("--force", is_flag=True, help="Reingest all documents.")
@click.option("--knowledge-dir", type=click.Path(path_type=Path), default=KNOWLEDGE_DIR)
@click.option("--vectorstore-dir", type=click.Path(path_type=Path), default=VECTORSTORE_DIR)
def ingest(force: bool, knowledge_dir: Path, vectorstore_dir: Path) -> None:
    """Ingest documents from knowledge/ into ChromaDB."""
    import logging

    logging.basicConfig(level=logging.INFO)
    from kb_qa.ingest import ingest as _ingest

    count = _ingest(knowledge_dir=knowledge_dir, vectorstore_dir=vectorstore_dir, force=force)
    click.echo(f"Ingested {count} new chunks.")


@cli.command()
@click.option("--knowledge-dir", type=click.Path(path_type=Path), default=KNOWLEDGE_DIR)
@click.option("--vectorstore-dir", type=click.Path(path_type=Path), default=VECTORSTORE_DIR)
def status(knowledge_dir: Path, vectorstore_dir: Path) -> None:
    """Show chunk counts by type and delta between knowledge files and vector store."""
    import chromadb
    from collections import Counter

    from kb_qa.loader import load_all

    docs = load_all(knowledge_dir)
    type_counts = Counter(d["metadata"].get("type", "unknown") for d in docs)
    click.echo(f"Knowledge files: {len(docs)} chunks total")
    for t, n in type_counts.items():
        click.echo(f"  {t}: {n}")
    try:
        client = chromadb.PersistentClient(path=str(vectorstore_dir))
        col = client.get_collection("kb-qa-docs")
        n_stored = col.count()
        click.echo(f"Vector store: {n_stored} chunks indexed")
        delta = len(docs) - n_stored
        if delta > 0:
            click.echo(f"  Delta: {delta} chunks not yet ingested (run: kb-qa ingest)")
        elif delta < 0:
            click.echo(f"  Delta: {abs(delta)} extra chunks in store (run: kb-qa ingest --force to reingest)")
        else:
            click.echo("  Up to date.")
    except Exception:
        click.echo("Vector store: not found (run: kb-qa ingest)")


@cli.command()
@click.argument("question")
@click.option("--n-results", default=5, type=int)
@click.option("--type", "doc_type", default=None, type=click.Choice(["md", "pdf"]))
@click.option("--vectorstore-dir", type=click.Path(path_type=Path), default=VECTORSTORE_DIR)
def ask(question: str, n_results: int, doc_type: str | None, vectorstore_dir: Path) -> None:
    """Retrieve chunks and print them."""
    try:
        from kb_qa.query import retrieve

        docs = retrieve(question, n_results=n_results, vectorstore_dir=vectorstore_dir, doc_type_filter=doc_type)
        for i, doc in enumerate(docs, 1):
            click.echo(f"--- Result {i} ({doc['metadata'].get('type', '?')} | {doc['metadata'].get('name', '?')}) ---")
            click.echo(doc["text"][:500])
            click.echo()
    except Exception as e:
        click.echo(f"Error: {e}\nRun 'kb-qa ingest' first.", err=True)
