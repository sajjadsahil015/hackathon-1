"""Citation extraction service."""

import logging
from typing import Sequence

from ..models.citation import Citation
from .retrieval import RetrievedChunk

logger = logging.getLogger(__name__)


class CitationService:
    """Service for extracting and formatting citations from retrieved chunks."""

    def extract_citations(self, chunks: Sequence[RetrievedChunk]) -> list[Citation]:
        """Extract citations from retrieved chunks.

        Args:
            chunks: Sequence of retrieved book chunks.

        Returns:
            List of Citation objects.
        """
        citations = []
        for chunk in chunks:
            citation = Citation(
                chapter_number=chunk.chapter_number,
                chapter_title=chunk.chapter_title,
                section_number=chunk.section_number if chunk.section_number else None,
                section_title=chunk.section_title if chunk.section_title else None,
                page_start=chunk.page_start,
                page_end=chunk.page_end,
                relevance_score=round(chunk.score, 3),
            )
            citations.append(citation)

        return citations

    def deduplicate_citations(self, citations: list[Citation]) -> list[Citation]:
        """Remove duplicate citations based on chapter/section.

        Args:
            citations: List of citations to deduplicate.

        Returns:
            Deduplicated list of citations.
        """
        seen = set()
        unique = []

        for citation in citations:
            key = (
                citation.chapter_number,
                citation.section_number,
            )
            if key not in seen:
                seen.add(key)
                unique.append(citation)

        return unique

    def format_citations_text(self, citations: list[Citation]) -> str:
        """Format citations as a readable text block.

        Args:
            citations: List of citations to format.

        Returns:
            Formatted citation text.
        """
        if not citations:
            return ""

        lines = ["Sources:"]
        for i, citation in enumerate(citations, 1):
            lines.append(f"{i}. {citation.format_reference()}")

        return "\n".join(lines)

    def calculate_overall_confidence(self, citations: list[Citation]) -> float:
        """Calculate overall confidence score from citations.

        Uses the maximum relevance score as the confidence.

        Args:
            citations: List of citations.

        Returns:
            Overall confidence score (0.0 to 1.0).
        """
        if not citations:
            return 0.0
        return max(c.relevance_score for c in citations)


# Singleton instance
_citation_service: CitationService | None = None


def get_citation_service() -> CitationService:
    """Get the singleton citation service instance."""
    global _citation_service
    if _citation_service is None:
        _citation_service = CitationService()
    return _citation_service
