# Project Baseline

> Optional, fill-in-once skeleton for project kickoff. Fill a first draft
> before the first task, review to close gaps, then keep the filled copy as
> the project's single reference baseline (for example
> `<project>/docs/project-baseline.md`). The 01-spec stage uses it as an input
> source, but stays bound to `Repository Context` observed facts and the
> task-provided request. This file is a mechanism, not authoritative content:
> project-specific facts recorded here belong to the project, not to the
> harness pack.

## 1. Project Info

- Project name:
- Product contact:
- Technical contact:
- Version / date:
- Repositories:
- Prototype / design links:

## 2. Business Context And Goals

### Background

- [Business problem, current pain, why now]

### Goals (3-5)

- [Goal 1]
- [Goal 2]
- [Goal 3]

### Non-Goals (Out Of Scope)

- [Explicitly not in this delivery, to prevent scope creep]

## 3. Users And Scenarios

### Target Users

- Role A:
- Role B:

### Core Scenarios (priority ordered)

1. [Scenario 1]
2. [Scenario 2]
3. [Scenario 3]

### Key Business Flows (brief)

- Flow 1: `start -> node -> end`
- Flow 2: `start -> node -> end`

## 4. Functional Requirements (Acceptable)

| ID | Feature | Description | Priority (P0/P1/P2) | Acceptance Criteria (testable) |
|---|---|---|---|---|
| FR-001 |  |  | P0 |  |
| FR-002 |  |  | P0 |  |
| FR-003 |  |  | P1 |  |

> Rule: every feature must have observable, verifiable acceptance criteria.

## 5. API Contract Baseline

### Conventions

- Base URL:
- Environments: dev / staging / prod
- Auth: Bearer / Cookie / other
- Idempotency: `Idempotency-Key` / business key / none
- Time fields: UTC millis / ISO8601
- Error model: `code + message + details`

### Endpoints

| API ID | Method | Path | Purpose | Key request fields | Key response fields | Business error codes |
|---|---|---|---|---|---|---|
| API-001 |  |  |  |  |  |  |
| API-002 |  |  |  |  |  |  |

### Contract Details (per endpoint)

#### API-001

- Request example:
```json
{}
```
- Response example:
```json
{}
```
- Failure example:
```json
{}
```
- Constraints:
  - Required fields:
  - Defaults for optional fields:
  - Allowed enum values:

### Compatibility And Versioning

- Version strategy: v1 / header version / path version
- Backward compatibility requirement:
- Field deprecation strategy:

## 6. Data And State Model Contract

### Core Entities

| Entity | Key fields | Field constraints | Source (backend fact / locally derived) |
|---|---|---|---|
| Entity-1 |  |  |  |
| Entity-2 |  |  |  |

### State Machine / Flow States

- States:
- Allowed transitions:
- Forbidden transitions:
- Terminal states:

### Consistency Rules

- Single source of truth:
- Derived-state rules:
- Conflict handling:

## 7. Non-Functional Requirements

### Performance

- Cold start:
- First meaningful screen:
- Core operation response time:

### Reliability

- Availability target (SLO):
- Retry policy:
- Degraded-failure strategy:

### Security

- Credential storage:
- Sensitive data handling:
- Permission boundaries:

### Observability

- Logs:
- Metrics:
- Tracing:
- Alert thresholds:

### Offline Capability (if applicable)

- Offline reads:
- Offline writes:
- Sync strategy:
- Conflict strategy:

## 8. Architecture And Boundaries

### Layering

- Presentation / UI:
- Application / Controller:
- Data access / Repository:
- Core / infrastructure:

### Routing And State Strategy

- Routing source: direct UI / state-driven / mixed (note exceptions)
- State management approach:

### Forbidden Items

- [e.g. UI calls APIs directly]
- [e.g. Application layer bypasses Repository]
- [e.g. multiple competing states]

## 9. Testing Strategy And Quality Gates

### Test Layers

- Unit:
- Component / widget:
- Integration:
- Manual regression:

### Quality Gates (CI)

- [Primary validation command, e.g. `bash harness/scripts/validate.sh`]
- [Secondary gates, e.g. coverage, smoke checks]

### Regression Matrix (example)

| Flow | Online | Offline | Weak network | Restart recovery | Conflicts |
|---|---|---|---|---|---|
| Flow A |  |  |  |  |  |
| Flow B |  |  |  |  |  |

## 10. Release And Rollback

### Release Strategy

- Environment order: dev -> staging -> prod
- Canary / gradual rollout:
- Feature flags:

### Data Migration

- Migration scripts:
- Rollback preconditions:

### Rollback Plan

- Trigger conditions:
- Steps:
- Owner:

### Incident Response

- Severity levels:
- On-call and escalation path:

## 11. Phase And Task Breakdown

### Phase Plan

| Phase | Goal | Scope | Excluded | Exit criteria |
|---|---|---|---|---|
| Phase 1 |  |  |  |  |
| Phase 2 |  |  |  |  |

### Task List

| Task ID | Goal | Inputs | Outputs | Risks | Acceptance criteria |
|---|---|---|---|---|---|
| T-001 |  |  |  |  |  |
| T-002 |  |  |  |  |  |

## 12. Risk Register

| Risk | Level (high/med/low) | Trigger | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 13. Commands And Environment

- Validation / build commands:
- Local environment specifics:
- Network / proxy notes:

## 14. Pre-Flight Checklist

- [ ] Functional requirements are acceptable, not slogans
- [ ] API contracts are implementable (examples and error codes complete)
- [ ] State model and transitions are explicit
- [ ] Non-functional requirements have quantified targets
- [ ] Quality gates and regression matrix defined
- [ ] Release, rollback, and incident paths are clear
- [ ] Phase / task structure established before development starts
