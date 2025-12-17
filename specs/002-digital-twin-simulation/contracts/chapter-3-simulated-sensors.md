# Chapter Contract: Simulated Sensors for Perception

**Module**: 2 - The Digital Twin | **Chapter**: 3 of 3
**Target File**: `docs/module-2-simulation/03-simulated-sensors.md`
**Est. Reading Time**: 45-55 minutes

---

## Learning Objectives

By the end of this chapter, readers will be able to:

1. **LO-3.1**: Explain the purpose and components of sensor models in simulation
2. **LO-3.2**: Describe LiDAR sensor output (point clouds) and key parameters
3. **LO-3.3**: Describe depth camera output (depth images) and key parameters
4. **LO-3.4**: Describe IMU output (acceleration, angular velocity) and noise characteristics
5. **LO-3.5**: Trace the data flow from simulated sensor to ROS 2 topic

---

## Chapter Outline

### Section 3.1: Sensor Models Overview (8 min)
**Objective**: Establish the concept of sensor simulation

**Content**:
- Why simulate sensors: test perception without hardware
- Sensor model components: geometry, physics, noise
- Realism factors: noise, bias, dropout, latency
- Common simulated sensors: camera, LiDAR, depth, IMU, force/torque
- Sensor placement on humanoid robots

**Success Check**: Reader can list 4 factors that affect sensor realism

---

### Section 3.2: LiDAR Simulation (10 min)
**Objective**: Deep understanding of LiDAR sensor models

**Content**:
- LiDAR principle: laser ranging to measure distances
- Output: Point cloud (PointCloud2 message)
- Key parameters:
  - Range (min/max detection distance)
  - Angular resolution (ray density)
  - Update rate (scans per second)
  - Noise model (Gaussian on distance)
- Multi-plane LiDAR (vertical layers)
- Humanoid use: mapping, obstacle detection

**Diagram**: D3.2 - Point cloud visualization description

**Code Snippet**: S3.1 - LiDAR sensor SDF (12 lines)

**Success Check**: Reader can explain point cloud data structure

---

### Section 3.3: Depth Camera Simulation (10 min)
**Objective**: Deep understanding of depth camera models

**Content**:
- Depth camera principle: structured light or ToF
- Output: Depth image (Image message with depth encoding)
- Key parameters:
  - Resolution (width x height)
  - Field of view (horizontal, vertical)
  - Range (min/max depth)
  - Noise model (depth-dependent)
- Comparison to LiDAR: dense vs. sparse, range differences
- Humanoid use: manipulation, close-range perception

**Diagram**: D3.3 - Depth image visualization description

**Code Snippet**: S3.2 - Depth camera SDF (12 lines)

**Success Check**: Reader can explain depth image encoding

---

### Section 3.4: IMU Simulation (10 min)
**Objective**: Deep understanding of IMU models

**Content**:
- IMU principle: measuring acceleration and rotation
- Output: IMU message (linear acceleration, angular velocity)
- Components:
  - Accelerometer (3-axis linear acceleration)
  - Gyroscope (3-axis angular velocity)
- Key parameters:
  - Update rate (typically 100-1000 Hz)
  - Bias (systematic offset)
  - Noise (random variation)
- Humanoid use: balance, orientation estimation, fall detection

**Code Snippet**: S3.3 - IMU sensor SDF (10 lines)

**Success Check**: Reader can explain IMU data components

---

### Section 3.5: Sensor-to-ROS 2 Pipeline (8 min)
**Objective**: Understand how simulated data reaches perception nodes

**Content**:
- Sensor plugin architecture (Gazebo)
- Data flow: sensor → plugin → bridge → topic
- Topic naming conventions
- Message types summary:
  - LiDAR: sensor_msgs/PointCloud2
  - Depth: sensor_msgs/Image
  - IMU: sensor_msgs/Imu
- Verifying sensor data in RViz2
- Connection to perception algorithms

**Diagram**: D3.1 - Sensor to ROS 2 pipeline architecture

**Success Check**: Reader can trace data from sensor to perception node

---

## Requirements Coverage

| Requirement | Section | How Addressed |
|-------------|---------|---------------|
| FR-006 (LiDAR simulation) | 3.2 | Full section with parameters |
| FR-007 (depth camera simulation) | 3.3 | Full section with parameters |
| FR-008 (IMU simulation) | 3.4 | Full section with parameters |
| FR-009 (sensor to ROS 2 topics) | 3.5 | Full pipeline coverage |
| FR-010 (cite official docs) | All | References to sensor specs |
| FR-011 (concept-first style) | All | Theory before SDF |

---

## Diagrams Required

| ID | Type | Description | Tool |
|----|------|-------------|------|
| D3.1 | Architecture | Sensor → Plugin → Bridge → Topic | Mermaid flowchart LR |
| D3.2 | Visualization | Point cloud example | Description for illustration |
| D3.3 | Visualization | Depth image example | Description for illustration |
| D3.4 | Comparison | Parameter effect visualization | Table or description |

---

## Code Snippets Required

| ID | Language | Lines | Purpose |
|----|----------|-------|---------|
| S3.1 | XML (SDF) | 12 | LiDAR sensor definition |
| S3.2 | XML (SDF) | 12 | Depth camera definition |
| S3.3 | XML (SDF) | 10 | IMU sensor definition |

---

## Success Criteria Mapping

| Success Criterion | Verification |
|-------------------|--------------|
| SC-005 (sensor output formats) | Sections 3.2, 3.3, 3.4 |
| SC-006 (3 sensor realism parameters) | Section 3.1 + all sensor sections |

---

## Chapter Dependencies

**Requires**:
- Chapter 1: Gazebo and simulation concepts
- Chapter 2: Understanding of both Gazebo and Unity contexts
- Module 1: ROS 2 topics and messages

**Enables**:
- Module 3: Perception pipelines consume sensor data
- Module 4: VLA systems use sensor inputs

---

## Sensor Summary Table

| Sensor | Output Type | ROS 2 Message | Key Parameters |
|--------|-------------|---------------|----------------|
| LiDAR | Point Cloud | sensor_msgs/PointCloud2 | Range, resolution, noise |
| Depth Camera | Depth Image | sensor_msgs/Image | Resolution, FOV, range |
| IMU | Accel + Gyro | sensor_msgs/Imu | Rate, bias, noise |

---

## Review Checklist

- [ ] All learning objectives addressed with clear explanations
- [ ] Each sensor type thoroughly covered
- [ ] Output data formats clearly explained
- [ ] Parameters and their effects described
- [ ] Pipeline diagram shows complete data flow
- [ ] SDF snippets minimal and readable
- [ ] Success checks embedded at section ends
- [ ] Official sensor documentation cited
- [ ] Concept-first: theory before configuration
- [ ] ~45-55 minute reading time
