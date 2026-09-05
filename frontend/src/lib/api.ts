// Lyra API client — wraps all backend calls

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

// ── Poems ─────────────────────────────────────────────────────
export const getPoems = (limit = 20, offset = 0) =>
  api<{ poems: Poem[] }>(`/poems?limit=${limit}&offset=${offset}`);

export const getPoem = (id: string) =>
  api<Poem>(`/poems/${id}`);

// ── Ingest ────────────────────────────────────────────────────
export const ingestPoem = (body: IngestRequest) =>
  api<{ poem_id: string; status: string }>("/ingest/", {
    method: "POST",
    body: JSON.stringify(body),
  });

// ── Analysis ──────────────────────────────────────────────────
export const getAnalysis = (poemId: string) =>
  api<PoemAnalysis>(`/analysis/${poemId}`);

// ── Discovery ─────────────────────────────────────────────────
export const findSimilar = (poemId: string, topK = 6) =>
  api<{ results: DiscoveryResult[] }>(`/discovery/similar/${poemId}?top_k=${topK}`);

export const semanticSearch = (q: string, topK = 6) =>
  api<{ query: string; results: DiscoveryResult[] }>(
    `/discovery/search?q=${encodeURIComponent(q)}&top_k=${topK}`
  );

// ── Lineage ───────────────────────────────────────────────────
export const getLineage = (poemId: string) =>
  api<LineageResult>(`/lineage/${poemId}`);

// ── Types ─────────────────────────────────────────────────────
export interface Poet {
  id: string;
  name: string;
  birth_year?: number;
  death_year?: number;
  nationality?: string;
  traditions: string[];
  bio?: string;
}

export interface Poem {
  id: string;
  title: string;
  body: string;
  poet_id: string;
  year?: number;
  language: string;
  form?: string;
  tags: string[];
  poets?: Poet;
}

export interface PoemAnalysis {
  poem_id: string;
  meter?: string;
  rhyme_scheme?: string;
  tone: string[];
  themes: string[];
  cultural_context?: string;
  influences: string[];
  summary?: string;
}

export interface DiscoveryResult extends Poem {
  similarity_score: number;
}

export interface LineageResult {
  poem_id: string;
  influences_others: LineageEdge[];
  influenced_by: LineageEdge[];
}

export interface LineageEdge {
  id: string;
  source_poem_id: string;
  influenced_poem_id: string;
  confidence_score: number;
  rationale?: string;
}

export interface IngestRequest {
  title: string;
  body: string;
  poet_name: string;
  year?: number;
  language?: string;
  form?: string;
  tags?: string[];
}
