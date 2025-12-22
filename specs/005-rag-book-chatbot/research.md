# Research: RAG Chatbot for Technical Book

**Feature**: 005-rag-book-chatbot
**Date**: 2025-12-18

## Research Tasks

### 1. OpenAI ChatKit SDK for Agent Orchestration

**Decision**: Use OpenAI ChatKit SDK (chatkit-python) for agent building and streaming responses

**Rationale**:
- User explicitly requested ChatKit for agent building
- Native SSE streaming support via `StreamingResult` and `stream_agent_response()`
- Clean abstraction with `ChatKitServer` base class for custom implementations
- Built-in thread management with `ThreadMetadata` and `AgentContext`
- Works seamlessly with OpenAI Agents SDK for tool definitions

**Alternatives Considered**:
- LangChain: More complex, larger dependency footprint
- Raw FastAPI streaming: No agent abstraction, manual implementation
- Semantic Kernel: Microsoft ecosystem, less Python-native

**Implementation Notes**:
- Extend `ChatKitServer` class with custom `RAGChatKitServer`
- Implement `respond()` method returning `AsyncIterator[ThreadStreamEvent]`
- Use `AgentContext` for thread/store management
- Define RAG tools (search_book_content, get_citation) for agent
- FastAPI endpoint pattern:
```python
@app.post("/chatkit")
async def chatkit_endpoint(request: Request):
    result = await server.process(await request.body(), {})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    return Response(content=result.json, media_type="application/json")
```

### 2. Gemini Flash 2.5 for RAG

**Decision**: Use Google Gemini Flash 2.5 for both embeddings and response generation

**Rationale**:
- User explicitly requested Gemini Flash 2.5
- Cost-effective for educational/book applications
- Supports both embedding and generation in single API
- Good context window (1M tokens) for book content

**Alternatives Considered**:
- OpenAI GPT-4: Higher cost, better quality but overkill for book Q&A
- Claude: No native embedding support, would need separate embedding model
- Local models: Deployment complexity, hardware requirements

**Implementation Notes**:
- Use `google-generativeai` Python SDK
- Model: `gemini-2.0-flash-exp` (or latest stable)
- Embedding model: `text-embedding-004` (Gemini embedding)

### 2. Vector Store Selection

**Decision**: Use Qdrant for vector storage (per constitution)

**Rationale**:
- Specified in project constitution
- Excellent Python SDK
- Supports filtering by metadata (chapter, section)
- Free cloud tier available for small-scale production

**Alternatives Considered**:
- Pinecone: Good but paid, not in constitution
- ChromaDB: Good for local dev but less production-ready
- pgvector: Would simplify to single DB but less vector-optimized

**Implementation Notes**:
- Use Qdrant Cloud free tier or self-hosted Docker
- Collection: `book_chunks`
- Vector size: 768 (Gemini embedding dimension)
- Distance metric: Cosine

### 3. Chunking Strategy for Technical Content

**Decision**: 512 tokens per chunk with 50-token overlap, respecting section boundaries

**Rationale**:
- 512 tokens balances context richness vs retrieval precision
- Overlap prevents information loss at boundaries
- Section boundaries preserve semantic coherence
- Technical content benefits from larger chunks than typical web content

**Alternatives Considered**:
- 256 tokens: Too fragmented for technical explanations
- 1024 tokens: Too coarse, reduces retrieval precision
- Semantic chunking: More complex, marginal benefit for well-structured book

**Implementation Notes**:
- Use `langchain.text_splitter.RecursiveCharacterTextSplitter`
- Custom separators: ["\n## ", "\n### ", "\n\n", "\n", " "]
- Store metadata: chapter, section, page_start, page_end

### 4. Relevance Threshold Implementation

**Decision**: 0.7 cosine similarity threshold with graceful refusal

**Rationale**:
- Spec requires refusing low-confidence answers
- 0.7 balances recall (not too strict) vs precision (filters noise)
- Clear user feedback when threshold not met

**Alternatives Considered**:
- 0.5: Too permissive, would include irrelevant passages
- 0.8: Too strict, would refuse valid but partial matches
- No threshold: Would violate spec requirement

**Implementation Notes**:
- Qdrant query with score_threshold=0.7
- Return top 5 passages above threshold
- Refusal message: "I could not find information about this topic in the book."

### 5. Citation Extraction

**Decision**: Extract citations from chunk metadata during retrieval

**Rationale**:
- Citations are required by FR-003
- Metadata already stored during ingestion
- No additional processing needed at query time

**Implementation Notes**:
- Citation format: "Chapter X: [Title], Section Y: [Title] (p. Z)"
- Multiple citations listed when answer spans sections
- Citations included in response JSON, not embedded in text

### 6. Selected-Text Mode Implementation

**Decision**: Bypass vector retrieval; use provided text directly as LLM context

**Rationale**:
- FR-008 requires limiting context to selected text only
- No retrieval needed when user provides context
- Simpler implementation, faster response

**Implementation Notes**:
- Detect mode from request: `mode="selected_text"` + `selected_text` field present
- Validate minimum text length (10 characters per spec edge case)
- No citations in selected-text mode (text is self-contained)

## Technology Summary

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.11+ |
| Web Framework | FastAPI | 0.109+ |
| Agent Framework | OpenAI ChatKit SDK | chatkit-python latest |
| Agent SDK | OpenAI Agents SDK | openai-agents latest |
| LLM | Google Gemini Flash 2.5 | gemini-2.0-flash-exp |
| Embeddings | Gemini text-embedding-004 | latest |
| Vector Store | Qdrant | 1.7+ |
| Relational DB | Neon Postgres | 16+ |
| Testing | pytest + pytest-asyncio | latest |
| Deployment | Docker | latest |

## Open Questions (None)

All technical decisions resolved. Ready for Phase 1 design.
