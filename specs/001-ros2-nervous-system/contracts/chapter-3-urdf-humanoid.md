# Chapter Contract: URDF for Humanoid Robots

**Module**: 1 - The Robotic Nervous System | **Chapter**: 3 of 3
**Target File**: `docs/module-1-ros2/03-urdf-humanoid.md`
**Est. Reading Time**: 40-50 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-3.1**: Explain the purpose of URDF for robot description and simulation
2. **LO-3.2**: Identify link elements and their properties (visual, collision, inertial)
3. **LO-3.3**: Describe joint types and their motion constraints
4. **LO-3.4**: Interpret a URDF snippet representing a humanoid limb
5. **LO-3.5**: Understand the kinematic chain structure of a humanoid robot

---

## Chapter Outline

### Section 3.1: What is URDF? (10 min)
**Objective**: Understand URDF's role in robotics

**Content**:
- URDF: Unified Robot Description Format
- Purpose: Describing robot structure for simulation and visualization
- XML-based format with standardized elements
- How URDF relates to ROS 2 (robot_state_publisher, tf2)
- URDF vs. runtime communication (static structure vs. dynamic data)

**Diagram**: D3.1 - URDF element hierarchy

**Success Check**: Reader can explain why URDF is needed separately from ROS 2 communication

---

### Section 3.2: Links - The Robot's Skeleton (12 min)
**Objective**: Understand link elements and their properties

**Content**:
- Links as rigid body segments (like bones)
- Visual properties: what the robot looks like
- Collision properties: what the physics engine uses
- Inertial properties: mass and moments of inertia
- Origin and coordinate frames

**Code Snippet**: C3.1 - Basic link definition (10 lines XML)

**Success Check**: Reader can identify the three property types of a link

---

### Section 3.3: Joints - Where Movement Happens (12 min)
**Objective**: Understand joint types and their constraints

**Content**:
- Joints as connections between links
- Parent-child relationship
- Joint types for humanoids:
  - Revolute: rotation with limits (elbows, knees)
  - Continuous: unlimited rotation (wheels)
  - Prismatic: linear motion
  - Fixed: rigid attachment
- Joint properties: axis, limits, dynamics

**Diagram**: D3.3 - Joint types visualization

**Code Snippet**: C3.2 - Joint definition (12 lines XML)

**Success Check**: Reader can select appropriate joint type for a given motion

---

### Section 3.4: Humanoid Robot Structure (12 min)
**Objective**: Apply URDF concepts to humanoid robots

**Content**:
- Humanoid topology: torso as base, limbs as chains
- Kinematic chains: shoulder → upper_arm → elbow → forearm → wrist → hand
- Degrees of freedom in humanoid limbs
- Example: humanoid arm URDF fragment
- Connection to simulation: how URDF enables Gazebo/Isaac

**Diagram**: D3.2 - Humanoid link-joint structure (3D visualization description)
**Diagram**: D3.4 - Humanoid kinematic chain tree

**Code Snippet**: C3.3 - Humanoid arm chain (25 lines XML)

**Success Check**: Reader can trace the kinematic chain of a humanoid limb

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-007 (URDF link and joint elements) | 3.2, 3.3 | Full sections with attributes |
| FR-008 (URDF humanoid examples) | 3.4 | Full humanoid structure section |
| FR-010 (cite official docs) | All | References to URDF spec |
| FR-011 (concept-first style) | All | Theory before XML |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D3.1 | Hierarchy | URDF element containment | Mermaid flowchart |
| D3.2 | 3D concept | Humanoid link-joint structure | Description for illustration |
| D3.3 | Comparison | Joint types visualization | Mermaid or illustration |
| D3.4 | Tree | Humanoid kinematic chain | Mermaid graph TD |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| C3.1 | XML | 10 | Basic link definition |
| C3.2 | XML | 12 | Joint definition |
| C3.3 | XML | 25 | Humanoid arm chain |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-005 (80% interpret link-joint) | Section 3.2, 3.3 clear definitions |
| SC-006 (3 URDF examples for humanoid) | Section 3.4 humanoid structure |

---

## Chapter Dependencies

**Requires**:
- Chapter 1: Understanding of ROS 2 graph (URDF feeds into it)
- Chapter 2: Context for robot_state_publisher node

**Enables**:
- Module 2: Gazebo uses URDF for physics simulation
- Module 3: Isaac Sim uses URDF/USD for robot representation
- Module 4: VLA systems need robot structure understanding

---

## Key Vocabulary

| Term | Definition |
|------|------------|
| Link | Rigid body segment in URDF |
| Joint | Kinematic connection between links |
| Revolute | Rotation joint with limits |
| Prismatic | Linear sliding joint |
| Fixed | Rigid, non-moving connection |
| Kinematic Chain | Series of links and joints |
| DOF | Degrees of Freedom - number of independent motions |

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] URDF purpose clearly distinguished from ROS 2 communication
- [ ] Links explained with all three property types
- [ ] Joint types relevant to humanoids covered
- [ ] Humanoid structure example is illustrative
- [ ] XML snippets are readable and well-commented
- [ ] Success checks embedded at section ends
- [ ] Official URDF documentation cited
- [ ] Concept-first: theory before XML
- [ ] ~40-50 minute reading time
