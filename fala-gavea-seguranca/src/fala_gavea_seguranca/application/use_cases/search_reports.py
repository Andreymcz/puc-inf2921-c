from __future__ import annotations

from dataclasses import dataclass

from ...infrastructure.vector_store.chroma_client import search


@dataclass
class SearchResult:
    id: str
    text: str
    category: str
    status: str
    distance: float
    lat: float | None
    lon: float | None
    territory_name: str | None


class SearchReports:
    def execute(
        self,
        query: str,
        n_results: int = 10,
        category: str | None = None,
        lat_min: float | None = None,
        lat_max: float | None = None,
        lon_min: float | None = None,
        lon_max: float | None = None,
        doc_type: str = "relato",
    ) -> list[SearchResult]:
        where: dict = {"type": {"$eq": doc_type}}
        if category:
            where["category"] = {"$eq": category}
        # ChromaDB where supports $and for multiple filters
        conditions = [{"type": {"$eq": doc_type}}]
        if category:
            conditions.append({"category": {"$eq": category}})
        final_where = {"$and": conditions} if len(conditions) > 1 else conditions[0]

        hits = search(query, n_results=n_results, where=final_where)

        results = []
        for h in hits:
            m = h["metadata"]
            lat = m.get("lat")
            lon = m.get("lon")
            # client-side bbox filter (ChromaDB doesn't support range on float metadata natively in all versions)
            if lat_min is not None and (lat is None or lat < lat_min):
                continue
            if lat_max is not None and (lat is None or lat > lat_max):
                continue
            if lon_min is not None and (lon is None or lon < lon_min):
                continue
            if lon_max is not None and (lon is None or lon > lon_max):
                continue
            results.append(SearchResult(
                id=h["id"],
                text=h["text"],
                category=m.get("category", ""),
                status=m.get("status", ""),
                distance=h["distance"],
                lat=lat,
                lon=lon,
                territory_name=m.get("territory_name"),
            ))
        return results
