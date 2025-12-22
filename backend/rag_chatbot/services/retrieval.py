"""Qdrant vector search service for book content retrieval."""

import logging
from dataclasses import dataclass

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

from ..config import get_settings
from .embeddings import get_embedding_service

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    """A chunk retrieved from the vector store."""

    id: str
    text: str
    chapter_number: int
    chapter_title: str
    section_number: int
    section_title: str
    page_start: int
    page_end: int
    chunk_index: int
    score: float


class RetrievalService:
    """Service for retrieving relevant book chunks from Qdrant."""

    def __init__(self) -> None:
        """Initialize the retrieval service."""
        self.settings = get_settings()
        self._client: QdrantClient | None = None
        self._embedding_service = get_embedding_service()

    @property
    def client(self) -> QdrantClient:
        """Get or create Qdrant client."""
        if self._client is None:
            self._client = QdrantClient(
                url=self.settings.qdrant_url,
                api_key=self.settings.qdrant_api_key if self.settings.qdrant_api_key else None,
            )
        return self._client

    async def search(
        self,
        query: str,
        limit: int | None = None,
        chapter_filter: int | None = None,
    ) -> list[RetrievedChunk]:
        """Search for relevant book chunks.

        Args:
            query: The search query text.
            limit: Maximum number of results. Defaults to settings.max_results.
            chapter_filter: Optional chapter number to filter results.

        Returns:
            List of retrieved chunks above the relevance threshold.
        """
        limit = limit or self.settings.max_results
        threshold = self.settings.relevance_threshold

        # Generate query embedding
        logger.debug(f"Generating embedding for query: {query[:50]}...")
        query_embedding = await self._embedding_service.embed_query(query)

        # Build filter if chapter specified
        search_filter = None
        if chapter_filter is not None:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="chapter_number",
                        match=MatchValue(value=chapter_filter),
                    )
                ]
            )

        # Search Qdrant using query_points (new API in qdrant-client 1.7+)
        logger.debug(f"Searching Qdrant with threshold={threshold}, limit={limit}")
        search_result = self.client.query_points(
            collection_name=self.settings.qdrant_collection_name,
            query=query_embedding,
            limit=limit,
            score_threshold=threshold,
            query_filter=search_filter,
        )
        results = search_result.points

        # Convert to RetrievedChunk objects
        chunks = []
        for result in results:
            payload = result.payload or {}
            chunk = RetrievedChunk(
                id=str(result.id),
                text=payload.get("text", ""),
                chapter_number=payload.get("chapter_number", 0),
                chapter_title=payload.get("chapter_title", ""),
                section_number=payload.get("section_number", 0),
                section_title=payload.get("section_title", ""),
                page_start=payload.get("page_start", 0),
                page_end=payload.get("page_end", 0),
                chunk_index=payload.get("chunk_index", 0),
                score=result.score,
            )
            chunks.append(chunk)

        logger.info(f"Found {len(chunks)} relevant chunks for query")
        return chunks

    async def search_with_threshold_check(
        self,
        query: str,
        limit: int | None = None,
    ) -> tuple[list[RetrievedChunk], bool]:
        """Search with explicit threshold check.

        Args:
            query: The search query text.
            limit: Maximum number of results.

        Returns:
            Tuple of (chunks, has_relevant_results).
            has_relevant_results is True if at least one chunk meets threshold.
        """
        chunks = await self.search(query, limit)
        has_relevant = len(chunks) > 0
        return chunks, has_relevant


# Singleton instance
_retrieval_service: RetrievalService | None = None


def get_retrieval_service() -> RetrievalService:
    """Get the singleton retrieval service instance."""
    global _retrieval_service
    if _retrieval_service is None:
        _retrieval_service = RetrievalService()
    return _retrieval_service
