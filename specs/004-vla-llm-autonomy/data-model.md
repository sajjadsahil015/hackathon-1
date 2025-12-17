# Data Model: Module 4 - Vision-Language-Action (VLA)

**Date**: 2025-12-16
**Branch**: `004-vla-llm-autonomy`

## Key Entities

### VLA System

**Definition**: Integrated architecture processing visual observations and language commands to produce robot actions.

**Attributes**:
- vision_encoder: Component transforming images to embeddings
- language_model: Component processing text and generating plans
- fusion_module: Component combining vision and language representations
- action_decoder: Component generating robot action outputs

**Relationships**:
- Contains multiple Voice Commands (input)
- Generates multiple Task Plans (output)
- Uses Grounding to resolve references

### Voice Command

**Definition**: Spoken instruction captured as audio waveform, processed through speech recognition.

**Attributes**:
- audio_waveform: Raw audio data
- transcript: Text output from speech recognition
- confidence: Recognition confidence score
- timestamp: When command was issued

**Relationships**:
- Parsed into one Intent
- Part of VLA System input

### Intent

**Definition**: Semantic meaning extracted from language input.

**Attributes**:
- action_type: Category of action requested (fetch, navigate, manipulate)
- target_objects: List of referenced objects
- spatial_references: Location descriptions
- constraints: Timing, ordering, or other constraints

**Relationships**:
- Derived from one Voice Command
- Decomposed into one Task Plan

### Task Plan

**Definition**: Sequence of subtasks generated from high-level instruction.

**Attributes**:
- subtasks: Ordered list of Action Primitives
- dependencies: Prerequisites between subtasks
- estimated_duration: Expected completion time
- fallback_strategy: What to do if subtask fails

**Relationships**:
- Generated from one Intent
- Contains multiple Action Primitives

### Action Primitive

**Definition**: Atomic robot capability executable via ROS 2 action server.

**Attributes**:
- name: Canonical action name (navigate_to, grasp, release, look_at)
- parameters: Action-specific parameters
- ros2_interface: Corresponding ROS 2 action/service type
- preconditions: Required state before execution
- postconditions: Expected state after execution

**Relationships**:
- Part of Task Plan
- Executed by ROS 2 action server

### Grounding

**Definition**: Process of mapping language references to objects in robot's perception.

**Attributes**:
- language_reference: Original text reference ("the red cup")
- object_candidates: Potential matches from perception
- resolved_object: Selected object with pose
- confidence: Grounding confidence score

**Relationships**:
- Links Intent target_objects to perception outputs
- Required for Action Primitive parameter resolution

### Autonomy Stack

**Definition**: Complete integrated system from sensors through reasoning to actuators.

**Attributes**:
- perception_layer: Sensor input and processing (Module 3)
- localization_layer: VSLAM and pose estimation (Module 3)
- planning_layer: VLA task planning (Module 4)
- control_layer: Action execution (Module 1 ROS 2)

**Relationships**:
- Integrates all book modules
- Processes Voice Commands to robot motion

## Chapter-Entity Mapping

### Chapter 1: VLA Architecture

| Section | Primary Entities | Diagrams |
|---------|------------------|----------|
| 1.1 Introduction to VLA | VLA System | VLA overview diagram |
| 1.2 Vision Encoding | VLA System.vision_encoder | Vision encoder pipeline |
| 1.3 Language Processing | VLA System.language_model | LLM architecture diagram |
| 1.4 Multimodal Fusion | VLA System.fusion_module | Fusion comparison diagram |
| 1.5 Action Decoding | VLA System.action_decoder | Action space diagram |

### Chapter 2: Voice and Language-Based Planning

| Section | Primary Entities | Diagrams |
|---------|------------------|----------|
| 2.1 Voice-to-Action Overview | Voice Command, Intent | Pipeline flowchart |
| 2.2 Speech Recognition | Voice Command | Whisper pipeline |
| 2.3 Intent Parsing | Intent | Intent extraction diagram |
| 2.4 Task Decomposition | Task Plan, Intent | LLM planning diagram |
| 2.5 Grounding | Grounding | Grounding process diagram |
| 2.6 ROS 2 Action Mapping | Action Primitive | Primitive catalog table |

### Chapter 3: Capstone - The Autonomous Humanoid

| Section | Primary Entities | Diagrams |
|---------|------------------|----------|
| 3.1 The Complete Stack | Autonomy Stack | Full stack diagram |
| 3.2 Module Integration | All entities | Integration architecture |
| 3.3 Scenario: Fetch a Drink | All entities | Sequence diagram |
| 3.4 Data Flow Tracing | All entities | Data flow diagram |
| 3.5 Gaps and Future Work | Autonomy Stack | Gap analysis table |

## Diagram Specifications

### D1: VLA System Overview
- **Type**: Block diagram
- **Elements**: Vision encoder, Language model, Fusion, Action decoder
- **Flow**: Left-to-right (input → output)
- **Annotations**: Data types at each stage

### D2: Voice-to-Action Pipeline
- **Type**: Flowchart
- **Elements**: Speech → Text → Intent → Plan → Actions
- **Technology labels**: Whisper, GPT, ROS 2
- **Example data**: "Fetch red cup" traced through

### D3: Grounding Process
- **Type**: Sequence diagram
- **Actors**: Language Parser, Perception System, Grounding Module
- **Messages**: Query, candidates, selection

### D4: Complete Autonomy Stack
- **Type**: Layered architecture diagram
- **Layers**: Perception, Localization, Planning, Control
- **Module labels**: Module 1-4 attribution per layer

### D5: Fetch Drink Scenario
- **Type**: Sequence diagram
- **Timeline**: Command → Recognition → Planning → Navigation → Grasp → Return
- **Module attribution**: Color-coded by module

## Validation Checklist

- [ ] All spec Key Entities represented in data model
- [ ] All functional requirements traceable to chapter sections
- [ ] All diagrams support specific learning objectives
- [ ] Entity relationships match spec acceptance scenarios
- [ ] Terminology consistent with research.md canonical terms
