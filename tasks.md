# Tasks: Physical AI & Humanoid Robotics Book

**Input**: Design documents from `/specs/` (all 4 modules), Docusaurus configuration files
**Prerequisites**: Node.js 18+, npm, Git

**Tests**: Manual review (Docusaurus build validation, link checking)

**Organization**: Tasks are grouped by development phase for the complete book project.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- Include exact file paths in descriptions

## Path Conventions

- **Documentation content**: `docs/`
- **Specifications**: `specs/`
- **Static assets**: `static/`
- **Configuration**: Root directory (`package.json`, `docusaurus.config.js`, etc.)

---

## Phase 1: Environment Setup

**Purpose**: Install Docusaurus and initialize the development environment

- [ ] T001 Install Node.js dependencies by running `npm install` in project root
- [ ] T002 Verify Docusaurus installation by running `npm run start`
- [ ] T003 [P] Create .nvmrc file specifying Node.js version 18 in project root
- [ ] T004 [P] Verify Mermaid diagram rendering works by visiting any chapter with diagrams

**Checkpoint**: Development server running at localhost:3000

---

## Phase 2: Docusaurus Configuration Refinement

**Purpose**: Finalize Docusaurus configuration for production deployment

- [ ] T005 Update docusaurus.config.js with actual GitHub username and repository name
- [ ] T006 [P] Replace placeholder logo.svg with production logo in static/img/logo.svg
- [ ] T007 [P] Create proper favicon.ico (32x32 ICO format) in static/img/favicon.ico
- [ ] T008 [P] Create social-card.png (1200x630) for Open Graph in static/img/social-card.png
- [ ] T009 [P] Update footer links in docusaurus.config.js with actual repository URLs
- [ ] T010 Verify dark mode toggle works correctly across all pages

**Checkpoint**: Site configuration complete with proper branding

---

## Phase 3: Content Validation - Module 1 (ROS 2)

**Purpose**: Validate Module 1 content renders correctly in Docusaurus

**Goal**: Verify all Module 1 chapters render with proper formatting and diagrams

**Independent Test**: Navigate through all 3 chapters, verify Mermaid diagrams render, all links work

- [ ] T011 [US1] Verify docs/module-1-ros2/01-ros2-architecture.md renders correctly
- [ ] T012 [US1] Verify all Mermaid diagrams in Chapter 1 render properly
- [ ] T013 [US1] Verify docs/module-1-ros2/02-python-agents-rclpy.md renders correctly
- [ ] T014 [US1] Verify all code snippets in Chapter 2 have proper syntax highlighting
- [ ] T015 [US1] Verify docs/module-1-ros2/03-urdf-humanoid.md renders correctly
- [ ] T016 [US1] Verify XML code blocks in Chapter 3 render with proper formatting
- [ ] T017 [US1] Test all external links in Module 1 chapters are accessible

**Checkpoint**: Module 1 renders correctly with all diagrams and code blocks

---

## Phase 4: Content Validation - Module 2 (Simulation)

**Purpose**: Validate Module 2 content renders correctly in Docusaurus

**Goal**: Verify all Module 2 chapters render with proper formatting and diagrams

**Independent Test**: Navigate through all 3 chapters, verify Mermaid diagrams render, all links work

- [ ] T018 [US2] Verify docs/module-2-simulation/01-digital-twins-gazebo.md renders correctly
- [ ] T019 [US2] Verify all Mermaid diagrams in Chapter 1 render properly
- [ ] T020 [US2] Verify docs/module-2-simulation/02-unity-hri-rendering.md renders correctly
- [ ] T021 [US2] Verify comparison tables in Chapter 2 render with proper formatting
- [ ] T022 [US2] Verify docs/module-2-simulation/03-simulated-sensors.md renders correctly
- [ ] T023 [US2] Verify XML/YAML code blocks in Chapter 3 render properly
- [ ] T024 [US2] Test all external links in Module 2 chapters are accessible

**Checkpoint**: Module 2 renders correctly with all diagrams and code blocks

---

