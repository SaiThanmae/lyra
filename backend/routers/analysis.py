"""
Analysis router — trigger and fetch Gemini-powered poem analysis.
"""

import json
import google.generativeai as genai
from fastapi import APIRouter, HTTPException
from config import settings
from tools.supabase_tool import _get_client, get_poem, store_analysis

genai.configure(api_key=settings.google_api_key)
model = genai.GenerativeModel("gemini-flash-latest")

router = APIRouter()

ANALYSIS_PROMPT = """
You are a literary scholar AI specialising in global poetic traditions.
Analyse the following poem and return a JSON object with these exact keys:
- meter: string (dominant metrical pattern, e.g. "iambic pentameter", "free verse")
- rhyme_scheme: string (e.g. "ABAB", "none", "ghazal radif")
- tone: array of 2-4 strings (e.g. ["elegiac", "devotional"])
- themes: array of 3-5 strings (e.g. ["exile", "memory", "identity"])
- cultural_context: string (one paragraph situating the poem historically/culturally)
- influences: array of up to 3 strings (poet names or movements this echoes)
- summary: string (two sentences for a general reader)

Return ONLY valid JSON, no markdown, no explanation.

Poem title: {title}
Poem:
{body}
"""


@router.post("/{poem_id}")
async def analyse_poem(poem_id: str):
    """Run Gemini analysis on a poem and store the result."""
    poem = await get_poem(poem_id)
    if not poem:
        raise HTTPException(status_code=404, detail="Poem not found")

    prompt = ANALYSIS_PROMPT.format(title=poem["title"], body=poem["body"])
    response = model.generate_content(prompt)

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Gemini returned invalid JSON")

    result = await store_analysis(
        poem_id=poem_id,
        meter=data.get("meter", ""),
        rhyme_scheme=data.get("rhyme_scheme", ""),
        tone=data.get("tone", []),
        themes=data.get("themes", []),
        cultural_context=data.get("cultural_context", ""),
        influences=data.get("influences", []),
        summary=data.get("summary", ""),
        raw_json=data,
    )
    return result


@router.get("/{poem_id}")
async def get_analysis(poem_id: str):
    """Fetch existing analysis for a poem."""
    client = _get_client()
    result = (
        client.table("analysis")
        .select("*")
        .eq("poem_id", poem_id)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Analysis not yet available. POST to /analysis/{poem_id} to generate.")
    return result.data
