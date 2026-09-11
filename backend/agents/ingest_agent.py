"""
IngestAgent — validates and persists an incoming poem to Supabase.
"""

from google.adk.agents import LlmAgent
from tools.supabase_tool import upsert_poet, upsert_poem

INSTRUCTION = """
You are the IngestAgent for Lyra. Given a poem submission (title, body,
poet name, year, language, form), you:
1. Look up or create the poet record in Supabase.
2. Store the poem with its full metadata.
3. Return the assigned poem_id for downstream agents.

Validate that the body is non-empty and the title is present before persisting.
"""

ingest_agent = LlmAgent(
    name="ingest_agent",
    model="gemini-1.5-flash",
    instruction=INSTRUCTION,
    tools=[upsert_poet, upsert_poem],
)