## Phase 5: Content Validation - Module 3 (Isaac)

**Purpose**: Validate Module 3 content renders correctly in Docusaurus

**Goal**: Verify all Module 3 chapters render with proper formatting and diagrams

**Independent Test**: Navigate through all 3 chapters, verify Mermaid diagrams render, all links work

- [ ] T025 [US3] Verify docs/module-3-isaac/01-perception-isaac-sim.md renders correctly
- [ ] T026 [US3] Verify all Mermaid diagrams in Chapter 1 render properly
- [ ] T027 [US3] Verify docs/module-3-isaac/02-vslam-isaac-ros.md renders correctly
- [ ] T028 [US3] Verify YAML config snippets in Chapter 2 render properly
- [ ] T029 [US3] Verify docs/module-3-isaac/03-nav2-path-planning.md renders correctly
- [ ] T030 [US3] Verify behavior tree diagrams in Chapter 3 render properly
- [ ] T031 [US3] Test all external links in Module 3 chapters are accessible

**Checkpoint**: Module 3 renders correctly with all diagrams and code blocks

---

## Phase 6: Content Validation - Module 4 (VLA)

**Purpose**: Validate Module 4 content renders correctly in Docusaurus

**Goal**: Verify all Module 4 chapters including Capstone render properly

**Independent Test**: Navigate through all 3 chapters, verify Mermaid diagrams render, all links work

- [ ] T032 [US4] Verify docs/module-4-vla/01-vla-architecture.md renders correctly
- [ ] T033 [US4] Verify all Mermaid diagrams in Chapter 1 render properly
- [ ] T034 [US4] Verify docs/module-4-vla/02-voice-language-planning.md renders correctly
- [ ] T035 [US4] Verify sequence diagrams in Chapter 2 render properly
- [ ] T036 [US4] Verify docs/module-4-vla/03-capstone-autonomous.md renders correctly
- [ ] T037 [US4] Verify the comprehensive autonomy stack diagrams in Capstone render
- [ ] T038 [US4] Test all external links in Module 4 chapters are accessible

**Checkpoint**: Module 4 renders correctly with all diagrams and code blocks

---

## Phase 7: Navigation and Cross-References

**Purpose**: Verify navigation structure and cross-module references

- [ ] T039 Verify sidebar navigation shows all 4 modules with correct chapter ordering
- [ ] T040 Verify docs/intro.md renders as the landing page
- [ ] T041 Verify docs/glossary.md renders correctly with all tables
- [ ] T042 [P] Test navigation between chapters using "Next" and "Previous" links
- [ ] T043 [P] Verify table of contents renders correctly on each page
- [ ] T044 Verify module category pages (/module-1-ros2, etc.) display chapter lists
- [ ] T045 Test search functionality (if Algolia configured) or document search setup needed

**Checkpoint**: All navigation works correctly across the book

---

## Phase 8: Build and Deployment Preparation

**Purpose**: Prepare for production deployment

- [ ] T046 Run `npm run build` and verify build completes without errors
- [ ] T047 Run `npm run serve` and test production build locally
- [ ] T048 [P] Fix any broken links reported during build
- [ ] T049 [P] Fix any Mermaid rendering issues in production build
- [ ] T050 Verify all images and assets are included in build output
- [ ] T051 Check build output size and optimize if needed (target < 50MB)
- [ ] T052 [P] Create CNAME file in static/ if using custom domain

**Checkpoint**: Production build ready for deployment

---

## Phase 9: GitHub Pages Deployment

**Purpose**: Deploy the book to GitHub Pages

- [ ] T053 Create GitHub repository if not already created
- [ ] T054 Push all code to GitHub main branch
- [ ] T055 Configure GitHub Pages in repository settings (Settings > Pages)
- [ ] T056 Run `npm run deploy` to deploy to gh-pages branch
- [ ] T057 Verify site is accessible at https://[username].github.io/[repo-name]/
- [ ] T058 Test all pages load correctly in production
- [ ] T059 Verify Mermaid diagrams render in production environment
- [ ] T060 Test mobile responsiveness on production site

