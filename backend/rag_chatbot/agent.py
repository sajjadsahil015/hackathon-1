"""RAG Agent for book Q&A using OpenAI Agents SDK patterns."""

import logging
from dataclasses import dataclass
from typing import Any, AsyncIterator

from .config import get_settings
from .models import Citation, QueryMode, QueryResponse
from .services.citation import get_citation_service
from .services.generation import get_generation_service
from .services.retrieval import RetrievedChunk, get_retrieval_service

logger = logging.getLogger(__name__)


# Agent instructions - strict book-only answering
AGENT_INSTRUCTIONS = """You are a helpful assistant for the Physical AI & Humanoid Robotics book.

CRITICAL RULES:
1. You MUST ONLY answer questions based on the book content.
2. You MUST use the search_book_content tool to find relevant information.
3. You MUST include citations for all information you provide.
4. You MUST NOT make up information or use general knowledge.
5. If no relevant content is found (score below 0.7), you MUST refuse to answer.

RESPONSE FORMAT:
- Provide clear, concise, technical answers
- Always cite chapter, section, and page numbers
- If the question cannot be answered from the book, say so clearly

REFUSAL MESSAGE:
"I could not find information about this topic in the book. Please try rephrasing or ask about a topic covered in the book."
"""


@dataclass
class AgentContext:
    """Context for agent execution."""

    mode: QueryMode
    question: str
    selected_text: str | None = None


class RAGAgent:
    """RAG Agent for answering questions about the book."""

    def __init__(self) -> None:
        """Initialize the RAG agent."""
        self.settings = get_settings()
        self.retrieval_service = get_retrieval_service()
        self.generation_service = get_generation_service()
        self.citation_service = get_citation_service()

    async def process_query(
        self,
        question: str,
        mode: QueryMode = QueryMode.FULL_BOOK,
        selected_text: str | None = None,
    ) -> QueryResponse:
        """Process a user query and generate a response.

        Args:
            question: The user's question.
            mode: Query mode (full_book or selected_text).
            selected_text: Optional selected text for selected_text mode.

        Returns:
            QueryResponse with answer and citations.
        """
        import time
        start_time = time.time()

        if mode == QueryMode.SELECTED_TEXT and selected_text:
            return await self._process_selected_text_query(
                question, selected_text, start_time
            )
        else:
            return await self._process_full_book_query(question, start_time)

    async def _process_full_book_query(
        self,
        question: str,
        start_time: float,
    ) -> QueryResponse:
        """Process a full-book context query."""
        import time

        # Search for relevant chunks
        chunks, has_relevant = await self.retrieval_service.search_with_threshold_check(
            question
        )

        if not has_relevant:
            # Return refusal response
            return QueryResponse(
                answer=(
                    "I could not find information about this topic in the book. "
                    "Please try rephrasing or ask about a topic covered in the book."
                ),
                citations=[],
                mode=QueryMode.FULL_BOOK,
                found_in_book=False,
                confidence=0.0,
                processing_time_ms=int((time.time() - start_time) * 1000),
            )

        # Generate response
        answer = await self.generation_service.generate_response(question, chunks)

        # Extract citations
        citations = self.citation_service.extract_citations(chunks)
        citations = self.citation_service.deduplicate_citations(citations)
        confidence = self.citation_service.calculate_overall_confidence(citations)

        return QueryResponse(
            answer=answer,
            citations=citations,
            mode=QueryMode.FULL_BOOK,
            found_in_book=True,
            confidence=confidence,
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    async def _process_selected_text_query(
        self,
        question: str,
        selected_text: str,
        start_time: float,
    ) -> QueryResponse:
        """Process a selected-text context query."""
        import time

        # Generate response using only the selected text
        answer = await self.generation_service.generate_from_selected_text(
            question, selected_text
        )

        return QueryResponse(
            answer=answer,
            citations=[],  # No citations for selected-text mode
            mode=QueryMode.SELECTED_TEXT,
            found_in_book=True,  # Selected text is from the book
            confidence=1.0,  # Full confidence since user provided context
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    async def stream_response(
        self,
        question: str,
        mode: QueryMode = QueryMode.FULL_BOOK,
        selected_text: str | None = None,
    ) -> AsyncIterator[dict[str, Any]]:
        """Stream response events for ChatKit integration.

        Args:
            question: The user's question.
            mode: Query mode.
            selected_text: Optional selected text.

        Yields:
            Dictionary events for streaming response.
        """
        import time
        start_time = time.time()

        # Search phase
        if mode == QueryMode.FULL_BOOK:
            yield {"type": "status", "message": "Searching book content..."}

            chunks, has_relevant = await self.retrieval_service.search_with_threshold_check(
                question
            )

            if not has_relevant:
                yield {
                    "type": "text",
                    "content": (
                        "I could not find information about this topic in the book. "
                        "Please try rephrasing or ask about a topic covered in the book."
                    ),
                }
                yield {
                    "type": "complete",
                    "found_in_book": False,
                    "confidence": 0.0,
                    "processing_time_ms": int((time.time() - start_time) * 1000),
                }
                return

            # Generate response
            yield {"type": "status", "message": "Generating response..."}
            answer = await self.generation_service.generate_response(question, chunks)

            # Extract citations
            citations = self.citation_service.extract_citations(chunks)
            citations = self.citation_service.deduplicate_citations(citations)
            confidence = self.citation_service.calculate_overall_confidence(citations)

            yield {"type": "text", "content": answer}
            yield {
                "type": "citations",
                "citations": [c.model_dump() for c in citations],
            }
            yield {
                "type": "complete",
                "found_in_book": True,
                "confidence": confidence,
                "processing_time_ms": int((time.time() - start_time) * 1000),
            }

        else:
            # Selected text mode
            yield {"type": "status", "message": "Analyzing selected text..."}
            answer = await self.generation_service.generate_from_selected_text(
                question, selected_text or ""
            )

            yield {"type": "text", "content": answer}
            yield {
                "type": "complete",
                "found_in_book": True,
                "confidence": 1.0,
                "processing_time_ms": int((time.time() - start_time) * 1000),
            }


# Singleton instance
_rag_agent: RAGAgent | None = None


def get_rag_agent() -> RAGAgent:
    """Get the singleton RAG agent instance."""
    global _rag_agent
    if _rag_agent is None:
        _rag_agent = RAGAgent()
    return _rag_agent
