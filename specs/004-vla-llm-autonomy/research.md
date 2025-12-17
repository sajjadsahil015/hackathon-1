# Research: Module 4 - Vision-Language-Action (VLA)

**Date**: 2025-12-16
**Branch**: `004-vla-llm-autonomy`
**Purpose**: Resolve technical decisions and document research findings for VLA module

## VLA System Architecture Patterns

### Decision: VLA Architecture Model to Present

**Choice**: Present generalized VLA architecture pattern (not specific model implementations)

**Rationale**:
- Specific models (RT-2, PaLM-E, VIMA) evolve rapidly; pattern remains stable
- Constitution Principle VI (Conceptual Clarity) requires separating concepts from implementations
- Readers need transferable understanding, not model-specific knowledge

**Alternatives Considered**:
- Deep-dive on RT-2 architecture: Rejected (too specific, Google-proprietary)
- Survey multiple models in detail: Rejected (scope creep, rapidly outdated)
- Focus only on open-source models: Rejected (limits conceptual completeness)

### Key VLA Components to Cover

1. **Vision Encoder**: Transforms visual input to embeddings
   - Types: CNN-based (ResNet), Transformer-based (ViT)
   - Output: Visual tokens/embeddings for fusion

2. **Language Model**: Processes text and generates plans
   - Architecture: Transformer decoder (GPT-style)
   - Role: Reasoning, task decomposition, action generation

3. **Multimodal Fusion**: Combines vision and language
   - Approaches: Early fusion, late fusion, cross-attention
   - Output: Joint representation for action prediction

4. **Action Decoder**: Generates robot actions
   - Output types: Discrete actions, continuous control, action tokens
   - Connection to ROS 2: Action servers and services

## Voice-to-Action Pipeline

### Decision: Pipeline Architecture

**Choice**: Four-stage pipeline (Speech → Text → Plan → Actions)

**Rationale**:
- Clear separation of concerns matches modular ROS 2 design
- Each stage can be independently tested and replaced
- Aligns with industry practice (Whisper → LLM → execution)

**Pipeline Stages**:

```text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Speech    │───▶│   Intent    │───▶│    Task     │───▶│   Action    │
│ Recognition │    │   Parsing   │    │   Planning  │    │  Execution  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     Whisper          LLM parse         LLM decompose       ROS 2 actions
```

### Speech Recognition

**Choice**: OpenAI Whisper API (cloud-based)

**Rationale**:
- Constitution constraint: API-based LLM usage (not training)
- Whisper is industry standard with excellent accuracy
- Cloud API simplifies deployment for educational context

### Intent Parsing and Task Planning

**Choice**: LLM-based approach with structured output

**Rationale**:
- LLMs excel at natural language understanding
- Can generate structured task plans from ambiguous commands
- Aligns with spec FR-004 (LLM decomposition of instructions)

**Output Format**: JSON task plan with action sequence

```json
{
  "intent": "fetch_object",
  "target": "red cup",
  "location": "kitchen table",
  "subtasks": [
    {"action": "navigate_to", "target": "kitchen table"},
    {"action": "detect_object", "target": "red cup"},
    {"action": "grasp", "target": "red cup"},
    {"action": "navigate_to", "target": "user location"},
    {"action": "release", "target": "red cup"}
  ]
}
```

## LLM-to-ROS 2 Integration

### Decision: Action Primitive Mapping

**Choice**: Map LLM outputs to predefined ROS 2 action primitives

**Rationale**:
- Maintains safety through bounded action space
- LLM selects from validated primitives, not arbitrary commands
- Aligns with spec Key Entity "Action Primitive"

**Action Primitive Catalog**:

| Primitive | ROS 2 Interface | Parameters |
|-----------|-----------------|------------|
| `navigate_to` | Action: NavigateToPose | goal_pose |
| `look_at` | Action: LookAt | target_point |
| `grasp` | Action: Grasp | object_id |
| `release` | Action: Release | - |
| `speak` | Service: TextToSpeech | text |
| `wait` | - | duration |

