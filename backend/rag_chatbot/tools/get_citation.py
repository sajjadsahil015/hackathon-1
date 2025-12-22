"""Agent tool for getting citation information."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def get_citation(
    chapter_number: int,
    chapter_title: str,
    section_number: int | None = None,
    section_title: str | None = None,
    page_start: int = 1,
    page_end: int = 1,
    relevance_score: float = 1.0,
) -> dict[str, Any]:
    """Format a citation for a book reference.

    This tool creates a properly formatted citation for referencing
    content from the Physical AI & Humanoid Robotics book.

    Args:
        chapter_number: The chapter number (1-based).
        chapter_title: The title of the chapter.
        section_number: Optional section number within the chapter.
        section_title: Optional section title.
        page_start: Starting page number.
        page_end: Ending page number.
        relevance_score: Relevance score for the citation (0-1).

    Returns:
        Dictionary containing the formatted citation with:
        - formatted: Human-readable citation string
        - chapter_number, chapter_title, section_number, section_title
        - page_start, page_end, relevance_score
    """
    logger.debug(f"Creating citation for Chapter {chapter_number}: {chapter_title}")

    # Build formatted reference
    parts = [f"Chapter {chapter_number}: {chapter_title}"]
    if section_number and section_title:
        parts.append(f"Section {section_number}: {section_title}")
    parts.append(f"(pp. {page_start}-{page_end})")
    formatted = ", ".join(parts)

    return {
        "formatted": formatted,
        "chapter_number": chapter_number,
        "chapter_title": chapter_title,
        "section_number": section_number,
        "section_title": section_title,
        "page_start": page_start,
        "page_end": page_end,
        "relevance_score": round(relevance_score, 3),
    }


# Tool definition for agent frameworks
GET_CITATION_TOOL = {
    "name": "get_citation",
    "description": (
        "Create a formatted citation for referencing content from the book. "
        "Use this after finding relevant content to provide proper source attribution."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "chapter_number": {
                "type": "integer",
                "description": "The chapter number (1-based)",
            },
            "chapter_title": {
                "type": "string",
                "description": "The title of the chapter",
            },
            "section_number": {
                "type": "integer",
                "description": "Optional section number within the chapter",
            },
            "section_title": {
                "type": "string",
                "description": "Optional section title",
            },
            "page_start": {
                "type": "integer",
                "description": "Starting page number",
                "default": 1,
            },
            "page_end": {
                "type": "integer",
                "description": "Ending page number",
                "default": 1,
            },
            "relevance_score": {
                "type": "number",
                "description": "Relevance score for the citation (0-1)",
                "default": 1.0,
            },
        },
        "required": ["chapter_number", "chapter_title"],
    },
    "function": get_citation,
}
