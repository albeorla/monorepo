# Project Decisions Log

## Architectural Decisions

### AD-001: Monorepo Structure (2025-04-22)
- **Decision**: Use Bazel as the build system for a polyglot monorepo
- **Context**: Need to support Python, TypeScript, Go, and Rust with consistent tooling
- **Consequences**: Increased setup complexity but better long-term consistency

### AD-002: Language Support Prioritization (2025-04-22)
- **Decision**: Prioritize Python and TypeScript (P0), make Go and Rust optional (P1)
- **Context**: Core services use Python and TypeScript, while Go and Rust are emerging needs
- **Consequences**: Reduces initial complexity; allows growth without breaking changes

### AD-003: Cost Efficiency as First-Class Concern (2025-04-22)
- **Decision**: Implement cost tracking and budgeting as a P0 feature
- **Context**: CI/CD and infrastructure costs can grow unexpectedly in a monorepo
- **Consequences**: Additional initial work but better long-term cost management

### AD-004: Eisenhower Matrix for Task Prioritization (2025-05-08)
- **Decision**: Implement Eisenhower Matrix in todost module for task prioritization
- **Context**: Need a systematic method for categorizing tasks beyond simple priority levels
- **Consequences**: Enhanced prioritization capabilities with more nuanced task classification

## Technical Decisions

### TD-001: Using Cookiecutter and Hygen for Templates (2025-04-23)
- **Decision**: Use Cookiecutter for Python modules and Hygen for TypeScript modules
- **Context**: Need consistent project templates with customizable options
- **Consequences**: Slightly different workflows per language but better idiomatic code

### TD-002: Ruff for Python Linting (2025-04-24)
- **Decision**: Use Ruff instead of multiple separate Python linting tools
- **Context**: Need fast, comprehensive linting with minimal configuration
- **Consequences**: Single tool dependency, faster execution, but some customization limitations

### TD-003: GitHub Actions for CI/CD (2025-04-24)
- **Decision**: Use GitHub Actions instead of self-hosted CI
- **Context**: Need integration with GitHub and cost-effective CI/CD
- **Consequences**: Reliance on GitHub ecosystem but reduced infrastructure management

### TD-004: GitHub Container Registry for Images (2025-05-07)
- **Decision**: Use GitHub Container Registry (GHCR) for container image storage
- **Context**: Need integrated container registry with GitHub workflow support
- **Consequences**: Improved CI/CD integration, free tier for open source projects

### TD-005: Eisenhower Matrix Implementation Approach (2025-05-08)
- **Decision**: Implement Eisenhower Matrix using boolean flags for urgency/importance
- **Context**: Need to extend GTD model with Eisenhower quadrants while maintaining compatibility
- **Consequences**: More flexible task classification with clear quadrant boundaries

## Process Decisions

### PD-001: Agile Sprint Structure (2025-04-22)
- **Decision**: Use 2-week sprints with .codex directory for tracking
- **Context**: Need structured planning that aligns with PRD milestones
- **Consequences**: More documentation overhead but better project visibility

### PD-002: MCP Tools for Planning (2025-05-06)
- **Decision**: Integrate MCP softwareplanner into the development workflow
- **Context**: Need structured planning tools that integrate with Claude Code
- **Consequences**: Enhanced planning capabilities with better task tracking

### PD-003: Documentation Standards (2025-05-06)
- **Decision**: Maintain comprehensive docs in dedicated docs directory with PRD references
- **Context**: Need traceability between requirements and implementation
- **Consequences**: Improved project tracking and onboarding for new developers

### PD-004: Source of Truth for Planning (2025-05-08)
- **Decision**: Use sprint files in docs/planning/sprints/ as the primary source of truth
- **Context**: Need a consistent place to track planned work and progress
- **Consequences**: Clear accountability and tracking, with dashboard providing a quick overview