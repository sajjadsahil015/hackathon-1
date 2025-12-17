# Module 4 Assets: Vision-Language-Action & Autonomy

**Purpose**: Reusable Mermaid diagrams and code snippets for Module 4 chapters.

---

## Diagrams

### D4.1: VLA System Overview

```mermaid
flowchart LR
    subgraph Input["📥 Input"]
        Vis[Vision/Camera]
        Lang[Language/Voice]
    end

    subgraph VLA["🧠 VLA System"]
        VE[Vision Encoder]
        LM[Language Model]
        Fuse[Multimodal Fusion]
        AD[Action Decoder]
    end

    subgraph Output["📤 Output"]
        Act[Robot Actions]
    end

    Vis --> VE
    Lang --> LM
    VE --> Fuse
    LM --> Fuse
    Fuse --> AD
    AD --> Act
```

### D4.2: Vision Encoder Pipeline

```mermaid
flowchart LR
    subgraph Input["📷 Visual Input"]
        RGB[RGB Image]
        Depth[Depth Image]
    end

    subgraph Encoder["🔍 Vision Encoder"]
        Backbone[CNN/ViT Backbone]
        Features[Feature Maps]
        Pool[Spatial Pooling]
    end

    subgraph Output["📊 Output"]
        Emb[Visual Embeddings]
    end

    RGB --> Backbone
    Depth --> Backbone
    Backbone --> Features
    Features --> Pool
    Pool --> Emb
```

### D4.3: Language Model in VLA

```mermaid
flowchart LR
    subgraph Input["💬 Language Input"]
        Text[Text Command]
        Tok[Tokenizer]
    end

    subgraph LLM["🧠 Language Model"]
        Enc[Encoder]
        Attn[Self-Attention]
        Dec[Decoder]
    end

    subgraph Output["📊 Output"]
        Intent[Intent Representation]
    end

    Text --> Tok
    Tok --> Enc
    Enc --> Attn
    Attn --> Dec
    Dec --> Intent
```

### D4.4: Multimodal Fusion Approaches

```mermaid
flowchart TB
    subgraph Early["Early Fusion"]
        E1[Visual Features] --> EC[Concatenate]
        E2[Language Features] --> EC
        EC --> EP[Joint Processing]
    end

    subgraph Late["Late Fusion"]
        L1[Visual Processing] --> LP[Processed Visual]
        L2[Language Processing] --> LQ[Processed Language]
        LP --> LM[Merge]
        LQ --> LM
    end

    subgraph Cross["Cross-Attention"]
        C1[Visual Tokens] --> CA[Cross-Attention]
        C2[Language Tokens] --> CA
        CA --> CO[Fused Representation]
    end
```

### D4.5: Action Space for Humanoids

```mermaid
mindmap
  root((Action Space))
    Navigation
      MoveTo
      Turn
      Stop
    Manipulation
      Reach
      Grasp
      Release
      Place
    Head/Gaze
      LookAt
      Track
    Communication
      Speak
      Gesture
    Whole Body
      Sit
      Stand
      Wave
```

### D4.6: Voice-to-Action Pipeline

```mermaid
flowchart LR
    subgraph Voice["🎤 Voice Input"]
        Audio[Audio Waveform]
    end

    subgraph STT["🗣️ Speech Recognition"]
        Whisper[Whisper/ASR]
        Trans[Transcript]
    end

    subgraph NLU["🧠 Understanding"]
        Parse[Intent Parser]
        Intent[Structured Intent]
    end

    subgraph Plan["📋 Planning"]
        LLM[LLM Planner]
        Tasks[Task Plan]
    end

    subgraph Execute["⚡ Execution"]
        ROS[ROS 2 Actions]
    end

    Audio --> Whisper
    Whisper --> Trans
    Trans --> Parse
    Parse --> Intent
    Intent --> LLM
    LLM --> Tasks
    Tasks --> ROS
```

### D4.7: Whisper Speech Pipeline

```mermaid
flowchart LR
    subgraph Input["🎤 Input"]
        Mic[Microphone]
        Stream[Audio Stream]
    end

    subgraph Whisper["🗣️ Whisper"]
        Mel[Mel Spectrogram]
        Enc[Audio Encoder]
        Dec[Text Decoder]
    end

    subgraph Output["📝 Output"]
        Text[Transcript]
        Conf[Confidence]
    end

    Mic --> Stream
    Stream --> Mel
    Mel --> Enc
    Enc --> Dec
    Dec --> Text
    Dec --> Conf
```

