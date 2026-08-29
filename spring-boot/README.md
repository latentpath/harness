# Spring Boot Harness

Install this directory as `harness/` in a Spring Boot repository. It provides
durable engineering rules, four stage prompts, task-scoped handoff artifacts,
and a technical validation command.

## Use

0. Optional: at project kickoff, fill `harness/templates/project-baseline.md`
   once and keep the filled copy as the project's reference baseline. It is a
   source input for the spec stage, never authoritative on its own.
1. Choose a unique `<task-id>` and create `harness/work/<task-id>/`.
2. Follow `harness/prompts/01-spec.md` to write `spec.md`.
3. Follow `harness/prompts/02-plan.md` to write `plan.md`.
4. Explicitly approve every plan in the full four-stage workflow by writing
   `harness/work/<task-id>/approval.json` with `status`, `spec_sha256`,
   `plan_sha256`, `approved_at`, and `approved_by`.
5. Follow `harness/prompts/03-implement.md` to implement, test, and write
   `development.md`.
6. Follow `harness/prompts/04-review.md` to write `review.md`.

Every prompt requires `harness/AGENTS.md`. Use the artifacts and inspected code
for handoff rather than a prior chat transcript.

## Layout

- `AGENTS.md`: durable Spring Boot engineering and workflow rules.
- `prompts/`: the four stage-specific prompts.
- `harness/work/<task-id>/`: `spec.md`, `plan.md`, `development.md`, and
   `review.md`.
- `templates/`: optional project artifacts – `project-constitution.md`
  (Main layer), `phase.md` (phase gate), `project-baseline.md` (spec input).
- `scripts/validate.sh`: Maven test validation.
- `scripts/check-approval.sh`: verifies approval status and the current plan
   and spec SHA-256 values before implementation.
- `scripts/harnessctl.py`: records state and checks stage file ownership.
- `scripts/metrics-capture.sh`: emits machine-readable task metrics.
- `scripts/self-check.sh`: validates the installed Harness files and scripts.

When `TASK_ID` is supplied, validation resets and writes
`harness/work/<task-id>/validation.log` and `validation.status`; `0` means PASS,
non-zero means FAILED, and missing evidence means NOT_RUN. Review must require
status `0` before an `APPROVED` verdict.
