# Bazel Monorepo Platform Documentation

This directory contains all documentation for the Bazel Monorepo Platform project. The documentation is organized into the following sections:

## Key Documents

- [Product Requirements Document (PRD)](PRD.md) - High-level product requirements and vision
- [Planning Documentation](planning/README.md) - Sprint plans, roadmap, and project dashboard
- [Architectural Decisions](decisions/README.md) - Decision records explaining key technical choices
- [Work Reports](reports/README.md) - Detailed summaries of completed work

## Directory Structure

```
docs/
├── PRD.md                          # Product Requirements Document
├── decisions/                      # Architectural Decision Records
│   ├── README.md                   # Overview of decisions documentation
│   └── decisions.md                # Detailed decision log
├── planning/                       # Project planning documents
│   ├── README.md                   # Overview of planning process
│   ├── dashboard.md                # Current project status and metrics
│   ├── roadmap.md                  # Long-term project roadmap
│   └── sprints/                    # Sprint planning documents
│       ├── sprint_2025-04-23.md    # Sprint 1 (Apr 23-May 5)
│       └── sprint_2025-05-06.md    # Sprint 2 (May 6-20)
└── reports/                        # Work summaries and progress reports
    ├── README.md                   # Overview of reporting process
    ├── work_summary_2025-04-23.md  # Python infrastructure work
    ├── work_summary_2025-04-24.md  # CI/CD pipeline work
    └── work_summary_2025-05-06.md  # Repository maintenance work
```

## Documentation Workflows

### For Developers

1. Review the PRD to understand project requirements
2. Check current sprint tasks in `planning/sprints/` directory
3. Update work progress in daily/weekly work summaries

### For Project Managers

1. Track overall progress in the dashboard and roadmap
2. Review decisions for technical direction and rationale
3. Use sprint plans and work summaries to monitor progress

## Documentation Standards

All documentation should:
1. Reference PRD requirements where applicable (e.g., F-1, F-5)
2. Include clear implementation details and next steps
3. Be updated alongside code changes
4. Follow markdown formatting conventions