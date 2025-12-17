# Module 1 Assets: Diagrams and Code Snippets

This file contains reusable diagrams and code snippets for Module 1 chapters.

---

## D1.1: Nervous System Analogy

```mermaid
mindmap
  root((Robot Nervous System))
    Neurons
      Nodes
        Independent processes
        Defined interfaces
    Sensory Pathways
      Topics
        Continuous data streams
        Many-to-many
    Motor Commands
      Services
        Request-response
        Discrete actions
    Neural Signals
      Messages
        Typed data packets
        Structured information
```

**Alternative flowchart version:**

```mermaid
flowchart LR
    subgraph Biological["🧠 Biological System"]
        N[Neurons]
        SP[Sensory Pathways]
        MC[Motor Commands]
        NS[Neural Signals]
    end

    subgraph ROS2["🤖 ROS 2 System"]
        Nodes[Nodes]
        Topics[Topics]
        Services[Services]
        Messages[Messages]
    end

    N -->|"maps to"| Nodes
    SP -->|"maps to"| Topics
    MC -->|"maps to"| Services
    NS -->|"maps to"| Messages
```

---

## D1.2: ROS 2 Node Graph

```mermaid
flowchart LR
    subgraph Sensors["Sensor Nodes"]
        CAM[camera_node]
        LID[lidar_node]
        IMU[imu_node]
    end

    subgraph Processing["Processing Nodes"]
        PER[perception_node]
        PLAN[planner_node]
    end

    subgraph Control["Control Nodes"]
        CTRL[controller_node]
    end

    CAM -->|"/camera/image"| PER
    LID -->|"/lidar/scan"| PER
    IMU -->|"/imu/data"| CTRL
    PER -->|"/obstacles"| PLAN
    PLAN -->|"/path"| CTRL
    CTRL -->|"/cmd_vel"| MOT[Motors]

    PER -.->|"/get_objects"| SRV1[Service]
    PLAN -.->|"/set_goal"| SRV2[Service]
```

---

## D1.3: Topic Publish-Subscribe Sequence

```mermaid
sequenceDiagram
    participant Pub as Publisher Node
    participant Topic as /sensor/data
    participant Sub1 as Subscriber 1
    participant Sub2 as Subscriber 2

    Pub->>Topic: publish(message)
    Topic-->>Sub1: callback(message)
    Topic-->>Sub2: callback(message)
    Note over Pub,Sub2: Asynchronous, fire-and-forget
    Pub->>Topic: publish(message)
    Topic-->>Sub1: callback(message)
    Topic-->>Sub2: callback(message)
```

---

## D1.4: Service Request-Response Sequence

```mermaid
sequenceDiagram
    participant Client as Client Node
    participant Service as /spawn_entity
    participant Server as Server Node

    Client->>Service: request(params)
    Service->>Server: handle_request(params)
    Server-->>Server: process request
    Server->>Service: response(result)
    Service-->>Client: return result
    Note over Client,Server: Synchronous, blocking call
```

---

## D1.5: Communication Pattern Decision Flowchart

```mermaid
flowchart TD
    START[Need to communicate?] --> Q1{Continuous data stream?}
    Q1 -->|Yes| TOPIC[Use Topic]
    Q1 -->|No| Q2{Need response?}
    Q2 -->|No| TOPIC
    Q2 -->|Yes| Q3{Long-running task?}
    Q3 -->|No| SERVICE[Use Service]
    Q3 -->|Yes| ACTION[Use Action]

    TOPIC --> EX1["Examples: sensor data,<br/>robot state, commands"]
    SERVICE --> EX2["Examples: spawn entity,<br/>get parameter, configure"]
    ACTION --> EX3["Examples: navigate to goal,<br/>pick object, follow path"]
```

---

## C1.1: Topic Message Definition

```yaml
# Example: sensor_msgs/msg/LaserScan.msg
# Standard message for LiDAR data

Header header           # timestamp and frame
float32 angle_min       # start angle of scan [rad]
float32 angle_max       # end angle of scan [rad]
float32 angle_increment # angular step between measurements [rad]
float32 time_increment  # time between measurements [sec]
float32 scan_time       # time for complete scan [sec]
float32 range_min       # minimum range value [m]
float32 range_max       # maximum range value [m]
float32[] ranges        # range data [m]
float32[] intensities   # intensity data (optional)
```

---

## C1.2: Service Definition

```yaml
# Example: std_srvs/srv/SetBool.srv
# Standard service for toggling boolean state

# Request
bool data    # Desired state

---

# Response
bool success # Whether the call succeeded
string message # Status message
```

**Custom service example:**

```yaml
# example_interfaces/srv/SpawnRobot.srv

# Request
string robot_name
float64 x
float64 y
float64 theta

---

# Response
bool success
string status_message
int32 robot_id
```

---

## Usage Notes

- Copy Mermaid blocks directly into chapter markdown files
- Docusaurus will render Mermaid diagrams automatically
- Code snippets use YAML format for message/service definitions
- Adjust diagram labels and colors as needed for specific contexts
