"""Configuration module using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Cohere Configuration (for embeddings)
    cohere_api_key: str = ""

    # Google Gemini API (for generation only)
    google_api_key: str = ""

    # Qdrant Vector Store
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "book_chunks"

    # PostgreSQL Database
    database_url: str = "postgresql://ragchatbot:ragchatbot_dev@localhost:5432/ragchatbot"

    # RAG Configuration
    relevance_threshold: float = 0.35  # Adjusted for Cohere embeddings
    max_results: int = 5
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # Embedding Configuration (Cohere)
    embedding_model: str = "embed-english-v3.0"
    embedding_dimension: int = 1024

    # Generation Configuration (Gemini)
    generation_model: str = "gemini-2.0-flash"
    max_response_tokens: int = 1024

    # Logging
    log_level: str = "INFO"
    debug: bool = False

    # Application
    app_name: str = "RAG Chatbot"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
