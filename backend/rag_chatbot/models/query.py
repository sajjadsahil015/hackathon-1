"""Query and Response models for the RAG chatbot API."""

from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from .citation import Citation


class QueryMode(str, Enum):
    """Query mode enumeration."""

    FULL_BOOK = "full_book"
    SELECTED_TEXT = "selected_text"


class QueryRequest(BaseModel):
    """Incoming query request from user."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="The question to ask about the book content",
    )
    mode: QueryMode = Field(
        default=QueryMode.FULL_BOOK,
        description="Query mode: full_book searches entire book, selected_text uses provided text",
    )
    selected_text: str | None = Field(
        None,
        min_length=10,
        max_length=5000,
        description="Text passage for selected_text mode",
    )

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        """Validate question is not just whitespace."""
        stripped = v.strip()
        if len(stripped) < 1:
            raise ValueError("Question cannot be empty")
        return stripped

    @field_validator("selected_text")
    @classmethod
    def validate_selected_text(cls, v: str | None) -> str | None:
        """Validate selected text if provided."""
        if v is not None:
            stripped = v.strip()
            if len(stripped) < 10:
                raise ValueError("Selected text must be at least 10 characters")
            return stripped
        return v


class QueryResponse(BaseModel):
    """Response from the chatbot."""

    answer: str = Field(..., description="The generated answer text")
    citations: list[Citation] = Field(
        default_factory=list, description="Source citations (empty for selected_text mode)"
    )
    mode: QueryMode = Field(..., description="Mode used for query")
    found_in_book: bool = Field(..., description="True if answer derived from book content")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Overall confidence score (0.0 to 1.0)"
    )
    query_id: str = Field(
        default_factory=lambda: str(uuid4()), description="UUID for tracking"
    )
    processing_time_ms: int = Field(..., ge=0, description="Time to generate response in ms")


class RefusalResponse(BaseModel):
    """Response when no relevant content is found."""

    answer: str = Field(
        default="I could not find information about this topic in the book. "
        "Please try rephrasing or ask about a topic covered in the book.",
        description="Refusal message",
    )
    citations: list[Citation] = Field(default_factory=list)
    mode: QueryMode
    found_in_book: bool = Field(default=False)
    confidence: float = Field(default=0.0)
    query_id: str = Field(default_factory=lambda: str(uuid4()))
    processing_time_ms: int = Field(..., ge=0)
