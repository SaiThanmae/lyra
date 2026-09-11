"""
BigQuery tool functions — embedding storage and cosine similarity search.
"""

from __future__ import annotations

from google.cloud import bigquery
from config import settings

_bq: bigquery.Client | None = None


def _get_client() -> bigquery.Client:
    global _bq
    if _bq is None:
        _bq = bigquery.Client(project=settings.google_cloud_project)
    return _bq


def _table(name: str) -> str:
    return f"`{settings.google_cloud_project}.{settings.bigquery_dataset}.{name}`"


async def store_embedding(poem_id: str, embedding: list[float]) -> bool:
    """
    Insert or replace a poem's embedding vector in BigQuery.
    Table: lyra_corpus.embeddings  (poem_id STRING, embedding ARRAY<FLOAT64>)
    """
    client = _get_client()
    rows = [{"poem_id": poem_id, "embedding": embedding}]
    errors = client.insert_rows_json(_table("embeddings"), rows)
    return len(errors) == 0


async def query_similar(
    query_embedding: list[float],
    top_k: int = 10,
    exclude_poem_id: str | None = None,
) -> list[dict]:
    """
    Find the top-k most similar poems using cosine similarity in BigQuery.

    Returns a list of {poem_id, similarity_score} dicts ordered by score desc.
    """
    client = _get_client()

    # BigQuery doesn't have a native cosine fn, so we compute it inline.
    # ML.DISTANCE is available in BQ ML — use it when the dataset is large.
    vector_str = ", ".join(str(v) for v in query_embedding)
    exclude_clause = f"AND poem_id != '{exclude_poem_id}'" if exclude_poem_id else ""

    sql = f"""
    WITH query AS (
      SELECT [{vector_str}] AS qvec
    ),
    dots AS (
      SELECT
        e.poem_id,
        (
          SELECT SUM(q * d)
          FROM UNNEST(query.qvec) AS q WITH OFFSET i
          JOIN UNNEST(e.embedding) AS d WITH OFFSET j ON i = j
        ) AS dot_product,
        SQRT((SELECT SUM(v * v) FROM UNNEST(e.embedding) AS v)) AS norm_e,
        SQRT((SELECT SUM(v * v) FROM UNNEST(query.qvec) AS v)) AS norm_q
      FROM {_table("embeddings")} AS e, query
      {exclude_clause}
    )
    SELECT
      poem_id,
      SAFE_DIVIDE(dot_product, norm_e * norm_q) AS similarity_score
    FROM dots
    ORDER BY similarity_score DESC
    LIMIT {top_k}
    """

    job = client.query(sql)
    rows = job.result()
    return [{"poem_id": row.poem_id, "similarity_score": row.similarity_score} for row in rows]
