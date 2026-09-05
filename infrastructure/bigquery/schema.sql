-- ============================================================
-- Lyra — Supabase (PostgreSQL) Schema
-- Run in the Supabase SQL editor or via psql
-- ============================================================

-- Enable pgvector extension (for local/future use; BigQuery handles
-- large-scale vector search for the corpus)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- ─── Poets ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS poets (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        TEXT NOT NULL UNIQUE,
    birth_year  INT,
    death_year  INT,
    nationality TEXT,
    traditions  TEXT[]  DEFAULT '{}',
    bio         TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Collections ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS collections (
    id         UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title      TEXT NOT NULL,
    poet_id    UUID REFERENCES poets(id) ON DELETE CASCADE,
    year       INT,
    publisher  TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Poems ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS poems (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title         TEXT NOT NULL,
    body          TEXT NOT NULL,
    poet_id       UUID REFERENCES poets(id) ON DELETE SET NULL,
    year          INT,
    language      TEXT NOT NULL DEFAULT 'en',
    form          TEXT,                          -- sonnet, haiku, ghazal, free verse …
    collection_id UUID REFERENCES collections(id) ON DELETE SET NULL,
    tags          TEXT[] DEFAULT '{}',
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS poems_poet_idx ON poems(poet_id);
CREATE INDEX IF NOT EXISTS poems_form_idx ON poems(form);
CREATE INDEX IF NOT EXISTS poems_language_idx ON poems(language);

-- ─── Analysis ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS analysis (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    poem_id          UUID UNIQUE REFERENCES poems(id) ON DELETE CASCADE,
    meter            TEXT,
    rhyme_scheme     TEXT,
    tone             TEXT[] DEFAULT '{}',
    themes           TEXT[] DEFAULT '{}',
    cultural_context TEXT,
    influences       TEXT[] DEFAULT '{}',
    summary          TEXT,
    raw_json         JSONB,
    analysed_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Lineages ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lineages (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_poem_id      UUID REFERENCES poems(id) ON DELETE CASCADE,
    influenced_poem_id  UUID REFERENCES poems(id) ON DELETE CASCADE,
    confidence_score    NUMERIC(4,3) CHECK (confidence_score BETWEEN 0 AND 1),
    rationale           TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (source_poem_id, influenced_poem_id)
);

-- ─── Row Level Security ────────────────────────────────────────
-- Public read, authenticated write
ALTER TABLE poets      ENABLE ROW LEVEL SECURITY;
ALTER TABLE poems      ENABLE ROW LEVEL SECURITY;
ALTER TABLE collections ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis   ENABLE ROW LEVEL SECURITY;
ALTER TABLE lineages   ENABLE ROW LEVEL SECURITY;

CREATE POLICY "public_read_poets"   ON poets      FOR SELECT USING (true);
CREATE POLICY "public_read_poems"   ON poems      FOR SELECT USING (true);
CREATE POLICY "public_read_analysis" ON analysis  FOR SELECT USING (true);
CREATE POLICY "public_read_lineages" ON lineages  FOR SELECT USING (true);

-- Authenticated users (poets, scholars) can insert/update
CREATE POLICY "auth_write_poems" ON poems
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
CREATE POLICY "auth_write_poets" ON poets
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');
