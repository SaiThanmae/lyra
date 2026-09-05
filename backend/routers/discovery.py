"""Discovery router — semantic similarity search."""

from fastapi import APIRouter, Query
from backend.tools.vertex_tool import generate_embedding
from backend.tools.bigquery_tool import query_similar
from backend.tools.supabase_tool import get_poem

router = APIRouter()


@router.get("/similar/{poem_id}")
async def find_similar(poem_id: str, top_k: int = Query(default=6, le=20)):
    """Find poems similar to a given poem_id using vector search."""
    poem = await get_poem(poem_id)
    if not poem:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Poem not found")

    embedding = await generate_embedding(poem["body"])
    similar = await query_similar(embedding, top_k=top_k, exclude_poem_id=poem_id)

    # Enrich with poem metadata
    enriched = []
    for item in similar:
        meta = await get_poem(item["poem_id"])
        enriched.append({**meta, "similarity_score": item["similarity_score"]})

    return {"results": enriched}


@router.get("/search")
async def semantic_search(q: str = Query(..., min_length=3), top_k: int = Query(default=6, le=20)):
    """Embed a free-text query and find the most relevant poems."""
    embedding = await generate_embedding(q)
    similar = await query_similar(embedding, top_k=top_k)

    enriched = []
    for item in similar:
        meta = await get_poem(item["poem_id"])
        enriched.append({**meta, "similarity_score": item["similarity_score"]})

    return {"query": q, "results": enriched}
