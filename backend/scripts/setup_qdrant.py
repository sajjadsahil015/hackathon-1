#!/usr/bin/env python3
"""Setup Qdrant vector store with book_chunks collection."""

import os
import sys
from pathlib import Path

# Load .env file before any other imports
from dotenv import dotenv_values

_env_path = Path(__file__).parent.parent.parent / ".env"
if _env_path.exists():
    _env_config = dotenv_values(_env_path)
    for key, value in _env_config.items():
        if value:
            os.environ[key] = value

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from rag_chatbot.config import get_settings


def setup_qdrant() -> None:
    """Create and configure the book_chunks collection in Qdrant."""
    settings = get_settings()

    print(f"Connecting to Qdrant at {settings.qdrant_url}...")

    # Initialize client
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
    )

    collection_name = settings.qdrant_collection_name

    # Check if collection exists
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if collection_name in collection_names:
        print(f"Collection '{collection_name}' already exists.")
        response = input("Do you want to recreate it? (y/N): ")
        if response.lower() != "y":
            print("Keeping existing collection.")
            return
        print(f"Deleting existing collection '{collection_name}'...")
        client.delete_collection(collection_name)

    # Create collection with vector configuration
    print(f"Creating collection '{collection_name}'...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    # Create payload indexes for filtering
    print("Creating payload indexes...")
    client.create_payload_index(
        collection_name=collection_name,
        field_name="chapter_number",
        field_schema="integer",
    )

    print(f"Successfully created collection '{collection_name}'")
    print(f"  - Vector size: {settings.embedding_dimension}")
    print(f"  - Distance metric: Cosine")
    print(f"  - Indexed fields: chapter_number")


if __name__ == "__main__":
    setup_qdrant()
