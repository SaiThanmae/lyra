"""Poems CRUD router."""

from fastapi import APIRouter, HTTPException
from tools.supabase_tool import get_poem, upsert_poem, upsert_poet
from models.schemas import Poem

router = APIRouter()


@router.get("/{poem_id}", response_model=dict)
async def read_poem(poem_id: str):
    poem = await get_poem(poem_id)
    if not poem:
        raise HTTPException(status_code=404, detail="Poem not found")
    return poem


@router.get("/")
async def list_poems(limit: int = 20, offset: int = 0):
    from tools.supabase_tool import _get_client
    client = _get_client()
    result = (
        client.table("poems")
        .select("id, title, language, form, year, poets(name)")
        .range(offset, offset + limit - 1)
        .order("year", desc=True)
        .execute()
    )
    return {"poems": result.data, "limit": limit, "offset": offset}
