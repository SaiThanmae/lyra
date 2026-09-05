"""
Pydantic models — the core data contracts for Lyra.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class Poet(BaseModel):
    id: Optional[str] = None
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    nationality: Optional[str] = None
    traditions: list[str] = Field(default_factory=list)
    bio: Optional[str] = None


class Poem(BaseModel):
    id: Optional[str] = None
    title: str
    body: str
    poet_id: str
    year: Optional[int] = None
    language: str = "en"
    form: Optional[str] = None          # sonnet, haiku, ghazal, free verse …
    collection_id: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class Collection(BaseModel):
    id: Optional[str] = None
    title: str
    poet_id: str
    year: Optional[int] = None
    publisher: Optional[str] = None


class PoemAnalysis(BaseModel):
    id: Optional[str] = None
    poem_id: str
    meter: Optional[str] = None
    rhyme_scheme: Optional[str] = None
    tone: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    cultural_context: Optional[str] = None
    influences: list[str] = Field(default_factory=list)
    summary: Optional[str] = None
    raw_json: Optional[dict] = None


class Lineage(BaseModel):
    id: Optional[str] = None
    source_poem_id: str
    influenced_poem_id: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    rationale: Optional[str] = None


class DiscoveryResult(BaseModel):
    poem: Poem
    similarity_score: float
    reason: Optional[str] = None


class IngestRequest(BaseModel):
    title: str
    body: str
    poet_name: str
    year: Optional[int] = None
    language: str = "en"
    form: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
