
# Feature Specification: RAG Chatbot for Technical Book

**Feature Branch**: `005-rag-book-chatbot`
**Created**: 2025-12-18
**Status**: Draft
**Input**: User description: "RAG Chatbot for Technical Book - Answer questions grounded strictly in book content with two query modes: full-book context search and user-selected-text answering"

## Clarifications

### Session 2025-12-18
- Q: What is the expected scale for concurrent users? → A: Up to 50 concurrent users (small-scale production)
- Q: Which LLM provider should the system use? → A: Google Gemini Flash 2.5

- Q: When retrieved passages have low relevance scores, what should happen? → A: Set minimum relevance threshold; refuse answer if no passage meets threshold (e.g., similarity > 0.7)


## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full-Book Context Question (Priority: P1)

A reader of the Physical AI & Humanoid Robotics book has a question about a concept mentioned in the book. They want to ask the chatbot and receive an answer that is grounded in the book's content, with references to where the information can be found.

**Why this priority**: This is the core value proposition - allowing readers to get contextual answers from the entire book content. Without this capability, the chatbot provides no value.

**Independent Test**: Can be fully tested by asking a question about a topic covered in the book and verifying the response cites relevant book sections.

**Acceptance Scenarios**:

1. **Given** a reader has loaded the chatbot interface, **When** they type a question about a concept from the book (e.g., "What is sensor fusion in humanoid robots?"), **Then** the system returns an answer derived from relevant book passages with citations to specific sections.

2. **Given** a reader asks a question, **When** the answer spans multiple chapters or sections, **Then** the response synthesizes information from all relevant passages and lists all source sections.

3. **Given** a reader asks a question about a topic not covered in the book, **When** no relevant content is found, **Then** the system responds with a clear message indicating the topic is not covered in the book content.

---
### User Story 2 - Selected-Text Context Question (Priority: P2)

A reader is reading a specific passage and does not understand a term or concept within that passage. They select the text and ask a clarifying question. The chatbot answers based only on the selected text without searching the broader book.

**Why this priority**: This provides focused, contextual clarification that improves comprehension during active reading. It builds on P1 but offers a more targeted experience.

**Independent Test**: Can be fully tested by selecting a passage, asking a question about it, and verifying the response only uses the selected text as context.

**Acceptance Scenarios**:

1. **Given** a reader has selected a paragraph from the book, **When** they ask "What does this mean?", **Then** the system explains the selected text without referencing other book sections.

2. **Given** a reader selects text containing technical terminology, **When** they ask about a specific term within the selection, **Then** the system explains that term using only the context provided in the selected text.

3. **Given** a reader asks a question that cannot be answered from the selected text alone, **When** the selected context is insufficient, **Then** the system indicates the answer cannot be determined from the selection and optionally suggests switching to full-book mode.

---
### User Story 3 - Source Attribution and Traceability (Priority: P3)

A reader wants to verify the chatbot's answer by checking the original book content. They need clear citations that point them to the exact location in the book.

**Why this priority**: Traceability builds trust and supports deeper learning by enabling readers to explore source material. It enhances P1 and P2 but is not essential for basic functionality.

**Independent Test**: Can be fully tested by asking a question and verifying that the response includes section/chapter references that correspond to actual book locations.

**Acceptance Scenarios**:

1. **Given** a reader receives an answer from the chatbot, **When** citations are included, **Then** each citation references a specific chapter, section, or page that the reader can navigate to.

2. **Given** an answer is synthesized from multiple book sections, **When** displayed to the reader, **Then** all contributing sections are listed with clear references.

---
### User Story 4 - No Answer Available (Priority: P3)

A reader asks a question that cannot be answered from the book content. The chatbot must gracefully refuse rather than hallucinate.

**Why this priority**: Preventing hallucination is critical for trust and educational integrity, but this is a constraint behavior rather than a primary feature.

**Independent Test**: Can be fully tested by asking questions outside the book's scope and verifying appropriate refusal responses.

**Acceptance Scenarios**:

1. **Given** a reader asks about a topic not covered in the book, **When** no relevant passages are found, **Then** the system responds with: "I could not find information about this topic in the book. Please try rephrasing or ask about a topic covered in the book."

