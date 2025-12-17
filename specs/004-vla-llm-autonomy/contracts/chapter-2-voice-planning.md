# Chapter Contract: Voice and Language-Based Robot Planning

**Chapter**: 02-voice-language-planning.md
**Module**: 4 - Vision-Language-Action
**Estimated Reading Time**: 50-65 minutes

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-2.1**: Trace a voice command through the complete voice-to-action pipeline
2. **LO-2.2**: Explain how LLMs decompose high-level instructions into executable subtasks
3. **LO-2.3**: Describe the grounding process that maps language to perceived objects
4. **LO-2.4**: Identify how language-based plans map to ROS 2 action servers

## Prerequisites

- Chapter 1: VLA architecture components
- Module 1: ROS 2 actions and services
- Module 3: Object detection and perception outputs
- Familiarity with API-based LLM usage

## Section Outline

### 2.1 The Voice-to-Action Pipeline (8 min)

**Content**:
- Overview of the four-stage pipeline
- Why voice is natural for human-robot interaction
- Pipeline components: Speech → Text → Plan → Actions
- End-to-end data flow

**Key Concepts**: Voice interface, pipeline architecture, modular design

**Diagram**: Complete pipeline flowchart with technology labels

### 2.2 Speech Recognition with Whisper (10 min)

**Content**:
- Role of automatic speech recognition (ASR)
- OpenAI Whisper capabilities and API usage
- Handling recognition errors and confidence
- Real-time vs batch processing considerations

**Key Concepts**: ASR, transcription, confidence scores, robustness

**Diagram**: Whisper processing flow (audio → preprocessing → model → text)

### 2.3 Intent Parsing: Understanding What the User Wants (10 min)

**Content**:
- From transcript to structured intent
- Intent components: action type, objects, locations, constraints
- LLM-based intent extraction
- Handling ambiguous or incomplete commands

**Key Concepts**: Intent, slot filling, semantic parsing, disambiguation

**Diagram**: Intent extraction showing input text and structured output

### 2.4 Task Decomposition: Breaking Down Complex Instructions (12 min)

**Content**:
- Why high-level instructions need decomposition
- LLM as task planner: prompt engineering for planning
- Generating subtask sequences
- Handling dependencies and ordering

**Key Concepts**: Task planning, decomposition, subtasks, dependencies

**Diagram**: LLM decomposition example ("fetch red cup" → subtask sequence)

**Example**: JSON task plan structure

### 2.5 Grounding: Connecting Language to Perception (10 min)

**Content**:
- The grounding problem: "the red cup" → which cup?
- Using perception outputs (Module 3) for grounding
- Multi-object disambiguation strategies
- Confidence and fallback handling

**Key Concepts**: Grounding, object resolution, disambiguation, perception integration

**Diagram**: Grounding process (language reference → perception query → resolved object)

### 2.6 Mapping to ROS 2 Action Primitives (10 min)

**Content**:
- Action primitive catalog for humanoid robots
- Mapping task plan subtasks to ROS 2 interfaces
- Action servers vs services for different primitive types
- Execution monitoring and feedback

**Key Concepts**: Action primitives, ROS 2 actions, execution feedback

**Table**: Action primitive catalog (name, ROS 2 interface, parameters)

**Diagram**: Subtask-to-action mapping flow

## Success Criteria Mapping

| Success Criterion | Section(s) | How Verified |
|-------------------|------------|--------------|
| SC-003: 85% trace voice command | 2.1, All | LO-2.1 walkthrough |
| SC-004: Explain LLM planning | 2.4 | LO-2.2 comprehension |

## Cross-References

- Chapter 1: VLA architecture (language model component)
- Module 1: ROS 2 actions and services (2.6)
- Module 3: Perception outputs (2.5 grounding)
- Chapter 3: Full pipeline in action (capstone)

## Key Takeaways

1. Voice-to-action requires four stages: recognition, parsing, planning, execution
2. Speech recognition (Whisper) converts audio to text with confidence
3. Intent parsing extracts structured meaning from natural language
4. LLMs can decompose complex instructions into executable subtask sequences
5. Grounding resolves language references to specific perceived objects
6. Action primitives provide safe, validated robot capabilities via ROS 2
