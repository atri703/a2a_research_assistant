# A2A Research Assistant

A modular research-paper assistant built with **Python, LangGraph, OpenAI, Redis, FastAPI, OpenAlex and A2A 1.0**.

## Architecture

```text
A2A Client / REST Client
        |
        v
Research Supervisor
        |
        v
LangGraph
  |       |        |
  v       v        v
Research Writer  Reviewer
 Agent    Agent    Agent
  |                  |
OpenAlex            OpenAI
        \            /
             Redis
```

The supervisor is the entry point and delegates work to specialist subagents. LangGraph controls routing, revision loops and section progression.

## Features

- LangGraph supervisor workflow
- OpenAI Responses API
- Research, writer and reviewer subagents
- OpenAlex literature search provider
- Redis workflow/project memory
- Review-and-revision loop
- A2A 1.0 `AgentExecutor` + JSON-RPC server
- FastAPI REST endpoint
- Pydantic structured outputs
- Docker-ready layout
- Interfaces for future LLM, research and persistence backends

## Project structure

```text
app/
├── a2a/
│   ├── executor.py   # A2A -> LangGraph bridge
│   ├── server.py     # A2A JSON-RPC server
│   ├── card.py
│   └── service.py
├── agents/
│   ├── planner.py
│   ├── researcher.py
│   ├── writer.py
│   └── reviewer.py
├── graph/
│   ├── state.py
│   └── workflow.py
├── llm/
├── memory/
├── research/
├── schemas/
├── dependencies.py
└── main.py
```

## Workflow

```text
Request
  -> Plan
  -> Research
  -> Write section
  -> Review
       -> revise if rejected
       -> advance if approved/max retries
  -> next section
  -> complete
```

## Setup

```bash
git clone https://github.com/atri703/a2a_research_assistant.git
cd a2a_research_assistant
python -m venv .venv
pip install -r requirements.txt
```

Create `.env` from `.env.example`:

```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-5.6
REDIS_URL=redis://localhost:6379/0
```

Start Redis:

```bash
docker compose up redis -d
```

## Run REST API

```bash
uvicorn app.main:app --reload --port 8000
```

REST endpoint:

```text
POST /research
```

Example body:

```json
{
  "topic": "Impact of social networking on academic outcomes and mental health among university students",
  "citation_style": "APA 7",
  "target_word_count": 5000,
  "sections": ["introduction", "literature_review", "methodology", "discussion", "conclusion"]
}
```

## Run as an A2A agent

```bash
python -m app.a2a.server
```

The A2A server listens on port `9999` and exposes discovery plus JSON-RPC routes. A client can send either plain text (treated as the research topic) or JSON matching `ResearchRequest`.

## Modularity / future enhancements

The code separates `LLMService`, `ResearchProvider`, and `MemoryStore`, so implementations can be replaced without changing the graph.

Recommended next additions:

1. Make ResearchAgent, WriterAgent and ReviewerAgent independently hosted A2A services; the current supervisor already delegates to them as modular subagents, while A2A is exposed at the supervisor boundary.
2. Add Semantic Scholar, Crossref, PubMed and arXiv providers.
3. Add full-text/abstract evidence extraction and evidence chunking.
4. Add a deterministic citation manager and claim-to-source verifier.
5. Move durable project data to PostgreSQL and semantic memory to pgvector, keeping Redis for short-lived state/cache/locks.
6. Add LangGraph human-approval checkpoints.
7. Add a dataset-analysis agent so Results sections are generated only from real supplied data.
8. Add DOCX/PDF/LaTeX exporters.
9. Add auth, rate limits, tracing and stronger integration tests.

## Memory roadmap

```text
Today:
Redis -> workflow/project state

Future:
Redis      -> transient state/cache/locks
PostgreSQL -> durable projects/tasks/papers/audit trail
pgvector   -> evidence + semantic long-term memory
Object Store -> PDFs, datasets and exports
```

## Safety against fake research

The writer is instructed to use only supplied evidence for source-dependent claims, emit internal citation markers like `[CITE:SOURCE_ID]`, and never fabricate references, data, experiments or results. Results should eventually be produced by a dedicated analysis agent from real data.

## Tests

```bash
pytest
```
