#!/usr/bin/env python3
"""Setup PostgreSQL database schema for book metadata."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import psycopg2
from psycopg2 import sql

from rag_chatbot.config import get_settings

# SQL schema for book metadata
SCHEMA_SQL = """
-- Book metadata table
CREATE TABLE IF NOT EXISTS book_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_title VARCHAR(255) NOT NULL,
    total_chapters INT NOT NULL,
    total_pages INT NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    ingested_at TIMESTAMP NOT NULL DEFAULT NOW(),
    chunk_count INT NOT NULL DEFAULT 0
);

-- Chapters table
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES book_metadata(id) ON DELETE CASCADE,
    chapter_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    page_start INT NOT NULL,
    page_end INT NOT NULL,
    section_count INT NOT NULL DEFAULT 0,
    UNIQUE(book_id, chapter_number)
);

-- Sections table
CREATE TABLE IF NOT EXISTS sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    section_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    page_start INT NOT NULL,
    page_end INT NOT NULL,
    chunk_count INT NOT NULL DEFAULT 0,
    UNIQUE(chapter_id, section_number)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_chapters_book_id ON chapters(book_id);
CREATE INDEX IF NOT EXISTS idx_sections_chapter_id ON sections(chapter_id);
CREATE INDEX IF NOT EXISTS idx_chapters_chapter_number ON chapters(book_id, chapter_number);
CREATE INDEX IF NOT EXISTS idx_sections_section_number ON sections(chapter_id, section_number);
"""


def setup_database() -> None:
    """Create database schema for book metadata."""
    settings = get_settings()

    print(f"Connecting to PostgreSQL...")

    try:
        conn = psycopg2.connect(settings.database_url)
        conn.autocommit = True
        cursor = conn.cursor()

        print("Creating database schema...")
        cursor.execute(SCHEMA_SQL)

        print("Schema created successfully!")

        # Verify tables exist
        cursor.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name IN ('book_metadata', 'chapters', 'sections')
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"Created tables: {', '.join(t[0] for t in tables)}")

        cursor.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
