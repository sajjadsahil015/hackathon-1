# Physical AI & Humanoid Robotics

A conceptual guide to building autonomous humanoid robots with ROS 2, simulation, NVIDIA Isaac, and Vision-Language-Action systems.

## Overview

This book provides a comprehensive foundation for understanding autonomous humanoid robot systems across four modules:

| Module | Topic | Chapters |
|--------|-------|----------|
| **Module 1** | The Robotic Nervous System (ROS 2) | 3 |
| **Module 2** | The Digital Twin (Simulation) | 3 |
| **Module 3** | The AI-Robot Brain (NVIDIA Isaac) | 3 |
| **Module 4** | Vision-Language-Action | 3 |

**Total Reading Time**: ~10.5 hours

## Project Structure

```
physical-ai-book/
├── frontend/                      # Docusaurus documentation site
│   ├── docs/                      # Book content (markdown)
│   ├── src/                       # Custom components and CSS
│   ├── static/                    # Static assets (images)
│   ├── docusaurus.config.js       # Docusaurus configuration
│   ├── sidebars.js                # Sidebar navigation
│   └── package.json               # Frontend dependencies
├── backend/                       # Backend API (coming soon)
├── specs/                         # Design specifications
├── history/                       # Prompt history records & ADRs
├── .specify/                      # SpecKit configuration
├── tasks.md                       # Project task list
└── README.md                      # This file
```

## Quick Start

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn

### Frontend (Documentation Site)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The site will be available at `http://localhost:3000`.

### Build for Production

```bash
cd frontend

# Build static files
npm run build

# Serve production build locally
npm run serve
```

## Features

- **Mermaid Diagrams**: 50+ embedded diagrams for visual learning
- **Code Snippets**: Python, YAML, and XML examples
- **Dark Mode**: Full dark mode support
- **Responsive**: Mobile-friendly design
- **Glossary**: 100+ terms organized by module

## Deployment

### GitHub Pages

1. Update `frontend/docusaurus.config.js`:
   - Set `url` to your GitHub Pages URL
   - Set `baseUrl` to `/physical-ai-book/` (or your repo name)
   - Set `organizationName` to your GitHub username
   - Set `projectName` to your repository name

2. Deploy:
   ```bash
   cd frontend
   npm run deploy
   ```

### Other Platforms

Build the static files and deploy to any static hosting:

```bash
cd frontend
npm run build
# Upload contents of 'frontend/build' folder
```

## Contributing

Contributions are welcome! Please see the specs/ directory for design documentation.

## License

MIT License - see LICENSE file for details.

## Resources

- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [NVIDIA Isaac](https://developer.nvidia.com/isaac)
- [Nav2 Navigation](https://navigation.ros.org/)
- [Gazebo Simulation](https://gazebosim.org/)
