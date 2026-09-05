"""Ingest router — accepts poem submissions and runs the full ADK pipeline."""

from fastapi import APIRouter, BackgroundTasks
from backend.models.schemas import IngestRequest
from backend.tools.supabase_tool import upsert_poet, upsert_poem
from backend.tools.vertex_tool import generate_embedding
from backend.tools.bigquery_tool import store_embedding

router = APIRouter()


@router.post("/", status_code=202)
async def ingest_poem(request: IngestRequest, background_tasks: BackgroundTasks):
    """
    Accepts a poem submission.
    1. Synchronously stores poet + poem in Supabase.
    2. Kicks off background embedding + analysis pipeline.
    """
    # 1. Upsert poet
    poet = await upsert_poet(name=request.poet_name)
    poet_id = poet.get("id")

    # 2. Store poem
    poem = await upsert_poem(
        title=request.title,
        body=request.body,
        poet_id=poet_id,
        year=request.year,
        language=request.language,
        form=request.form,
        tags=request.tags,
    )
    poem_id = poem.get("id")

    # 3. Queue embedding + analysis in background
    background_tasks.add_task(_run_pipeline, poem_id, request.body)

    return {"poem_id": poem_id, "status": "accepted", "message": "Analysis pipeline queued."}


async def _run_pipeline(poem_id: str, body: str):
    """Background: generate embedding and trigger ADK analysis agent."""
    embedding = await generate_embedding(body)
    await store_embedding(poem_id, embedding)
    # ADK analysis agent will be invoked here once ADK session management
    # is wired to Firestore in the next sprint.
