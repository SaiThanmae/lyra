# 🎭 Lyra
### An AI-Driven Ecosystem for Culturally Sustainable Poetry Preservation and Analysis

> *Patchamomma 2026 — Build Phase Submission*
> Built by: Sai Thanmae

---

## 🎯 Problem Statement

Independent poetry and literary arts are disappearing into fragmented, inaccessible archives. Unlike mainstream literature, poetic works — especially from underrepresented cultures and oral traditions — lack:

- **Structured, searchable digital archives** with meaningful metadata
- **AI-powered analytical tools** that can evaluate cadence, form, thematic lineage, and cultural influence without reducing art to data
- **Community-driven preservation pipelines** that allow poets and scholars to contribute and grow the corpus
- **Semantic discovery** — the ability to find poems by mood, influence, era, or stylistic similarity, not just keyword

**Lyra** solves this by combining a richly structured relational database with Google Cloud's AI stack to make the world's poetic heritage discoverable, analyzable, and culturally sustainable.

---

## 🏗️ Architecture

```
[Input Sources]
  Poet submissions (web UI / API)
  Public domain corpora (Project Gutenberg, PoetryFoundation CC)
  Oral tradition transcripts (uploaded audio → Cloud Speech-to-Text)
        │
        ▼
[Ingestion & Storage]
  Cloud Storage          — raw manuscripts, audio files, images
  Supabase (PostgreSQL)  — structured poem/author/lineage/metadata
  BigQuery               — analytical corpus (embeddings, analysis results)
        │
        ▼
[Intelligence Layer — Vertex AI + ADK]
  ┌─────────────────────────────────────────────────────┐
  │  Orchestrator Agent (ADK)                           │
  │  ├─ IngestAgent       — parse, validate, store      │
  │  ├─ AnalysisAgent     — cadence, form, themes       │
  │  ├─ EmbeddingAgent    — generate & store vectors    │
  │  ├─ LineageAgent      — detect influence & lineage  │
  │  └─ DiscoveryAgent    — semantic search & recs      │
  └─────────────────────────────────────────────────────┘
  LLM:       Gemini 1.5 Pro (Vertex AI)
  Embeddings: text-embedding-004 (Vertex AI)
  DB Tool:   MCP Toolbox for Databases → BigQuery + Supabase
        │
        ▼
[Application Layer]
  FastAPI backend  — Cloud Run (serverless)
  Next.js frontend — Firebase Hosting
  Firestore        — session state, user reading lists, agent memory
  Firebase Auth    — poet/scholar/reader roles
        │
        ▼
[Analytics & Reporting]
  Looker Studio — corpus growth, form distribution, cultural coverage
  BigQuery ML   — thematic clustering across eras
```

---

## 🤖 Multi-Agent Design (Google ADK)

| Agent | Tools Used | Responsibility |
|---|---|---|
| **Orchestrator** | All sub-agents | Routes user intent, aggregates results, manages state |
| **IngestAgent** | Supabase Tool, Storage Tool | Parses submitted poems, validates metadata, persists to DB |
| **AnalysisAgent** | Vertex AI (Gemini) | Evaluates meter, rhyme scheme, form, tone, cultural context |
| **EmbeddingAgent** | Vertex AI text-embedding-004, BigQuery | Generates semantic vector embeddings, stores in BQ |
| **LineageAgent** | BigQuery Tool, Gemini | Detects stylistic ancestors, maps influence networks |
| **DiscoveryAgent** | BigQuery vector search | Finds semantically similar poems, generates reading recommendations |

---

## 📊 Data Model (Supabase / PostgreSQL)

```sql
poets         (id, name, birth_year, death_year, nationality, traditions[], bio)
poems         (id, title, body, poet_id, year, language, form, collection_id)
collections   (id, title, poet_id, year, publisher)
analysis      (id, poem_id, meter, rhyme_scheme, tone[], themes[], influences[], raw_json)
lineages      (id, source_poem_id, influenced_poem_id, confidence_score, rationale)
embeddings    (poem_id, embedding VECTOR(768))  -- BigQuery
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Relational DB | Supabase (PostgreSQL) |
| Analytical DB | BigQuery |
| Vector Search | BigQuery + Vertex AI Embeddings (text-embedding-004) |
| LLM / Analysis | Gemini 1.5 Pro via Vertex AI |
| Agent Framework | Google ADK (Agent Development Kit) |
| DB Orchestration | MCP Toolbox for Databases |
| Speech-to-Text | Google Cloud Speech-to-Text API |
| Backend | FastAPI on Cloud Run |
| Frontend | Next.js on Firebase Hosting |
| Auth | Firebase Auth |
| Session/Memory | Firestore |
| File Storage | Cloud Storage |
| Analytics | Looker Studio + BigQuery ML |

---

## 📅 Build Timeline

| Milestone | Date | Status |
|---|---|---|
| Project scaffold + data schema | Aug 15 | ✅ |
| Supabase schema + synthetic corpus | Aug 17 | 🔲 |
| ADK agents: Ingest + Analysis | Aug 20 | 🔲 First Checkpoint |
| Vertex AI embeddings + BQ vector search | Aug 23 | 🔲 |
| Next.js frontend: poem reader + analysis view | Aug 26 | 🔲 |
| Lineage graph + discovery recommendations | Aug 28 | 🔲 Second Checkpoint |
| End-to-end integration, auth, Cloud Run deploy | Sep 3 | 🔲 |
| Final polish + demo video | Sep 5 | 🔲 Final Checkpoint |
| Lock submission | Sep 7 | 🔲 |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone <repo-url>
cd lyra

# 2. Backend setup
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
uvicorn main:app --reload

# 3. Frontend setup
cd ../frontend
npm install
cp .env.local.example .env.local   # fill in Firebase config
npm run dev
```

### Required environment variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_API_KEY=your-ai-studio-api-key          # Gemini
VERTEX_AI_LOCATION=us-central1

# Supabase
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key

# Firebase
FIREBASE_PROJECT_ID=your-firebase-project
```

---

## 👤 Team
- **Sai Thanmae** — Lead Engineer

---

*Built for Patchamomma 2026 | Google Cloud · Vertex AI · ADK · Supabase · Next.js*
