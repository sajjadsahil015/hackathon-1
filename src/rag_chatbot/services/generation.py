"""Qwen response generation service via Hugging Face."""

import logging

from huggingface_hub import InferenceClient

from ..config import get_settings
from .retrieval import RetrievedChunk

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a helpful assistant that answers questions about the Physical AI & Humanoid Robotics book.

IMPORTANT RULES:
1. ONLY answer questions based on the provided book content.
2. If the provided context does not contain relevant information, say "I could not find information about this topic in the book."
3. NEVER make up information or provide answers from general knowledge.
4. ALWAYS cite the chapter and section when providing information.
5. Be concise and technical in your responses.
6. If asked about topics outside the book, politely decline and explain you can only answer about the book content.

Your responses should be grounded strictly in the book content provided in the context."""


class GenerationService:
    """Service for generating responses using Qwen via Hugging Face."""

    def __init__(self) -> None:
        """Initialize the generation service."""
        self.settings = get_settings()
        if not self.settings.qwen_api_key:
            raise RuntimeError(
                "QWEN_API_KEY not configured. Please set it in your .env file."
            )
        self.client = InferenceClient(
            model=self.settings.generation_model,
            token=self.settings.qwen_api_key,
        )

    def _format_context(self, chunks: list[RetrievedChunk]) -> str:
        """Format retrieved chunks as context for the model.

        Args:
            chunks: List of retrieved book chunks.

        Returns:
            Formatted context string.
        """
        if not chunks:
            return "No relevant content found in the book."

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            source = f"[Source: Chapter {chunk.chapter_number}: {chunk.chapter_title}"
            if chunk.section_title:
                source += f", Section {chunk.section_number}: {chunk.section_title}"
            source += f", pp. {chunk.page_start}-{chunk.page_end}]"

            context_parts.append(f"--- Context {i} {source} ---\n{chunk.text}")

        return "\n\n".join(context_parts)

    async def generate_response(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> str:
        """Generate a response based on retrieved chunks.

        Args:
            question: The user's question.
            chunks: Retrieved book chunks for context.

        Returns:
            Generated response text.
        """
        context = self._format_context(chunks)

        user_prompt = f"""Based on the following book content, answer the question.

BOOK CONTENT:
{context}

QUESTION: {question}

Provide a clear, accurate answer based only on the book content above. Include citations to specific chapters and sections."""

        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=self.settings.max_response_tokens,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise RuntimeError(f"Response generation failed: {e}") from e

    async def generate_from_selected_text(
        self,
        question: str,
        selected_text: str,
    ) -> str:
        """Generate a response based on user-selected text only.

        Args:
            question: The user's question.
            selected_text: The text passage selected by the user.

        Returns:
            Generated response text.
        """
        user_prompt = f"""Based ONLY on the following selected text, answer the question.
Do NOT use any information outside of this selected passage.

SELECTED TEXT:
{selected_text}

QUESTION: {question}

Provide a clear explanation based only on the selected text above. If the question cannot be answered from the selected text alone, indicate that clearly."""

        try:
            response = self.client.chat_completion(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=self.settings.max_response_tokens,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Failed to generate response from selected text: {e}")
            raise RuntimeError(f"Response generation failed: {e}") from e


# Singleton instance
_generation_service: GenerationService | None = None


def get_generation_service() -> GenerationService:
    """Get the singleton generation service instance."""
    global _generation_service
    if _generation_service is None:
        _generation_service = GenerationService()
    return _generation_service
