# Spring Boot Harness

Install this directory as `harness/` in a Spring Boot repository. It provides
durable engineering rules, four stage prompts, task-scoped handoff artifacts,
and a technical validation command.

## Installation Contract

Copy the **contents** of this Spring Boot pack into `harness/` at the target
project root:

```bash
mkdir -p /path/to/project/harness
cp -R /path/to/distribution/harness/spring-boot/. /path/to/project/harness/
cd /path/to/project
bash harness/scripts/self-check.sh
```

The installed path must be `project/harness/AGENTS.md`, not
`project/harness/spring-boot/AGENTS.md`. Scripts assume the directory is named
`harness` and is directly below the project root. Python 3, Bash, Git, Java,
and Maven or the Maven Wrapper must be available.

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
and exit criteria. Undecided technology or business contracts remain undecided;
do not fill templates by guessing.

## Starting A Task

The operator must supply the task ID, raw requirement, and governing phase.
Start SPEC with a fresh agent session using this shape:

```text
Read the project root `AGENTS.md`, `harness/AGENTS.md`, and the governing
phase definition.

Task ID: `create-product`
Governing phase: `docs/phases/phase-1.md`

Raw requirement:
<requirement>

Execute only SPEC according to `harness/prompts/01-spec.md`.
Record the governing phase path in SPEC Repository Context.
Stop after COMPLETED, BLOCKED, or NEEDS_REVISION.
```

The Harness does not infer the current project phase. Every task binds its
governing phase during SPEC so later phase changes cannot silently alter an
already approved task contract.

## Workflow Profiles

- **Full**: separate `SPEC -> PLAN -> APPROVAL -> IMPLEMENT -> VALIDATE ->
  REVIEW` stages. Use for normal features and all ambiguous or higher-risk
  work.
- **Lite**: create a compact but normalized SPEC and PLAN in one preparation
  session, then run `APPROVAL -> IMPLEMENT -> VALIDATE`. Lite still requires
  both artifacts, hash-bound approval, and machine validation evidence.

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
- `harness/work/<task-id>/`: stage baselines, `spec.md`, `plan.md`,
  `approval.json`, `state.json`, `development.md`, `validation.log`,
  `validation.status`, `validation.json`, `metrics.json`, and `review.md`.
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