2. **Given** a reader asks a speculative or opinion-based question, **When** no factual book content applies, **Then** the system declines to speculate and explains it only provides answers grounded in the book.

---
### Edge Cases

- What happens when the selected text is empty or too short (fewer than 10 characters)?
- How does the system handle questions in languages other than the book's language?
- What happens when the user's question is ambiguous and matches multiple unrelated sections?
- How does the system handle requests for information that exists in figures, diagrams, or tables rather than text?
- What happens when the book content contains contradictory information across different sections?
- How does the system respond to follow-up questions when there is no conversational memory?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept natural language questions from users and return answers grounded in the book content.
- **FR-002**: System MUST support two query modes: (a) full-book context search, and (b) user-selected-text-only answering.
- **FR-003**: System MUST include source citations (chapter, section, or page references) in every answer derived from book content.
- **FR-004**: System MUST refuse to answer questions when no relevant content is found in the book, providing a clear refusal message.
- **FR-005**: System MUST NOT generate speculative, opinionated, or externally-sourced answers - all responses must be traceable to book content.
- **FR-006**: System MUST process each query independently without retaining context from previous queries (stateless operation).
- **FR-007**: System MUST distinguish between "full-book mode" and "selected-text mode" based on user input or explicit mode selection.
- **FR-008**: In selected-text mode, System MUST limit its response context strictly to the provided text selection.
- **FR-009**: System MUST return responses in plain text or Markdown-compatible format suitable for display in reading interfaces.
- **FR-010**: System MUST handle queries where no answer is possible by returning a standardized "not found" response rather than attempting to guess.
- **FR-011**: System MUST enforce a minimum relevance threshold on retrieved passages; if no passage meets the threshold, the system refuses to answer rather than using low-confidence content.

### Key Entities

- **Book Content**: The full text of the Physical AI & Humanoid Robotics book, organized by chapters, sections, and pages. Contains the authoritative knowledge base for all answers.
- **Query**: A user's question, consisting of the question text and optionally a selected passage for context. Each query is independent (no session state).
- **Response**: The system's answer to a query, containing the answer text, source citations, and confidence indicators. Must be traceable to book content.
- **Citation**: A reference to a specific location in the book (chapter number, section title, page number) that supports the answer provided.
- **Selected Text**: An optional passage highlighted by the user that constrains the answer context to that specific excerpt only.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of questions about topics covered in the book receive answers that correctly cite relevant sections.
- **SC-002**: 100% of questions about topics not covered in the book result in a clear "not found" response rather than hallucinated content.
- **SC-003**: Users can receive a response to their question within 5 seconds of submission.
- **SC-004**: 90% of users report that citations accurately point to relevant book sections when verified.
- **SC-005**: In selected-text mode, 100% of responses use only the provided selection as context (no external book content leakage).
- **SC-006**: Responses are readable and concise, averaging under 300 words for typical clarification questions.
- **SC-007**: Users can complete a question-and-answer cycle in under 30 seconds total (including reading the response).
- **SC-008**: System supports up to 50 concurrent users without degradation in response time or availability.

## Assumptions

- The book content is available in a text-extractable format (not scanned images without OCR).
- The book has a clear chapter/section structure that can be used for citations.
- Users interact with the chatbot through a text-based interface (web, embedded reader, or similar).
- The book is written in a single primary language (assumed English unless specified otherwise).
- Figures, diagrams, and tables may have limited support initially; text content is prioritized.
- The chatbot is not responsible for user authentication or access control to the book content.

## Constraints

- **Knowledge Source**: Only the Physical AI & Humanoid Robotics book content may be used - no external knowledge bases, internet search, or general AI knowledge.
- **Architecture**: RAG-based retrieval system (no fine-tuning of language models on book content).
- **Style**: Technical, clear, and non-speculative responses only.
- **Memory**: No conversational memory - each query is processed independently.
- **Output Format**: Plain text or Markdown-compatible responses.
- **LLM Provider**: Google Gemini Flash 2.5 for both embeddings and response generation.

## Out of Scope

- General-purpose chatbot capabilities
- Internet or external knowledge search
- Opinionated or speculative answers
- Conversational memory beyond a single query
- User accounts or personalization features
- Integration with e-commerce or book purchasing
- Support for multiple books simultaneously
- Audio/voice interaction
- Translation services
