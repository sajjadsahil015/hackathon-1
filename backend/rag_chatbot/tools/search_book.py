"""Agent tool for searching book content."""

import logging
from typing import Any

from ..services.retrieval import get_retrieval_service

logger = logging.getLogger(__name__)


async def search_book_content(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search the book for relevant content.

    This tool searches the Physical AI & Humanoid Robotics book
    for passages that are relevant to the query.

    Args:
        query: The search query to find relevant book content.
        limit: Maximum number of results to return (default: 5).

    Returns:
        List of relevant passages with metadata including:
        - text: The passage content
        - chapter_number: Chapter number
        - chapter_title: Chapter title
        - section_number: Section number
        - section_title: Section title
        - page_start: Starting page
        - page_end: Ending page
        - score: Relevance score (0-1)
    """
    logger.info(f"Searching book for: {query[:50]}...")

    retrieval_service = get_retrieval_service()
    chunks = await retrieval_service.search(query, limit=limit)

    results = []
    for chunk in chunks:
        results.append({
            "text": chunk.text,
            "chapter_number": chunk.chapter_number,
            "chapter_title": chunk.chapter_title,
            "section_number": chunk.section_number,
            "section_title": chunk.section_title,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "score": round(chunk.score, 3),
        })

    logger.info(f"Found {len(results)} relevant passages")
    return results


# Tool definition for agent frameworks
SEARCH_BOOK_TOOL = {
    "name": "search_book_content",
    "description": (
        "Search the Physical AI & Humanoid Robotics book for content relevant to a query. "
        "Use this to find information from the book to answer questions. "
        "Returns passages with chapter, section, and page references."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find relevant book content",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    "function": search_book_content,
}
