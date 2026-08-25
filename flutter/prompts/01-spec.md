# Stage 1: Write Spec

Read `harness/AGENTS.md` first. Read the request and inspect only the code,
tests, configuration, or external contract needed to resolve material facts.

Create `harness/work/<task-id>/spec.md`. Do not edit production code, tests,
or configuration in this stage.

Phase ownership: SPEC may write only `harness/work/<task-id>/spec.md`. Do not
modify `harness/work/<task-id>/plan.md`,
`harness/work/<task-id>/approval.json`, production code, tests, configuration,
`harness/work/<task-id>/development.md`, or
`harness/work/<task-id>/review.md`.

Turn the request into an implementable contract. Use the smallest amount of
detail that removes material ambiguity. Use safe defaults for non-material
details, and label unverified statements as assumptions.

Use this structure:

```markdown
# <Task Title> Spec

## Goal
## Repository Context
## Functional Requirements
## Runtime Requirements
## Constraints And Non-Goals
## API, Data, And UI Contract
## Dependency And Version Policy
## Accepted Simplifications And Defaults
## Acceptance Criteria
## Blocking Decisions
## Open Questions
```

`Repository Context` contains only observed facts. `Blocking Decisions` is
`none` unless a missing decision materially affects interfaces, dependencies,
persistence, routing, architecture, or runtime safety. Do not invent behavior
that is absent from the request and has no material consequence.

The task specification is the normative requirement truth. Project
constitutions and active phase gates provide project constraints and context;
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
