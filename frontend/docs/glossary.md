# Glossary

A comprehensive glossary of terms used throughout this book, organized by module.

---

## Module 1: ROS 2 - The Robotic Nervous System

| Term | Definition |
|------|------------|
| **Node** | Independent ROS 2 process with defined communication interfaces |
| **Topic** | Named channel for publish-subscribe message passing |
| **Service** | Named endpoint for synchronous request-response communication |
| **Message** | Typed data structure for inter-node communication |
| **Publisher** | Node interface that sends messages to a topic |
| **Subscriber** | Node interface that receives messages from a topic |
| **Callback** | Function invoked when a message arrives or timer fires |
| **URDF** | Unified Robot Description Format for robot structure |
| **Link** | Rigid body segment in URDF |
| **Joint** | Kinematic connection between URDF links |
| **Kinematic Chain** | Series of links connected by joints from base to end-effector |
| **QoS** | Quality of Service - reliability and durability settings for topics |
| **Action** | ROS 2 interface for long-running tasks with feedback |

---

## Module 2: Simulation - The Digital Twin

| Term | Definition |
|------|------------|
| **Digital Twin** | Virtual replica of physical robot for simulation and testing |
| **Physics Engine** | Component computing forces, collisions, and motion |
| **World** | Simulated environment containing robots and objects |
| **SDF** | Simulation Description Format used by Gazebo |
| **Rigid Body** | Object treated as non-deformable solid in physics simulation |
| **Collision Detection** | Process of finding contact between objects |
| **Contact Force** | Reaction force computed at collision points |
| **Sensor Model** | Virtual sensor with configurable parameters and noise |
| **Point Cloud** | 3D data from LiDAR consisting of XYZ points |
| **Depth Image** | 2D image where each pixel represents a distance value |
| **IMU** | Inertial Measurement Unit measuring acceleration and rotation |
| **Noise Model** | Mathematical model of sensor imperfections |
| **ros_gz_bridge** | ROS 2 package bridging Gazebo and ROS 2 topics |

---

## Module 3: Isaac - The AI-Robot Brain

| Term | Definition |
|------|------------|
| **Perception Pipeline** | End-to-end flow from raw sensors to semantic understanding |
| **Synthetic Data** | Computer-generated training data with automatic labels |
| **Domain Randomization** | Varying simulation parameters for model robustness |
| **Ground Truth** | Automatically generated correct labels for training data |
| **Visual Odometry (VO)** | Pose estimation from sequential camera images |
| **VSLAM** | Visual Simultaneous Localization and Mapping |
| **Loop Closure** | Recognizing previously visited locations to correct drift |
| **Keyframe** | Reference image used for visual localization |
| **Costmap** | Grid representation of navigation traversability costs |
| **Global Planner** | Computes full path from start to goal pose |
| **Local Planner** | Optimizes trajectory while avoiding local obstacles |
| **Behavior Tree** | Hierarchical decision structure for robot behavior |
| **Recovery Behavior** | Action taken when navigation fails (spin, backup, wait) |
| **Inflation Layer** | Safety buffer added around obstacles in costmaps |
| **TensorRT** | NVIDIA library for optimized neural network inference |

---

## Module 4: VLA - Vision-Language-Action

| Term | Definition |
|------|------------|
| **VLA System** | Architecture processing vision and language to produce actions |
| **Vision Encoder** | Component transforming images to feature embeddings |
| **Language Model (LLM)** | Neural network processing text and generating responses |
| **Multimodal Fusion** | Combining representations from multiple modalities |
| **Action Decoder** | Component generating robot action outputs |
| **Voice Command** | Spoken instruction captured and processed by ASR |
| **ASR** | Automatic Speech Recognition (speech-to-text) |
| **Intent** | Semantic meaning extracted from language input |
| **Task Plan** | Sequence of subtasks generated from high-level instruction |
| **Action Primitive** | Atomic robot capability executable via ROS 2 |
| **Grounding** | Mapping language references to perceived objects |
| **Task Decomposition** | Breaking complex instructions into executable steps |
| **Autonomy Stack** | Complete integrated system from sensors to actuators |
| **Embodied AI** | AI that interacts with physical world through robot body |

---

## Cross-Module Terms

| Term | Definition | Modules |
|------|------------|---------|
| **Transform (TF)** | Coordinate frame relationship in ROS 2 | 1, 3 |
| **cmd_vel** | Velocity command topic for robot motion | 1, 3 |
| **Pose** | Position and orientation in 3D space | 1, 3, 4 |
| **Frame ID** | Identifier for coordinate reference frame | 1, 2, 3 |
| **Latency** | Time delay in processing or communication | 2, 3, 4 |
| **Inference** | Running a trained neural network on new data | 3, 4 |
| **End-to-End** | Learning directly from inputs to outputs | 3, 4 |

---

## ROS 2 Message Types

| Message Type | Package | Description |
|--------------|---------|-------------|
| `sensor_msgs/Image` | sensor_msgs | Camera images (RGB, depth) |
| `sensor_msgs/PointCloud2` | sensor_msgs | LiDAR point cloud data |
| `sensor_msgs/Imu` | sensor_msgs | IMU measurements |
| `geometry_msgs/Twist` | geometry_msgs | Linear and angular velocities |
| `geometry_msgs/PoseStamped` | geometry_msgs | Timestamped 3D pose |
| `nav_msgs/Path` | nav_msgs | Sequence of poses (path) |
| `nav_msgs/OccupancyGrid` | nav_msgs | 2D costmap/occupancy data |
| `tf2_msgs/TFMessage` | tf2_msgs | Coordinate transforms |
| `std_msgs/String` | std_msgs | Simple text message |

---

## Acronyms

| Acronym | Full Form |
|---------|-----------|
| **ROS** | Robot Operating System |
| **URDF** | Unified Robot Description Format |
| **SDF** | Simulation Description Format |
| **IMU** | Inertial Measurement Unit |
| **LiDAR** | Light Detection and Ranging |
| **SLAM** | Simultaneous Localization and Mapping |
| **VSLAM** | Visual SLAM |
| **VO** | Visual Odometry |
| **VLA** | Vision-Language-Action |
| **LLM** | Large Language Model |
| **ASR** | Automatic Speech Recognition |
| **TTS** | Text-to-Speech |
| **NLU** | Natural Language Understanding |
| **DOF** | Degrees of Freedom |
| **FOV** | Field of View |
| **GPU** | Graphics Processing Unit |
| **HRI** | Human-Robot Interaction |
| **Nav2** | Navigation 2 (ROS 2 navigation stack) |
| **QoS** | Quality of Service |
| **API** | Application Programming Interface |
| **SDK** | Software Development Kit |
