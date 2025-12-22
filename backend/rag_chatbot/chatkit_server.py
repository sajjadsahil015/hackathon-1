"""ChatKit server implementation for RAG chatbot.

This module implements a ChatKit-compatible server for streaming
responses to client applications.
"""

import json
import logging
from typing import Any, AsyncIterator

from .agent import get_rag_agent
from .models import QueryMode

logger = logging.getLogger(__name__)


class RAGChatKitServer:
    """ChatKit server for RAG chatbot.

    Implements the ChatKit protocol for streaming responses.
    """

    def __init__(self) -> None:
        """Initialize the ChatKit server."""
        self.agent = get_rag_agent()

    async def respond(
        self,
        thread_id: str,
        message: str,
        mode: str = "full_book",
        selected_text: str | None = None,
        context: Any = None,
    ) -> AsyncIterator[bytes]:
        """Stream response events for a message.

        Implements the ChatKit respond pattern, yielding Server-Sent Events
        for real-time streaming to clients.

        Args:
            thread_id: Unique identifier for the conversation thread.
            message: The user's message/question.
            mode: Query mode ("full_book" or "selected_text").
            selected_text: Optional selected text for selected_text mode.
            context: Optional request context.

        Yields:
            Bytes representing SSE data events.
        """
        logger.info(f"Processing request for thread {thread_id}: {message[:50]}...")

        query_mode = QueryMode.SELECTED_TEXT if mode == "selected_text" else QueryMode.FULL_BOOK

        try:
            async for event in self.agent.stream_response(
                question=message,
                mode=query_mode,
                selected_text=selected_text,
            ):
                # Format as SSE
                event_data = json.dumps(event)
                yield f"data: {event_data}\n\n".encode("utf-8")

        except Exception as e:
            logger.error(f"Error processing request: {e}")
            error_event = {
                "type": "error",
                "message": "An error occurred while processing your request.",
                "details": str(e),
            }
            yield f"data: {json.dumps(error_event)}\n\n".encode("utf-8")

    async def process(
        self,
        request_body: bytes,
        context: Any = None,
    ) -> AsyncIterator[bytes] | dict[str, Any]:
        """Process a ChatKit request.

        Parses the incoming request and routes to appropriate handler.

        Args:
            request_body: Raw request body bytes.
            context: Optional request context.

        Returns:
            Either an async iterator for streaming or a dict for JSON response.
        """
        try:
            request = json.loads(request_body)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request: {e}")
            return {"error": "invalid_json", "message": str(e)}

        request_type = request.get("type", "stream")

        if request_type == "stream":
            # Streaming request
            thread = request.get("thread", {})
            thread_id = thread.get("id", "default")
            input_data = request.get("input", {})
            message = input_data.get("content", "")
            mode = request.get("mode", "full_book")
            selected_text = request.get("selected_text")

            return self.respond(
                thread_id=thread_id,
                message=message,
                mode=mode,
                selected_text=selected_text,
                context=context,
            )

        elif request_type == "query":
            # Non-streaming query request
            message = request.get("question", "")
            mode = request.get("mode", "full_book")
            selected_text = request.get("selected_text")

            query_mode = (
                QueryMode.SELECTED_TEXT if mode == "selected_text" else QueryMode.FULL_BOOK
            )

            response = await self.agent.process_query(
                question=message,
                mode=query_mode,
                selected_text=selected_text,
            )

            return response.model_dump()

        else:
            return {"error": "unknown_request_type", "message": f"Unknown type: {request_type}"}


# Singleton instance
_chatkit_server: RAGChatKitServer | None = None


def get_chatkit_server() -> RAGChatKitServer:
    """Get the singleton ChatKit server instance."""
    global _chatkit_server
    if _chatkit_server is None:
        _chatkit_server = RAGChatKitServer()
    return _chatkit_server
