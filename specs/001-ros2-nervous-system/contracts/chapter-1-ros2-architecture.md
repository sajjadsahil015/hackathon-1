# Chapter Contract: ROS 2 Architecture and Communication

**Module**: 1 - The Robotic Nervous System | **Chapter**: 1 of 3
**Target File**: `docs/module-1-ros2/01-ros2-architecture.md`
**Est. Reading Time**: 45-60 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-1.1**: Explain the ROS 2 communication model using the nervous system analogy
2. **LO-1.2**: Define nodes, topics, services, and messages with their characteristics
3. **LO-1.3**: Identify when to use topics vs. services for a given robotics scenario
4. **LO-1.4**: Diagram a simple ROS 2 node graph with appropriate connections
5. **LO-1.5**: Describe the role of message types in ensuring type-safe communication

---

## Chapter Outline

### Section 1.1: The Robot's Nervous System (10 min)
**Objective**: Establish the mental model for ROS 2 concepts

**Content**:
- Opening hook: How do robot parts "talk" to each other?
- The nervous system analogy introduction
- Mapping table: neurons→nodes, pathways→topics, commands→services
- Why distributed communication matters for robots

**Diagram**: D1.1 - Nervous System Analogy mindmap

**Success Check**: Reader can explain the analogy to a peer

---

### Section 1.2: Topics - The Sensory Pathways (12 min)
**Objective**: Deep understanding of publish-subscribe pattern

**Content**:
- What is a topic? Named channel with typed messages
- Publishers and subscribers: many-to-many relationship
- Message flow: asynchronous, fire-and-forget
- Real-world example: camera images flowing to perception
- When to use topics: continuous data, sensor streams

**Diagram**: D1.3 - Topic publish-subscribe sequence

**Code Snippet**: C1.1 - Message type definition (5 lines YAML)

**Success Check**: Reader can list 3 scenarios where topics are appropriate

---

### Section 1.3: Services - The Motor Commands (12 min)
**Objective**: Deep understanding of request-response pattern

**Content**:
- What is a service? Named endpoint for discrete operations
- Request and response messages: typed pair
- Service flow: synchronous, blocking call
- Real-world example: spawning an entity, changing mode
- When to use services: one-time operations, configuration

**Diagram**: D1.4 - Service request-response sequence

**Code Snippet**: C1.2 - Service definition (8 lines YAML)

**Success Check**: Reader can list 3 scenarios where services are appropriate

---

### Section 1.4: Nodes in the Graph (12 min)
**Objective**: Understand node composition and topology

**Content**:
- Nodes as independent processes
- Node naming and namespaces
- The computation graph: visualizing node topology
- Typical robot node graph example
- Node lifecycle overview (create, configure, activate)

**Diagram**: D1.2 - ROS 2 node graph (camera, lidar, perception, planner, controller)

**Success Check**: Reader can identify nodes and connections in a diagram

---

### Section 1.5: Choosing Communication Patterns (10 min)
**Objective**: Practical decision-making for communication design

**Content**:
- Decision framework: topics vs. services vs. actions
- Key questions: Is data continuous? Is response needed?
- Common patterns in robotics
- Actions preview (covered in later modules)
- Summary table with use cases

**Diagram**: D1.5 - Communication pattern decision tree

**Success Check**: Reader can justify pattern choice for 5 scenarios

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-001 (nodes as processes) | 1.4 | Node definition and lifecycle |
| FR-002 (topics as channels) | 1.2 | Full section on topics |
| FR-003 (services as request-response) | 1.3 | Full section on services |
| FR-004 (nervous system analogy) | 1.1 | Opening section with mapping |
| FR-010 (cite official docs) | All | References to ROS 2 docs |
| FR-011 (concept-first style) | All | Theory before code |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D1.1 | Conceptual | Nervous system to ROS 2 mapping | Mermaid mindmap |
| D1.2 | Architecture | 5-node robot graph | Mermaid graph |
| D1.3 | Sequence | Topic pub-sub flow | Mermaid sequence |
| D1.4 | Sequence | Service request-response | Mermaid sequence |
| D1.5 | Flowchart | Communication pattern decision | Mermaid flowchart |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| C1.1 | YAML | 5 | Message type example |
| C1.2 | YAML | 8 | Service definition example |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-001 (90% identify topic vs service) | Section 1.5 decision framework + exercises |
| SC-002 (diagram 5-node graph in 10 min) | Section 1.4 graph example + practice |

---

## Chapter Dependencies

**Requires**: None (first chapter of first module)

**Enables**:
- Chapter 2: Python agents use nodes, topics, services
- Chapter 3: URDF loaded and visualized via ROS 2

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] Nervous system analogy consistently applied
- [ ] Topics and services clearly differentiated
- [ ] Diagrams support comprehension (not just decoration)
- [ ] Code snippets minimal and illustrative
- [ ] Success checks embedded at section ends
- [ ] Official ROS 2 documentation cited
- [ ] Concept-first: theory before any code
- [ ] No installation or setup instructions
- [ ] ~45-60 minute reading time
