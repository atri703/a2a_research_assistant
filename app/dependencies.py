from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.reviewer import ReviewerAgent
from app.agents.writer import SectionWriterAgent
from app.graph.workflow import ResearchWorkflow
from app.llm.openai_service import OpenAIService
from app.memory.redis_store import RedisMemoryStore
from app.research.openalex import OpenAlexProvider

def build_workflow() -> ResearchWorkflow:
    llm = OpenAIService()
    return ResearchWorkflow(
        planner=PlannerAgent(llm),
        researcher=ResearchAgent(OpenAlexProvider()),
        writer=SectionWriterAgent(llm),
        reviewer=ReviewerAgent(llm),
        memory=RedisMemoryStore(),
    )
