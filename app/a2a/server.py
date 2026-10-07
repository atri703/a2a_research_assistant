import uvicorn
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from starlette.applications import Starlette
from app.a2a.executor import ResearchSupervisorExecutor


def build_agent_card() -> AgentCard:
    skill = AgentSkill(
        id="research-paper",
        name="Research Paper Workflow",
        description="Plan, research, draft, review and revise academic paper sections.",
        input_modes=["text/plain"],
        output_modes=["text/plain"],
        tags=["research", "academic-writing", "langgraph"],
        examples=["Write a literature review on retrieval augmented generation"],
    )
    return AgentCard(
        name="Research Supervisor",
        description="A LangGraph supervisor that delegates research-paper work to specialist subagents.",
        version="0.2.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False),
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url="http://127.0.0.1:9999",
                protocol_version="1.0",
            )
        ],
        skills=[skill],
    )


def create_app() -> Starlette:
    card = build_agent_card()
    handler = DefaultRequestHandler(
        agent_executor=ResearchSupervisorExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )
    routes = []
    routes.extend(create_agent_card_routes(card))
    routes.extend(create_jsonrpc_routes(handler, "/"))
    return Starlette(routes=routes)


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9999)
