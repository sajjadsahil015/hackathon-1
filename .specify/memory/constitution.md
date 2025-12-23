<!--
## Sync Impact Report
- Version change: 0.0.0 → 1.0.0
- Modified principles: None (initial version)
- Added sections:
  - Six core principles (Technical Accuracy, Source Integrity, Spec-Driven Reproducibility,
    Practical Rigor, API Currency, Conceptual Clarity)
  - Technical Constraints section
  - Quality Standards section
  - Governance section with amendment procedures
- Removed sections: None
- Templates requiring updates:
  - `.specify/templates/plan-template.md` - ✅ Compatible (Constitution Check section exists)
  - `.specify/templates/spec-template.md` - ✅ Compatible (requirements structure aligned)
  - `.specify/templates/tasks-template.md` - ✅ Compatible (phase structure supports principles)
- Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Technical Book Constitution

## Core Principles

### I. Technical Accuracy

All technical claims, explanations, and code examples MUST be verifiable against
official documentation, peer-reviewed sources, or authoritative references.

- Technical statements MUST cite or be traceable to official documentation
- Prefer primary sources (official docs, RFCs, published papers) over secondary
- When official documentation is unavailable, clearly mark content as "community-derived"
  or "inferred from source code"
- Speculation or forward-looking statements MUST be explicitly labeled as such
- Rationale: A technical book loses all value if readers cannot trust its accuracy

### II. Source Integrity

No hallucinated APIs, tools, methods, or references are permitted. Every external
reference MUST exist and be accessible.

- API signatures, function names, and parameters MUST match current stable releases
- Tool versions MUST be explicitly stated with pinned dependencies where applicable
- URLs and documentation links MUST be validated before publication
- If a source becomes unavailable, content MUST be updated or removed
- Rationale: Phantom references waste reader time and destroy credibility

### III. Spec-Driven Reproducibility

All content and implementations MUST be reproducible following the spec-driven
development methodology.

- Each module MUST have a clear specification before implementation
- Code examples MUST include environment setup and dependency requirements
- Tutorials MUST be tested end-to-end on clean environments before publication
- Version-specific instructions MUST specify exact versions used during testing
- Rationale: Reproducibility is the foundation of technical education

### IV. Practical Rigor

Theory MUST be paired with real tools, working code, and hands-on exercises.

- Conceptual explanations MUST include practical demonstrations
- Simulation and real-world examples MUST use industry-standard tools
  (ROS 2, Gazebo, Unity, NVIDIA Isaac, etc.)
- Code MUST be runnable, not pseudocode (unless explicitly labeled)
- Performance claims MUST include benchmarks or measurable validation
- Rationale: Robotics is an applied field; theory without practice is incomplete

### V. API Currency

All code examples and API references MUST match current stable API versions
at time of writing.

- Use long-term support (LTS) or stable releases, not alpha/beta/RC versions
- Document API version explicitly at the start of each code section
- When APIs change, content MUST be updated or versioned appropriately
- Deprecated APIs MUST NOT be used without explicit migration guidance
- Rationale: Outdated code examples are worse than no examples

### VI. Conceptual Clarity

Clear separation MUST be maintained between concepts, implementation details,
and speculation about future developments.

- Theoretical foundations MUST be presented before implementation
- Implementation-specific details MUST NOT be conflated with general concepts
- Future roadmap items MUST be clearly distinguished from current capabilities
- Different abstraction levels (hardware, firmware, middleware, application)
  MUST be explicitly identified
- Rationale: Confused abstraction levels lead to confused readers

## Technical Constraints

The project operates within the following technical boundaries:

**Platform & Deployment:**
- Documentation platform: Docusaurus static site
- Hosting: GitHub Pages
- Development tooling: Spec-Kit Plus, Claude Code

**Technical Scope:**
- Primary domain: Physical AI, Embodied Intelligence, Humanoid Robotics
- Core technologies: ROS 2, Gazebo, Unity, NVIDIA Isaac Sim
- AI focus: Vision-Language-Action (VLA) models, embodied reasoning

**RAG Chatbot Stack:**
- Agent framework: OpenAI Agents SDK / ChatKit
- Backend: FastAPI (Python)
- Vector store: Qdrant
- Relational store: Neon Postgres
- Embedding model: Gemini (free tier)
- Chatbot scope: Full-book Q&A and user-selected-text contextual questions only

**Explicit Non-Goals:**
- General-purpose chatbot functionality beyond book content
- Real-time robot control interfaces
- Hardware-specific drivers or firmware

## Quality Standards

### Content Quality Gates

- [ ] All code examples tested on documented environment
- [ ] All external links validated and accessible
- [ ] All API references match stated version
- [ ] No placeholder or TODO content in published sections
- [ ] Technical reviewer sign-off for each module

### Code Quality Requirements

- All code MUST include explicit imports and dependencies
- Environment setup MUST be documented (OS, Python version, packages)
- Error handling MUST be present for all I/O operations
- Comments MUST explain "why" not "what" where logic is non-obvious

### Testing Requirements

- Tutorial code MUST include expected output for verification
- RAG chatbot MUST have integration tests for retrieval accuracy
- Simulation examples MUST include validation criteria

### Documentation Requirements

- Each chapter MUST have learning objectives stated upfront
- Prerequisites MUST be explicitly listed
- Cross-references MUST use relative links that resolve correctly

## Governance

This constitution supersedes all other practices for this project. Amendments
require the following process:

1. **Proposal**: Document the proposed change with rationale
2. **Review**: Technical review for consistency with existing principles
3. **Approval**: Explicit sign-off before merging
4. **Migration**: Update all affected artifacts if principles change

**Versioning Policy:**
- MAJOR version: Principle removal or fundamental redefinition
- MINOR version: New principle or significant expansion
- PATCH version: Clarifications, typos, non-semantic changes

**Compliance Review:**
All pull requests and code reviews MUST verify compliance with this constitution.
Use `/sp.plan` Constitution Check to validate alignment before implementation.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
