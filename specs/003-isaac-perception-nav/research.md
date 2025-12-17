# Research Findings: Module 3 - The AI-Robot Brain (NVIDIA Isaac)

**Phase**: 0 (Research) | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)

## Overview

This document captures research findings for Module 3 on AI perception and navigation using NVIDIA Isaac. The module covers synthetic data generation (Isaac Sim), Visual SLAM (Isaac ROS), and path planning (Nav2).

---

## 1. AI Perception Pipeline

### End-to-End Flow

```
Raw Sensor Data → Preprocessing → Feature Extraction → Model Inference → Semantic Output
      │                │                  │                  │               │
  camera/lidar    normalization      CNN/ViT           detection/       objects,
                  cropping          backbone          segmentation      obstacles,
                                                                        depth
```

### Perception Tasks for Humanoids

| Task | Input | Output | Humanoid Use |
|------|-------|--------|--------------|
| Object Detection | RGB image | Bounding boxes + classes | Manipulation, navigation |
| Semantic Segmentation | RGB image | Per-pixel class labels | Scene understanding |
| Instance Segmentation | RGB image | Per-pixel instance IDs | Object counting, tracking |
| Depth Estimation | RGB/stereo | Depth map | 3D reconstruction |
| Pose Estimation | RGB image | Keypoints, poses | Human interaction |

### Why Synthetic Data?

| Challenge with Real Data | Synthetic Solution |
|-------------------------|-------------------|
| Expensive to collect | Automated generation |
| Hard to label | Automatic ground truth |
| Limited scenarios | Infinite variation |
| Safety concerns | Risk-free simulation |
| Privacy issues | No real people needed |

---

## 2. NVIDIA Isaac Sim Deep Dive

### Isaac Sim Overview

- High-fidelity simulator built on NVIDIA Omniverse
- Photorealistic rendering for perception
- USD (Universal Scene Description) format
- Domain randomization for training robustness
- Automatic ground truth generation

### Synthetic Data Generation Pipeline

```
Scene Setup → Domain Randomization → Rendering → Ground Truth → Dataset Export
     │               │                   │            │              │
  URDF/USD     textures, lighting    RTX render    labels,       COCO/KITTI
  import       positions, colors     ray tracing   masks,        format
                                                   depth
```

### Domain Randomization Types

| Randomization | What Changes | Why It Helps |
|--------------|--------------|--------------|
| Texture | Object surface appearance | Generalize to real textures |
| Lighting | Light position, intensity, color | Handle real lighting variation |
| Pose | Object position, rotation | Detect at various angles |
| Camera | Position, angle, lens params | Robust to viewpoint changes |
| Distractor | Background objects | Ignore irrelevant items |

### Ground Truth Types

| Label Type | Description | Use Case |
|------------|-------------|----------|
| Bounding Box | 2D/3D rectangles around objects | Object detection |
| Segmentation Mask | Per-pixel object ID | Semantic understanding |
| Depth Map | Per-pixel distance | 3D reconstruction |
| Surface Normal | Per-pixel orientation | Scene geometry |
| Optical Flow | Per-pixel motion | Motion tracking |

---

## 3. Visual SLAM Concepts

### What is VSLAM?

Visual Simultaneous Localization and Mapping:
- **Localization**: Where am I?
- **Mapping**: What does the environment look like?
- **Visual**: Using camera images (vs. LiDAR SLAM)
- **Simultaneous**: Both at the same time

### VSLAM Pipeline Components

```
Camera Images → Feature Extraction → Feature Matching → Motion Estimation → Map Building
      │               │                    │                   │                │
   frames      keypoints, desc         tracking              pose           landmarks,
              (ORB, SIFT, etc)       across frames          update           graph
```

### Visual Odometry vs. Full SLAM

| Aspect | Visual Odometry | Full SLAM |
|--------|-----------------|-----------|
| Output | Incremental pose | Map + trajectory |
| Loop Closure | No | Yes |
| Drift | Accumulates | Corrected |
| Compute | Lower | Higher |
| Use Case | Short-term | Long-term navigation |

### Isaac ROS VSLAM

- GPU-accelerated using CUDA
- cuVSLAM implementation
- Real-time performance on Jetson
- Outputs: pose, map, localization status
- Integrates with Nav2 for navigation

---

## 4. Nav2 Navigation Stack

### Nav2 Overview

- ROS 2 navigation framework
- Modular architecture with plugins
- Behavior trees for decision logic
- Supports various robot types (adaptation for humanoids)

### Nav2 Architecture

```
                    ┌─────────────────┐
                    │  Behavior Tree  │ ◄── Mission logic
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Global Planner│    │ Local Planner │    │  Controller   │
│ (NavFn, etc)  │    │ (DWB, etc)    │    │ (cmd_vel out) │
└───────┬───────┘    └───────┬───────┘    └───────────────┘
        │                    │
        └────────┬───────────┘
                 ▼
        ┌───────────────┐
        │   Costmap     │ ◄── Obstacle representation
        │  (2D/3D grid) │
        └───────────────┘
```