### Grounding Strategy

**Decision**: Visual grounding through object detection

**Choice**: Use perception module output (Module 3) for grounding

**Rationale**:
- Builds on prior module knowledge (Isaac Sim perception)
- Separates language understanding from visual grounding
- Matches spec FR-006 (grounding explanation)

**Grounding Pipeline**:
1. Extract object references from language ("the red cup")
2. Query perception system for matching objects
3. Resolve to specific object IDs with poses
4. Pass resolved references to action primitives

## Capstone Task Selection

### Decision: Example Autonomous Task

**Choice**: "Fetch a drink from the kitchen" scenario

**Rationale**:
- Exercises all four modules:
  - Module 1: ROS 2 communication for all components
  - Module 2: Simulation environment (kitchen)
  - Module 3: Perception (object detection), navigation (Nav2)
  - Module 4: VLA (voice command, planning, execution)
- Relatable to readers (household robot scenario)
- Decomposable into clear subtasks

**Task Breakdown for Capstone**:

1. **Voice Input**: "Robot, bring me a drink from the kitchen"
2. **Speech Recognition**: Whisper transcription
3. **Intent Parsing**: Identify fetch task, target (drink), location (kitchen)
4. **Task Planning**: LLM generates subtask sequence
5. **Grounding**: Perception identifies "drink" objects in kitchen
6. **Navigation**: Nav2 path planning to kitchen
7. **Manipulation**: Grasp selected drink (conceptual only per out-of-scope)
8. **Return Navigation**: Nav2 path to user
9. **Completion**: Verbal confirmation

## Diagram Requirements

### Chapter 1: VLA Architecture
1. VLA system block diagram (vision encoder, language model, action decoder)
2. Multimodal fusion comparison (early vs late vs cross-attention)
3. VLA vs single-modality comparison diagram

### Chapter 2: Voice-to-Action Pipeline
1. End-to-end voice pipeline flowchart
2. LLM task decomposition example
3. Grounding process diagram
4. ROS 2 action primitive mapping

### Chapter 3: Capstone
1. Complete autonomy stack diagram (all modules integrated)
2. "Fetch drink" scenario sequence diagram
3. Module responsibility mapping for autonomous task
4. Data flow diagram through entire pipeline

## Style and Terminology

### Canonical Terms (per spec Key Entities)

| Term | Definition | Avoid |
|------|------------|-------|
| VLA System | Integrated vision-language-action architecture | VLM (ambiguous) |
| Voice Command | Spoken instruction (audio) | Speech command |
| Intent | Semantic meaning from language | Goal (too generic) |
| Task Plan | Sequence of subtasks from high-level instruction | Plan (too generic) |
| Action Primitive | Atomic robot capability via ROS 2 | Action (too generic) |
| Grounding | Mapping language to perception | Resolution |
| Autonomy Stack | Complete integrated system | Robot system |

### Writing Style Guidelines

- **Concept-first**: Explain "why" before "how"
- **Analogies**: Use "robot brain" analogy for VLA (connects to Module 3 title)
- **Diagrams**: Introduce every major concept with a diagram first
- **Code**: Minimal, pseudocode-style when needed
- **Cross-references**: Link to prior modules for prerequisites

## Source References

### Primary Sources (Official Documentation)
- OpenAI Whisper API: https://platform.openai.com/docs/guides/speech-to-text
- OpenAI GPT API: https://platform.openai.com/docs/guides/text-generation
- ROS 2 Actions: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Actions.html
- Nav2: https://nav2.org/
- Isaac Sim: https://developer.nvidia.com/isaac-sim

### Secondary Sources (Academic/Research)
- RT-2: Google DeepMind (for architectural patterns, not implementation)
- PaLM-E: Google Research (multimodal embodied reasoning patterns)
- SayCan: Google (language grounding for robotics)

---

**Research Complete**: All NEEDS CLARIFICATION items resolved. Ready for Phase 1 design artifacts.
