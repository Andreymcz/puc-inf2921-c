from mcp.server.fastmcp import FastMCP
from kb_qa.query import retrieve as _retrieve

mcp = FastMCP("kb-qa")


@mcp.tool()
def query_knowledge(question: str, n_results: int = 5, doc_type: str | None = None) -> list[dict]:
    """Search the local knowledge base for relevant document chunks.

    Call this to retrieve context from local .md and .pdf documents before
    answering questions. The knowledge base contains whatever documents were
    placed in the knowledge/ directory and ingested via `uv run python -m kb_qa ingest`.

    Args:
        question: Natural language question or keyword.
        n_results: Number of chunks to return (default 5, max 20).
        doc_type: Optional filter — "md" or "pdf".

    Returns:
        List of dicts with keys: text, type, name, source.
        On error: [{"error": "Vector store not found. Run: uv run python -m kb_qa ingest"}]
    """
    try:
        n_results = min(n_results, 20)
        docs = _retrieve(question, n_results=n_results, doc_type_filter=doc_type)
        return [
            {
                "text": d["text"],
                "type": d["metadata"].get("type"),
                "name": d["metadata"].get("name"),
                "source": d["metadata"].get("source"),
            }
            for d in docs
        ]
    except Exception as e:
        return [{"error": str(e)}]


if __name__ == "__main__":
    mcp.run()
