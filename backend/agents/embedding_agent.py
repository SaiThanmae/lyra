"""
EmbeddingAgent — generates Vertex AI text embeddings and stores them in BigQuery.
Uses text-embedding-004 (768-dim) for semantic similarity across the corpus.
"""

from google.adk.agents import LlmAgent
from tools.vertex_tool import generate_embedding
from tools.bigquery_tool import store_embedding, query_similar

INSTRUCTION = """
You are the EmbeddingAgent for Lyra. Given a poem_id:
1. Fetch the poem text from Supabase.
2. Generate a 768-dimensional semantic embedding using Vertex AI
   text-embedding-004.
3. Store the embedding in BigQuery (lyra_corpus.embeddings table).
4. Return the embedding vector and confirm storage success.

If asked to find similar poems, use query_similar to run a cosine
similarity search in BigQuery and return the top-k results.
"""

embedding_agent = LlmAgent(
    name="embedding_agent",
    model="gemini-1.5-flash",
    instruction=INSTRUCTION,
    tools=[generate_embedding, store_embedding, query_similar],
)