### D4.8: Intent Extraction

```mermaid
flowchart TD
    Input["'Fetch the red cup from the kitchen'"]

    subgraph Parse["🔍 Parsing"]
        Action[Action: fetch]
        Target[Target: red cup]
        Location[Location: kitchen]
        Constraints[Constraints: none]
    end

    Input --> Parse

    subgraph Intent["📋 Structured Intent"]
        JSON["{ action: 'fetch',
               target: 'red cup',
               from: 'kitchen' }"]
    end

    Parse --> Intent
```

### D4.9: LLM Task Decomposition

```mermaid
flowchart TD
    subgraph Input["📥 Input"]
        Intent["Intent: Fetch red cup from kitchen"]
        Context["Context: Robot in living room"]
    end

    subgraph LLM["🧠 LLM Planner"]
        Prompt[Structured Prompt]
        Reason[Chain of Thought]
        Output[Task List]
    end

    subgraph Tasks["📋 Task Plan"]
        T1["1. Navigate to kitchen"]
        T2["2. Locate red cup"]
        T3["3. Approach cup"]
        T4["4. Grasp cup"]
        T5["5. Navigate to user"]
        T6["6. Present cup"]
    end

    Intent --> Prompt
    Context --> Prompt
    Prompt --> Reason
    Reason --> Output
    Output --> T1 --> T2 --> T3 --> T4 --> T5 --> T6
```

### D4.10: Grounding Process

```mermaid
sequenceDiagram
    participant Lang as Language Parser
    participant Perc as Perception System
    participant Ground as Grounding Module

    Lang->>Ground: Reference: "red cup"
    Ground->>Perc: Query objects in view
    Perc->>Ground: Detected objects with poses
    Note over Ground: Match "red cup" to candidates
    Ground->>Ground: Score candidates
    Ground->>Lang: Resolved: Object_42 @ (1.2, 0.5, 0.8)
```

### D4.11: Action Primitive Catalog

| Primitive | Parameters | ROS 2 Interface | Description |
|-----------|------------|-----------------|-------------|
| `navigate_to` | pose, tolerance | `nav2_msgs/NavigateToPose` | Move to location |
| `look_at` | point, duration | `control_msgs/FollowJointTrajectory` | Direct gaze |
| `grasp` | object_id, force | Custom action | Close gripper |
| `release` | - | Custom action | Open gripper |
| `reach` | pose, velocity | `moveit_msgs/MoveGroup` | Move arm |
| `speak` | text | `std_msgs/String` | Text-to-speech |

### D4.12: Complete Autonomy Stack

```mermaid
flowchart TB
    subgraph Sensors["📷 Sensors (Module 2)"]
        Cam[Cameras]
        LiDAR[LiDAR]
        IMU[IMU]
    end

    subgraph Perception["🔍 Perception (Module 3)"]
        Det[Object Detection]
        Seg[Segmentation]
        SLAM[VSLAM]
    end

    subgraph Planning["🧠 Planning (Module 4)"]
        VLA[VLA System]
        TaskPlan[Task Planning]
        NavPlan[Nav2 Planning]
    end

    subgraph Control["⚡ Control (Module 1)"]
        Actions[ROS 2 Actions]
        Motion[Motion Control]
    end

    Sensors --> Perception
    Perception --> Planning
    Planning --> Control
    Control --> Robot[🤖 Robot]

    Voice[🎤 Voice] --> VLA
```

### D4.13: Fetch Drink Scenario Sequence

```mermaid
sequenceDiagram
    participant User
    participant Voice as Voice Pipeline
    participant VLA as VLA System
    participant Nav as Navigation
    participant Arm as Manipulation
    participant Perc as Perception

    User->>Voice: "Get me a drink"
    Voice->>VLA: Intent: fetch drink

    Note over VLA: Task decomposition
    VLA->>Perc: Locate drinks
    Perc->>VLA: Cup at kitchen counter

    VLA->>Nav: Navigate to kitchen
    Nav->>Nav: Path planning
    Nav-->>VLA: Arrived

    VLA->>Perc: Locate cup precisely
    Perc->>VLA: Cup pose

    VLA->>Arm: Approach and grasp
    Arm-->>VLA: Grasped

    VLA->>Nav: Navigate to user
    Nav-->>VLA: Arrived

    VLA->>Arm: Present cup
    VLA->>User: "Here's your drink"
```

