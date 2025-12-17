# Research Findings: Module 2 - The Digital Twin (Gazebo & Unity)

**Phase**: 0 (Research) | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)

## Overview

This document captures research findings for Module 2 content on digital twins and simulation. The module explains physics simulation (Gazebo), high-fidelity rendering (Unity), and sensor simulation for humanoid robot development.

---

## 1. Digital Twin Concept

### Definition and Purpose

A digital twin is a virtual replica of a physical robot that:
- Mirrors the robot's structure, appearance, and behavior
- Enables testing without physical hardware risk
- Supports faster iteration during development
- Provides ground truth data for algorithm training

### Digital Twin Benefits for Humanoid Robotics

| Benefit | Description | Humanoid Application |
|---------|-------------|---------------------|
| Safety | Test dangerous scenarios virtually | Fall recovery, collision testing |
| Cost | No hardware wear during development | Iterative gait tuning |
| Speed | Faster-than-realtime simulation | RL training acceleration |
| Reproducibility | Exact scenario replay | Debugging perception failures |
| Scale | Parallel simulation instances | Parameter sweeps |

### Simulation Fidelity Spectrum

```
Low Fidelity ─────────────────────────────► High Fidelity
     │                                           │
  Kinematic         Rigid Body          Soft Body/Deformable
  (Position only)   (Forces, Contacts)  (Muscles, Cloth)
     │                   │                      │
   Fast, simple    Good balance        Slow, realistic
```

---

## 2. Physics Simulation Fundamentals

### Core Simulated Phenomena

| Phenomenon | What It Is | Why It Matters |
|------------|------------|----------------|
| Gravity | Downward force on mass | Balance, falls, weight distribution |
| Rigid Body Dynamics | Motion of solid objects | Link movements, momentum |
| Collision Detection | Finding contact points | Preventing interpenetration |
| Contact Forces | Reaction to collisions | Ground contact, manipulation |
| Friction | Resistance to sliding | Foot grip, object grasping |
| Joint Constraints | Motion limits | Realistic joint behavior |

### Physics Engine Architecture

```
World State
    │
    ▼
┌─────────────────────────┐
│   Collision Detection   │ ◄── Broad phase + Narrow phase
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Contact Generation    │ ◄── Contact points, normals
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Constraint Solver     │ ◄── Joints + Contacts
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Integration           │ ◄── Velocity → Position
└───────────┬─────────────┘
            │
            ▼
New World State
```

### Simulation Step (Time Stepping)

- Fixed timestep: Consistent physics behavior
- Typical: 1ms (1000 Hz physics)
- Trade-off: Smaller steps = more accurate but slower

---

## 3. Gazebo Deep Dive

### Gazebo Overview

- Open-source robotics simulator
- Native ROS 2 integration via ros_gz bridge
- Multiple physics engines (DART, Bullet, ODE)
- SDF (Simulation Description Format) for worlds

### Gazebo Strengths

| Strength | Description |
|----------|-------------|
| ROS 2 Native | Direct topic/service integration |
| Physics Options | Multiple engines for different needs |
| Sensor Plugins | Built-in camera, LiDAR, IMU models |
| Open Source | Free, extensible, community supported |
| Industry Standard | Widely used in robotics research |

### Gazebo Limitations

| Limitation | Impact |
|------------|--------|
| Rendering Quality | Not photorealistic (improving in newer versions) |
| Complex Environments | Performance degrades with scene complexity |
| Learning Curve | SDF format and plugin architecture |

### Gazebo-ROS 2 Integration

```
Gazebo Simulation          ROS 2 System
┌─────────────────┐        ┌─────────────────┐
│  Robot Model    │        │  Control Node   │
│  (SDF/URDF)     │        │  (rclpy)        │
└────────┬────────┘        └────────┬────────┘
         │                          │
         ▼                          ▼
┌─────────────────┐        ┌─────────────────┐
│  Sensor Plugins │◄──────►│  ros_gz_bridge  │
│  (camera, lidar)│ Topics │  (bidirectional)│
└─────────────────┘        └─────────────────┘
```

---

## 4. Unity Deep Dive

### Unity for Robotics

- Commercial game engine adapted for simulation
- High-fidelity rendering (HDRP)
- Unity Robotics Hub for ROS integration
- Used for perception testing and HRI

### Unity Strengths

| Strength | Description |
|----------|-------------|
| Visual Fidelity | Photorealistic rendering |
| Environment Tools | Rich asset ecosystem |
| HRI Scenarios | Human avatars, animations |
| Perception Testing | Realistic visual inputs |
| Cross-Platform | Windows, Linux, cloud |

### Unity Limitations

| Limitation | Impact |
|------------|--------|
| Physics Accuracy | PhysX less accurate than specialized engines |
| ROS Integration | Requires additional packages |
| Licensing | Commercial considerations |
| Learning Curve | Game development concepts |

### Unity-ROS 2 Integration

```
Unity Simulation            ROS 2 System
┌─────────────────┐        ┌─────────────────┐
│  Robot + Scene  │        │  Perception     │
│  (URDF import)  │        │  Node (rclpy)   │
└────────┬────────┘        └────────┬────────┘
         │                          │
         ▼                          ▼
┌─────────────────┐        ┌─────────────────┐
│  ROS-TCP-Conn   │◄──────►│  ros_tcp_endpt  │
│  (Unity side)   │  TCP   │  (ROS 2 side)   │
└─────────────────┘        └─────────────────┘
```

