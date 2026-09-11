"""Lineage router — poem influence and ancestry graph."""

from fastapi import APIRouter, HTTPException
from tools.supabase_tool import _get_client

router = APIRouter()


@router.get("/{poem_id}")
async def get_lineage(poem_id: str):
    """Return all lineage edges where this poem is the source or the influenced poem."""
    client = _get_client()

    as_source = (
        client.table("lineages")
        .select("*, influenced:influenced_poem_id(id, title, poets(name))")
        .eq("source_poem_id", poem_id)
        .order("confidence_score", desc=True)
        .execute()
    )
    as_influenced = (
        client.table("lineages")
        .select("*, source:source_poem_id(id, title, poets(name))")
        .eq("influenced_poem_id", poem_id)
        .order("confidence_score", desc=True)
        .execute()
    )

    return {
        "poem_id": poem_id,
        "influences_others": as_source.data,
        "influenced_by": as_influenced.data,
    }
