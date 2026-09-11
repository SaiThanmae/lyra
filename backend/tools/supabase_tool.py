"""
Supabase tool functions — ADK-compatible callables for the agents.
Each function is a plain Python async function decorated as an ADK tool.
"""

from __future__ import annotations

import uuid
from typing import Optional

from supabase import create_client, Client
from config import settings

_client: Optional[Client] = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_service_key)
    return _client


async def upsert_poet(name: str, nationality: str = "", traditions: list[str] | None = None, bio: str = "") -> dict:
    """Create or update a poet record in Supabase. Returns the poet row."""
    client = _get_client()
    payload = {
        "name": name,
        "nationality": nationality,
        "traditions": traditions or [],
        "bio": bio,
    }
    # upsert on name — simple dedup strategy
    result = client.table("poets").upsert(payload, on_conflict="name").execute()
    return result.data[0] if result.data else {}


async def upsert_poem(
    title: str,
    body: str,
    poet_id: str,
    year: int | None = None,
    language: str = "en",
    form: str | None = None,
    tags: list[str] | None = None,
    collection_id: str | None = None,
) -> dict:
    """Store a poem in Supabase. Returns the poem row including its id."""
    client = _get_client()
    payload = {
        "id": str(uuid.uuid4()),
        "title": title,
        "body": body,
        "poet_id": poet_id,
        "year": year,
        "language": language,
        "form": form,
        "tags": tags or [],
        "collection_id": collection_id,
    }
    result = client.table("poems").insert(payload).execute()
    return result.data[0] if result.data else {}


async def get_poem(poem_id: str) -> dict:
    """Fetch a single poem by id from Supabase."""
    client = _get_client()
    result = client.table("poems").select("*, poets(*)").eq("id", poem_id).single().execute()
    return result.data or {}


async def store_analysis(
    poem_id: str,
    meter: str = "",
    rhyme_scheme: str = "",
    tone: list[str] | None = None,
    themes: list[str] | None = None,
    cultural_context: str = "",
    influences: list[str] | None = None,
    summary: str = "",
    raw_json: dict | None = None,
) -> dict:
    """Persist analysis results to Supabase."""
    client = _get_client()
    payload = {
        "poem_id": poem_id,
        "meter": meter,
        "rhyme_scheme": rhyme_scheme,
        "tone": tone or [],
        "themes": themes or [],
        "cultural_context": cultural_context,
        "influences": influences or [],
        "summary": summary,
        "raw_json": raw_json or {},
    }
    result = client.table("analysis").upsert(payload, on_conflict="poem_id").execute()
    return result.data[0] if result.data else {}


async def store_lineage(
    source_poem_id: str,
    influenced_poem_id: str,
    confidence_score: float,
    rationale: str = "",
) -> dict:
    """Store a lineage relationship in Supabase."""
    client = _get_client()
    payload = {
        "source_poem_id": source_poem_id,
        "influenced_poem_id": influenced_poem_id,
        "confidence_score": confidence_score,
        "rationale": rationale,
    }
    result = client.table("lineages").insert(payload).execute()
    return result.data[0] if result.data else {}
