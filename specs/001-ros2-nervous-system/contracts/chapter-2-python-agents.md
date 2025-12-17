# Chapter Contract: Python Agents with rclpy

**Module**: 1 - The Robotic Nervous System | **Chapter**: 2 of 3
**Target File**: `docs/module-1-ros2/02-python-agents-rclpy.md`
**Est. Reading Time**: 40-50 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-2.1**: Describe the structure of an rclpy node (initialization, callbacks, spin)
2. **LO-2.2**: Explain how publishers and subscribers connect nodes in Python
3. **LO-2.3**: Identify where AI decision logic executes within the rclpy callback model
4. **LO-2.4**: Outline the lifecycle of an AI agent node from sensor input to command output
5. **LO-2.5**: Recognize callback patterns for processing sensor data

---

## Chapter Outline

### Section 2.1: rclpy Node Structure (12 min)
**Objective**: Understand the anatomy of a Python ROS 2 node

**Content**:
- rclpy: The Python client library for ROS 2
- Minimal node structure: class inheriting from Node
- Initialization: `super().__init__()` with node name
- The main entry point pattern
- Spin: keeping the node alive and processing callbacks

**Diagram**: D2.1 - rclpy node structure (class diagram)

**Code Snippet**: C2.1 - Minimal rclpy node (15 lines)

**Success Check**: Reader can identify the 4 essential parts of an rclpy node

---

### Section 2.2: Publishers and Subscribers (12 min)
**Objective**: Implement topic-based communication in Python

**Content**:
- Creating a publisher: `create_publisher(msg_type, topic, qos)`
- Publishing messages: `publisher.publish(msg)`
- Creating a subscriber: `create_subscription(msg_type, topic, callback, qos)`
- Callback function signature and message access
- Connecting nodes through topics

**Code Snippet**: C2.2 - Publisher setup (8 lines)
**Code Snippet**: C2.3 - Subscriber with callback (12 lines)

**Success Check**: Reader can trace message flow from publisher to subscriber callback

---

### Section 2.3: Service Clients and Servers (10 min)
**Objective**: Implement request-response communication in Python

**Content**:
- Creating a service server: `create_service(srv_type, name, callback)`
- Service callback: receiving request, returning response
- Creating a service client: `create_client(srv_type, name)`
- Calling a service: async pattern with future
- When to use services in agent design

**Code Snippet**: C2.4 - Service server (15 lines)

**Success Check**: Reader can explain the service call flow

---

### Section 2.4: AI Agent Integration (12 min)
**Objective**: Connect AI decision-making to ROS 2 node structure

**Content**:
- The AI agent pattern: sense → decide → act
- Where decisions happen in the callback model
- Timer-based decision loops for periodic inference
- State management across callbacks
- Example: obstacle avoidance agent structure

**Diagram**: D2.2 - Callback execution model
**Diagram**: D2.3 - AI agent integration points
**Diagram**: D2.4 - Sensor → Decision → Actuator flow

**Code Snippet**: C2.5 - AI decision callback (10 lines)

**Success Check**: Reader can outline an AI agent node for a given scenario

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-005 (rclpy node structure) | 2.1 | Full section with code |
| FR-006 (AI decision integration) | 2.4 | Full section on agent pattern |
| FR-009 (rclpy with version) | All | All code uses rclpy |
| FR-010 (cite official docs) | All | References to rclpy API |
| FR-011 (concept-first style) | All | Theory before code |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D2.1 | Architecture | rclpy node class structure | Mermaid class |
| D2.2 | Flowchart | Callback execution model | Mermaid flowchart |
| D2.3 | Architecture | AI agent integration points | Mermaid block |
| D2.4 | Sequence | Sensor → Decision → Actuator | Mermaid sequence |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| C2.1 | Python | 15 | Minimal rclpy node |
| C2.2 | Python | 8 | Publisher setup |
| C2.3 | Python | 12 | Subscriber with callback |
| C2.4 | Python | 15 | Service server |
| C2.5 | Python | 10 | AI decision callback |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-003 (85% outline agent node) | Section 2.4 agent pattern + structure |
| SC-004 (identify pub/sub in 5 min) | Section 2.2 clear code patterns |

---

## Chapter Dependencies

**Requires**:
- Chapter 1: Understanding of nodes, topics, services, messages

**Enables**:
- Chapter 3: Python context for loading and using URDF
- Module 2-4: All use rclpy patterns for agent implementation

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] rclpy patterns shown with minimal, readable code
- [ ] AI agent integration clearly explained (not just ROS basics)
- [ ] Callback model thoroughly covered
- [ ] Code snippets are complete enough to understand, minimal enough to focus
- [ ] Success checks embedded at section ends
- [ ] Official rclpy documentation cited
- [ ] Concept-first: theory before each code block
- [ ] No full working programs (concept-first approach)
- [ ] ~40-50 minute reading time
