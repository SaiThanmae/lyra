-- ============================================================
-- Lyra — BigQuery Dataset Setup
-- Run via bq CLI or Google Cloud Console
-- ============================================================

-- Create dataset
-- bq mk --dataset --location=US $GOOGLE_CLOUD_PROJECT:lyra_corpus

-- ─── Embeddings table ─────────────────────────────────────────
-- Stores 768-dimensional Vertex AI text-embedding-004 vectors.
-- poem_id is a string FK matching Supabase poems.id (UUID as STRING).

CREATE TABLE IF NOT EXISTS `lyra_corpus.embeddings` (
    poem_id   STRING NOT NULL,
    embedding ARRAY<FLOAT64>,               -- 768 dims
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
OPTIONS (
    description = 'Semantic embeddings for Lyra corpus poems (text-embedding-004, 768-dim)'
);

-- ─── Thematic Clusters (populated by BigQuery ML) ─────────────
CREATE TABLE IF NOT EXISTS `lyra_corpus.thematic_clusters` (
    centroid_id       INT64,
    poem_id           STRING,
    cluster_label     STRING,
    distance_to_centroid FLOAT64
);

-- ─── Corpus Stats View ────────────────────────────────────────
-- Used by Looker Studio for analytics dashboard
CREATE OR REPLACE VIEW `lyra_corpus.corpus_stats` AS
SELECT
    COUNT(DISTINCT poem_id) AS total_poems,
    TIMESTAMP_TRUNC(MAX(created_at), DAY) AS last_updated
FROM `lyra_corpus.embeddings`;
