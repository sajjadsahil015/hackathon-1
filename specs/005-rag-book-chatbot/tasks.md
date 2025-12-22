# Tasks: RAG Chatbot for Technical Book

**Input**: Design documents from `/specs/005-rag-book-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## User Story Summary

| Story | Title | Priority | Description |
|-------|-------|----------|-------------|
| US1 | Full-Book Context Question | P1 | Core RAG: question → search book → answer with citations |
| US2 | Selected-Text Context Question | P2 | Answer using only user-provided text selection |
| US3 | Source Attribution & Traceability | P3 | Enhanced citation formatting and verification |
| US4 | No Answer Available | P3 | Graceful refusal when relevance < 0.7 |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [x] T001 Create project structure per plan.md in src/rag_chatbot/
- [x] T002 Initialize Python 3.11+ project with pyproject.toml and requirements.txt
- [x] T003 [P] Create .env.example with required environment variables (GOOGLE_API_KEY, QDRANT_URL, DATABASE_URL, RELEVANCE_THRESHOLD)
- [x] T004 [P] Configure ruff for linting and formatting in pyproject.toml
- [x] T005 [P] Create Docker Compose file for local Qdrant in docker-compose.yml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create config module with Pydantic Settings in src/rag_chatbot/config.py
- [x] T007 [P] Create Citation model in src/rag_chatbot/models/citation.py
- [x] T008 [P] Create QueryMode enum, QueryRequest, QueryResponse models in src/rag_chatbot/models/query.py
- [x] T009 [P] Create models/__init__.py with exports in src/rag_chatbot/models/__init__.py
- [x] T010 Create Qdrant setup script with book_chunks collection in scripts/setup_qdrant.py
- [x] T011 Create Postgres database schema (book_metadata, chapters, sections) in scripts/setup_db.py
- [x] T012 Implement Gemini embedding service in src/rag_chatbot/services/embeddings.py
- [x] T013 [P] Create services/__init__.py with exports in src/rag_chatbot/services/__init__.py
- [x] T014 Create FastAPI app skeleton with health endpoint in src/rag_chatbot/main.py
- [x] T015 [P] Implement rate limiting middleware (10 req/min per IP) in src/rag_chatbot/api/middleware.py
- [x] T016 [P] Create api/__init__.py in src/rag_chatbot/api/__init__.py
- [x] T017 Create book ingestion pipeline (chunking, embedding, storage) in scripts/ingest_book.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Full-Book Context Question (Priority: P1)

**Goal**: Enable users to ask questions and receive answers grounded in book content with citations

**Independent Test**: Ask "What is sensor fusion in humanoid robots?" and verify response includes relevant citations

### Implementation for User Story 1

- [x] T018 [US1] Implement Qdrant vector search with relevance threshold in src/rag_chatbot/services/retrieval.py
- [x] T019 [US1] Implement Gemini response generation with context injection in src/rag_chatbot/services/generation.py
- [x] T020 [US1] Implement citation extraction from chunk metadata in src/rag_chatbot/services/citation.py
- [x] T021 [P] [US1] Create search_book_content agent tool in src/rag_chatbot/tools/search_book.py
- [x] T022 [P] [US1] Create get_citation agent tool in src/rag_chatbot/tools/get_citation.py
- [x] T023 [P] [US1] Create tools/__init__.py with exports in src/rag_chatbot/tools/__init__.py
- [x] T024 [US1] Create RAG agent with book-only instructions in src/rag_chatbot/agent.py
- [x] T025 [US1] Implement ChatKit server extending ChatKitServer in src/rag_chatbot/chatkit_server.py
- [x] T026 [US1] Add POST /chatkit endpoint with SSE streaming in src/rag_chatbot/main.py
- [x] T027 [US1] Add POST /query REST endpoint for JSON responses in src/rag_chatbot/api/routes.py
- [x] T028 [US1] Wire up full RAG pipeline: embed → retrieve → generate → respond in src/rag_chatbot/api/routes.py

**Checkpoint**: User Story 1 complete - full-book Q&A functional with citations

---

## Phase 4: User Story 2 - Selected-Text Context Question (Priority: P2)

**Goal**: Allow users to select text and ask questions using only that selection as context

**Independent Test**: Provide selected text + question "What does this mean?" and verify response uses only selected text

### Implementation for User Story 2

- [x] T029 [US2] Add selected_text mode handling to QueryRequest validation in src/rag_chatbot/models/query.py
- [x] T030 [US2] Implement direct context path (bypass retrieval) in generation service in src/rag_chatbot/services/generation.py
- [x] T031 [US2] Update agent to handle selected_text mode in src/rag_chatbot/agent.py
- [x] T032 [US2] Update /query endpoint to route by mode in src/rag_chatbot/api/routes.py
- [x] T033 [US2] Update ChatKit server respond() for selected_text mode in src/rag_chatbot/chatkit_server.py
- [x] T034 [US2] Add validation for minimum selected text length (10 chars) in src/rag_chatbot/api/routes.py

**Checkpoint**: User Story 2 complete - selected-text mode functional

---

## Phase 5: User Story 3 - Source Attribution & Traceability (Priority: P3)

**Goal**: Provide detailed, accurate citations that readers can use to find original content

**Independent Test**: Verify citations include chapter, section, page references that match actual book structure

### Implementation for User Story 3

- [x] T035 [US3] Enhance citation format with full chapter/section/page detail in src/rag_chatbot/services/citation.py
- [x] T036 [US3] Add citation deduplication for multi-passage answers in src/rag_chatbot/services/citation.py
- [x] T037 [US3] Add relevance_score to each citation in response in src/rag_chatbot/models/citation.py
- [x] T038 [US3] Create citation formatting helper for consistent output in src/rag_chatbot/services/citation.py

**Checkpoint**: User Story 3 complete - enhanced citations with full traceability

---

## Phase 6: User Story 4 - No Answer Available (Priority: P3)

**Goal**: Gracefully refuse when no relevant content found (relevance < 0.7)

**Independent Test**: Ask about topic not in book and verify standardized refusal message

### Implementation for User Story 4

- [x] T039 [US4] Implement relevance threshold check (0.7) in retrieval service in src/rag_chatbot/services/retrieval.py
- [x] T040 [US4] Create RefusalResponse model in src/rag_chatbot/models/query.py
- [x] T041 [US4] Add refusal path in generation service when no relevant passages in src/rag_chatbot/services/generation.py
- [x] T042 [US4] Return standardized refusal message per FR-004 in src/rag_chatbot/api/routes.py
- [x] T043 [US4] Handle speculative/opinion questions with refusal in src/rag_chatbot/agent.py

**Checkpoint**: User Story 4 complete - graceful refusal for out-of-scope questions

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T044 [P] Add GET /stats endpoint for service statistics in src/rag_chatbot/api/routes.py
- [x] T045 [P] Add structured logging throughout services in src/rag_chatbot/
- [x] T046 [P] Add error handling for Gemini API failures in src/rag_chatbot/services/
- [x] T047 [P] Add error handling for Qdrant connection failures in src/rag_chatbot/services/retrieval.py
- [x] T048 [P] Create pytest configuration in tests/conftest.py
- [x] T049 Run quickstart.md validation - test full setup flow
- [x] T050 Verify OpenAPI contract compliance with contracts/openapi.yaml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational completion
  - Stories can proceed in parallel or sequentially in priority order
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Start after Foundational - No dependencies on other stories
- **US2 (P2)**: Start after Foundational - Extends US1 generation service but independently testable
- **US3 (P3)**: Start after Foundational - Enhances US1 citation service but independently testable
- **US4 (P3)**: Start after Foundational - Adds refusal path to US1 retrieval but independently testable

### Within Each User Story

- Services before agent integration
- Agent before endpoints
- Core implementation before edge cases

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T003, T004, T005 can run in parallel
```

**Phase 2 (Foundational)**:
```
T007, T008, T009 can run in parallel (models)
T015, T016 can run in parallel (api setup)
```

**Phase 3 (US1)**:
```
T021, T022, T023 can run in parallel (tools)
```

**Phase 7 (Polish)**:
```
T044, T045, T046, T047, T048 can run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test full-book Q&A independently
5. Deploy/demo with core RAG functionality

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Full-book Q&A works → **MVP Deploy**
3. Add US2 → Selected-text mode works → Deploy
4. Add US3 → Enhanced citations → Deploy
5. Add US4 → Graceful refusal → Deploy
6. Polish → Production ready

### Task Counts

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 12 tasks
- **Phase 3 (US1)**: 11 tasks
- **Phase 4 (US2)**: 6 tasks
- **Phase 5 (US3)**: 4 tasks
- **Phase 6 (US4)**: 5 tasks
- **Phase 7 (Polish)**: 7 tasks
- **Total**: 50 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story independently testable after completion
- Commit after each task or logical group
- Relevance threshold: 0.7 cosine similarity
- Rate limit: 10 req/min per IP
