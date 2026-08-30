# Flutter Harness

Install this directory as `harness/` in a Flutter repository. It provides one
set of durable engineering rules, four stage prompts, task-scoped handoff
artifacts, and a technical validation command.

## Installation Contract

Copy the **contents** of this Flutter pack into `harness/` at the target
project root:

```bash
mkdir -p /path/to/project/harness
cp -R /path/to/distribution/harness/flutter/. /path/to/project/harness/
cd /path/to/project
bash harness/scripts/self-check.sh
```

The installed path must be `project/harness/AGENTS.md`, not
`project/harness/flutter/AGENTS.md`. Scripts assume the directory is named
`harness` and is directly below the project root. Python 3, Bash, Git, Flutter,
and Dart must be available.

## Instruction And State Layers

| Path | Owner and purpose | Change cadence |
|---|---|---|
| `/AGENTS.md` | Project-owned constitution: stable project facts, architecture, technology, and prohibitions | Infrequent, reviewed project decision |
| `/harness/AGENTS.md` | Harness-owned workflow contract for agents | Only when upgrading the Harness |
| `/docs/phases/*.md` | Project-owned phase scope, API gates, and exit criteria | Per project phase |
| `/harness/work/<task-id>/` | Task contract, plan, approval, evidence, state, and review | Per task |

Do not put project-specific decisions in `harness/AGENTS.md`. Do not copy the
four-stage workflow into the root `AGENTS.md`. The root constitution must not
store the active phase or task status.

## Project Initialization

```bash
cp harness/templates/project-constitution.md AGENTS.md
mkdir -p docs/phases
cp harness/templates/phase.md docs/phases/phase-1.md
```

Fill `AGENTS.md` only with established project facts and durable rules. Fill
the phase file with that phase's allowed scope, blocked scope, contract gates,
and exit criteria. Do not fill undecided choices by guessing.

## Starting A Task

The operator supplies the task ID, raw requirement, and governing phase:

```text
Read the project root `AGENTS.md`, `harness/AGENTS.md`, and the governing
phase definition.

Task ID: `add-login-flow`
Governing phase: `docs/phases/phase-1.md`

Raw requirement:
<requirement>

Execute only SPEC according to `harness/prompts/01-spec.md`.
Record the governing phase path in SPEC Repository Context.
Stop after COMPLETED, BLOCKED, or NEEDS_REVISION.
```

The Harness does not infer the current project phase. Every task binds its
governing phase during SPEC.

## Workflow Profiles

- **Full**: separate `SPEC -> PLAN -> APPROVAL -> IMPLEMENT -> VALIDATE ->
  REVIEW` stages.
- **Lite**: create a compact but normalized SPEC and PLAN in one preparation
  session, then run `APPROVAL -> IMPLEMENT -> VALIDATE`. Lite still requires
  both artifacts, hash-bound approval, and validation evidence.

Do not use Lite for public API changes, persistence or migrations,
authentication, payments, concurrency, idempotency, destructive operations,
external contracts, or material ambiguity.

## Use

0. Optional: at project kickoff, fill `harness/templates/project-baseline.md`
   once and keep the filled copy as the project's reference baseline. It is a
   source input for the spec stage, never authoritative on its own.
1. Choose a unique `<task-id>`. Do not create
   `harness/work/<task-id>/` manually. The SPEC prompt starts with:

   ```bash
   python3 harness/scripts/harnessctl.py stage-start <task-id> spec
   ```

   This validates the task ID, creates the task directory, and records the
   SPEC stage baseline.
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
- `harness/work/<task-id>/`: stage baselines, `spec.md`, `plan.md`,
  `approval.json`, `state.json`, `development.md`, `validation.log`,
  `validation.status`, `validation.json`, `metrics.json`, and `review.md`.
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
