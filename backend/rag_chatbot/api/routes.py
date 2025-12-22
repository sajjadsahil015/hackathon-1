"""REST API routes for RAG chatbot."""

import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException

from ..agent import get_rag_agent
from ..config import get_settings
from ..models import QueryMode, QueryRequest, QueryResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Query"])

# Track simple stats
_stats = {
    "total_queries": 0,
    "full_book_queries": 0,
    "selected_text_queries": 0,
    "successful_queries": 0,
    "refusals": 0,
    "errors": 0,
    "start_time": datetime.utcnow().isoformat(),
}


@router.post("/query", response_model=QueryResponse)
async def submit_query(request: QueryRequest) -> QueryResponse:
    """Submit a question to the RAG chatbot.

    Accepts a natural language question and returns an answer grounded in book content.

    Two modes available:
    - `full_book`: Searches entire book for relevant passages
    - `selected_text`: Uses only the provided text as context

    Args:
        request: The query request containing question, mode, and optional selected text.

    Returns:
        QueryResponse with answer, citations, and metadata.

    Raises:
        HTTPException: If validation fails or processing error occurs.
    """
    logger.info(f"Received query: {request.question[:50]}... (mode: {request.mode})")

    # Validate selected_text for selected_text mode
    if request.mode == QueryMode.SELECTED_TEXT:
        if not request.selected_text or len(request.selected_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "validation_error",
                    "message": "Selected text must be at least 10 characters",
                    "field": "selected_text",
                },
            )

    try:
        agent = get_rag_agent()
        response = await agent.process_query(
            question=request.question,
            mode=request.mode,
            selected_text=request.selected_text,
        )
        return response

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "validation_error",
                "message": str(e),
            },
        )
    except Exception as e:
        logger.error(f"Processing error: {e}")
        _stats["errors"] += 1
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An error occurred while processing your request.",
            },
        )


@router.get("/stats")
async def get_stats() -> dict:
    """Get service statistics.

    Returns:
        Dictionary with service statistics.
    """
    settings = get_settings()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "stats": _stats,
        "config": {
            "relevance_threshold": settings.relevance_threshold,
            "max_results": settings.max_results,
            "rate_limit_per_minute": settings.rate_limit_per_minute,
        },
    }
