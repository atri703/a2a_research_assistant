from pydantic import BaseModel, Field
from app.llm.base import LLMService
from app.schemas.models import EvidenceItem, SectionReview

class ReviewPayload(BaseModel):
    approved: bool
    score: float = Field(ge=0, le=1)
    feedback: list[str] = Field(default_factory=list)

class ReviewerAgent:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm
    async def run(self, section: str, content: str, evidence: list[EvidenceItem]) -> SectionReview:
        valid_ids = [e.source_id for e in evidence]
        result = await self.llm.structured(
            "You are a strict academic reviewer. Check coherence, academic tone, unsupported claims and citation grounding. Reject fabricated results/citations. Approve only if score >= 0.8.",
            f"Section: {section}\nValid citation IDs: {valid_ids}\nContent:\n{content}",
            ReviewPayload,
        )
        approved = result.approved and result.score >= 0.8
        return SectionReview(section=section, approved=approved, score=result.score, feedback=result.feedback)
