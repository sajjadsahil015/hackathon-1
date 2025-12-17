// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  bookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'module-1-ros2/ros2-architecture',
          label: '1. ROS 2 Architecture',
        },
        {
          type: 'doc',
          id: 'module-1-ros2/python-agents-rclpy',
          label: '2. Python Agents with rclpy',
        },
        {
          type: 'doc',
          id: 'module-1-ros2/urdf-humanoid',
          label: '3. URDF for Humanoid Robots',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'module-2-simulation/digital-twins-gazebo',
          label: '1. Digital Twins and Gazebo',
        },
        {
          type: 'doc',
          id: 'module-2-simulation/unity-hri-rendering',
          label: '2. Unity and HRI Rendering',
        },
        {
          type: 'doc',
          id: 'module-2-simulation/simulated-sensors',
          label: '3. Simulated Sensors',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'module-3-isaac/perception-isaac-sim',
          label: '1. Perception and Isaac Sim',
        },
        {
          type: 'doc',
          id: 'module-3-isaac/vslam-isaac-ros',
          label: '2. VSLAM with Isaac ROS',
        },
        {
          type: 'doc',
          id: 'module-3-isaac/nav2-path-planning',
          label: '3. Path Planning with Nav2',
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action',
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'module-4-vla/vla-architecture',
          label: '1. VLA Architecture',
        },
        {
          type: 'doc',
          id: 'module-4-vla/voice-language-planning',
          label: '2. Voice and Language Planning',
        },
        {
          type: 'doc',
          id: 'module-4-vla/capstone-autonomous',
          label: '3. Capstone: Autonomous Humanoid',
        },
      ],
    },
    {
      type: 'doc',
      id: 'glossary',
      label: 'Glossary',
    },
  ],
};

export default sidebars;