---

## 5. Platform Comparison

### Decision Framework

| Requirement | Gazebo | Unity | Recommendation |
|-------------|--------|-------|----------------|
| Physics accuracy | ✅ Strong | ⚠️ Adequate | Gazebo |
| Visual realism | ⚠️ Basic | ✅ Excellent | Unity |
| ROS 2 integration | ✅ Native | ⚠️ Bridge | Gazebo |
| Complex scenes | ⚠️ Limited | ✅ Strong | Unity |
| HRI scenarios | ⚠️ Basic | ✅ Strong | Unity |
| Open source | ✅ Yes | ❌ No | Gazebo |
| Learning curve | ⚠️ Moderate | ⚠️ Moderate | Similar |

### When to Use Each

**Use Gazebo when**:
- Physics accuracy is critical
- Native ROS 2 integration needed
- Open source requirement
- Standard sensor simulation sufficient

**Use Unity when**:
- Photorealistic perception testing
- Human-robot interaction scenarios
- Complex environment design
- Visual ML training data generation

**Use Both when**:
- Different development stages need different fidelity
- Team has expertise in both platforms

---

## 6. Sensor Simulation

### LiDAR Simulation

```yaml
sensor: LiDAR
output: Point Cloud (sensor_msgs/PointCloud2)
key_parameters:
  - range_min/max: Detection distance limits
  - samples: Points per scan
  - update_rate: Scan frequency (Hz)
  - noise_model: Gaussian noise on distance
  - ray_count: Vertical layers (multi-plane)
humanoid_use: Obstacle detection, mapping
```

### Depth Camera Simulation

```yaml
sensor: Depth Camera
output: Depth Image (sensor_msgs/Image)
key_parameters:
  - resolution: Width x Height pixels
  - fov: Field of view (horizontal, vertical)
  - range: Min/max depth
  - noise_model: Depth-dependent noise
  - update_rate: Frame rate (Hz)
humanoid_use: Manipulation, close obstacle detection
```

### IMU Simulation

```yaml
sensor: IMU (Inertial Measurement Unit)
output: IMU Data (sensor_msgs/Imu)
key_parameters:
  - accelerometer: 3-axis linear acceleration
  - gyroscope: 3-axis angular velocity
  - bias: Systematic offset per axis
  - noise: Random noise (Gaussian)
  - update_rate: Typically 100-1000 Hz
humanoid_use: Balance, orientation estimation
```

### Sensor Realism Considerations

| Factor | Impact on Realism | Typical Model |
|--------|-------------------|---------------|
| Noise | Adds realistic variation | Gaussian |
| Bias | Systematic errors | Constant offset |
| Dropout | Missing data | Probability-based |
| Latency | Time delay | Fixed or variable |
| Range limits | Detection boundaries | Min/max cutoff |

---

## 7. Diagram Requirements

### Chapter 1: Digital Twins and Gazebo

| Diagram | Type | Purpose |
|---------|------|---------|
| D1.1 | Conceptual | Digital twin concept overview |
| D1.2 | Architecture | Physics engine pipeline |
| D1.3 | Architecture | Gazebo-ROS 2 integration |
| D1.4 | Flowchart | Simulation loop |

### Chapter 2: Unity for HRI

| Diagram | Type | Purpose |
|---------|------|---------|
| D2.1 | Comparison | Gazebo vs Unity decision matrix |
| D2.2 | Architecture | Unity-ROS 2 integration |
| D2.3 | Conceptual | HRI scenario examples |
| D2.4 | Screenshot | Unity robot visualization (described) |

### Chapter 3: Simulated Sensors

| Diagram | Type | Purpose |
|---------|------|---------|
| D3.1 | Architecture | Sensor to ROS 2 topic flow |
| D3.2 | Visualization | LiDAR point cloud example |
| D3.3 | Visualization | Depth camera output |
| D3.4 | Comparison | Sensor parameter effects |

---

## 8. Source References

### Official Documentation

- Gazebo: https://gazebosim.org/docs
- Unity Robotics Hub: https://github.com/Unity-Technologies/Unity-Robotics-Hub
- ROS 2 Gazebo Integration: https://gazebosim.org/docs/latest/ros2_integration

### Version Targeting

- **Gazebo**: Harmonic (current LTS) or Ionic (latest)
- **Unity**: 2022 LTS or newer
- **ROS 2**: Humble/Jazzy (consistent with Module 1)

---

## 9. Content Balance Analysis

### Target Distribution

| Content Type | Target % | Module 2 Plan |
|--------------|----------|---------------|
| Conceptual explanation | 70% | Digital twin concept, physics fundamentals |
| Comparisons/decisions | 20% | Gazebo vs Unity framework |
| Technical details | 10% | Sensor parameters, integration diagrams |

### Reading Time Estimates

| Chapter | Sections | Est. Time |
|---------|----------|-----------|
| Ch 1: Digital Twins & Gazebo | 5 | 45-55 min |
| Ch 2: Unity for HRI | 4 | 40-50 min |
| Ch 3: Simulated Sensors | 5 | 45-55 min |
| **Total Module** | 14 | ~2.5-3 hours |

---

**Next**: Create [data-model.md](./data-model.md) with entity definitions and chapter mappings.
