"""
Discovery router — find similar poems using Gemini embeddings.
"""

import google.generativeai as genai
from fastapi import APIRouter, Query, HTTPException
from config import settings
from tools.supabase_tool import get_poem, _get_client

genai.configure(api_key=settings.google_api_key)

router = APIRouter()


def _embed(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="SEMANTIC_SIMILARITY",
    )
    return result["embedding"]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


@router.get("/similar/{poem_id}")
async def find_similar(poem_id: str, top_k: int = Query(default=4, le=10)):
    """Find poems similar to a given poem_id."""
    poem = await get_poem(poem_id)
    if not poem:
        raise HTTPException(status_code=404, detail="Poem not found")

    client = _get_client()
    all_poems = client.table("poems").select("id, title, body, year, form, tags, poets(name)").neq("id", poem_id).execute()

    if not all_poems.data:
        return {"results": []}

    query_embedding = _embed(poem["body"])
    scored = []
    for p in all_poems.data:
        emb = _embed(p["body"])
        score = _cosine_similarity(query_embedding, emb)
        scored.append({**p, "similarity_score": round(score, 4)})

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {"results": scored[:top_k]}


@router.get("/search")
async def semantic_search(q: str = Query(..., min_length=3), top_k: int = Query(default=4, le=10)):
    """Embed a free-text query and find the most relevant poems."""
    client = _get_client()
    all_poems = client.table("poems").select("id, title, body, year, form, tags, poets(name)").execute()

    if not all_poems.data:
        return {"query": q, "results": []}

    query_embedding = _embed(q)
    scored = []
    for p in all_poems.data:
        emb = _embed(p["body"])
        score = _cosine_similarity(query_embedding, emb)
        scored.append({**p, "similarity_score": round(score, 4)})

    scored.sort(key=lambda x: x["similarity_score"], reverse=True)
    return {"query": q, "results": scored[:top_k]}
