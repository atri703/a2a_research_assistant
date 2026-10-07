from typing import TypedDict, Any

class ResearchState(TypedDict, total=False):
    project_id: str
    request: dict[str, Any]
    plan: dict[str, Any]
    evidence: list[dict[str, Any]]
    sections: dict[str, str]
    reviews: dict[str, dict[str, Any]]
    current_section: str | None
    revision_count: int
    status: str
