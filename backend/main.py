"""
Lyra — FastAPI backend entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import poems, analysis, discovery, ingest

app = FastAPI(
    title="Lyra API",
    description="AI-Driven Poetry Preservation and Analysis Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(poems.router, prefix="/poems", tags=["poems"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(discovery.router, prefix="/discovery", tags=["discovery"])
app.include_router(ingest.router, prefix="/ingest", tags=["ingest"])


@app.get("/health")
async def health():
    return {"status": "ok", "service": "lyra-api"}
