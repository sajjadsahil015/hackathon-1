# Chapter Contract: Visual SLAM with Isaac ROS

**Module**: 3 - The AI-Robot Brain | **Chapter**: 2 of 3
**Target File**: `docs/module-3-isaac/02-vslam-isaac-ros.md`
**Est. Reading Time**: 45-55 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-2.1**: Explain visual odometry concepts (feature extraction, tracking, pose estimation)
2. **LO-2.2**: Describe the difference between visual odometry and full SLAM
3. **LO-2.3**: Explain loop closure and why it corrects drift
4. **LO-2.4**: Understand Isaac ROS VSLAM acceleration and integration
5. **LO-2.5**: Describe how VSLAM output feeds into navigation

---

## Chapter Outline

### Section 2.1: Visual Odometry Concepts (12 min)
**Objective**: Understand how pose is estimated from images

**Content**:
- What is visual odometry? Pose estimation from sequential images
- Visual odometry pipeline:
  - Feature extraction (keypoints, descriptors)
  - Feature matching (tracking across frames)
  - Motion estimation (essential/fundamental matrix)
  - Pose update (incremental transform)
- Feature types: ORB, SIFT, learned features
- Why visual: rich information, passive sensing
- Limitations: drift accumulates over time

**Diagram**: D2.1 - Visual odometry pipeline

**Success Check**: Reader can trace data from image to pose update

---

### Section 2.2: From Visual Odometry to Full SLAM (12 min)
**Objective**: Understand what SLAM adds beyond visual odometry

**Content**:
- SLAM = Localization + Mapping simultaneously
- What SLAM adds:
  - Map building (landmark storage)
  - Loop closure detection
  - Global optimization (pose graph)
- Loop closure explained:
  - Recognize previously visited place
  - Create constraint in pose graph
  - Optimize to eliminate accumulated drift
- SLAM map types: sparse, semi-dense, dense
- Trade-offs: compute vs. map quality

**Diagram**: D2.2 - Visual odometry vs. full SLAM comparison
**Diagram**: D2.4 - Loop closure concept

**Success Check**: Reader can explain why loop closure is essential

---

### Section 2.3: Isaac ROS VSLAM (12 min)
**Objective**: Understand GPU-accelerated VSLAM

**Content**:
- Isaac ROS overview: GPU-accelerated ROS 2 packages
- cuVSLAM: CUDA-accelerated visual SLAM
- Performance benefits: real-time on Jetson
- Input requirements: stereo or RGB-D camera
- Output: robot pose, localization status, map
- Comparison to CPU-based alternatives
- When to use Isaac ROS VSLAM

**Diagram**: D2.3 - Isaac ROS VSLAM integration

**Code Snippet**: S2.1 - Isaac ROS VSLAM launch concept (12 lines)

**Success Check**: Reader can list 3 benefits of GPU-accelerated VSLAM

---

### Section 2.4: VSLAM Output and Navigation Integration (10 min)
**Objective**: Connect VSLAM to the navigation stack

**Content**:
- VSLAM output topics:
  - Pose (geometry_msgs/PoseStamped)
  - Transform (tf2)
  - Map (optional visualization)
- How Nav2 uses localization:
  - Costmap updates need robot position
  - Planning needs current pose
  - Controller needs accurate feedback
- VSLAM vs. other localization (AMCL, GPS, wheel odometry)
- Choosing localization method for humanoids

**Success Check**: Reader can describe data flow from VSLAM to Nav2

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-004 (VSLAM concepts) | 2.1, 2.2 | Full coverage |
| FR-005 (Isaac ROS acceleration) | 2.3 | GPU benefits explained |
| FR-008 (VSLAM to Nav2 connection) | 2.4 | Integration coverage |
| FR-009 (cite official docs) | All | References to Isaac ROS |
| FR-010 (concept-first style) | All | Concepts before tools |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D2.1 | Pipeline | VO: Features → Matching → Pose | Mermaid flowchart LR |
| D2.2 | Comparison | Visual odometry vs. full SLAM | Table or side-by-side |
| D2.3 | Architecture | Isaac ROS VSLAM integration | Mermaid flowchart |
| D2.4 | Conceptual | Loop closure illustration | Description |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| S2.1 | YAML | 12 | Isaac ROS VSLAM launch concept |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-003 (VO vs. SLAM difference) | Section 2.2 explicit comparison |
| SC-004 (VSLAM pipeline) | Section 2.1, 2.2 |

---

## Chapter Dependencies

**Requires**:
- Chapter 1: Perception concepts (feature extraction)
- Module 2: Camera simulation, sensor data

**Enables**:
- Chapter 3: Localization for Nav2
- Module 4: Spatial awareness for VLA

---

## Key Vocabulary

| Term | Definition |
|------|------------|
| Visual Odometry | Incremental pose estimation from images |
| Feature | Distinctive point in image (corner, blob) |
| Descriptor | Numerical representation of feature |
| Keyframe | Reference image in SLAM map |
| Loop Closure | Recognition of revisited location |
| Pose Graph | Graph of robot poses with constraints |
| Drift | Accumulated error in pose estimation |
| cuVSLAM | NVIDIA's CUDA-accelerated VSLAM |

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] Visual odometry pipeline clearly explained
- [ ] Loop closure concept thoroughly covered
- [ ] SLAM vs. VO differences explicit
- [ ] Isaac ROS benefits clearly stated
- [ ] Navigation integration explained
- [ ] Success checks embedded at section ends
- [ ] Official Isaac ROS documentation cited
- [ ] Concept-first: theory before implementation
- [ ] ~45-55 minute reading time
