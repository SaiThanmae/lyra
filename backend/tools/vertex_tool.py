"""
Vertex AI tool functions — embedding generation via text-embedding-004.
"""

from __future__ import annotations

import vertexai
from vertexai.language_models import TextEmbeddingModel
from config import settings

_model: TextEmbeddingModel | None = None


def _get_model() -> TextEmbeddingModel:
    global _model
    if _model is None:
        vertexai.init(
            project=settings.google_cloud_project,
            location=settings.vertex_ai_location,
        )
        _model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return _model


async def generate_embedding(text: str) -> list[float]:
    """
    Generate a 768-dimensional embedding for the given text
    using Vertex AI text-embedding-004.
    """
    model = _get_model()
    result = model.get_embeddings([text])
    return result[0].values
