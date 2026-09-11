"""
LineageAgent — maps stylistic ancestry and influence networks between poems.
Uses both embedding similarity (BigQuery) and Gemini reasoning.
"""

from google.adk.agents import LlmAgent
from tools.bigquery_tool import query_similar
from tools.supabase_tool import get_poem, store_lineage

INSTRUCTION = """
You are the LineageAgent for Lyra. Your task is to trace the cultural and
stylistic lineage of poems — who influenced whom, and how.

Given a poem_id:
1. Retrieve its analysis (themes, meter, cultural context, listed influences).
2. Use query_similar to find the top 10 semantically similar poems in BigQuery.
3. For each candidate, use your literary knowledge and the poem texts to judge:
   - Is the similarity coincidental or substantive?
   - Which specific elements (imagery, form, diction, theme) are shared?
4. For meaningful connections, create a lineage record with:
   - confidence_score (0.0–1.0)
   - rationale (1–2 sentences citing specific textual evidence)
5. Store confirmed lineages via store_lineage.
6. Return a lineage map: a list of (source → influenced) pairs with rationales.

Be rigorous. A high confidence_score requires specific textual evidence,
not just thematic proximity.
"""

lineage_agent = LlmAgent(
    name="lineage_agent",
    model="gemini-1.5-pro",
    instruction=INSTRUCTION,
    tools=[query_similar, get_poem, store_lineage],
)
