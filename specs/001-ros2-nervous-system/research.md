# Research Findings: Module 1 - The Robotic Nervous System (ROS 2)

**Phase**: 0 (Research) | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)

## Overview

This document captures research findings that inform the content strategy for Module 1. The module introduces ROS 2 as the foundational communication middleware, using the "nervous system" metaphor to make abstract concepts accessible.

---

## 1. The Nervous System Analogy

### Biological-Robotic Mapping

| Biological System | ROS 2 Concept | Shared Characteristics |
|-------------------|---------------|------------------------|
| Neuron | Node | Independent processing unit with defined inputs/outputs |
| Sensory pathway | Topic | Continuous data stream from sensors to brain |
| Motor command | Service | Discrete request-response for specific actions |
| Neural signal | Message | Typed data packet transmitted between units |
| Spinal cord | Executor | Manages timing and coordination of processes |

### Why This Analogy Works

1. **Familiarity**: Most readers understand nervous systems at a basic level
2. **Scalability**: Analogy extends from simple reflexes to complex behaviors
3. **Intuition**: Helps readers predict ROS 2 behavior before learning details
4. **Retention**: Memorable mental model for abstract software architecture

### Analogy Limitations (to address in content)

- Biological systems are analog; ROS 2 is digital
- Neurons can rewire; ROS 2 topology is typically static at runtime
- Biological signals degrade; ROS 2 messages are lossless within network

---

## 2. ROS 2 Communication Patterns

### When to Use Topics vs. Services

| Pattern | Use Case | Characteristics |
|---------|----------|-----------------|
| **Topic** | Sensor data, continuous state | Async, many-to-many, fire-and-forget |
| **Service** | Configuration, discrete actions | Sync, one-to-one, request-response |
| **Action** | Long-running tasks with feedback | Async with progress, cancellable |

### Topic Pattern Deep Dive

```
Publisher → Topic → Subscriber(s)

Key concepts:
- Named channel (e.g., /camera/image_raw)
- Typed messages (e.g., sensor_msgs/Image)
- QoS policies for reliability/durability
- Multiple publishers allowed
- Multiple subscribers allowed
```

### Service Pattern Deep Dive

```
Client → Request → Server
         ←Response←

Key concepts:
- Named endpoint (e.g., /spawn_entity)
- Request/Response message pair
- Blocking call (client waits)
- Single server per service name
```

### Actions (mentioned but not deep-dived in Module 1)

Actions combine topics and services for long-running tasks. Covered in later modules for robot motion.

---

## 3. rclpy Node Patterns

### Minimal Node Structure

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        # Setup publishers, subscribers, timers

    def callback(self, msg):
        # Process incoming data
        pass

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### AI Agent Integration Points

Where decision logic fits in the rclpy model:

1. **Callback processing**: Transform sensor data into features
2. **Decision timer**: Periodic AI inference calls
3. **Publication**: Send commands to actuators
4. **State management**: Track robot state across callbacks

### Node Lifecycle (for concept chapter)

```
Created → Configured → Activated → Executing ← (loop)
                                        ↓
                           Deactivated → Finalized → Destroyed
```

---

## 4. URDF for Humanoid Robots

### URDF Structure Overview

```xml
<robot name="humanoid">
  <link name="base_link">...</link>
  <joint name="hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="upper_leg"/>
    ...
  </joint>
  <link name="upper_leg">...</link>
</robot>
```

### Key Elements

| Element | Purpose | Attributes |
|---------|---------|------------|
| `<link>` | Rigid body segment | visual, collision, inertial |
| `<joint>` | Connection between links | type, parent, child, limits |
| `<visual>` | Rendering geometry | geometry, material, origin |
| `<collision>` | Physics geometry | geometry, origin |
| `<inertial>` | Mass properties | mass, inertia tensor, origin |

### Joint Types for Humanoids

| Type | DOF | Humanoid Use |
|------|-----|--------------|
| `revolute` | 1 | Elbows, knees, fingers |
| `continuous` | 1 | Wheels (not typical for humanoids) |
| `prismatic` | 1 | Telescoping elements |
| `fixed` | 0 | Rigid attachments |
| `floating` | 6 | Base link to world |

### Humanoid Kinematic Chain

```
                    head
                      ↑
             left_arm ← torso → right_arm
                         ↑
              left_leg ← pelvis → right_leg
```

Each limb forms a chain: shoulder → upper_arm → elbow → forearm → wrist → hand

---

## 5. Diagram Requirements

### Chapter 1: ROS 2 Architecture

| Diagram | Type | Purpose |
|---------|------|---------|
| D1.1 | Conceptual | Nervous system analogy overview |
| D1.2 | Architecture | ROS 2 node graph example |
| D1.3 | Sequence | Topic publish-subscribe flow |
| D1.4 | Sequence | Service request-response flow |
| D1.5 | Comparison | Topics vs. Services decision tree |

### Chapter 2: Python Agents

| Diagram | Type | Purpose |
|---------|------|---------|
| D2.1 | Architecture | rclpy node structure |
| D2.2 | Flowchart | Callback execution model |
| D2.3 | Architecture | AI agent integration points |
| D2.4 | Sequence | Sensor → Decision → Actuator flow |

### Chapter 3: URDF

| Diagram | Type | Purpose |
|---------|------|---------|
| D3.1 | Hierarchy | URDF element relationships |
| D3.2 | 3D | Humanoid link-joint structure |
| D3.3 | Comparison | Joint types visualization |
| D3.4 | Tree | Humanoid kinematic chain |

---

## 6. Source References

### Official Documentation

- ROS 2 Humble Documentation: https://docs.ros.org/en/humble/
- rclpy API Reference: https://docs.ros2.org/latest/api/rclpy/
- URDF Specification: http://wiki.ros.org/urdf/XML

### Key Concepts Pages

- Understanding Topics: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/
- Understanding Services: https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/
- Creating a Simple Publisher/Subscriber: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

### Version Targeting

- **Primary**: ROS 2 Humble Hawksbill (LTS until May 2027)
- **Secondary**: ROS 2 Jazzy Jalisco (current stable)

---

## 7. Content Balance Analysis

### Target Distribution

| Content Type | Target % | Module 1 Plan |
|--------------|----------|---------------|
| Conceptual explanation | 70% | Core nervous system analogy, ROS 2 concepts |
| Code examples | 20% | Minimal rclpy snippets, URDF fragments |
| Diagrams | 10% | ~12 diagrams across 3 chapters |

### Reading Time Estimates

| Chapter | Sections | Est. Time |
|---------|----------|-----------|
| Ch 1: ROS 2 Architecture | 5 | 45-60 min |
| Ch 2: Python Agents | 4 | 40-50 min |
| Ch 3: URDF | 4 | 40-50 min |
| **Total Module** | 13 | ~2.5-3 hours |

---

## 8. Open Questions (Resolved)

| Question | Resolution |
|----------|------------|
| Should we cover ROS 1 differences? | No - out of scope per spec |
| Include QoS details? | No - advanced topic for later |
| Show full working examples? | No - concept-first, minimal code |
| Cover actions in Module 1? | Mention only, detail in Module 4 |

---

**Next**: Create [data-model.md](./data-model.md) with entity definitions and chapter mappings.
