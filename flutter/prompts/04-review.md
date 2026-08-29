# Stage 4: Review

Read `harness/AGENTS.md`, `harness/work/<task-id>/spec.md`,
`harness/work/<task-id>/plan.md`, and
`harness/work/<task-id>/development.md`. Inspect the actual diff, changed
paths, relevant tests, and machine validation evidence. When validation
evidence is expected, require `validation.status`, require its value to be `0`
before an `APPROVED` verdict, and inspect `validation.log` as needed. Missing
evidence is `NOT_RUN`; a failed status is `FAILED`. Machine evidence wins over
contradictory narrative claims in `development.md`. Review only; do not edit
code.

Run `python3 harness/scripts/harnessctl.py stage-start <task-id> review` before
writing. After writing, run `stage-check <task-id> review`, then
`state <task-id> review <VERDICT>` with the same script.

Review in this order: (1) SPEC, (2) approved PLAN, (3) actual implementation,
(4) machine validation evidence, and (5) the development narrative. Verify the
implementation against SPEC independently, then separately against the
approved PLAN. SPEC is normative and `SPEC > PLAN`; an approved PLAN that
materially weakens SPEC is a finding, not authorization. Do not invent
requirements absent from SPEC or report preferences, optional cleanup, or
hypothetical edge cases as defects.

Phase ownership: REVIEW may write only `review.md`. Do not modify spec, plan,
approval, implementation code, or tests.

Create `harness/work/<task-id>/review.md` using this structure:

```markdown
# <Task Title> Review

## Findings
## Acceptance Criteria And Runtime Coverage
## Validation Checked
## Security Review
## Open Questions
## Verdict
## Spec Or Plan Feedback
```

`review.md` is a human-readable prose artifact. Machine-extractable evidence
(exit codes, timestamps, booleans) lives in other files; `review.md` refers to
them but does not duplicate structured fields.

List findings first, ordered by severity. Every finding must include severity,
file and line reference when available, concrete impact, and supporting
evidence. State `No findings` explicitly when applicable. Set `Verdict` to
`APPROVED`, `CHANGES_REQUESTED`, or `BLOCKED`. Do not set `APPROVED` when
`validation.status` is absent or non-zero. A review finding returns to
IMPLEMENT unless it invalidates the spec or plan; then return to the affected
upstream stage.

## Security Review

Apply the `Security Review` section when the spec touches auth, persistence,
payments, destructive or concurrent operations, caching, retries, migrations,
lifecycle behavior, or an external/cross-service API. Otherwise state
`Scope: none`.

Audit each applicable checklist item on the actual call path, not by file
structure:

- Auth: tokens derive from the saved/authoritative source; no token, key, or
  secret is hard-coded, logged, or committed.
- Persistence: writes go through the layer owning storage; no direct bypass;
  DTOs map explicitly to domain models.
- Payments / destructive operations: guarded per the approved contract; no
  unreviewed destructive path; idempotency/duplicate-guard where the contract
  requires it.
- Concurrency: in-flight operations are guarded; same-resource competing
  actions are serialized or rejected.
- External API: request/response mapping matches the cited contract; error and
  unauthorized paths handled correctly on the call path.
- Input/error: validation centralized and errors reuse existing result/wrappers;
  no raw exception leakage that reveals internals.

A security finding uses the same severity / impact / evidence / reference rules
as all findings and is listed first.
