---
id: 0004
title: Add ChatKit SDK Integration
stage: plan
date: 2025-12-19
surface: agent
model: claude-opus-4-5-20251101
feature: 005-rag-book-chatbot
branch: 005-rag-book-chatbot
user: user
command: direct request
labels: ["chatkit", "agent-framework", "sse-streaming", "integration"]
links:
  spec: specs/005-rag-book-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-rag-book-chatbot/plan.md
  - specs/005-rag-book-chatbot/research.md
  - specs/005-rag-book-chatbot/quickstart.md
tests:
  - null
---

## Prompt

i forget to tell you that i want to use chatkit for agent building and the latest documentation of openai chatkit sdk is available in context7 mcp server so add this in in files where needed to be add

## Response snapshot

Integrated OpenAI ChatKit SDK into the RAG chatbot planning artifacts. Fetched ChatKit documentation from Context7 MCP server and updated:

1. **plan.md**: Added ChatKit as agent framework, updated architecture diagram to show ChatKitServer layer and RAG Agent with tools, added new source files (chatkit_server.py, agent.py, tools/)
2. **research.md**: Added new research section for ChatKit SDK with rationale, alternatives, and implementation notes including FastAPI endpoint pattern
3. **quickstart.md**: Added ChatKit package installation, ChatKit streaming endpoint example with SSE response format, updated project structure

Key ChatKit patterns integrated:
- `RAGChatKitServer` extending `ChatKitServer`
- `respond()` method returning `AsyncIterator[ThreadStreamEvent]`
- `AgentContext` for thread/store management
- `stream_agent_response()` for SSE streaming
- Agent tools: `search_book_content`, `get_citation`

## Outcome

- Impact: Added agent orchestration layer with streaming support
- Tests: None (planning phase)
- Files: 3 files updated (plan.md, research.md, quickstart.md)
- Next prompts: Run /sp.tasks to generate implementation tasks
- Reflection: ChatKit provides clean abstraction for streaming agent responses, well-suited for RAG chatbot with real-time answer delivery

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement ChatKitServer with Gemini as model provider
