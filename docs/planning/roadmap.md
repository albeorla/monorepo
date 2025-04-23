# Project Roadmap (2025-05-06)

## Vision
"Ship polyglot services at the speed of thought—on a budget that scales gracefully."

## Timeline Overview
Based on the Product Requirements Document (PRD v0.5)

| Milestone             | Target Date | Status       | Features                         |
|-----------------------|-------------|--------------|----------------------------------|
| **Kick-off**          | Apr 22      | ✅ Complete  | Repository initialization         |
| **CI Green & FinOps** | May 6       | ✅ Complete  | F-1,2,5,6,8,13,22               |
| **IaC Dev complete**  | May 13      | 🔄 In Progress | F-12 (dev env)                  |
| **Polyglot support**  | May 20      | 🔄 Planned   | F-3,4,7                         |
| **Integration MVP**   | May 27      | 🔄 Planned   | F-14                            |
| **Container & Cache** | Jun 3       | 🔄 Planned   | F-9,10                          |
| **IaC Prod & Release**| Jun 10      | 🔄 Planned   | F-12 (prod), F-17               |
| **v1.0 GA**           | Jun 17      | 🔄 Planned   | All P0 features                  |
| **v1.1**              | Jul 15      | 🔄 Planned   | All P1 features                  |
| **v2.0**              | Aug 12      | 🔄 Planned   | P2 enhancements                  |

## Priority-Based Delivery

### P0 Features (Must-have for GA)
- ✅ F-1: Python build / test / run
- ✅ F-2: TypeScript build / test / run
- ✅ F-5: Cookiecutter template (Py)
- ✅ F-6: Hygen generator (TS)
- ✅ F-8: GitHub Actions CI
- ✅ F-13: Quality Gate (static & sec-scan)
- ✅ F-22: Cost Efficiency & FinOps

### P1 Features (v1.1)
- 🔄 F-3: Go toolchain integration (optional)
- 🔄 F-4: Rust toolchain integration (optional) 
- 🔄 F-7: Shell scaffolds (Go/Rust)
- 🔄 F-12: Terraform IaC baseline
- 🔄 F-14: Integration Test Harness
- 🔄 F-17: Release Versioning & Promotion

### P2 Features (Post-v1.1)
- 🔄 F-9: Remote Build Cache
- 🔄 F-10: OCI Images
- 🔄 F-15: Observability Hooks
- 🔄 F-16: Disaster Recovery & Backups
- 🔄 F-18: Secrets Governance & Rotation
- 🔄 F-20: Performance Budgets

### P3/P4 Features (Opportunistic)
- 🔄 F-11: Docs Site
- 🔄 F-19: Dev Onboarding Script
- 🔄 F-21: Optional k8s Deploy Modules

## Current Focus
Sprint 2 (May 6-20) is focused on:
1. Container infrastructure (OCI Images)
2. Remote build cache with BuildBuddy
3. Terraform IaC baseline
4. Integration test harness

## Key Success Metrics
- CI cost per PR: ≤$0.10
- Monthly infra spend: Within 5% of budget
- Static analysis violations: 0 critical/quarter
- Integration test coverage: ≥70%
- Mean time to bootstrap: ≤10 minutes