# Project Planning Documentation

This directory contains the planning documents for the Bazel Monorepo Platform project. The planning process follows an Agile methodology with two-week sprints.

## Directory Structure

- `sprints/` - Sprint planning documents containing detailed task breakdowns
- `dashboard.md` - Current project status, progress metrics, and upcoming milestones
- `roadmap.md` - Long-term planning document aligned with the PRD

## Sprint Planning Process

1. Each sprint begins with a planning session to define goals and tasks
2. Tasks are prioritized based on the PRD requirements
3. Daily progress is tracked in the dashboard
4. End-of-sprint reviews are captured in sprint summary documents

## Using MCP Tools for Planning

The project uses Claude's MCP capabilities for planning:

```bash
claude mcp
```

The softwareplanner tool helps create structured development plans with:

1. Clear goals and objectives
2. Task breakdowns with complexity estimates
3. Progress tracking
4. Implementation details

## References

- PRD: `/docs/PRD.md`
- Decisions: `/docs/decisions/`
- Sprint Reports: `/docs/reports/`