### D4.14: Data Flow Trace

```mermaid
flowchart LR
    subgraph Voice["🎤"]
        A1[Audio] -->|16kHz| A2[Whisper]
        A2 -->|Text| A3[Parser]
    end

    subgraph Vision["📷"]
        V1[RGB-D] -->|640x480| V2[Detection]
        V2 -->|Boxes| V3[Tracker]
    end

    subgraph Fusion["🧠"]
        A3 --> F1[Intent]
        V3 --> F2[Objects]
        F1 --> F3[Grounding]
        F2 --> F3
    end

    subgraph Action["⚡"]
        F3 --> X1[Plan]
        X1 --> X2[ROS 2]
        X2 --> X3[Motion]
    end
```

### D4.15: Gap Analysis for Autonomous Humanoids

| Capability | Current State | Gap | Research Direction |
|------------|---------------|-----|-------------------|
| **Language Understanding** | Good for simple commands | Complex reasoning, ambiguity | Larger context LLMs |
| **Grounding** | Works in controlled scenes | Cluttered environments | Better open-vocab detection |
| **Task Planning** | Linear task sequences | Dynamic replanning | Hierarchical planners |
| **Manipulation** | Basic grasping | Dexterous manipulation | Learning-based control |
| **Recovery** | Limited | Graceful failure handling | Robust error recovery |

---

## Code Snippets

### C4.1: Voice Command Processing Concept

```python
# Conceptual voice-to-intent pipeline
import whisper
from openai import OpenAI

class VoiceToIntent:
    def __init__(self):
        self.whisper = whisper.load_model("base")
        self.llm = OpenAI()

    def transcribe(self, audio_path: str) -> str:
        result = self.whisper.transcribe(audio_path)
        return result["text"]

    def parse_intent(self, transcript: str) -> dict:
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "Extract intent as JSON: {action, target, location}"
            }, {
                "role": "user",
                "content": transcript
            }]
        )
        return json.loads(response.choices[0].message.content)
```

### C4.2: Task Decomposition Prompt Concept

```python
# Conceptual LLM prompt for task decomposition
DECOMPOSITION_PROMPT = """
You are a robot task planner. Given a high-level command and context,
decompose it into a sequence of primitive actions.

Available primitives:
- navigate_to(location): Move robot to location
- look_at(target): Direct gaze at target
- grasp(object): Pick up object
- release(): Release held object
- speak(text): Say something

Command: {command}
Context: {context}
Detected objects: {objects}

Output a JSON list of actions with parameters.
"""
```

### C4.3: ROS 2 Action Client Concept

```python
# Conceptual ROS 2 action execution
import rclpy
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose

class ActionExecutor:
    def __init__(self, node):
        self.nav_client = ActionClient(
            node, NavigateToPose, 'navigate_to_pose'
        )

    async def navigate_to(self, x: float, y: float, theta: float):
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        # Set orientation from theta...

        future = self.nav_client.send_goal_async(goal)
        result = await future
        return result.status
```

### C4.4: Grounding Module Concept

```python
# Conceptual grounding: language reference → object pose
class GroundingModule:
    def __init__(self, detector, embedder):
        self.detector = detector  # Object detector
        self.embedder = embedder  # Text embedder (CLIP-like)

    def ground(self, reference: str, image) -> dict:
        # Detect all objects
        detections = self.detector.detect(image)

        # Embed the language reference
        ref_embedding = self.embedder.encode_text(reference)

        # Score each detection
        scores = []
        for det in detections:
            crop = image[det.bbox]
            img_embedding = self.embedder.encode_image(crop)
            score = cosine_similarity(ref_embedding, img_embedding)
            scores.append((det, score))

        # Return best match
        best = max(scores, key=lambda x: x[1])
        return {"object": best[0], "confidence": best[1]}
```

---

## Integration Reference

| Book Module | Autonomy Layer | Key Interface |
|-------------|---------------|---------------|
| Module 1: ROS 2 | Control & Communication | Topics, Services, Actions |
| Module 2: Simulation | Virtual Testing | Gazebo/Unity environments |
| Module 3: Isaac | Perception & Localization | Detection, VSLAM, Nav2 |
| Module 4: VLA | Planning & Reasoning | Voice → Intent → Tasks |

---

**Usage**: Import these diagrams and snippets into chapter markdown files using MDX imports or copy-paste.