**Checkpoint**: Book deployed and accessible on GitHub Pages

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final polish and documentation

- [ ] T061 [P] Add Google Analytics or Plausible analytics (optional) in docusaurus.config.js
- [ ] T062 [P] Configure Algolia DocSearch for full-text search (optional)
- [ ] T063 Update README.md with actual deployment URL and badges
- [ ] T064 [P] Create CONTRIBUTING.md with contribution guidelines
- [ ] T065 [P] Create LICENSE file if not present
- [ ] T066 Run Lighthouse audit and address any accessibility issues
- [ ] T067 Test all success check questions render correctly with tip styling
- [ ] T068 Final review of all pages for formatting consistency
- [ ] T069 Create GitHub release with version tag v1.0.0

**Checkpoint**: Book fully deployed, documented, and ready for readers

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Environment Setup)**: No dependencies - can start immediately
- **Phase 2 (Configuration)**: Depends on Phase 1 (npm install must complete)
- **Phases 3-6 (Content Validation)**: Depend on Phase 1 - Can run in parallel
- **Phase 7 (Navigation)**: Depends on Phases 3-6 completion
- **Phase 8 (Build)**: Depends on Phase 7 completion
- **Phase 9 (Deployment)**: Depends on Phase 8 (build must succeed)
- **Phase 10 (Polish)**: Depends on Phase 9 (deployment must work)

### Content Validation Parallelization

Modules 1-4 validation (Phases 3-6) can be done in parallel by different reviewers:

- **Reviewer A**: Module 1 (ROS 2)
- **Reviewer B**: Module 2 (Simulation)
- **Reviewer C**: Module 3 (Isaac)
- **Reviewer D**: Module 4 (VLA)

### Within Each Phase

- Tasks marked [P] can run in parallel
- Other tasks should run sequentially

---

## Parallel Example: Content Validation

```bash
# Launch all module validations in parallel:
Task: "Verify Module 1 chapters render correctly"
Task: "Verify Module 2 chapters render correctly"
Task: "Verify Module 3 chapters render correctly"
Task: "Verify Module 4 chapters render correctly"

# Launch all link checks in parallel:
Task: "Test all external links in Module 1"
Task: "Test all external links in Module 2"
Task: "Test all external links in Module 3"
Task: "Test all external links in Module 4"
```

---

## Implementation Strategy

### MVP First (Phase 1-2 Only)

1. Complete Phase 1: Install dependencies
2. Complete Phase 2: Basic configuration
3. **STOP and VALIDATE**: Verify site runs locally
4. Demo development environment

### Incremental Delivery

1. Phases 1-2 → Development environment ready
2. Phases 3-6 → Content validated (can demo locally)
3. Phase 7 → Navigation complete
4. Phase 8 → Build ready
5. Phase 9 → **DEPLOYED** - Book live!
6. Phase 10 → Polish and enhancements

### Quick Start Commands

```bash
# Phase 1: Setup
npm install
npm run start

# Phase 8: Build
npm run build
npm run serve

# Phase 9: Deploy
npm run deploy
```

---

## Summary

| Phase | Tasks | Parallel Opportunities |
|-------|-------|----------------------|
| Environment Setup | 4 | 2 |
| Configuration | 6 | 4 |
| Module 1 Validation | 7 | 0 |
| Module 2 Validation | 7 | 0 |
| Module 3 Validation | 7 | 0 |
| Module 4 Validation | 7 | 0 |
| Navigation | 7 | 2 |
| Build Preparation | 7 | 3 |
| Deployment | 8 | 0 |
| Polish | 9 | 4 |
| **Total** | **69** | **15** |

---

## Notes

- [P] tasks = different files, no dependencies
- [US#] label maps task to module validation for traceability
- Run `npm run start` for development, `npm run build` for production
- Verify Mermaid diagrams render in both dev and production builds
- Test on multiple browsers (Chrome, Firefox, Safari)
- Mobile responsiveness is critical for documentation sites
