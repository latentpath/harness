# Stage 1: Write Spec

Read `harness/AGENTS.md` first. Read the request and inspect only the code,
tests, configuration, or external contract needed to resolve material facts.
Read the project root `AGENTS.md` when present. When the task supplies a
governing phase path, read that file, record its path in `Repository Context`,
and check the request against its gate. Do not infer an active phase.

Run `python3 harness/scripts/harnessctl.py stage-start <task-id> spec` before
writing. After writing, run `stage-check <task-id> spec`, then
`state <task-id> spec <STATUS>` with the same script.

Create `harness/work/<task-id>/spec.md`. Do not edit production code, tests,
or configuration in this stage.

Phase ownership: SPEC may write only `spec.md`. Do not modify `plan.md`,
`approval.json`, production code, tests, configuration, `development.md`, or
`review.md`.

Turn the request into an implementable contract. Use safe defaults for
non-material details, and label unverified statements as assumptions.

Use this structure:

```markdown
# <Task Title> Spec

## Goal
## Repository Context
## Functional Requirements
## Runtime Requirements
## Constraints And Non-Goals
## API And Data Contract
## Dependency And Version Policy
## Accepted Simplifications And Defaults
## Acceptance Criteria
## Blocking Decisions
## Open Questions
```

`Repository Context` contains only observed facts. `Blocking Decisions` is
`none` unless a missing decision materially affects interfaces, dependencies,
persistence, transactions, architecture, or runtime safety.

The task specification is the normative requirement truth. Project
constitutions and task-provided governing phase gates provide constraints and context;
they do not authorize a later PLAN to weaken the specification. Observed truth
is verified repository reality. If the requirement is materially ambiguous or
conflicts with a governing project constraint, classify an expected
implementation delta, `NEEDS_REVISION`, or `BLOCKED`; do not silently choose a
weaker contract.

When a task involves authentication, persistence, payments, destructive or
concurrent operations, caching, retries, migrations, lifecycle behavior, or a
cross-service/external API, cite the authoritative contract in the spec. Record
only the task-relevant contract fragment and state runtime requirements as
testable behavior rather than a summary.
