import httpx
from app.research.base import ResearchProvider
from app.schemas.models import EvidenceItem

class OpenAlexProvider(ResearchProvider):
    BASE_URL = "https://api.openalex.org/works"

    async def search(self, query: str, limit: int = 8) -> list[EvidenceItem]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(self.BASE_URL, params={"search": query, "per-page": limit})
            response.raise_for_status()
            data = response.json()
        items = []
        for work in data.get("results", []):
            source_id = work.get("id", "").rsplit("/", 1)[-1]
            authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", []) if a.get("author", {}).get("display_name")]
            items.append(EvidenceItem(
                source_id=source_id,
                title=work.get("title") or "Untitled",
                authors=authors,
                year=work.get("publication_year"),
                url=work.get("doi") or work.get("id"),
                doi=(work.get("doi") or "").replace("https://doi.org/", "") or None,
                claim=work.get("title") or "",
                relevance=f"Retrieved for query: {query}",
                section_tags=["introduction", "literature_review", "discussion"],
            ))
        return items
