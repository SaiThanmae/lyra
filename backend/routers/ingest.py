"""Ingest router — accepts poem submissions and stores them in Supabase."""

from fastapi import APIRouter
from models.schemas import IngestRequest
from tools.supabase_tool import upsert_poet, upsert_poem

router = APIRouter()


@router.post("/", status_code=202)
async def ingest_poem(request: IngestRequest):
    """Store poet + poem in Supabase. Returns poem_id."""
    poet = await upsert_poet(name=request.poet_name)
    poet_id = poet.get("id")

    poem = await upsert_poem(
        title=request.title,
        body=request.body,
        poet_id=poet_id,
        year=request.year,
        language=request.language,
        form=request.form,
        tags=request.tags,
    )
    return {"poem_id": poem.get("id"), "status": "stored"}
