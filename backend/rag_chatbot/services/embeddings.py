"""Cohere embedding service for text vectorization."""

import logging
from typing import Sequence

import cohere

from ..config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Cohere."""

    def __init__(self) -> None:
        """Initialize the embedding service."""
        self.settings = get_settings()
        self.model = self.settings.embedding_model
        self._client: cohere.Client | None = None

    @property
    def client(self) -> cohere.Client:
        """Get or create Cohere client."""
        if self._client is None:
            if not self.settings.cohere_api_key:
                raise RuntimeError(
                    "COHERE_API_KEY not configured. Please set it in your .env file."
                )
            self._client = cohere.Client(api_key=self.settings.cohere_api_key)
        return self._client

    def _generate_embedding(
        self, texts: list[str], input_type: str = "search_document"
    ) -> list[list[float]]:
        """Call Cohere API to generate embeddings.

        Args:
            texts: The texts to embed.
            input_type: Either "search_document" for indexing or "search_query" for queries.

        Returns:
            List of embedding vectors.
        """
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=input_type,
            embedding_types=["float"],
        )
        return response.embeddings.float

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text (for document indexing).

        Args:
            text: The text to embed.

        Returns:
            List of floats representing the embedding vector.

        Raises:
            ValueError: If text is empty.
            RuntimeError: If embedding generation fails.
        """
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")

        try:
            embeddings = self._generate_embedding([text], input_type="search_document")
            return embeddings[0]
        except cohere.CohereError as e:
            logger.error(f"Cohere API error: {e}")
            raise RuntimeError(f"Embedding generation failed: {e}") from e
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise RuntimeError(f"Embedding generation failed: {e}") from e

    async def embed_query(self, query: str) -> list[float]:
        """Generate embedding for a search query.

        Args:
            query: The search query to embed.

        Returns:
            List of floats representing the embedding vector.
        """
        if not query or not query.strip():
            raise ValueError("Cannot embed empty query")

        try:
            # Use "search_query" input type for queries
            embeddings = self._generate_embedding([query], input_type="search_query")
            return embeddings[0]
        except cohere.CohereError as e:
            logger.error(f"Cohere API error: {e}")
            raise RuntimeError(f"Query embedding generation failed: {e}") from e
        except Exception as e:
            logger.error(f"Failed to generate query embedding: {e}")
            raise RuntimeError(f"Query embedding generation failed: {e}") from e

    async def embed_batch(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: Sequence of texts to embed.

        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []

        # Filter out empty texts
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            raise ValueError("All texts are empty")

        try:
            # Cohere supports batch embedding up to 96 texts per request
            batch_size = 96
            all_embeddings = []

            for i in range(0, len(valid_texts), batch_size):
                batch = list(valid_texts[i : i + batch_size])
                embeddings = self._generate_embedding(batch, input_type="search_document")
                all_embeddings.extend(embeddings)

            return all_embeddings
        except cohere.CohereError as e:
            logger.error(f"Cohere API error during batch embedding: {e}")
            raise RuntimeError(f"Batch embedding generation failed: {e}") from e
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise RuntimeError(f"Batch embedding generation failed: {e}") from e


# Singleton instance
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """Get the singleton embedding service instance."""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service
