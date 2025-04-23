# Bazel Monorepo Platform – Product Requirements Document (PRD)

**Version 0.5 • 2025-04-22**

> **Change log (v0.5)**  
> • Elevated **cost efficiency** to a cross-cutting, P0 concern; added explicit FinOps feature and KPIs.  
> • Clarified that Go/Rust tooling is optional and future-gated to avoid complexity‑overrun.  
> • Adjusted milestones (F‑22 now part of CI baseline) and updated success metrics.

---

## 1 Background & Problem Statement

Our engineering organization ships micro-services in several languages (Python for data, TypeScript for UI and Node APIs, and an emerging interest in Go and Rust for compute‑heavy back‑ends). Build scripts, test harnesses, deploy steps, and infra provisioning differ per repo, producing:

- Duplicate boilerplate
- Slow, non-hermetic builds and flaky CI
- Infra drift across environments
- Steep onboarding for new engineers and SREs

A **single Bazel monorepo** with shared CI/CD plus **cloud‑agnostic Infrastructure as Code (IaC)** eliminates drift and supports future scale.

---

## 2 Purpose & Vision

Deliver a cohesive developer experience where any engineer can:

1. Scaffold a new service in less than 60 s.
2. `bazel test //…` locally and get identical results in CI.
3. Produce a Docker or serverless artifact with one command.
4. Spin up production‑grade infra through repeatable IaC modules.
5. Merge code confident that build, test, and infra rollout are deterministic.

**Vision:** “Ship polyglot services at the speed of thought—on a budget that scales gracefully.”

---

## 3 Cost Efficiency Principle

> **Hard requirement:** Maintain or reduce baseline monthly spend (CI minutes, cache storage, registry egress) while adding new capabilities. All new features must include a cost impact analysis.

---

## 4 Priority Levels

| Level  | Definition                                                      | Target release window |
| ------ | --------------------------------------------------------------- | --------------------- |
| **P0** | Must‑have for developer workflow **and** proven cost‑efficient. | **v1.0 GA** (T + 8 w) |
| **P1** | Important; enables future scale; cost within 20 % of baseline.  | **v1.1** (T + 12 w)   |
| **P2** | Enhances perf, UX, or further reduces cost.                     | Post‑v1.1 (T + 16 w)  |
| **P3** | Nice‑to‑have/platform polish.                                   | Opportunistic         |
| **P4** | Long‑range / research items.                                    | Backlog               |

---

## 5 Detailed Feature Specification

| ID       | Title                                   | Description                                                                             | Priority | Acceptance Criteria                                                                          |
| -------- | --------------------------------------- | --------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------- |
| F‑1      | Python build / test / run               | `py_library`, `py_binary`, `pytest` integration                                         | **P0**   | `bazel run //python/...` prints hello; tests green in CI; <60 s CI wall‑time                 |
| F‑2      | TypeScript build / test / run           | `ts_project`, Jest harness                                                              | **P0**   | Same cost/time target as F‑1                                                                 |
| F‑3      | Go toolchain integration _(optional)_   | `rules_go` + Gazelle behind feature flag `--//features:go`                              | **P1**   | Disabled by default; zero overhead if unused                                                 |
| F‑4      | Rust toolchain integration _(optional)_ | `rules_rust` behind flag `--//features:rust`                                            | **P1**   | Disabled by default; zero overhead if unused                                                 |
| F‑5      | Cookiecutter template (Py)              | Parameterised skeleton                                                                  | **P0**   |                                                                                              |
| F‑6      | Hygen generator (TS)                    | EJS template                                                                            | **P0**   |                                                                                              |
| F‑7      | Shell scaffolds (Go/Rust)               | Bash generators, no CI job unless flag enabled                                          | **P1**   |                                                                                              |
| F‑8      | GitHub Actions CI                       | Build ➜ test ➜ lint **with cost dashboard**                                             | **P0**   |                                                                                              |
| F‑9      | Remote Build Cache                      | BuildBuddy cloud with cost cap alerts                                                   | **P2**   |                                                                                              |
| F‑10     | OCI Images                              | `oci_image` target per service, distroless                                              | **P2**   |                                                                                              |
| F‑11     | Docs Site                               | GitHub Pages auto‑publish docs                                                          | **P3**   |                                                                                              |
| F‑12     | Terraform IaC baseline                  | Cloud‑agnostic modules                                                                  | **P1**   |                                                                                              |
| F‑13     | Quality Gate (static & sec‑scan)        | Ruff, ESLint, Trivy                                                                     | **P0**   | CI fails on critical findings                                                                |
| F‑14     | Integration Test Harness                | `bazel test --test_tag_filters=integ`                                                   | **P1**   | Sample cross‑service test green in CI                                                        |
| F‑15     | Observability Hooks                     | OTEL libs + BuildBuddy metrics                                                          | **P2**   | Services emit traces to OTEL endpoint                                                        |
| F‑16     | Disaster Recovery & Backups             | State snapshots, cache backup                                                           | **P2**   | Quarterly DR drill passes                                                                    |
| F‑17     | Release Versioning & Promotion          | Semver tag triggers image push + GitHub Release                                         | **P1**   | `v1.0.0` tag publishes image & SBOM                                                          |
| F‑18     | Secrets Governance & Rotation           | OIDC auth, rotation schedule                                                            | **P2**   | Tokens auto‑rotate ≤90 d                                                                     |
| F‑19     | Dev Onboarding Script                   | `bootstrap_dev.sh` installs deps & hooks                                                | **P3**   | New laptop ready in <10 min                                                                  |
| F‑20     | Performance Budgets                     | Build graph & wall‑clock alerts                                                         | **P3**   | Alert fires when p95 build >10 min                                                           |
| F‑21     | Optional k8s Deploy Modules             | Helm chart + TF `helm_release`                                                          | **P4**   | Demo env deploys to k3d                                                                      |
| **F‑22** | Cost Efficiency & FinOps                | Capture CI minutes, cache/registry storage; monthly budget alert; cost report in README | **P0**   | ≤$0.10 per PR build; monthly infra spend tracked; CI fails if cost > budget without override |

