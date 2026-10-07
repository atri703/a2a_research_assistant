from app.llm.base import LLMService
from app.schemas.models import EvidenceItem, ResearchPlan

class SectionWriterAgent:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm
    async def run(self, section: str, plan: ResearchPlan, evidence: list[EvidenceItem], feedback: list[str] | None = None) -> str:
        sources = "\n".join(f"[{e.source_id}] {e.title} ({e.year or 'n.d.'}) - {e.url or ''}" for e in evidence)
        system = "You are an academic section writer. Use only supplied evidence for source-dependent claims. Cite with [CITE:SOURCE_ID]. Never fabricate references, data, experiments, or results."
        user = f"Paper title: {plan.title}\nResearch question: {plan.research_question}\nSection: {section}\nCitation style: {plan.citation_style}\nEvidence:\n{sources}\nReviewer feedback: {feedback or []}\nWrite the section in clear academic prose."
        return await self.llm.text(system, user)
