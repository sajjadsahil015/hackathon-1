#!/usr/bin/env python3
"""Ingest documentation files with proper chapter/module metadata."""

import asyncio
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import dotenv_values

# Load .env file
_env_path = Path(__file__).parent.parent.parent / ".env"
if _env_path.exists():
    _env_config = dotenv_values(_env_path)
    for key, value in _env_config.items():
        if value:
            os.environ[key] = value

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from rag_chatbot.config import get_settings
from rag_chatbot.services.embeddings import get_embedding_service


# Module mapping
MODULE_INFO = {
    "module-1-ros2": {"number": 1, "title": "The Robotic Nervous System (ROS 2)"},
    "module-2-simulation": {"number": 2, "title": "The Digital Twin (Simulation)"},
    "module-3-isaac": {"number": 3, "title": "The AI-Robot Brain (NVIDIA Isaac)"},
    "module-4-vla": {"number": 4, "title": "Vision-Language-Action (VLA)"},
}

# Chapter titles by filename
CHAPTER_TITLES = {
    "intro.md": "Introduction",
    "glossary.md": "Glossary",
    "01-ros2-architecture.md": "ROS 2 Architecture and Communication",
    "02-python-agents-rclpy.md": "Python Agents with rclpy",
    "03-urdf-humanoid.md": "URDF for Humanoid Robots",
    "01-digital-twins-gazebo.md": "Digital Twins and Physics with Gazebo",
    "02-unity-hri-rendering.md": "High-Fidelity Rendering and HRI in Unity",
    "03-simulated-sensors.md": "Simulated Sensors for Perception",
    "01-perception-isaac-sim.md": "Perception and Synthetic Data with Isaac Sim",
    "02-vslam-isaac-ros.md": "Visual SLAM with Isaac ROS",
    "03-nav2-path-planning.md": "Path Planning with Nav2",
    "01-vla-architecture.md": "VLA Architecture",
    "02-voice-language-planning.md": "Voice and Language Planning",
    "03-capstone-autonomous.md": "Capstone: Autonomous Humanoid",
}


def get_chapter_number(filename: str) -> int:
    """Extract chapter number from filename.

    Returns 1 for files without a numeric prefix (like intro.md).
    """
    match = re.match(r"(\d+)-", filename)
    if match:
        return int(match.group(1))
    # Default to 1 for non-numbered files (intro, glossary, etc.)
    return 1


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        # Try to break at paragraph or sentence
        if end < text_len:
            # Look for paragraph break
            para_break = text.rfind("\n\n", start + chunk_size - 300, end)
            if para_break > start:
                end = para_break + 2
            else:
                # Look for sentence end
                sentence_end = text.rfind(". ", start + chunk_size - 200, end)
                if sentence_end > start:
                    end = sentence_end + 2

        chunk = text[start:end].strip()
        if chunk and len(chunk) > 50:  # Skip very small chunks
            chunks.append(chunk)

        start = end - overlap

    return chunks


async def ingest_docs(docs_path: Path) -> None:
    """Ingest all documentation files."""
    settings = get_settings()

    print("Initializing services...")
    embedding_service = get_embedding_service()

    print(f"Connecting to Qdrant at {settings.qdrant_url}...")
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
        timeout=120,
    )

    # Clear existing collection
    print(f"Recreating collection '{settings.qdrant_collection_name}'...")
    try:
        client.delete_collection(settings.qdrant_collection_name)
    except Exception:
        pass

    from qdrant_client.models import Distance, VectorParams
    client.create_collection(
        collection_name=settings.qdrant_collection_name,
        vectors_config=VectorParams(
            size=settings.embedding_dimension,
            distance=Distance.COSINE,
        ),
    )

    # Find all markdown files
    md_files = list(docs_path.glob("**/*.md"))
    md_files = [f for f in md_files if "_assets" not in f.name]
    print(f"Found {len(md_files)} markdown files")

    total_chunks = 0
    all_points = []

    for md_file in md_files:
        # Determine module info
        parent_dir = md_file.parent.name
        module_info = MODULE_INFO.get(parent_dir, {"number": 1, "title": "Book Introduction"})

        # Get chapter info
        chapter_num = get_chapter_number(md_file.name)
        chapter_title = CHAPTER_TITLES.get(md_file.name, md_file.stem.replace("-", " ").title())

        print(f"\nProcessing: {md_file.name}")
        print(f"  Module {module_info['number']}: {module_info['title']}")
        print(f"  Chapter {chapter_num}: {chapter_title}")

        # Read and chunk content
        content = md_file.read_text(encoding="utf-8")

        # Remove frontmatter
        if content.startswith("---"):
            end_frontmatter = content.find("---", 3)
            if end_frontmatter > 0:
                content = content[end_frontmatter + 3:].strip()

        chunks = chunk_text(content)
        print(f"  Created {len(chunks)} chunks")

        # Generate embeddings with rate limiting
        for i, chunk_text_content in enumerate(chunks):
            # Rate limit: wait every 10 embeddings
            if total_chunks > 0 and total_chunks % 10 == 0:
                print(f"  Waiting 20s for rate limit... ({total_chunks} total)")
                time.sleep(20)

            # Generate embedding with retry
            embedding = None
            for retry in range(5):
                try:
                    embedding = await embedding_service.embed_text(chunk_text_content)
                    break
                except Exception as e:
                    if "429" in str(e) or "rate" in str(e).lower() or "TooMany" in str(e):
                        print(f"    Rate limited, waiting 65s...")
                        time.sleep(65)
                    else:
                        raise

            if embedding is None:
                continue

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk_text_content,
                    "module_number": module_info["number"],
                    "module_title": module_info["title"],
                    "chapter_number": chapter_num,
                    "chapter_title": chapter_title,
                    "section_number": i + 1,
                    "section_title": f"Section {i + 1}",
                    "page_start": i + 1,
                    "page_end": i + 2,
                    "chunk_index": i,
                    "source_file": md_file.name,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                },
            )
            all_points.append(point)
            total_chunks += 1

    # Upload all points in batches
    print(f"\nUploading {len(all_points)} chunks to Qdrant...")
    batch_size = 50
    for i in range(0, len(all_points), batch_size):
        batch = all_points[i:i + batch_size]
        client.upsert(
            collection_name=settings.qdrant_collection_name,
            points=batch,
        )
        print(f"  Uploaded {min(i + batch_size, len(all_points))}/{len(all_points)}")

    print(f"\nSuccessfully ingested {len(all_points)} chunks from {len(md_files)} files")


def main():
    docs_path = Path(__file__).parent.parent.parent / "frontend" / "docs"
    if not docs_path.exists():
        print(f"Error: Docs path not found: {docs_path}")
        sys.exit(1)

    asyncio.run(ingest_docs(docs_path))


if __name__ == "__main__":
    main()