---

## 6 Milestones & Timeline

| Week         | Date (approx) | Milestone                          | Included Features      |
| ------------ | ------------- | ---------------------------------- | ---------------------- |
| **T0**       | 22‑Apr‑25     | Kick‑off / repo skeleton           | –                      |
| **T + 2 w**  | 06‑May‑25     | CI Green & FinOps baseline         | F‑1,2,5,6,8,13,22      |
| **T + 3 w**  | 13‑May‑25     | IaC Dev complete                   | F‑12 (dev env)         |
| **T + 4 w**  | 20‑May‑25     | Polyglot support (flagged)         | F‑3,4,7                |
| **T + 5 w**  | 27‑May‑25     | Integration harness MVP            | F‑14                   |
| **T + 6 w**  | 03‑Jun‑25     | Containerisation & remote cache    | F‑9,10                 |
| **T + 7 w**  | 10‑Jun‑25     | IaC Prod ready + Release promotion | F‑12 (prod), F‑17      |
| **T + 8 w**  | 17‑Jun‑25     | **v1.0 GA** (all P0)               | Cost guardrails active |
| **T + 12 w** | 15‑Jul‑25     | **v1.1** (P1 bundle)               | Remaining P1 features  |
| **T + 16 w** | 12‑Aug‑25     | P2 enhancements                    | Cost‑driven perf & DR  |
| Ongoing      | —             | Backlog                            | P3 / P4                |

---

## 7 Success Metrics & KPIs

| Metric                                       | Target               | Measurement                              |
| -------------------------------------------- | -------------------- | ---------------------------------------- |
| **CI cost per PR build**                     | ≤ $0.10              | GitHub billing export → FinOps dashboard |
| Monthly infra spend (cache, registry, state) | Within 5 % of budget | Cloud cost explorer                      |
| Static‑analysis violations merged            | 0 critical / quarter | CI trends                                |
| Integration test coverage                    | ≥70 %                | Bazel coverage plugin                    |
| Mean time to bootstrap new dev               | ≤10 min              | Post‑onboarding survey                   |

---

## 8 Operational Considerations

- **Cost Controls:** Tag all infra; Terraform budget alert; CI step `ci‑cost‑check` fails build if forecast exceeds budget.
- **Optional language flags:** `--//features:go`, `--//features:rust` default false; CI matrix excludes those targets unless flag list is set.

_(Further architecture, IaC, security, and glossary sections omitted for brevity in this artifact.)_

---

### Revision History

| Version | Date       | Author  | Notes                                                                     |
| ------- | ---------- | ------- | ------------------------------------------------------------------------- |
| 0.1     | 2025‑04‑22 | Albert  | Initial draft                                                             |
| 0.2     | 2025‑04‑22 | ChatGPT | Added architecture, OCI, metrics                                          |
| 0.3     | 2025‑04‑22 | ChatGPT | Cloud‑agnostic IaC additions                                              |
| 0.4     | 2025‑04‑22 | ChatGPT | Quality, testing, obs, DR, release, secrets, onboarding, perf‑budget, k8s |
| **0.5** | 2025‑04‑22 | ChatGPT | Cost efficiency elevated to P0; Go/Rust optional; FinOps feature & KPIs   |
