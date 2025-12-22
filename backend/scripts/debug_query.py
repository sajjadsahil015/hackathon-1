#!/usr/bin/env python3
"""Debug script to test the query pipeline step by step."""

import asyncio
import os
import sys
import traceback
from pathlib import Path

# Load .env file before any other imports
from dotenv import dotenv_values

_env_path = Path(__file__).parent.parent.parent / ".env"
_env_config = dotenv_values(_env_path)
for key, value in _env_config.items():
    if value:
        os.environ[key] = value

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag_chatbot.config import get_settings
from rag_chatbot.services.embeddings import get_embedding_service
from rag_chatbot.services.retrieval import get_retrieval_service
from rag_chatbot.services.generation import get_generation_service


async def debug_query(question: str = "What is ROS 2?") -> None:
    """Debug the query pipeline step by step."""
    settings = get_settings()
    print(f"Settings loaded:")
    print(f"  - Qdrant URL: {settings.qdrant_url}")
    print(f"  - Collection: {settings.qdrant_collection_name}")
    print(f"  - Relevance threshold: {settings.relevance_threshold}")
    print(f"  - Generation model: {settings.generation_model}")
    print()

    # Step 1: Test embeddings
    print("Step 1: Testing embedding service...")
    try:
        embedding_service = get_embedding_service()
        embedding = await embedding_service.embed_query(question)
        print(f"  [OK] Generated embedding with {len(embedding)} dimensions")
    except Exception as e:
        print(f"  [FAIL] Embedding failed: {e}")
        traceback.print_exc()
        return

    # Step 2: Test retrieval
    print("\nStep 2: Testing retrieval service...")
    try:
        retrieval_service = get_retrieval_service()
        chunks, has_relevant = await retrieval_service.search_with_threshold_check(question)
        print(f"  [OK] Retrieved {len(chunks)} chunks, has_relevant={has_relevant}")
        if chunks:
            for i, chunk in enumerate(chunks[:3]):
                print(f"    - Chunk {i+1}: score={chunk.score:.3f}, chapter={chunk.chapter_number}")
    except Exception as e:
        print(f"  [FAIL] Retrieval failed: {e}")
        traceback.print_exc()
        return

    # Step 3: Test generation
    print("\nStep 3: Testing generation service...")
    try:
        generation_service = get_generation_service()
        if chunks:
            answer = await generation_service.generate_response(question, chunks)
            print(f"  [OK] Generated response ({len(answer)} chars)")
            print(f"    Preview: {answer[:200]}...")
        else:
            print("  [WARN] No chunks to generate from (would return refusal message)")
    except Exception as e:
        print(f"  [FAIL] Generation failed: {e}")
        traceback.print_exc()
        return

    print("\n[SUCCESS] All steps passed!")


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is ROS 2?"
    asyncio.run(debug_query(question))
