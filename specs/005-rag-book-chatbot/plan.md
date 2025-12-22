# Implementation Plan: RAG Chatbot for Technical Book

**Branch**: `005-rag-book-chatbot` | **Date**: 2025-12-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-rag-book-chatbot/spec.md`

## Summary

Build a RAG-based chatbot that answers questions grounded strictly in the Physical AI & Humanoid Robotics book content. Supports two query modes: full-book context search and user-selected-text-only answering. Uses **OpenAI ChatKit SDK** for agent orchestration, Google Gemini Flash 2.5 for embeddings and response generation, Qdrant for vector storage, and FastAPI for the backend API.

## Technical Context

**Language/Version**: Python 3.11+
**Agent Framework**: OpenAI ChatKit SDK (chatkit-python)
**Primary Dependencies**: FastAPI, chatkit, google-generativeai, qdrant-client, pydantic
**Storage**: Qdrant (vector store), Neon Postgres (metadata/citations)
**Testing**: pytest, pytest-asyncio
**Target Platform**: Linux server / Docker container
**Project Type**: Web API (backend only, stateless)
**Performance Goals**: <5s response time, 50 concurrent users
**Constraints**: Relevance threshold >0.7, no hallucination, book-content-only responses
**Scale/Scope**: Single book (~500 pages), 50 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Technical Accuracy | PASS | All responses grounded in book content with citations |
| II. Source Integrity | PASS | No hallucinated content; relevance threshold enforced |
| III. Spec-Driven Reproducibility | PASS | Clear spec with measurable acceptance criteria |
| IV. Practical Rigor | PASS | Real tools (Gemini, Qdrant, FastAPI) |
| V. API Currency | PASS | Using stable Gemini Flash 2.5, Qdrant latest |
| VI. Conceptual Clarity | PASS | Clear separation: retrieval vs generation vs citation |

**Technical Constraints Alignment:**
- ✅ RAG Chatbot Stack matches constitution (FastAPI, Qdrant, Gemini)
- ✅ Chatbot scope: Full-book Q&A and user-selected-text contextual questions only
- ✅ Non-goal: General-purpose chatbot functionality beyond book content

## Project Structure

### Documentation (this feature)

```text
specs/005-rag-book-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI spec)
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (via /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── rag_chatbot/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point with ChatKit endpoint
│   ├── config.py            # Settings and environment config
│   ├── chatkit_server.py    # ChatKit server implementation (extends ChatKitServer)
│   ├── agent.py             # RAG agent definition with tools
│   ├── models/
│   │   ├── __init__.py
│   │   ├── query.py         # Query and Response models
│   │   └── citation.py      # Citation models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── embeddings.py    # Gemini embedding service
│   │   ├── retrieval.py     # Qdrant vector search
│   │   ├── generation.py    # Gemini response generation
│   │   └── citation.py      # Citation extraction service
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_book.py   # Agent tool: search book content
│   │   └── get_citation.py  # Agent tool: get citation for chunk
│   └── api/
│       ├── __init__.py
│       ├── routes.py        # REST API endpoints (non-ChatKit)
│       └── middleware.py    # Rate limiting, error handling
├── scripts/
│   ├── ingest_book.py       # Book content ingestion pipeline
│   └── setup_qdrant.py      # Vector store initialization

tests/
├── conftest.py
├── unit/
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   └── test_generation.py
├── integration/
│   ├── test_api.py
│   └── test_rag_pipeline.py
└── contract/
    └── test_openapi.py
```

**Structure Decision**: Single backend API project. No frontend (API-only for integration with reading interfaces). Modular service layer for testability.

## Complexity Tracking

No constitution violations. Architecture is minimal and appropriate for scope:
- Single Python project (no microservices)
- Two storage systems justified: Qdrant for vectors, Postgres for structured metadata
- No additional abstraction layers beyond service pattern

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                          │
├─────────────────────────────────────────────────────────────────┤
│  POST /chatkit (ChatKit Protocol - SSE streaming)               │
│  POST /query   (REST API - JSON response)                       │
│  ├── mode: "full_book" | "selected_text"                       │
│  ├── question: string                                           │
│  └── selected_text?: string (for selected_text mode)           │
├─────────────────────────────────────────────────────────────────┤
│                   ChatKit Server Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  RAGChatKitServer (extends ChatKitServer)                 │  │
│  │  ├── respond() → AsyncIterator[ThreadStreamEvent]         │  │
│  │  ├── AgentContext (thread, store, request_context)        │  │
│  │  └── stream_agent_response() for SSE streaming            │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                   RAG Agent (Agents SDK)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Agent[AgentContext] with tools:                          │  │
│  │  ├── search_book_content(query) → retrieves from Qdrant   │  │
│  │  ├── get_citation(chunk_id) → returns citation info       │  │
│  │  └── Instructions: "Answer only from book content..."     │  │
│  └──────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                      Service Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Embeddings  │→│   Retrieval   │→│  Generation   │          │
│  │   (Gemini)   │  │   (Qdrant)   │  │   (Gemini)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                           ↓                                     │
│                    Citation Extraction                          │
├─────────────────────────────────────────────────────────────────┤
│                      Data Layer                                 │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │   Qdrant         │    │   Neon Postgres   │                  │
│  │  (vectors +      │    │  (book metadata,  │                  │
│  │   chunk text)    │    │   chapter info)   │                  │
│  └──────────────────┘    └──────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

1. **Agent Framework**: OpenAI ChatKit SDK for agent orchestration with SSE streaming support
2. **Chunking Strategy**: Split book into ~512 token chunks with 50-token overlap, preserving section boundaries
3. **Relevance Threshold**: 0.7 cosine similarity minimum; refuse answer if below
4. **Citation Format**: Chapter X, Section Y, Page Z (when available)
5. **Selected Text Mode**: Bypass retrieval; use provided text directly as context
6. **Rate Limiting**: 10 req/min per IP to support 50 concurrent users
7. **Dual API Support**: ChatKit `/chatkit` endpoint for streaming + REST `/query` for simple JSON responses

## Next Steps

- Phase 0: Complete research.md ✓
- Phase 1: Complete data-model.md, contracts/openapi.yaml, quickstart.md ✓
- Phase 2: Run `/sp.tasks` to generate implementation tasks
