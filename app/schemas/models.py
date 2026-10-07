from typing import Literal
from pydantic import BaseModel, Field

SectionName = Literal["abstract","introduction","literature_review","methodology","results","discussion","conclusion"]

class ResearchRequest(BaseModel):
    topic: str
    research_question: str | None = None
    citation_style: str = "APA 7"
    target_word_count: int = 5000
    sections: list[SectionName] = Field(default_factory=lambda: ["abstract","introduction","literature_review","methodology","discussion","conclusion"])

class ResearchPlan(BaseModel):
    title: str
    research_question: str
    citation_style: str
    target_word_count: int
    sections: list[SectionName]

class EvidenceItem(BaseModel):
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    url: str | None = None
    doi: str | None = None
    claim: str
    relevance: str
    section_tags: list[str] = Field(default_factory=list)

class SectionReview(BaseModel):
    section: str
    approved: bool
    score: float = Field(ge=0, le=1)
    feedback: list[str] = Field(default_factory=list)

class RunResponse(BaseModel):
    project_id: str
    status: str
    sections: dict[str, str]
    reviews: dict[str, SectionReview]
