#!/usr/bin/env python3
"""Book content ingestion pipeline.

Reads book content, chunks it, generates embeddings, and stores in Qdrant.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

# Load .env file before any other imports to override system env vars
from dotenv import dotenv_values

_env_path = Path(__file__).parent.parent.parent / ".env"
_env_config = dotenv_values(_env_path)
for key, value in _env_config.items():
    if value:
        os.environ[key] = value

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from rag_chatbot.config import get_settings
from rag_chatbot.services.embeddings import get_embedding_service


@dataclass
class BookChunk:
    """Represents a chunk of book content."""

    text: str
    chapter_number: int
    chapter_title: str
    section_number: int
    section_title: str
    page_start: int
    page_end: int
    chunk_index: int


class BookChunker:
    """Chunks book content preserving section boundaries."""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50) -> None:
        """Initialize chunker.

        Args:
            chunk_size: Target tokens per chunk.
            chunk_overlap: Overlap tokens between chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Approximate chars per token for English text
        self.chars_per_token = 4

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return len(text) // self.chars_per_token

    def _split_into_chunks(self, text: str) -> list[str]:
        """Split text into overlapping chunks."""
        max_chars = self.chunk_size * self.chars_per_token
        overlap_chars = self.chunk_overlap * self.chars_per_token

        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + max_chars

            # Try to break at sentence boundary
            if end < text_len:
                # Look for sentence end near the chunk boundary
                search_start = max(start + max_chars - 100, start)
                sentence_ends = [
                    m.end()
                    for m in re.finditer(r"[.!?]\s+", text[search_start:end])
                ]
                if sentence_ends:
                    end = search_start + sentence_ends[-1]

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start with overlap
            start = end - overlap_chars

        return chunks

    def chunk_book(self, content: str, metadata: dict) -> Iterator[BookChunk]:
        """Chunk book content with metadata.

        Args:
            content: Full book text content.
            metadata: Book metadata including chapters info.

        Yields:
            BookChunk instances.
        """
        # Parse chapters and sections from content
        # This is a simplified parser - adjust based on actual book format
        chapter_pattern = r"^#+\s*Chapter\s+(\d+)[:\s]*(.+?)$"
        section_pattern = r"^##+\s*(\d+\.?\d*)[:\s]*(.+?)$"

        current_chapter = 1
        current_chapter_title = "Introduction"
        current_section = 1
        current_section_title = "Overview"
        current_page = 1
        chunk_index = 0

        # Split by major headings
        lines = content.split("\n")
        current_text = []

        for line in lines:
            # Check for chapter heading
            chapter_match = re.match(chapter_pattern, line, re.IGNORECASE)
            if chapter_match:
                # Process accumulated text
                if current_text:
                    text = "\n".join(current_text)
                    for chunk_text in self._split_into_chunks(text):
                        yield BookChunk(
                            text=chunk_text,
                            chapter_number=current_chapter,
                            chapter_title=current_chapter_title,
                            section_number=current_section,
                            section_title=current_section_title,
                            page_start=current_page,
                            page_end=current_page + 1,
                            chunk_index=chunk_index,
                        )
                        chunk_index += 1
                    current_text = []

                current_chapter = int(chapter_match.group(1))
                current_chapter_title = chapter_match.group(2).strip()
                current_section = 1
                current_section_title = "Introduction"
                chunk_index = 0
                continue

            # Check for section heading
            section_match = re.match(section_pattern, line)
            if section_match:
                # Process accumulated text first
                if current_text:
                    text = "\n".join(current_text)
                    for chunk_text in self._split_into_chunks(text):
                        yield BookChunk(
                            text=chunk_text,
                            chapter_number=current_chapter,
                            chapter_title=current_chapter_title,
                            section_number=current_section,
                            section_title=current_section_title,
                            page_start=current_page,
                            page_end=current_page + 1,
                            chunk_index=chunk_index,
                        )
                        chunk_index += 1
                    current_text = []

                section_num = section_match.group(1)
                current_section = int(float(section_num))
                current_section_title = section_match.group(2).strip()
                chunk_index = 0
                continue

            current_text.append(line)

        # Process remaining text
        if current_text:
            text = "\n".join(current_text)
            for chunk_text in self._split_into_chunks(text):
                yield BookChunk(
                    text=chunk_text,
                    chapter_number=current_chapter,
                    chapter_title=current_chapter_title,
                    section_number=current_section,
                    section_title=current_section_title,
                    page_start=current_page,
                    page_end=current_page + 1,
                    chunk_index=chunk_index,
                )
                chunk_index += 1


async def ingest_book(input_path: Path, metadata_path: Path | None = None) -> None:
    """Ingest book content into Qdrant.

    Args:
        input_path: Path to book content file (markdown or text).
        metadata_path: Optional path to book metadata JSON.
    """
    settings = get_settings()

    print(f"Reading book content from {input_path}...")
    content = input_path.read_text(encoding="utf-8")

    # Load metadata if provided
    metadata = {}
    if metadata_path and metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    # Initialize services
    print("Initializing embedding service...")
    embedding_service = get_embedding_service()

    print(f"Connecting to Qdrant at {settings.qdrant_url}...")
    qdrant_client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
        timeout=120,  # Increase timeout for cloud operations
    )

    # Chunk the book
    print("Chunking book content...")
    chunker = BookChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = list(chunker.chunk_book(content, metadata))
    print(f"Created {len(chunks)} chunks")

    # Generate embeddings and upload
    print("Generating embeddings and uploading to Qdrant...")
    batch_size = 10  # Smaller batches for rate limiting
    total_uploaded = 0
    import time

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        points = []

        for chunk in batch:
            # Generate embedding with retry on rate limit
            embedding = None
            for retry in range(5):
                try:
                    embedding = await embedding_service.embed_text(chunk.text)
                    break
                except Exception as e:
                    error_str = str(e)
                    if "429" in error_str or "rate" in error_str.lower() or "TooMany" in error_str:
                        wait_time = 65  # Wait just over 1 minute
                        print(f"  Rate limited, waiting {wait_time}s (retry {retry+1}/5)...")
                        time.sleep(wait_time)
                    else:
                        raise

            if embedding is None:
                print(f"  Failed to get embedding after retries, skipping chunk")
                continue

            # Create point
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk.text,
                    "chapter_number": chunk.chapter_number,
                    "chapter_title": chunk.chapter_title,
                    "section_number": chunk.section_number,
                    "section_title": chunk.section_title,
                    "page_start": chunk.page_start,
                    "page_end": chunk.page_end,
                    "chunk_index": chunk.chunk_index,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            points.append(point)

        # Upload batch
        if points:
            qdrant_client.upsert(
                collection_name=settings.qdrant_collection_name,
                points=points,
            )
            total_uploaded += len(points)
            print(f"  Uploaded {total_uploaded}/{len(chunks)} chunks")

        # Rate limit: wait between batches (40 calls/min = ~1.5s per call)
        # For batch of 10, wait 20s to stay safe
        if i + batch_size < len(chunks):
            print(f"  Waiting 20s to avoid rate limit...")
            time.sleep(20)

    print(f"\nSuccessfully ingested {total_uploaded} chunks into Qdrant")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Ingest book content into vector store")
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        required=True,
        help="Path to book content file (markdown or text)",
    )
    parser.add_argument(
        "--metadata",
        "-m",
        type=Path,
        help="Path to book metadata JSON file (optional)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    asyncio.run(ingest_book(args.input, args.metadata))


if __name__ == "__main__":
    main()
