# Flutter Harness

Install this directory as `harness/` in a Flutter repository. It provides one
set of durable engineering rules, four stage prompts, task-scoped handoff
artifacts, and a technical validation command.

## Use

0. Optional: at project kickoff, fill `harness/templates/project-baseline.md`
   once and keep the filled copy as the project's reference baseline. It is a
   source input for the spec stage, never authoritative on its own.
1. Choose a unique `<task-id>` and create `harness/work/<task-id>/`.
2. Read and follow `harness/prompts/01-spec.md` to write `spec.md`.
3. Read and follow `harness/prompts/02-plan.md` to write `plan.md`.
4. Explicitly approve every plan in the full four-stage workflow by writing
  `harness/work/<task-id>/approval.json` with `status: approved`,
  `spec_sha256`, `plan_sha256`, `approved_at`, and `approved_by`.
5. Read and follow `harness/prompts/03-implement.md` to implement, test, and
   write `development.md`. The implement stage refuses to edit until
    `approval.json` is approved and its SPEC and PLAN hashes match.
6. Read and follow `harness/prompts/04-review.md` to write `review.md`,
  including the `Security Review` section when applicable.

Capture task evidence as you go:

- `TASK_ID=<task-id> bash harness/scripts/validate.sh` records the actual
  validation output and exit code to `harness/work/<task-id>/validation.log`
  and `validation.status`.
- `bash harness/scripts/metrics-capture.sh <task-id>` emits `metrics.json`
  (auto-derived validation and approval facts plus operator-supplied scalars).

Every prompt requires `harness/AGENTS.md`. Do not pass prior chat history as a
handoff; pass the relevant task artifacts and let the next stage inspect code.

## Approval

`harness/work/<task-id>/approval.json` is the **single source of truth** for the
approval fact. It binds both SPEC and PLAN at approval time; if either changes,
the implement stage detects the mismatch and stops. The `## Approval` section
of `plan.md` is informational only and never authoritative on its own. A
missing `approval.json` means the plan is a draft.

## Evidence

- `review.md` records the human verdict and narrative findings; machine facts
  (exit codes, approval data) live in `validation.status`, `validation.log`,
  and `metrics.json`, and are referenced rather than duplicated.

## Layout

- `AGENTS.md`: durable Flutter engineering and workflow rules.
- `prompts/`: the four stage-specific prompts.
- `harness/work/<task-id>/`: `spec.md`, `plan.md`, `approval.json`, `development.md`,
  `review.md`, `validation.log`, `validation.status`, `metrics.json`.
- `templates/`: optional project artifacts – `project-constitution.md`
  (Main layer), `phase.md` (phase gate), `project-baseline.md` (spec input).
- `scripts/validate.sh`: Flutter formatting, analysis, and test validation;
  captures validation evidence when `TASK_ID` is set.
- `scripts/metrics-capture.sh`: emits `metrics.json` for a task.
- `scripts/harnessctl.py`: validates approval, records `state.json`, and checks
  stage ownership against per-stage baselines.
- `scripts/self-check.sh`: validates the installed Harness files and scripts.

`work/` is intentionally task-scoped so parallel work and old handoffs do not
share a mutable workflow state file.
