# Stage 2: Make Plan

Read `harness/AGENTS.md` and `harness/work/<task-id>/spec.md` first. Inspect
the relevant code paths, tests, configuration, and dependencies before citing
an existing convention or file path.

Create `harness/work/<task-id>/plan.md`. Do not edit production code, tests,
or configuration. Do not approve the plan yourself.

Choose the smallest implementation that satisfies the spec. Separate observed
facts from inferences and proposed changes. Stop once the plan is actionable;
do not continue into optional cleanup or alternate architectures.

Use this structure:

```markdown
# <Task Title> Plan

## Repository Facts
## Implementation Strategy
## Steps
## Files To Change
## Test Strategy
## Validation
## Risks And Plan Conflicts
## Blocking Decisions
```

The plan is an implementation proposal. Do not add approval status or approver
fields to `plan.md`; approval truth belongs only in
`harness/work/<task-id>/approval.json`.

SPEC is normative requirement truth and `SPEC > PLAN`. Compare every proposed
implementation choice with the SPEC requirements. A PLAN may clarify details,
resolve unspecified choices, record repository constraints, identify risks, and
propose compatible strategies, but must not weaken a requirement, remove an
acceptance criterion, or make normative behavior optional. If no compliant
strategy is available, return `NEEDS_REVISION` or `BLOCKED` rather than
silently choosing a weaker contract; resolve the requirement at SPEC.

Approval of a PLAN authorizes execution of that exact hash-bound proposal. It
does not authorize a SPEC change or convert a PLAN/SPEC discrepancy into an
accepted requirement change.

Phase ownership: this stage may write only
`harness/work/<task-id>/plan.md`. Do not modify
`harness/work/<task-id>/spec.md`,
`harness/work/<task-id>/approval.json`, production code, tests, configuration,
`harness/work/<task-id>/development.md`, or
`harness/work/<task-id>/review.md`.

In `Files To Change`, distinguish verified existing paths from tentative new
paths. If verified repository facts conflict with the spec, describe the
conflict and stop for a material decision rather than silently expanding scope.
