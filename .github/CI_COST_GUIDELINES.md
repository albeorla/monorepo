# CI Cost Efficiency Guidelines

## Overview

This document outlines cost efficiency requirements and guidelines for CI/CD processes in this monorepo. These guidelines align with the PRD requirements (PRD-F22).

## Cost Budget

Per the PRD requirements:
- CI cost per PR must be ≤ $0.10
- Build times should remain under 60 seconds when possible

## Configuration

### Budget Setting

The CI cost budget is controlled via the `CI_COST_BUDGET` GitHub secret. If not set, a default of $0.10 is used.

### How to Set the Secret

1. Go to GitHub repository settings
2. Navigate to Secrets and Variables > Actions
3. Create a new repository secret named `CI_COST_BUDGET`
4. Set its value to the maximum cost per workflow run (e.g., `0.10` for 10 cents)

## Cost Tracking Implementation

### Cost Estimation

The `.github/actions/check-ci-cost` action:
- Runs before all other jobs
- Estimates the cost based on workflow type and job characteristics
- Blocks workflow execution if the estimated cost exceeds the budget

### Cost Reporting

The `.github/actions/report-ci-cost` action:
- Runs at the end of each job
- Calculates actual costs based on runtime metrics
- Reports costs in job summaries and logs
- Provides a consolidated summary at the end of a workflow

## Cost Optimization Guidelines

### For Contributors

1. **Optimize Test Scope**:
   - Use path filters in workflows to only run relevant tests
   - Consider running a subset of tests for PRs and full tests for main branch

2. **Reduce Build Time**:
   - Use Bazel's caching capabilities
   - Leverage remote caching when possible
   - Keep dependencies minimal and well-organized

3. **Optimize Workflow Structure**:
   - Use job dependencies to avoid running unnecessary jobs
   - Run expensive jobs only when needed

### For CI/CD Maintainers

1. **Regular Auditing**:
   - Review workflow run costs monthly
   - Identify and optimize expensive workflows

2. **Budget Adjustment**:
   - Adjust budgets based on actual usage patterns
   - Consider separate budgets for different workflow types

3. **Monitoring and Alerting**:
   - Set up alerts for workflows exceeding their budgets
   - Track cost metrics over time to identify trends

## Current Cost Metrics

| Workflow      | Typical Cost | Build Time |
|---------------|--------------|------------|
| Python CI     | $0.05        | 30-45 sec  |
| Bazel CI      | $0.08        | 45-60 sec  |

## Future Improvements

- Integrate with cloud cost APIs for more accurate reporting
- Implement automatic cost optimization suggestions
- Add workflow-specific budgets based on complexity