# A2A Research Assistant

A modular research-paper assistant built with **Python, LangGraph, OpenAI, Redis, FastAPI, OpenAlex, and an A2A-ready integration boundary**.

## What it does

The system takes a research topic, creates a paper plan, retrieves academic sources, writes requested sections, reviews them, and automatically revises weak sections before moving forward.

```text
User / A2A Client
       |
       v
Research Supervisor
       |
       v
LangGraph Workflow
       |
       +--> Planner Agent
       +--> Research Agent ----> OpenAlex
       +--> Section Writer ----> OpenAI
       +--> Reviewer Agent ----> OpenAI
       |
       v
Redis State / Memory
```

## Current architecture

- **PlannerAgent**: converts a topic into a structured paper plan.
- **ResearchAgent**: retrieves academic evidence through a provider interface. OpenAlex is the first implementation.
- **SectionWriterAgent**: generic writer for Abstract, Introduction, Literature Review, Methodology, Results, Discussion, and Conclusion.
- **ReviewerAgent**: scores each section and returns revision feedback.
- **LangGraph**: orchestrates plan -> research -> write -> review -> revise/advance.
- **Redis**: stores project workflow state today.
- **A2A boundary**: Agent Card and transport-specific code are isolated under `app/a2a/` so A2A execution can evolve independently.

## Project structure

```text
app/
├── a2a/          # Agent Card and A2A boundary
├── agents/       # Planner, researcher, writer, reviewer
├── graph/        # LangGraph state + workflow
├── llm/          # LLM abstraction + OpenAI implementation
├── memory/       # Memory abstraction + Redis
├── research/     # Academic source providers
├── schemas/      # Shared Pydantic models
├── config.py
├── dependencies.py
└── main.py
```

## Design principles

The project deliberately separates orchestration, agents, LLM provider, research provider, persistence, and A2A transport. This makes it easy to add Semantic Scholar/Crossref/PubMed, PostgreSQL/pgvector, alternative OpenAI models, more specialized agents, or remote A2A workers later.

The generic writer is reused for all sections instead of creating one agent per section. Source-dependent claims must use evidence supplied by the ResearchAgent and internal citation markers such as `[CITE:SOURCE_ID]`. The prompts explicitly prohibit fabricated citations, experiments, data, and results.

## Setup

```bash
git clone https://github.com/atri703/a2a_research_assistant.git
cd a2a_research_assistant
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set:

```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-5.6
REDIS_URL=redis://localhost:6379/0
```

Start Redis:

```bash
docker compose up redis -d
```

Start the API:

```bash
uvicorn app.main:app --reload
```

OpenAPI docs are available at `http://localhost:8000/docs`.

## Example request

```bash
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Impact of social networking on academic outcomes and mental health among university students",
    "citation_style": "APA 7",
    "target_word_count": 5000,
    "sections": ["introduction", "literature_review", "methodology", "discussion", "conclusion"]
  }'
```

## A2A

The MVP exposes an Agent Card at:

```text
GET /.well-known/agent-card.json
```

The intended future topology is:

```text
Supervisor A2A Agent
       |
       +---- A2A ----> Research Agent
       +---- A2A ----> Writer Agent
       +---- A2A ----> Reviewer Agent
```

The code already isolates `app/a2a/` so an official A2A SDK `AgentExecutor` and remote sub-agent clients can be added without rewriting the LangGraph workflow.

## Memory roadmap

Today:

```text
Redis -> workflow/project state
```

Recommended production evolution:

```text
Redis      -> short-lived state, cache, locks
PostgreSQL -> users, projects, tasks, final papers, audit trail
pgvector   -> long-term semantic memory and evidence retrieval
Object store -> uploaded PDFs, datasets, generated DOCX/PDF/LaTeX
```

## Recommended next enhancements

1. Full A2A SDK `AgentExecutor` for supervisor and remote sub-agents.
2. Semantic Scholar, Crossref, PubMed and arXiv providers.
3. Abstract/full-text extraction and evidence chunking.
4. Deterministic citation formatter for APA/IEEE/Harvard/Vancouver.
5. Claim-to-source citation verifier.
6. PostgreSQL + pgvector persistent memory.
7. Human approval checkpoints in LangGraph.
8. Dataset analysis agent for genuine Results sections.
9. DOCX/PDF/LaTeX export.
10. Authentication, rate limiting, tracing and richer tests.

## Tests

```bash
pytest
```

The current test verifies that the A2A Agent Card advertises the research-paper skill.
