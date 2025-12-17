# Module 3 Assets: NVIDIA Isaac Perception & Navigation

**Purpose**: Reusable Mermaid diagrams and code snippets for Module 3 chapters.

---

## Diagrams

### D3.1: Perception Pipeline Flow

```mermaid
flowchart LR
    subgraph Input["📷 Sensor Input"]
        RGB[RGB Camera]
        Depth[Depth Camera]
        LiDAR[LiDAR]
    end

    subgraph Processing["⚙️ Processing"]
        Pre[Preprocessing]
        Model[Neural Network]
    end

    subgraph Output["📊 Semantic Output"]
        Det[Object Detection]
        Seg[Segmentation]
        Pose[Pose Estimation]
    end

    RGB --> Pre
    Depth --> Pre
    LiDAR --> Pre
    Pre --> Model
    Model --> Det
    Model --> Seg
    Model --> Pose
```

### D3.2: Synthetic Data Generation Pipeline

```mermaid
flowchart LR
    subgraph Setup["🎬 Scene Setup"]
        Assets[3D Assets]
        Scene[Scene Configuration]
    end

    subgraph DR["🎲 Domain Randomization"]
        Tex[Texture]
        Light[Lighting]
        Pose[Object Pose]
        Cam[Camera]
    end

    subgraph Output["📦 Dataset Output"]
        Render[Rendered Images]
        GT[Ground Truth]
        Export[COCO/KITTI Format]
    end

    Assets --> Scene
    Scene --> DR
    DR --> Render
    Render --> GT
    GT --> Export
```

### D3.3: Domain Randomization Types

```mermaid
mindmap
  root((Domain Randomization))
    Visual
      Textures
      Lighting
      Backgrounds
    Geometric
      Object Poses
      Camera Angles
      Scene Layout
    Physical
      Object Scale
      Distractor Objects
    Sensor
      Noise Models
      Motion Blur
```

### D3.4: Ground Truth Types

```mermaid
flowchart TB
    subgraph GT["🏷️ Ground Truth Labels"]
        direction LR
        BB[2D Bounding Boxes]
        BB3D[3D Bounding Boxes]
        Seg[Semantic Segmentation]
        Inst[Instance Segmentation]
        Depth[Depth Maps]
        Pose[6DoF Poses]
    end

    Render[Rendered Frame] --> GT
    GT --> Dataset[Training Dataset]
```

### D3.5: Visual Odometry Pipeline

```mermaid
flowchart LR
    subgraph Input["📷 Input"]
        I1[Frame t-1]
        I2[Frame t]
    end

    subgraph VO["🔍 Visual Odometry"]
        Feat[Feature Extraction]
        Match[Feature Matching]
        Motion[Motion Estimation]
    end

    subgraph Output["📍 Output"]
        Pose[Pose Change Δ]
    end

    I1 --> Feat
    I2 --> Feat
    Feat --> Match
    Match --> Motion
    Motion --> Pose
```

### D3.6: VSLAM Architecture

```mermaid
flowchart TD
    subgraph Frontend["Frontend (Real-time)"]
        VO[Visual Odometry]
        Track[Feature Tracking]
        KF[Keyframe Selection]
    end

    subgraph Backend["Backend (Optimization)"]
        BA[Bundle Adjustment]
        LC[Loop Closure]
        Map[Map Management]
    end

    Camera[Camera Stream] --> VO
    VO --> Track
    Track --> KF
    KF --> BA
    BA --> Map
    Map --> LC
    LC -->|"Correction"| BA

    Map --> Output[Pose + Map]
```

### D3.7: Isaac ROS VSLAM Integration

```mermaid
flowchart LR
    subgraph Sensors["📷 Sensors"]
        Stereo[Stereo Camera]
        IMU[IMU]
    end

    subgraph Isaac["🚀 Isaac ROS"]
        VSLAM[cuVSLAM Node]
        GPU[GPU Acceleration]
    end

    subgraph Output["📍 Output"]
        Odom[Odometry]
        TF[TF Transforms]
    end

    Stereo --> VSLAM
    IMU --> VSLAM
    GPU -.->|"Accelerates"| VSLAM
    VSLAM --> Odom
    VSLAM --> TF
```

### D3.8: Nav2 Architecture Overview

```mermaid
flowchart TD
    subgraph BT["🌳 Behavior Tree"]
        BTNav[NavigateToPose]
    end

    subgraph Planning["📐 Planning"]
        GP[Global Planner]
        LP[Local Planner]
    end

    subgraph Execution["⚡ Execution"]
        Ctrl[Controller]
        Rec[Recovery Behaviors]
    end

    subgraph Maps["🗺️ Maps"]
        CM[Costmap]
    end

    BTNav --> GP
    BTNav --> LP
    GP --> CM
    LP --> CM
    GP --> Ctrl
    LP --> Ctrl
    Ctrl --> Rec
```

### D3.9: Costmap Layer Composition

