# Data Model: RAG Chatbot for Technical Book

**Feature**: 005-rag-book-chatbot
**Date**: 2025-12-18

## Entities

### 1. BookChunk (Qdrant Vector Collection)

Represents a chunk of book content stored in the vector database.

```
Collection: book_chunks
Vector Size: 768 (Gemini embedding dimension)
Distance: Cosine

Fields:
├── id: string (UUID)
├── vector: float[768] (embedding)
└── payload:
    ├── text: string (chunk content, max 2048 chars)
    ├── chapter_number: int (1-based)
    ├── chapter_title: string
    ├── section_number: int (1-based within chapter)
    ├── section_title: string
    ├── page_start: int
    ├── page_end: int
    ├── chunk_index: int (order within section)
    └── created_at: datetime (ISO 8601)
```

**Validation Rules**:
- `text` must be non-empty and ≤2048 characters
- `chapter_number` must be ≥1
- `page_start` ≤ `page_end`
- `chunk_index` must be ≥0

### 2. BookMetadata (Postgres)

Stores book structure metadata for citation generation.

```sql
Table: book_metadata
├── id: UUID (PK)
├── book_title: VARCHAR(255) NOT NULL
├── total_chapters: INT NOT NULL
├── total_pages: INT NOT NULL
├── language: VARCHAR(10) DEFAULT 'en'
├── ingested_at: TIMESTAMP NOT NULL
└── chunk_count: INT NOT NULL

Table: chapters
├── id: UUID (PK)
├── book_id: UUID (FK → book_metadata.id)
├── chapter_number: INT NOT NULL
├── title: VARCHAR(255) NOT NULL
├── page_start: INT NOT NULL
├── page_end: INT NOT NULL
└── section_count: INT NOT NULL

Table: sections
├── id: UUID (PK)
├── chapter_id: UUID (FK → chapters.id)
├── section_number: INT NOT NULL
├── title: VARCHAR(255) NOT NULL
├── page_start: INT NOT NULL
├── page_end: INT NOT NULL
└── chunk_count: INT NOT NULL

Indexes:
- chapters(book_id, chapter_number) UNIQUE
- sections(chapter_id, section_number) UNIQUE
```

### 3. Query (API Request Model)

Represents an incoming user query.

```python
class QueryMode(str, Enum):
    FULL_BOOK = "full_book"
    SELECTED_TEXT = "selected_text"

class QueryRequest(BaseModel):
    question: str                    # User's question (required)
    mode: QueryMode = FULL_BOOK      # Query mode (default: full_book)
    selected_text: str | None = None # Context for selected_text mode
    
    # Validation
    @validator('question')
    def question_not_empty(cls, v):
        if not v or len(v.strip()) < 3:
            raise ValueError('Question must be at least 3 characters')
        return v.strip()
    
    @validator('selected_text')
    def validate_selected_text(cls, v, values):
        if values.get('mode') == QueryMode.SELECTED_TEXT:
            if not v or len(v.strip()) < 10:
                raise ValueError('Selected text must be at least 10 characters')
        return v.strip() if v else None
```

### 4. Response (API Response Model)

Represents the chatbot's response to a query.

```python
class Citation(BaseModel):
    chapter_number: int
    chapter_title: str
    section_number: int | None = None
    section_title: str | None = None
    page_start: int
    page_end: int
    relevance_score: float  # 0.0 to 1.0

class QueryResponse(BaseModel):
    answer: str                      # Generated answer text
    citations: list[Citation]        # Source citations (empty for selected_text mode)
    mode: QueryMode                  # Mode used for query
    found_in_book: bool              # True if answer derived from book content
    confidence: float                # Overall confidence score (0.0 to 1.0)
    
    # Response metadata
    query_id: str                    # UUID for tracking
    processing_time_ms: int          # Time to generate response
```

### 5. RefusalResponse

Represents a response when no relevant content is found.

```python
class RefusalResponse(BaseModel):
    answer: str = "I could not find information about this topic in the book. Please try rephrasing or ask about a topic covered in the book."
    citations: list[Citation] = []
    mode: QueryMode
    found_in_book: bool = False
    confidence: float = 0.0
    query_id: str
    processing_time_ms: int
```

## State Transitions

### Query Processing Flow

```
┌─────────────┐
│   RECEIVED  │ ← Query arrives
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATED  │ ← Input validation passed
└──────┬──────┘
       │
       ├─── mode == selected_text ───┐
       │                              │
       ▼                              ▼
┌─────────────┐               ┌─────────────────┐
│  EMBEDDING  │               │ DIRECT_CONTEXT  │
└──────┬──────┘               └────────┬────────┘
       │                               │
       ▼                               │
┌─────────────┐                        │
│  RETRIEVAL  │                        │
└──────┬──────┘                        │
       │                               │
       ├─── score < 0.7 ───┐           │
       │                    │           │
       ▼                    ▼           │
┌─────────────┐     ┌─────────────┐    │
│ GENERATING  │     │  REFUSING   │    │
└──────┬──────┘     └──────┬──────┘    │
       │                    │           │
       ▼                    ▼           ▼
┌─────────────────────────────────────────┐
│              RESPONDING                  │
└─────────────────────────────────────────┘
```

## Relationships

```
BookMetadata (1) ─────< (N) Chapter
Chapter (1) ─────< (N) Section
Section (1) ─────< (N) BookChunk (logical, not FK)

Query (1) ────── (1) Response
```

## Indexes and Performance

### Qdrant Indexes
- HNSW index on vectors (automatic)
- Payload index on `chapter_number` for filtered search

### Postgres Indexes
- `chapters(book_id, chapter_number)` for chapter lookup
- `sections(chapter_id, section_number)` for section lookup

### Query Performance Targets
- Embedding generation: <500ms
- Vector search (top 5): <200ms
- LLM generation: <3000ms
- Total: <5000ms (per SC-003)
