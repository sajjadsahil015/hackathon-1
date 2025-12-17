# Chapter Contract: Path Planning with Nav2

**Module**: 3 - The AI-Robot Brain | **Chapter**: 3 of 3
**Target File**: `docs/module-3-isaac/03-nav2-path-planning.md`
**Est. Reading Time**: 50-60 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-3.1**: Describe the Nav2 navigation stack architecture and components
2. **LO-3.2**: Explain costmaps and their role in obstacle representation
3. **LO-3.3**: Differentiate between global and local planning
4. **LO-3.4**: Understand behavior trees for navigation decision logic
5. **LO-3.5**: Identify humanoid-specific navigation considerations

---

## Chapter Outline

### Section 3.1: Nav2 Architecture Overview (10 min)
**Objective**: Understand the navigation stack structure

**Content**:
- Nav2: ROS 2 navigation framework
- High-level architecture:
  - Behavior Tree (mission logic)
  - Global Planner (path finding)
  - Local Planner (trajectory optimization)
  - Controller (motion commands)
  - Recovery behaviors (failure handling)
- Navigation goal concept: target pose
- Typical navigation flow: goal → plan → execute

**Diagram**: D3.1 - Nav2 architecture

**Success Check**: Reader can name 5 Nav2 components and their roles

---

### Section 3.2: Costmaps and Obstacle Representation (12 min)
**Objective**: Understand how obstacles are represented for planning

**Content**:
- What is a costmap? Grid of traversability costs
- Costmap layers:
  - Static layer: from pre-built map
  - Obstacle layer: from live sensors
  - Inflation layer: safety buffer around obstacles
  - Voxel layer: 3D representation (optional)
- Cost values: free (0) → lethal (254) → unknown (255)
- How costmaps are updated from sensors
- 2D vs. 3D costmaps for humanoids

**Diagram**: D3.2 - Costmap layers visualization

**Code Snippet**: S3.2 - Costmap layer config (10 lines YAML)

**Success Check**: Reader can explain 3 costmap layers and their sources

---

### Section 3.3: Global and Local Planning (12 min)
**Objective**: Understand the two-level planning approach

**Content**:
- Global planner:
  - Input: current pose, goal pose, costmap
  - Output: path (sequence of waypoints)
  - Algorithms: NavFn (Dijkstra/A*), Smac, etc.
  - Replanning: when obstacles block path
- Local planner:
  - Input: global path, local costmap, velocity
  - Output: smooth trajectory, cmd_vel
  - Algorithms: DWB, TEB, MPPI
  - Handles dynamic obstacles
- Why two levels? Global efficiency + local reactivity

**Diagram**: D3.3 - Planning to control flow

**Success Check**: Reader can explain when replanning occurs

---

### Section 3.4: Behavior Trees for Navigation (10 min)
**Objective**: Understand decision logic in Nav2

**Content**:
- What are behavior trees? Hierarchical decision structures
- Nav2 default behavior tree structure
- Key node types:
  - Sequence: execute children in order
  - Fallback: try alternatives
  - Action: call navigation servers
  - Condition: check state
- Recovery behaviors: spin, backup, wait
- Customizing behavior for humanoids

**Success Check**: Reader can describe how recovery behaviors work

---

### Section 3.5: Humanoid Navigation Considerations (10 min)
**Objective**: Adapt navigation concepts for bipedal robots

**Content**:
- Challenges for humanoid navigation:
  - Bipedal stability constraints
  - Discrete footstep placement
  - Body volume at height (3D clearance)
  - Balance during motion
- Adaptations needed:
  - Footstep planning layer
  - Stability-aware velocity limits
  - 3D costmaps for body clearance
  - Gait controller integration
- Nav2 for humanoids: what works, what needs adaptation
- Research directions: integrated stepping planners

**Diagram**: D3.4 - Wheeled vs. humanoid navigation comparison

**Success Check**: Reader can list 3 humanoid navigation challenges

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-006 (Nav2 components) | 3.1, 3.2, 3.3 | Full stack coverage |
| FR-007 (humanoid considerations) | 3.5 | Full section |
| FR-008 (VSLAM to Nav2 connection) | 3.1 | Input requirements |
| FR-009 (cite official docs) | All | References to Nav2 |
| FR-010 (concept-first style) | All | Concepts before config |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D3.1 | Architecture | Nav2 stack components | Mermaid flowchart TD |
| D3.2 | Layered | Costmap layers stacked | Description or diagram |
| D3.3 | Flowchart | Goal → Global → Local → Control | Mermaid flowchart |
| D3.4 | Comparison | Wheeled vs. humanoid nav | Table or side-by-side |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| S3.1 | YAML | 15 | Nav2 params concept |
| S3.2 | YAML | 10 | Costmap layer config |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-005 (Nav2 components) | Section 3.1 explicit list |
| SC-006 (3 humanoid challenges) | Section 3.5 explicit list |

---

## Chapter Dependencies

**Requires**:
- Chapter 2: VSLAM for localization input
- Module 1: ROS 2 topics (cmd_vel, tf2)
- Module 2: Sensor data for costmaps

**Enables**:
- Module 4: Navigation for autonomous behavior

---

## Key Vocabulary

| Term | Definition |
|------|------------|
| Costmap | Grid representation of traversability costs |
| Global Planner | Computes path from start to goal |
| Local Planner | Optimizes trajectory avoiding local obstacles |
| Behavior Tree | Hierarchical decision structure |
| Recovery Behavior | Action taken when navigation fails |
| Inflation | Safety buffer around obstacles |
| Waypoint | Intermediate point along planned path |
| Footstep Planning | Converting path to foot placements |

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] Nav2 architecture clearly diagrammed
- [ ] Costmap concept thoroughly explained
- [ ] Global vs. local planning differentiated
- [ ] Behavior trees introduced appropriately
- [ ] Humanoid considerations specific and actionable
- [ ] Success checks embedded at section ends
- [ ] Official Nav2 documentation cited
- [ ] Concept-first: theory before configuration
- [ ] ~50-60 minute reading time
