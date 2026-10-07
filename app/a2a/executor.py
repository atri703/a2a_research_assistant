import json
from a2a.helpers import get_message_text, new_text_message
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Role
from app.dependencies import build_workflow
from app.schemas.models import ResearchRequest

class ResearchSupervisorExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        raw = get_message_text(context.message)
        try:
            payload = json.loads(raw)
            request = ResearchRequest.model_validate(payload)
        except Exception:
            request = ResearchRequest(topic=raw)

        workflow = build_workflow()
        import uuid
        project_id = str(uuid.uuid4())
        result = await workflow.graph.ainvoke({
            "project_id": project_id,
            "request": request.model_dump(),
            "status": "created",
        })
        response = {
            "project_id": project_id,
            "status": result.get("status"),
            "sections": result.get("sections", {}),
            "reviews": result.get("reviews", {}),
        }
        await event_queue.enqueue_event(
            new_text_message(json.dumps(response), role=Role.ROLE_AGENT)
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        raise NotImplementedError("Cancellation is not supported in the MVP")
