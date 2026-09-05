"""Analysis router — fetch or trigger poem analysis."""

from fastapi import APIRouter, HTTPException
from backend.tools.supabase_tool import _get_client

router = APIRouter()


@router.get("/{poem_id}")
async def get_analysis(poem_id: str):
    client = _get_client()
    result = (
        client.table("analysis")
        .select("*")
        .eq("poem_id", poem_id)
        .single()
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Analysis not yet available for this poem.")
    return result.data
