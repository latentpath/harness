# Stage 4: Review

Read `harness/AGENTS.md`, `harness/work/<task-id>/spec.md`,
`harness/work/<task-id>/plan.md`, and
`harness/work/<task-id>/development.md`. Inspect the actual diff, changed
paths, relevant tests, and validation evidence. Review only; do not edit code.

Review in this order: (1) SPEC, (2) approved PLAN, (3) actual implementation,
(4) machine validation evidence, and (5) the development narrative. Verify the
implementation against SPEC independently, then separately against the
approved PLAN. SPEC is normative and `SPEC > PLAN`; an approved PLAN that
materially weakens SPEC is a finding, not authorization. Do not invent
requirements absent from SPEC or report preferences or optional cleanup as
defects.

Before writing `review.md`, require `harness/work/<task-id>/validation.status`
when validation is expected. Its value must be `0` before an `APPROVED`
verdict; missing evidence is `NOT_RUN`, non-zero status is `FAILED`, and
machine evidence wins over contradictory narrative claims in
`development.md`.

Phase ownership: REVIEW may write only `review.md`. Do not modify spec, plan,
approval, implementation code, or tests.

Create `harness/work/<task-id>/review.md`:

```markdown
# <Task Title> Review

## Findings
## Acceptance Criteria And Runtime Coverage
## Validation Checked
## Open Questions
## Verdict
## Spec Or Plan Feedback
```

List findings first, ordered by severity. Every finding must include severity,
file and line reference when available, concrete impact, and evidence. State
`No findings` when applicable. Set `Verdict` to `APPROVED`,
`CHANGES_REQUESTED`, or `BLOCKED`. A review finding returns to IMPLEMENT
unless it invalidates the spec or plan; then return to the affected upstream
stage.
