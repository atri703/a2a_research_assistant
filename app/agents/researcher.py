from app.research.base import ResearchProvider
from app.schemas.models import EvidenceItem, ResearchPlan

class ResearchAgent:
    def __init__(self, provider: ResearchProvider) -> None:
        self.provider = provider
    async def run(self, plan: ResearchPlan) -> list[EvidenceItem]:
        return await self.provider.search(f"{plan.title} {plan.research_question}", limit=10)
