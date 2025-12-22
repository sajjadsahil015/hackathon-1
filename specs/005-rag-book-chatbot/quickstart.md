# Quickstart: RAG Chatbot for Technical Book

**Feature**: 005-rag-book-chatbot
**Date**: 2025-12-18

## Prerequisites

- Python 3.11+
- Docker (for Qdrant)
- Google Cloud account with Gemini API access
- PostgreSQL (Neon or local)

## Environment Setup

### 1. Clone and Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn google-generativeai qdrant-client psycopg2-binary pydantic python-dotenv pytest pytest-asyncio httpx

# Install ChatKit SDK for agent orchestration
pip install chatkit openai-agents
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```bash
# Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=  # Leave empty for local, set for cloud

# PostgreSQL (Neon)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# App Config
RELEVANCE_THRESHOLD=0.7
MAX_RESULTS=5
DEBUG=true
```

### 3. Start Qdrant (Docker)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 4. Initialize Database

```bash
python scripts/setup_db.py
```

## Book Ingestion

### 1. Prepare Book Content

Place your book content in `data/book/` directory:
- `book.md` or `book.txt` - Full book text
- `chapters.json` - Chapter/section metadata (optional)

### 2. Run Ingestion

```bash
python scripts/ingest_book.py --input data/book/book.md
```

This will:
- Split book into chunks (~512 tokens each)
- Generate embeddings via Gemini
- Store vectors in Qdrant
- Store metadata in PostgreSQL

## Running the API

### Development Server

```bash
uvicorn src.rag_chatbot.main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
uvicorn src.rag_chatbot.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Usage Examples

### ChatKit Streaming Endpoint (Recommended)

The ChatKit endpoint provides SSE streaming for real-time responses:

```bash
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -d '{
    "type": "stream",
    "thread": {"id": "thread-123"},
    "input": {
      "type": "user_message",
      "content": "What is sensor fusion in humanoid robots?"
    }
  }'
```

Response (Server-Sent Events):
```
data: {"type": "text_delta", "delta": "Sensor"}
data: {"type": "text_delta", "delta": " fusion"}
data: {"type": "text_delta", "delta": " in humanoid robots..."}
data: {"type": "message_complete", "citations": [...]}
```

### REST API: Full Book Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is sensor fusion in humanoid robots?",
    "mode": "full_book"
  }'
```

Response:
```json
{
  "answer": "Sensor fusion in humanoid robots refers to...",
  "citations": [
    {
      "chapter_number": 5,
      "chapter_title": "Perception and Sensing",
      "section_number": 3,
      "section_title": "Multi-Sensor Integration",
      "page_start": 142,
      "page_end": 145,
      "relevance_score": 0.89
    }
  ],
  "mode": "full_book",
  "found_in_book": true,
  "confidence": 0.89,
  "query_id": "550e8400-e29b-41d4-a716-446655440000",
  "processing_time_ms": 2340
}
```

### Selected Text Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this mean?",
    "mode": "selected_text",
    "selected_text": "The VLA model combines vision encoders with language models to enable robots to understand and execute natural language instructions in real-world environments."
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=src/rag_chatbot
```

## Project Structure

```
.
├── src/
│   └── rag_chatbot/
│       ├── main.py            # FastAPI app with ChatKit endpoint
│       ├── chatkit_server.py  # ChatKit server (extends ChatKitServer)
│       ├── agent.py           # RAG agent with tools
│       ├── config.py          # Configuration
│       ├── models/            # Pydantic models
│       ├── services/          # Business logic
│       ├── tools/             # Agent tools (search_book, get_citation)
│       └── api/               # API routes
├── scripts/
│   ├── ingest_book.py         # Book ingestion
│   └── setup_db.py            # Database setup
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── data/
│   └── book/                  # Book content
├── .env                       # Environment variables
└── requirements.txt           # Dependencies
```

## Troubleshooting

### "No relevant content found" for valid questions

- Check relevance threshold (default 0.7)
- Verify book was ingested: `python scripts/check_qdrant.py`
- Try rephrasing the question

### Slow response times

- Ensure Qdrant is running locally (not cloud with high latency)
- Check Gemini API quotas
- Reduce `MAX_RESULTS` if retrieving too many passages

### API key errors

- Verify `GOOGLE_API_KEY` is set correctly
- Check API key has Gemini access enabled
- Verify billing is set up for Gemini API

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement core services (embeddings, retrieval, generation)
3. Add book ingestion pipeline
4. Deploy to production environment
