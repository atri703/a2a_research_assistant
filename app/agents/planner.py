from app.llm.base import LLMService
from app.schemas.models import ResearchPlan, ResearchRequest

class PlannerAgent:
    def __init__(self, llm: LLMService) -> None:
        self.llm = llm
    async def run(self, request: ResearchRequest) -> ResearchPlan:
        return await self.llm.structured(
            "You supervise an academic research assistant. Create a precise plan and never invent study results.",
            f"Topic: {request.topic}\nResearch question: {request.research_question or 'derive one'}\nCitation style: {request.citation_style}\nTarget words: {request.target_word_count}\nSections: {request.sections}",
            ResearchPlan,
        )
