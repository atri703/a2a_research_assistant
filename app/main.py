from uuid import uuid4
from fastapi import FastAPI, HTTPException
from app.a2a.service import get_agent_card
from app.dependencies import build_workflow
from app.schemas.models import ResearchRequest, RunResponse, SectionReview

app = FastAPI(title="A2A Research Assistant", version="0.1.0")

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status":"ok"}

@app.get("/.well-known/agent-card.json")
async def agent_card():
    return get_agent_card()

@app.post("/research", response_model=RunResponse)
async def research(request: ResearchRequest) -> RunResponse:
    project_id = str(uuid4())
    workflow = build_workflow()
    try:
        result = await workflow.graph.ainvoke({"project_id":project_id, "request":request.model_dump(), "status":"created"})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return RunResponse(
        project_id=project_id,
        status=result["status"],
        sections=result.get("sections", {}),
        reviews={k:SectionReview.model_validate(v) for k,v in result.get("reviews", {}).items()},
    )
