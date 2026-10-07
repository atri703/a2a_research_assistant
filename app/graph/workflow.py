from langgraph.graph import END, StateGraph
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearchAgent
from app.agents.writer import SectionWriterAgent
from app.agents.reviewer import ReviewerAgent
from app.graph.state import ResearchState
from app.memory.base import MemoryStore
from app.schemas.models import EvidenceItem, ResearchPlan, ResearchRequest

class ResearchWorkflow:
    def __init__(self, planner: PlannerAgent, researcher: ResearchAgent, writer: SectionWriterAgent, reviewer: ReviewerAgent, memory: MemoryStore) -> None:
        self.planner = planner
        self.researcher = researcher
        self.writer = writer
        self.reviewer = reviewer
        self.memory = memory
        self.graph = self._build()

    def _build(self):
        graph = StateGraph(ResearchState)
        graph.add_node("plan", self._plan)
        graph.add_node("research", self._research)
        graph.add_node("write", self._write)
        graph.add_node("review", self._review)
        graph.add_node("advance", self._advance)
        graph.set_entry_point("plan")
        graph.add_edge("plan", "research")
        graph.add_edge("research", "write")
        graph.add_edge("write", "review")
        graph.add_conditional_edges("review", self._route_review, {"revise":"write", "advance":"advance"})
        graph.add_conditional_edges("advance", self._route_advance, {"write":"write", "done":END})
        return graph.compile()

    async def _persist(self, state: ResearchState) -> None:
        await self.memory.set(state["project_id"], dict(state))

    async def _plan(self, state: ResearchState) -> ResearchState:
        request = ResearchRequest.model_validate(state["request"])
        plan = await self.planner.run(request)
        next_state = {**state, "plan":plan.model_dump(), "sections":{}, "reviews":{}, "current_section":plan.sections[0], "revision_count":0, "status":"planned"}
        await self._persist(next_state)
        return next_state

    async def _research(self, state: ResearchState) -> ResearchState:
        plan = ResearchPlan.model_validate(state["plan"])
        evidence = await self.researcher.run(plan)
        next_state = {**state, "evidence":[e.model_dump() for e in evidence], "status":"researched"}
        await self._persist(next_state)
        return next_state

    async def _write(self, state: ResearchState) -> ResearchState:
        plan = ResearchPlan.model_validate(state["plan"])
        evidence = [EvidenceItem.model_validate(e) for e in state["evidence"]]
        section = state["current_section"]
        prior_review = state.get("reviews", {}).get(section, {})
        content = await self.writer.run(section, plan, evidence, prior_review.get("feedback"))
        next_state = {**state, "sections":{**state.get("sections", {}), section:content}, "status":f"written:{section}"}
        await self._persist(next_state)
        return next_state

    async def _review(self, state: ResearchState) -> ResearchState:
        evidence = [EvidenceItem.model_validate(e) for e in state["evidence"]]
        section = state["current_section"]
        review = await self.reviewer.run(section, state["sections"][section], evidence)
        revision_count = state.get("revision_count", 0) + (0 if review.approved else 1)
        next_state = {**state, "reviews":{**state.get("reviews", {}), section:review.model_dump()}, "revision_count":revision_count, "status":f"reviewed:{section}"}
        await self._persist(next_state)
        return next_state

    def _route_review(self, state: ResearchState) -> str:
        section = state["current_section"]
        if not state["reviews"][section]["approved"] and state.get("revision_count", 0) < 2:
            return "revise"
        return "advance"

    async def _advance(self, state: ResearchState) -> ResearchState:
        plan = ResearchPlan.model_validate(state["plan"])
        idx = plan.sections.index(state["current_section"])
        if idx + 1 >= len(plan.sections):
            next_state = {**state, "current_section":None, "status":"completed"}
        else:
            next_state = {**state, "current_section":plan.sections[idx+1], "revision_count":0, "status":"writing"}
        await self._persist(next_state)
        return next_state

    def _route_advance(self, state: ResearchState) -> str:
        return "done" if state.get("current_section") is None else "write"
