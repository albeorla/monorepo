# Monorepo Project Guide

## Project Structure

This monorepo contains multiple language-specific projects:

- `/python/` - Python projects including hello_python and todost
- `/go/` - Go projects including hello_go
- `/rust/` - Rust projects including hello_rust
- `/ts/` - TypeScript projects including hello_ts

## Agentic Workflows

When working with Codex CLI, use these core instructions for effective agentic problem-solving:

### 1. Persistence
Always see tasks through to completion before yielding control:
```
You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved.
```

### 2. Information Gathering
Avoid guesswork and use available tools:
```
If you are not sure about file content or codebase structure pertaining to the user's request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer.
```

### 3. Planning
Alternate between planning and acting:
```
You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully.
```

### Problem-Solving Strategy
Follow this step-by-step approach for complex tasks:
1. Understand the problem deeply
2. Investigate the codebase thoroughly
3. Develop a clear, step-by-step plan
4. Implement changes incrementally
5. Test frequently after each change
6. Debug as needed
7. Iterate until the solution is complete and verified

### Effective Code Modification
When modifying code, use these diff formats for higher success rates:

```
<edit>
<file>path/to/file.py</file>
<old_code>
def function():
    pass
</old_code>
<new_code>
def function():
    return "implementation"
</new_code>
</edit>
```

Or alternatively:

```
path/to/file.py
>>>>>>> SEARCH
def function():
    pass
=======
def function():
    return "implementation"
<<<<<<< REPLACE
```

## Build System

This project uses Bazel as the build system. When making changes, ensure they comply with Bazel build conventions:

- All new directories should include a BUILD.bazel file
- Follow existing dependency patterns for each language

### Common Build Commands

- Build and run: `bazel run //path/to/target` (e.g., `bazel run //python/hello_python`)
- Run all tests: `bazel test //...`
- Run integration tests: `bazel test --test_tag_filters=integ`
- Optional features: Use `--//features:go` or `--//features:rust` flags

## Coding Conventions

- Python:
  - Follow PEP 8 style guidelines
  - Line length 88 characters
  - Follow Ruff rules (PEP8 + additional checks)
  - Use snake_case for naming
  - Prefix unused variables with underscore
- TypeScript:
  - Follow the conventions in existing .ts files and comply with eslint rules (.eslintrc.js)
  - Use camelCase for naming
  - Order imports: builtin→external→internal→parent→sibling→index with newlines between groups
  - Add type annotations
  - Avoid console.log (use warn/error only)
- Go: Follow standard Go conventions with gofmt
- Rust: Follow the Rust style guide and use cargo fmt
- Bazel: Use buildifier for formatting

### Formatting Commands

- Format all code: Use pre-commit hooks (`pre-commit run --all-files`)
- Lint TypeScript: `cd ts && npx eslint .`
- Lint Python: `ruff check`

## Testing

- Add tests alongside new features
- Run appropriate tests for the language you're modifying
- Pytest is used for Python testing

## Project-Specific Notes

- When editing Python code, make sure imports are properly structured
- For TypeScript projects, maintain type definitions
- The todost Python app should maintain its current architecture

## Documentation

- Update README.md when adding significant features
- Document public APIs and interfaces

## CI/CD

- Changes should pass CI checks defined in .github/workflows
- Pre-commit hooks are defined in .pre-commit-config.yaml
- Cost efficiency requirements:
  - CI cost per PR must be ≤ $0.10
  - Keep build times under 60 seconds when possible

## Task Management

- Organize project work using a structured task hierarchy:
  ```
  Project
  ├── Epic 1 [PRD-XXX]
  │   ├── Story 1.1 [PRD-XXX-01]
  │   │   ├── Task 1.1.1
  │   │   └── Task 1.1.2
  │   └── Story 1.2 [PRD-XXX-02]
  └── Epic 2 [PRD-YYY]
      └── Story 2.1 [PRD-YYY-01]
  ```
- Create task plans in `.codex/plans/`:
  - Epic plans: `.codex/plans/epic_XXX_name.md`
  - Sprint plans: `.codex/plans/sprint_YYYY-MM-DD.md`
- Track task status with consistent labels:
  - `[NOT STARTED]` - Work not yet begun
  - `[IN PROGRESS]` - Currently being implemented
  - `[BLOCKED]` - Cannot proceed (include blocker details)
  - `[REVIEW]` - In code review
  - `[TESTING]` - In QA/testing phase
  - `[COMPLETE]` - Finished and verified
- Include completion metrics in task plans:
  - Estimated vs. actual time
  - % complete for in-progress tasks
  - Weekly progress summaries
- Weekly task audit: Update all task statuses every Friday

## PRD References

- Store PRDs in `docs/requirements/` using consistent naming:
  - `PRD-XXX-overview.md` - High-level feature description
  - `PRD-XXX-specifications.md` - Detailed technical requirements
  - `PRD-XXX-acceptance.md` - Testing and acceptance criteria
- Maintain a requirements traceability matrix in `docs/requirements/traceability.md`:
  ```
  | Req ID | Description | Priority | Status | Implemented In | Verified By |
  |--------|-------------|----------|--------|----------------|-------------|
  | PRD-001-01 | User login | HIGH | COMPLETE | #123, #145 | Test-001 |
  ```
- Use PRD IDs in all related artifacts:
  - Git branches: `feature/PRD-XXX-short-description`
  - Commit messages: `[PRD-XXX-01] Implement user login form`
  - Pull requests: `[PRD-XXX] User Authentication System`
  - Code comments: `// PRD-XXX-01: Custom validation required here`
- Version PRDs with clear change history:
  - Include a "Revision History" section in each PRD
  - Document significant requirement changes with rationale
  - When requirements change, update the traceability matrix

## Project Tracking

- Maintain a central dashboard in `.codex/dashboard.md`:

  ```
  # Project Dashboard (YYYY-MM-DD)

  ## Current Sprint: Sprint 12 (May 1-14)
  - Sprint Goal: Complete user authentication system
  - Progress: 65% complete (13/20 tasks)
  - Risks: API integration delayed (mitigation: using mock API)

  ## PRD Status
  - PRD-001: User Authentication - 80% complete
  - PRD-002: Data Export - 30% complete
  - PRD-003: Admin Dashboard - Not started

  ## Recent Milestones
  - ✅ Completed API design (Apr 28)
  - ✅ User testing round 1 (Apr 15)
  - 🔜 Feature freeze (May 12)
  ```

- Schedule regular check-ins:
  - Daily: Update in-progress task status
  - Weekly: Full dashboard review and update
  - Bi-weekly: Stakeholder progress report
- Maintain a decision log in `.codex/decisions.md`:

  ```
  # Decision Log

  ## YYYY-MM-DD: [Decision title]
  - Context: [Why is a decision needed]
  - Options Considered: [List of alternatives]
  - Decision: [The chosen approach]
  - Rationale: [Why this option was selected]
  - Implications: [What this means for the project]
  - Related PRDs: [PRD-XXX, PRD-YYY]
  ```

## Project Changelog

- Document all significant changes in the README.md with a dated changelog section
- Format for changelog entries:

  ```
  ## Changelog

  ### YYYY-MM-DD
  - Added: [feature name] - [brief description]
  - Fixed: [bug name] - [brief description]
  - Changed: [component name] - [description of changes]
  ```

- Link changelog entries to relevant pull requests or commit hashes