```mermaid
flowchart TB
    subgraph Layers["📊 Costmap Layers"]
        direction TB
        L1[Inflation Layer]
        L2[Obstacle Layer]
        L3[Static Layer]
    end

    subgraph Sources["📡 Data Sources"]
        Map[Static Map]
        Sensors[Sensor Data]
        Config[Inflation Radius]
    end

    Map --> L3
    Sensors --> L2
    Config --> L1

    L3 --> L2
    L2 --> L1
    L1 --> Final[Combined Costmap]
```

### D3.10: Global vs Local Planning

```mermaid
flowchart LR
    subgraph Global["🌍 Global Planner"]
        GC[Global Costmap]
        GP[Path Search]
        Path[Global Path]
    end

    subgraph Local["📍 Local Planner"]
        LC[Local Costmap]
        LP[Trajectory Optimization]
        Cmd[Velocity Commands]
    end

    Goal[Navigation Goal] --> GC
    GC --> GP
    GP --> Path
    Path --> LC
    LC --> LP
    LP --> Cmd
    Cmd --> Robot[Robot Motion]
```

### D3.11: Navigation Behavior Tree

```mermaid
flowchart TD
    Root[NavigateToPose]
    Root --> Seq1[Sequence]

    Seq1 --> ComputePath[ComputePathToPose]
    Seq1 --> Fallback[Fallback]

    Fallback --> FollowPath[FollowPath]
    Fallback --> Recovery[RecoveryNode]

    Recovery --> ClearCostmap[ClearCostmap]
    Recovery --> Spin[Spin]
    Recovery --> Wait[Wait]
```

---

## Code Snippets

### C3.1: Isaac Sim Replicator Concept

```python
# Conceptual synthetic data generation with Isaac Sim Replicator
import omni.replicator.core as rep

# Create randomized scene
with rep.new_layer():
    # Camera setup
    camera = rep.create.camera(
        position=(0, 0, 2),
        look_at=(0, 0, 0)
    )

    # Domain randomization
    with rep.trigger.on_frame(num_frames=1000):
        rep.randomizer.rotation(
            rep.get.prim("/World/Object"),
            distribution="uniform",
            min=(-180, -180, -180),
            max=(180, 180, 180)
        )
        rep.randomizer.light(
            intensity=(500, 2000)
        )

    # Output configuration
    rep.WriterRegistry.get("BasicWriter")(
        output_dir="/data/synthetic",
        rgb=True,
        bounding_box_2d_tight=True,
        semantic_segmentation=True
    )
```

### C3.2: Isaac ROS VSLAM Launch Concept

```yaml
# config/vslam_params.yaml
isaac_ros_visual_slam:
  ros__parameters:
    enable_slam_visualization: true
    enable_observations_view: true
    enable_landmarks_view: true
    denoise_input_images: false
    rectified_images: true
    enable_imu_fusion: true
    gyro_noise_density: 0.000244
    gyro_random_walk: 0.000019
    accel_noise_density: 0.001862
    accel_random_walk: 0.003
    calibration_frequency: 200.0
```

### C3.3: Nav2 Parameters Concept

```yaml
# config/nav2_params.yaml
bt_navigator:
  ros__parameters:
    default_bt_xml_filename: "navigate_to_pose_w_replanning_and_recovery.xml"

global_costmap:
  ros__parameters:
    update_frequency: 1.0
    publish_frequency: 1.0
    robot_radius: 0.3
    resolution: 0.05
    plugins: ["static_layer", "obstacle_layer", "inflation_layer"]

local_costmap:
  ros__parameters:
    update_frequency: 5.0
    publish_frequency: 2.0
    robot_radius: 0.3
    resolution: 0.05
    plugins: ["obstacle_layer", "inflation_layer"]
```

### C3.4: Costmap Layer Configuration Concept

```yaml
# Costmap layer configuration
static_layer:
  plugin: "nav2_costmap_2d::StaticLayer"
  map_subscribe_transient_local: true

obstacle_layer:
  plugin: "nav2_costmap_2d::ObstacleLayer"
  observation_sources: scan depth
  scan:
    topic: /scan
    max_obstacle_height: 2.0
    clearing: true
    marking: true
  depth:
    topic: /depth/points
    max_obstacle_height: 2.0

inflation_layer:
  plugin: "nav2_costmap_2d::InflationLayer"
  cost_scaling_factor: 3.0
  inflation_radius: 0.55
```

---

## Key Technology Reference

| Component | Technology | Purpose |
|-----------|------------|---------|
| Synthetic Data | Isaac Sim + Replicator | Generate training data with ground truth |
| VSLAM | Isaac ROS cuVSLAM | GPU-accelerated visual SLAM |
| Navigation | Nav2 | Path planning and execution |
| Costmap | Nav2 Costmap 2D | Obstacle representation |
| Behavior | Nav2 BT Navigator | Decision logic for navigation |

---

**Usage**: Import these diagrams and snippets into chapter markdown files using MDX imports or copy-paste.