### Nav2 Key Components

| Component | Purpose | Input/Output |
|-----------|---------|--------------|
| Costmap | Obstacle representation | Sensors → occupancy grid |
| Global Planner | Path finding | Start/goal → waypoints |
| Local Planner | Trajectory optimization | Path → smooth trajectory |
| Controller | Motion commands | Trajectory → cmd_vel |
| Recovery | Handle failures | Stuck → recovery behavior |

### Costmap Layers

| Layer | Source | Represents |
|-------|--------|------------|
| Static | Map | Known obstacles |
| Obstacle | Sensors | Dynamic obstacles |
| Inflation | Computed | Safety buffer |
| Voxel | 3D sensors | Height information |

---

## 5. Humanoid-Specific Navigation

### Challenges

| Challenge | Description | Impact |
|-----------|-------------|--------|
| Bipedal Stability | Must maintain balance | Limits acceleration/speed |
| Foot Placement | Discrete stepping | Not smooth motion |
| Height Variation | Different from wheeled | 3D costmap needs |
| Step Planning | Beyond cmd_vel | Gait integration |

### Adaptations for Humanoids

1. **Footstep Planning**: Convert path to foot placements
2. **Stability Constraints**: Limit velocity commands
3. **3D Costmaps**: Account for body volume at height
4. **Gait Integration**: Interface with locomotion controller

### Nav2 for Humanoids

```
Nav2 Path → Footstep Planner → Step Sequence → Gait Controller
     │              │               │               │
  waypoints    foot positions    timing        joint commands
```

---

## 6. Perception-to-Navigation Pipeline

### Complete Flow

```
Isaac Sim                Isaac ROS              Nav2
    │                        │                   │
Synthetic Data ──►  Train Models ──►  Perception
    │                                     │
                                    Object Detection
                                    Depth Estimation
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │    Isaac ROS        │
                              │      VSLAM          │
                              │  (Localization)     │
                              └─────────┬───────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │       Nav2          │
                              │  (Path Planning)    │
                              └─────────┬───────────┘
                                        │
                                        ▼
                                   Motion Commands
```

---

## 7. Diagram Requirements

### Chapter 1: Perception with Isaac Sim

| Diagram | Type | Purpose |
|---------|------|---------|
| D1.1 | Pipeline | Perception task flow |
| D1.2 | Architecture | Synthetic data generation pipeline |
| D1.3 | Comparison | Real vs. synthetic data |
| D1.4 | Examples | Domain randomization types |

### Chapter 2: VSLAM with Isaac ROS

| Diagram | Type | Purpose |
|---------|------|---------|
| D2.1 | Pipeline | VSLAM components |
| D2.2 | Comparison | Visual odometry vs. full SLAM |
| D2.3 | Architecture | Isaac ROS VSLAM integration |
| D2.4 | Sequence | Loop closure concept |

### Chapter 3: Nav2 Path Planning

| Diagram | Type | Purpose |
|---------|------|---------|
| D3.1 | Architecture | Nav2 stack components |
| D3.2 | Visualization | Costmap layers |
| D3.3 | Flowchart | Planning to control flow |
| D3.4 | Comparison | Wheeled vs. humanoid navigation |

---

## 8. Source References

### Official Documentation

- Isaac Sim: https://docs.omniverse.nvidia.com/isaacsim/
- Isaac ROS: https://nvidia-isaac-ros.github.io/
- Nav2: https://navigation.ros.org/

### Version Targeting

- **Isaac Sim**: 2023.1.0+ (Omniverse-based)
- **Isaac ROS**: Compatible with ROS 2 Humble/Jazzy
- **Nav2**: Humble/Jazzy releases

---

## 9. Content Balance Analysis

### Target Distribution

| Content Type | Target % | Module 3 Plan |
|--------------|----------|---------------|
| Conceptual explanation | 70% | Perception concepts, SLAM theory, Nav2 architecture |
| Pipeline diagrams | 20% | Data generation, VSLAM, navigation flows |
| Technical details | 10% | Isaac/Nav2 configuration concepts |

### Reading Time Estimates

| Chapter | Sections | Est. Time |
|---------|----------|-----------|
| Ch 1: Perception & Isaac Sim | 5 | 50-60 min |
| Ch 2: VSLAM & Isaac ROS | 4 | 45-55 min |
| Ch 3: Nav2 Path Planning | 5 | 50-60 min |
| **Total Module** | 14 | ~2.5-3 hours |

---

**Next**: Create [data-model.md](./data-model.md) with entity definitions and chapter mappings.
